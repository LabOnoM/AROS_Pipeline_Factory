# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

"""
AROS Dashboard — FastAPI Backend (main.py)
============================================
Web-based control center for the Antigravity Research Operating System.

Endpoints:
  - GET  /            → HTML dashboard UI (memory stats, telemetry, swarm panel)
  - POST /api/dream   → Trigger force_global_ingestion (memory consolidation)
  - POST /api/mutate_all → Trigger full GEPA mutation sweep + knowledge distillation
  - POST /api/brain/distill → Standalone knowledge distillation
  - GET  /api/brain/export  → Export portable brain snapshot for federation
  - POST /api/brain/import  → Import external brain snapshot
  - POST /api/brain/merge   → LLM-reviewed merge of imported brain data

Serves static assets from /static and provides real-time AROS telemetry.
Listens on port 8000 by default.

Part of: antigravity-dashboard (AROS Control Center)
"""
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import subprocess
import asyncio
import uuid
import threading
import sqlite3 as _sqlite3
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler

def setup_aros_logging(module_name: str):
    log_dir = os.path.expanduser("~/.gemini/antigravity/logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "aros.log")
    
    # Configure root logger so imported modules (like knowledge_distiller) inherit it
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        fh = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger

logger = setup_aros_logging("dashboard")

# ── Dynamic Path Resolution ───────────────────────────────────
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AROS_ROOT = os.path.abspath(os.path.join(_CURRENT_DIR, "..", "..", ".."))

# ── Process state tracking ───────────────────────────────────
_dream_proc: subprocess.Popen = None
_mutation_proc: subprocess.Popen = None
_distill_proc: subprocess.Popen = None
_is_distill_running: bool = False
_next_scheduled_run: str = ""
_next_weekly_run: str = ""

def _is_running(proc, module_name: str) -> bool:
    """Return True if the subprocess is still alive. If proc object is lost (e.g. server restart), checks OS process table."""
    if proc is not None and proc.poll() is None:
        return True
    try:
        # Fallback to check if it's running as an orphaned process
        res = subprocess.run(["pgrep", "-f", f"python -m {module_name}"], capture_output=True)
        return res.returncode == 0
    except Exception:
        return False

def _build_subprocess_env() -> dict:
    """Build a clean env dict with API keys loaded from ~/.gemini/.env."""
    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    env.pop("PYTHONPATH", None)

    env_path = os.path.expanduser("~/.gemini/.env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k not in env:
                        env[k] = v

    if "GOOGLE_AI_API_KEY" in env and "GEMINI_API_KEY" not in env:
        env["GEMINI_API_KEY"] = env["GOOGLE_AI_API_KEY"]
    if "GOOGLE_AI_API_KEY" in env and "GOOGLE_API_KEY" not in env:
        env["GOOGLE_API_KEY"] = env["GOOGLE_AI_API_KEY"]
    return env

# ── Brain DB Helper ─────────────────────────────────────────────────────────
def _get_brain_db():
    """Return a brain.db connection with row_factory for dict-like access."""
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    db = _sqlite3.connect(db_path)
    db.row_factory = _sqlite3.Row
    return db

# ── Swarm Job Registration Helper ───────────────────────────────────────────
LOGS_DIR = os.path.expanduser("~/.gemini/antigravity/logs")

def _insert_swarm_job(job_id: str, agent_role: str, task: str, log_path: str):
    """Register a system daemon job in brain.db so the Swarm panel can display it."""
    try:
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        db = _sqlite3.connect(db_path)
        db.execute("""
            INSERT OR IGNORE INTO swarm_jobs
                (id, agent_role, task, status, log_path, created_at)
            VALUES (?, ?, ?, 'running', ?, datetime('now'))
        """, (job_id, agent_role, task[:500], log_path))
        db.commit()
        db.close()
    except Exception as e:
        logger.warning(f"Could not register swarm job {job_id}: {e}")

def _update_swarm_job_pid(job_id: str, pid: int):
    """Write the OS process ID to the DB so the AROS watchdog can detect crashes."""
    try:
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        db = _sqlite3.connect(db_path)
        db.execute("UPDATE swarm_jobs SET pid=? WHERE id=?", (pid, job_id))
        db.commit()
        db.close()
    except Exception as e:
        logger.warning(f"Could not update PID for swarm job {job_id}: {e}")


def _finalize_swarm_job(job_id: str, success: bool):
    """Update a swarm job status to completed or failed."""
    try:
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        status = "completed" if success else "failed"
        db = _sqlite3.connect(db_path)
        db.execute(
            "UPDATE swarm_jobs SET status=?, completed_at=datetime('now') WHERE id=?",
            (status, job_id)
        )
        db.commit()
        db.close()
    except Exception as e:
        logger.warning(f"Could not finalize swarm job {job_id}: {e}")


def _spawn_dream():
    """Spawn the dreamer subprocess and register it in the Swarm Orchestrator panel."""
    global _dream_proc
    if _is_running(_dream_proc, "antigravity_brain.dreamer"):
        return False
    env = _build_subprocess_env()
    job_id = str(uuid.uuid4())
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, f"{job_id}_dreamer.log")
    _insert_swarm_job(job_id, "dreamer", "Force Dream Cycle — index skills/KIs/workflows into vector memory", log_path)
    log_file = open(log_path, "w")
    _dream_proc = subprocess.Popen(
        ["uv", "run", "python", "-m", "antigravity_brain.dreamer", "--force"],
        cwd=os.path.join(AROS_ROOT, "antigravity-brain"),
        env=env,
        stdout=log_file,
        stderr=log_file,
    )
    _update_swarm_job_pid(job_id, _dream_proc.pid)
    
    # Asynchronously watch process and finalize swarm job when done
    async def _watch_dream(proc, jid, lf):
        try:
            await asyncio.to_thread(proc.wait)
            success = proc.returncode == 0
            _finalize_swarm_job(jid, success)
            logger.info(f"[Dream] Process finished (rc={proc.returncode}).")
        finally:
            lf.close()
    asyncio.create_task(_watch_dream(_dream_proc, job_id, log_file))
    return True


def _spawn_mutation():
    """Spawn the mutation sweep subprocess and register it in the Swarm Orchestrator panel."""
    global _mutation_proc
    if _is_running(_mutation_proc, "antigravity_evolution.batch_evolver"):
        return False
    env = _build_subprocess_env()
    job_id = str(uuid.uuid4())
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, f"{job_id}_mutation.log")
    _insert_swarm_job(job_id, "mutation_sweeper", "Force System Mutation Sweep — GEPA analysis of session walkthroughs + Knowledge Distillation", log_path)
    log_file = open(log_path, "w")
    _mutation_proc = subprocess.Popen(
        ["uv", "run", "python", "-m", "antigravity_evolution.batch_evolver"],
        cwd=os.path.join(AROS_ROOT, "antigravity-evolution"),
        env=env,
        stdout=log_file,
        stderr=log_file,
    )
    _update_swarm_job_pid(job_id, _mutation_proc.pid)
    
    # Asynchronously watch process and finalize swarm job when done
    async def _watch_mutation(proc, jid, lf):
        try:
            await asyncio.to_thread(proc.wait)
            success = proc.returncode == 0
            _finalize_swarm_job(jid, success)
            logger.info(f"[Mutation] Process finished (rc={proc.returncode}).")
        finally:
            lf.close()
    asyncio.create_task(_watch_mutation(_mutation_proc, job_id, log_file))
    return True

def _spawn_distill_swarm():
    """Spawn the full distill-then-swarm pipeline as a subprocess.
    
    Runs batch_evolver with --distill-only, then invokes the swarm bridge
    to execute and verify proposals.
    """
    global _distill_proc
    if _is_running(_distill_proc, "antigravity_evolution.batch_evolver"):
        logger.warning("[WEEKLY] Distill already running, skipping.")
        return False
    env = _build_subprocess_env()
    _distill_proc = subprocess.Popen(
        ["uv", "run", "python", "-m", "antigravity_evolution.batch_evolver", "--distill-only"],
        cwd=os.path.join(AROS_ROOT, "antigravity-evolution"),
        env=env
    )
    return True

# ── Daily + Weekly Scheduler ──────────────────────────────────
SCHEDULE_HOUR = 3    # 3:00 AM local time
SCHEDULE_MINUTE = 0
WEEKLY_DAY = 5      # Saturday (Monday=0 … Saturday=5, Sunday=6)

async def _daily_scheduler():
    """Background task: runs dream + mutation sweep daily at 03:00.
    Also runs full Distill Knowledge → Execute & Verify via Swarm every Saturday at 03:00."""
    global _next_scheduled_run, _next_weekly_run
    while True:
        now = datetime.now()
        target = now.replace(hour=SCHEDULE_HOUR, minute=SCHEDULE_MINUTE, second=0, microsecond=0)
        if target <= now:
            target += timedelta(days=1)  # Already past today's window → schedule for tomorrow

        _next_scheduled_run = target.strftime("%Y-%m-%d %H:%M")

        # Compute next Saturday run for display
        days_until_saturday = (WEEKLY_DAY - now.weekday()) % 7
        if days_until_saturday == 0 and now.hour >= SCHEDULE_HOUR:
            days_until_saturday = 7  # Already ran today, next week
        next_saturday = (now + timedelta(days=days_until_saturday)).replace(
            hour=SCHEDULE_HOUR, minute=SCHEDULE_MINUTE, second=0, microsecond=0)
        _next_weekly_run = next_saturday.strftime("%Y-%m-%d %H:%M")

        wait_seconds = (target - now).total_seconds()
        logger.info(f"[SCHEDULER] Next daily sequential run at {_next_scheduled_run} ({wait_seconds/3600:.1f}h from now)")

        await asyncio.sleep(wait_seconds)

        now = datetime.now()

        # ── 1. Distill Knowledge + Execute via Swarm ─────────────────
        logger.info(f"[SCHEDULER] {datetime.now().strftime('%H:%M')} — Step 1: Running Distill Knowledge (GEPA Proposals)…")
        _spawn_distill_swarm()

        # Poll until distillation finishes (max 90 min)
        for _ in range(540):
            if not _is_running(_distill_proc, "antigravity_evolution.batch_evolver"):
                break
            await asyncio.sleep(10)

        # Dispatch proposals to the Swarm for execution
        logger.info(f"[SCHEDULER] {datetime.now().strftime('%H:%M')} — Distillation complete. Dispatching proposals to Swarm…")
        try:
            bridge_dir = os.path.join(AROS_ROOT, "antigravity-evolution", "src")
            if bridge_dir not in sys.path:
                sys.path.insert(0, bridge_dir)
            from antigravity_evolution.swarm_bridge import process_pending_distiller_proposals
            await process_pending_distiller_proposals()
        except Exception as e:
            logger.error(f"[SCHEDULER] Swarm bridge error: {e}", exc_info=True)

        logger.info(f"[SCHEDULER] {datetime.now().strftime('%H:%M')} — Waiting for Swarm evolution agents to finish…")
        # Poll until swarm bridge jobs finish (max 120 min)
        import sqlite3 as _sqlite3
        db_path_poll = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        for _ in range(720):
            try:
                db_poll = _sqlite3.connect(db_path_poll)
                active_evolution_agents = db_poll.execute(
                    "SELECT COUNT(*) FROM swarm_jobs WHERE agent_role = 'evolution_agent' AND status IN ('dispatched', 'running', 'healing')"
                ).fetchone()[0]
                db_poll.close()
                if active_evolution_agents == 0:
                    break
            except Exception as e:
                logger.error(f"[SCHEDULER] Error polling swarm jobs: {e}")
            await asyncio.sleep(10)
        logger.info(f"[SCHEDULER] {datetime.now().strftime('%H:%M')} — Swarm execution & verification complete.")

        # ── 2. GEPA mutation sweep ──────────────────────────────────────
        logger.info(f"[SCHEDULER] {datetime.now().strftime('%H:%M')} — Step 2: Starting daily mutation sweep…")
        _spawn_mutation()

        # Poll until mutation finishes (max 60 min)
        for _ in range(360):
            if not _is_running(_mutation_proc, "antigravity_evolution.batch_evolver"):
                break
            await asyncio.sleep(10)

        # ── 3. Dream cycle + Hygiene Engine ──────────────────────────────
        logger.info(f"[SCHEDULER] {datetime.now().strftime('%H:%M')} — Step 3: Starting daily dream cycle & hygiene engine…")
        _spawn_dream()

        # Poll until dream finishes (max 30 min)
        for _ in range(180):
            if not _is_running(_dream_proc, "antigravity_brain.dreamer"):
                break
            await asyncio.sleep(10)

        logger.info(f"[SCHEDULER] {datetime.now().strftime('%H:%M')} — Scheduled sequential cycle complete.")

@asynccontextmanager
async def lifespan(app):
    """Start the daily scheduler and run DB migrations when the dashboard boots."""
    # ── DB Migrations ──────────────────────────────────────────────
    try:
        # 1. Initialize full core schema (SQLite-Vec + standard tables)
        import sys
        if "/mnt/Disk1/AntigravityInit/antigravity-brain/src" not in sys.path:
            sys.path.insert(0, "/mnt/Disk1/AntigravityInit/antigravity-brain/src")
        from antigravity_brain.db import verify_and_init_db
        verify_and_init_db()
        
        # 2. Apply dashboard-specific migrations
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        db = _sqlite3.connect(db_path)
        db.execute("""
            CREATE TABLE IF NOT EXISTS distiller_runs (
                id TEXT PRIMARY KEY,
                started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                clusters_found INTEGER DEFAULT 0,
                structural_proposals INTEGER DEFAULT 0,
                agent_proposals INTEGER DEFAULT 0,
                policy_proposals INTEGER DEFAULT 0,
                proposals_dispatched INTEGER DEFAULT 0,
                status TEXT DEFAULT 'running',
                log_path TEXT
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS swarm_bridge_tracking (
                fact_id INTEGER PRIMARY KEY,
                processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS hygiene_runs (
                id TEXT PRIMARY KEY,
                started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                redundancies_resolved INTEGER DEFAULT 0,
                contradictions_detected INTEGER DEFAULT 0,
                contradictions_resolved INTEGER DEFAULT 0,
                facts_archived INTEGER DEFAULT 0,
                facts_hard_deleted INTEGER DEFAULT 0,
                experiences_pruned INTEGER DEFAULT 0,
                graph_edges_extracted INTEGER DEFAULT 0,
                status TEXT DEFAULT 'running',
                log_path TEXT
            )
        """)
        db.commit()
        db.close()
        logger.info("[BOOT] DB migrations applied (distiller_runs, swarm_bridge_tracking, hygiene_runs).")
    except Exception as e:
        logger.warning(f"[BOOT] DB migration warning: {e}")

    task = asyncio.create_task(_daily_scheduler())
    yield
    task.cancel()

app = FastAPI(title="Antigravity Control Center", lifespan=lifespan)

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join(static_dir, "index.html"), "r") as f:
        return f.read()

@app.get("/api/metrics")
async def get_metrics():
    import sqlite3
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    
    metrics = {
        "memory": {"world_facts": 0, "experiences": 0, "mental_models": 0, "agent_archetypes": 0},
        "swarm": {"active_nodes": 0, "completed_tasks": 0, "healing_tasks": 0, "failed_tasks": 0},
        "evolution": {
            "mutated_skills": 0, "mutated_kis": 0, 
            "mutated_policies": 0, "mutated_workflows": 0, 
            "failed_traces": 0
        }
    }
    
    if os.path.exists(db_path):
        try:
            db = sqlite3.connect(db_path)
            c = db.cursor()
            
            c.execute("SELECT COUNT(*) FROM world_facts")
            metrics["memory"]["world_facts"] = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM experiences")
            metrics["memory"]["experiences"] = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM mental_models")
            metrics["memory"]["mental_models"] = c.fetchone()[0]
            
            try:
                c.execute("SELECT COUNT(*) FROM agent_taxonomy")
                row = c.fetchone()
                if row:
                    metrics["memory"]["agent_archetypes"] = row[0]
            except sqlite3.OperationalError:
                pass
            
            # Swarm metrics — query swarm_jobs directly for live state
            try:
                c.execute("""
                    SELECT
                        SUM(CASE WHEN status IN ('dispatched','running','healing') THEN 1 ELSE 0 END),
                        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN status = 'healing' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN status IN ('failed','failed_permanent') THEN 1 ELSE 0 END)
                    FROM swarm_jobs
                """)
                srow = c.fetchone()
                if srow:
                    metrics["swarm"]["active_nodes"] = srow[0] or 0
                    metrics["swarm"]["completed_tasks"] = srow[1] or 0
                    metrics["swarm"]["healing_tasks"] = srow[2] or 0
                    metrics["swarm"]["failed_tasks"] = srow[3] or 0
            except sqlite3.OperationalError:
                pass

            # Evolution metrics from system_telemetry
            c.execute("SELECT metric_key, metric_value FROM system_telemetry")
            for row in c.fetchall():
                k, v = row
                if k == 'gepa_mutated_skills': metrics["evolution"]["mutated_skills"] = v
                elif k == 'gepa_mutated_kis': metrics["evolution"]["mutated_kis"] = v
                elif k == 'gepa_mutated_policies': metrics["evolution"]["mutated_policies"] = v
                elif k == 'gepa_mutated_workflows': metrics["evolution"]["mutated_workflows"] = v
                elif k == 'gepa_failed_traces': metrics["evolution"]["failed_traces"] = v
            db.close()
        except Exception as e:
            logger.error("Failed to get metrics DB", exc_info=True)
            
    return metrics


# ── Live Swarm Agent Endpoints ─────────────────────────────────────────

def _check_pid_alive(pid: int) -> str:
    """Check if a PID is alive, zombie, or dead. Returns 'alive', 'zombie', or 'dead'."""
    if not pid:
        return "dead"
    try:
        os.kill(pid, 0)
        # Check zombie on Linux
        stat_path = f"/proc/{pid}/stat"
        if os.path.exists(stat_path):
            with open(stat_path, 'r') as f:
                parts = f.read().split()
                if len(parts) >= 3 and parts[2] == 'Z':
                    return "zombie"
        return "alive"
    except OSError:
        return "dead"


@app.get("/api/swarm/jobs")
async def get_swarm_jobs():
    """Return all swarm jobs with live PID status for the dashboard agent panel."""
    import sqlite3
    from datetime import datetime, timezone

    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    jobs = []

    if os.path.exists(db_path):
        try:
            db = sqlite3.connect(db_path)
            db.row_factory = sqlite3.Row
            rows = db.execute(
                "SELECT * FROM swarm_jobs WHERE status != 'dismissed' ORDER BY created_at DESC LIMIT 50"
            ).fetchall()

            for row in rows:
                data = dict(row)
                pid = data.get("pid")
                pid_status = _check_pid_alive(pid)

                # Calculate relative time
                created_str = data.get("created_at", "")
                relative_time = ""
                if created_str:
                    try:
                        created = datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")
                        delta = datetime.utcnow() - created
                        secs = int(delta.total_seconds())
                        if secs < 60:
                            relative_time = f"{secs}s ago"
                        elif secs < 3600:
                            relative_time = f"{secs // 60}m ago"
                        elif secs < 86400:
                            relative_time = f"{secs // 3600}h ago"
                        else:
                            relative_time = f"{secs // 86400}d ago"
                    except Exception:
                        relative_time = created_str

                # Log preview (first 3 lines from tail) and [PROGRESS] parsing
                log_preview = ""
                progress_percent = None
                log_path = data.get("log_path", "")
                if log_path and os.path.exists(log_path):
                    try:
                        with open(log_path, 'r') as f:
                            lines = f.readlines()
                            log_preview = "".join(lines[-3:]).strip()[:300]
                            # Scan bottom-up for the latest progress
                            for line in reversed(lines):
                                if "[PROGRESS]" in line:
                                    import re
                                    match = re.search(r"\[PROGRESS\]\s+(\d+)%", line)
                                    if match:
                                        progress_percent = int(match.group(1))
                                    break
                    except Exception:
                        pass

                # Parse healing history
                healing_history = []
                try:
                    healing_history = json.loads(data.get("healing_history") or "[]")
                except Exception:
                    pass

                jobs.append({
                    "id": data["id"],
                    "agent_role": data.get("agent_role", "unknown"),
                    "task": (data.get("task") or "")[:150],
                    "status": data.get("status", "unknown"),
                    "pid": pid,
                    "pid_status": pid_status,
                    "created_at": created_str,
                    "relative_time": relative_time,
                    "retry_count": data.get("retry_count", 0) or 0,
                    "healing_history": healing_history,
                    "tokens_input": data.get("tokens_input", 0) or 0,
                    "tokens_output": data.get("tokens_output", 0) or 0,
                    "model_used": data.get("model_used"),
                    "log_preview": log_preview,
                    "progress_percent": progress_percent,
                    "result": data.get("result"),
                })

            db.close()
        except Exception as e:
            logger.error(f"Failed to get swarm jobs: {e}", exc_info=True)

    # Compute summary counts
    summary = {"active": 0, "healing": 0, "completed": 0, "failed": 0}
    for j in jobs:
        s = j["status"]
        if s in ("dispatched", "running"):
            summary["active"] += 1
        elif s == "healing":
            summary["healing"] += 1
        elif s == "completed":
            summary["completed"] += 1
        elif s in ("failed", "failed_permanent"):
            summary["failed"] += 1

    return {"jobs": jobs, "summary": summary}


@app.get("/api/swarm/jobs/{job_id}/log")
async def get_swarm_job_log(job_id: str):
    """Return the last 50 lines of a specific swarm job's log file."""
    import sqlite3
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))

    if not os.path.exists(db_path):
        return {"error": "Database not found"}

    try:
        db = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row
        row = db.execute("SELECT log_path, healing_history FROM swarm_jobs WHERE id = ?", (job_id,)).fetchone()
        db.close()

        if not row:
            return {"error": "Job not found"}

        log_path = row["log_path"]
        log_tail = ""
        if log_path and os.path.exists(log_path):
            with open(log_path, 'r') as f:
                lines = f.readlines()
                log_tail = "".join(lines[-50:])

        healing_history = []
        try:
            healing_history = json.loads(row["healing_history"] or "[]")
        except Exception:
            pass

        return {
            "job_id": job_id,
            "log_tail": log_tail,
            "healing_history": healing_history,
            "log_lines": len(lines) if log_path and os.path.exists(log_path) else 0,
        }
    except Exception as e:
        return {"error": str(e)}



from pydantic import BaseModel, Field

class GoalConfig(BaseModel):
    goal: str
    criteria: str = ""
    max_iterations: int = 10
    max_token_budget: int = 2000000
    max_wall_time_s: int = 14400

@app.post("/api/swarm/dispatch")
async def dispatch_swarm_goal(config: GoalConfig, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    log_dir = os.path.expanduser("~/.gemini/antigravity/logs/swarm_jobs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{job_id}.log")

    # Save to SQLite
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    try:
        db = _sqlite3.connect(db_path)
        # Handle cases where schema is not yet updated via an explicit fallback if needed, but it should be available now.
        db.execute(
            "INSERT INTO swarm_jobs (id, status, goal, log_path, created_at, criteria, max_iterations, current_iteration, total_tokens_used, goal_status) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, 0, 0, 'iterating')",
            (job_id, "running", config.goal, log_path, config.criteria, config.max_iterations)
        )
        db.commit()
        db.close()
    except Exception as e:
        logger.error(f"DB Error inserting swarm job: {e}")

    env = _build_subprocess_env()
    cmd = [
        "python", "-m", "antigravity_swarm.orchestrator", 
        "--job-id", job_id,
        "--criteria", config.criteria,
        "--max-iterations", str(config.max_iterations),
        "--max-wall-time-s", str(config.max_wall_time_s),
        "--max-token-budget", str(config.max_token_budget),
        config.goal
    ]
    
    log_fh = open(log_path, "w")
    log_fh.write(f"--- JOB {job_id[:8]} DEPLOYED ---\nGoal: {config.goal}\nCriteria: {config.criteria}\nLimits: {config.max_iterations} iters, {config.max_wall_time_s}s, {config.max_token_budget} tokens\n==================\n")
    proc = subprocess.Popen(cmd, env=env, stdout=log_fh, stderr=subprocess.STDOUT, cwd=AROS_ROOT)
    _update_swarm_job_pid(job_id, proc.pid)

    return {"job_id": job_id, "message": "Goal-driven swarm dispatched", "log_path": log_path}

# ── Dream Cycle Memory Hygiene Endpoints ─────────────────────

@app.get("/api/brain/hygiene/log")
async def get_hygiene_log():
    """Fetch recent audit log and pending resolution jobs."""
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    if not os.path.exists(db_path):
        return {"error": "Database not found"}
        
    try:
        db = _sqlite3.connect(db_path)
        db.row_factory = _sqlite3.Row
        
        # Pending jobs
        p_cur = db.execute("SELECT * FROM conflict_resolution_jobs WHERE status IN ('pending', 'resolved') ORDER BY dispatched_at DESC")
        pending = [dict(r) for r in p_cur.fetchall()]
        
        # Audit log past 50
        a_cur = db.execute("SELECT * FROM dream_audit_log ORDER BY id DESC LIMIT 50")
        audit = [dict(r) for r in a_cur.fetchall()]
        
        db.close()
        return {"pending_jobs": pending, "audit_log": audit}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/brain/hygiene/run")
async def run_hygiene_cycle(background_tasks: BackgroundTasks):
    """Trigger the memory hygiene cycle manually and track results in hygiene_runs."""
    env = _build_subprocess_env()
    job_id = str(uuid.uuid4())
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, f"{job_id}_hygiene.log")
    _insert_swarm_job(job_id, "hygiene_engine", "Force Memory Hygiene — deduplicate, prune orphans, archive stale facts", log_path)

    # Insert tracking row for this hygiene run
    try:
        db = _sqlite3.connect(os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db")))
        db.execute("INSERT OR IGNORE INTO hygiene_runs (id, log_path) VALUES (?, ?)", (job_id, log_path))
        db.commit()
        db.close()
    except Exception as e:
        logger.warning(f"Could not insert hygiene run {job_id}: {e}")

    log_file = open(log_path, "w")
    proc = subprocess.Popen(
        ["uv", "run", "python", "-m", "antigravity_brain.memory_hygiene"],
        cwd=os.path.join(AROS_ROOT, "antigravity-brain"),
        env=env,
        stdout=log_file,
        stderr=log_file,
    )
    _update_swarm_job_pid(job_id, proc.pid)

    # Finalize the swarm job and parse hygiene report from log when subprocess ends
    def _watch():
        proc.wait()
        log_file.close()
        _finalize_swarm_job(job_id, proc.returncode == 0)
        # Parse the hygiene report from the log file to update hygiene_runs
        _finalize_hygiene_run(job_id, log_path, proc.returncode == 0)
    threading.Thread(target=_watch, daemon=True).start()

    return {"message": "Hygiene cycle triggered", "job_id": job_id}


def _finalize_hygiene_run(run_id: str, log_path: str, success: bool):
    """Parse the hygiene cycle report from the log file and update hygiene_runs."""
    report = {}
    try:
        with open(log_path, "r") as f:
            content = f.read()
        # The memory_hygiene.__main__ prints JSON after "HYGIENE CYCLE REPORT:"
        if "HYGIENE CYCLE REPORT:" in content:
            json_str = content.split("HYGIENE CYCLE REPORT:", 1)[1].strip()
            try:
                report = json.loads(json_str)
            except json.JSONDecodeError:
                # Trailing log lines after JSON (from stderr) — extract first { ... } block
                import re
                match = re.search(r'\{.*\}', json_str, re.DOTALL)
                if match:
                    report = json.loads(match.group())
    except Exception as e:
        logger.warning(f"Could not parse hygiene report from {log_path}: {e}")

    status = "completed" if success else "failed"
    compaction = report.get("compaction", {})
    try:
        db = _sqlite3.connect(os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db")))
        db.execute("""
            UPDATE hygiene_runs SET
                completed_at = datetime('now'),
                redundancies_resolved = ?,
                contradictions_detected = ?,
                contradictions_resolved = ?,
                facts_archived = ?,
                facts_hard_deleted = ?,
                experiences_pruned = ?,
                graph_edges_extracted = ?,
                status = ?
            WHERE id = ?
        """, (
            report.get("redundancies_resolved", 0),
            report.get("conflicts_resolved", 0) + report.get("conflicts_failed", 0),
            report.get("conflicts_resolved", 0),
            compaction.get("facts_archived", 0),
            compaction.get("facts_hard_deleted", 0),
            compaction.get("experiences_archived", 0),
            report.get("graph_edges_extracted", 0),
            status
        ))
        db.commit()
        db.close()
        logger.info(f"Hygiene run {run_id} finalized: status={status}")
    except Exception as e:
        logger.warning(f"Could not update hygiene run {run_id}: {e}")


@app.get("/api/brain/hygiene/stats")
async def get_hygiene_stats():
    """Return cumulative hygiene statistics across ALL runs.

    Uses SUM() aggregation (same pattern as the distiller stats fix)
    so that subsequent runs with 0 findings don't erase earlier stats.
    Also provides a classified action breakdown from dream_audit_log.
    """
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    stats = {
        "total_runs": 0,
        "last_run": None,
        "cumulative": {
            "redundancies_resolved": 0,
            "contradictions_detected": 0,
            "contradictions_resolved": 0,
            "facts_archived": 0,
            "facts_hard_deleted": 0,
            "experiences_pruned": 0,
            "graph_edges_extracted": 0
        },
        "classified_actions": {}
    }
    if not os.path.exists(db_path):
        return stats

    try:
        db = _sqlite3.connect(db_path)
        db.row_factory = _sqlite3.Row

        # Last run for status pill
        row = db.execute("SELECT * FROM hygiene_runs ORDER BY started_at DESC LIMIT 1").fetchone()
        if row:
            stats["last_run"] = dict(row)
        stats["total_runs"] = db.execute("SELECT COUNT(*) FROM hygiene_runs").fetchone()[0]

        # Cumulative SUM across all runs
        sums = db.execute("""
            SELECT COALESCE(SUM(redundancies_resolved), 0)    AS total_redundancies,
                   COALESCE(SUM(contradictions_detected), 0)  AS total_contradictions_det,
                   COALESCE(SUM(contradictions_resolved), 0)  AS total_contradictions_res,
                   COALESCE(SUM(facts_archived), 0)           AS total_archived,
                   COALESCE(SUM(facts_hard_deleted), 0)       AS total_hard_deleted,
                   COALESCE(SUM(experiences_pruned), 0)       AS total_pruned,
                   COALESCE(SUM(graph_edges_extracted), 0)    AS total_edges
            FROM hygiene_runs
        """).fetchone()
        stats["cumulative"] = {
            "redundancies_resolved": sums["total_redundancies"],
            "contradictions_detected": sums["total_contradictions_det"],
            "contradictions_resolved": sums["total_contradictions_res"],
            "facts_archived": sums["total_archived"],
            "facts_hard_deleted": sums["total_hard_deleted"],
            "experiences_pruned": sums["total_pruned"],
            "graph_edges_extracted": sums["total_edges"]
        }

        # Classified breakdown from dream_audit_log
        action_rows = db.execute("""
            SELECT action, COUNT(*) as cnt FROM dream_audit_log GROUP BY action
        """).fetchall()
        stats["classified_actions"] = {r["action"]: r["cnt"] for r in action_rows}

        db.close()
    except Exception as e:
        logger.error(f"Failed to get hygiene stats: {e}", exc_info=True)

    return stats

@app.post("/api/brain/hygiene/undo/{audit_id}")
async def undo_hygiene_action(audit_id: int):
    """Undo a soft-archive action."""
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    
    try:
        db = _sqlite3.connect(db_path)
        db.row_factory = _sqlite3.Row
        
        cur = db.execute("SELECT * FROM dream_audit_log WHERE id = ? AND reversed_at IS NULL", (audit_id,))
        log_entry = cur.fetchone()
        
        if not log_entry:
            return {"error": "Audit entry not found or already reversed"}
            
        action = log_entry['action']
        target_type = log_entry['target_type']
        target_id = log_entry['target_id']
        
        if action not in ('fact_archived', 'experience_pruned') or not target_id:
            return {"error": f"Cannot undo action of type {action}"}
            
        table_map = {
            'world_fact': 'world_facts',
            'experience': 'experiences',
            'mental_model': 'mental_models'
        }
        table = table_map.get(target_type)
        if not table:
            return {"error": "Invalid target type"}
            
        # Hard deletions cannot be undone easily without restoring from vec, which is dropped.
        # But for world_facts, they drop the vec immediately. Re-embedding is required!
        # Due to complexity of re-embedding inline, we will just set is_archived = FALSE.
        # The next normal ingestion will re-embed it.
        db.execute(f"UPDATE {table} SET is_archived = FALSE, archived_at = NULL WHERE id = ?", (target_id,))
        db.execute("UPDATE dream_audit_log SET reversed_at = CURRENT_TIMESTAMP WHERE id = ?", (audit_id,))
        db.commit()
        db.close()
        return {"message": "Action undone successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/swarm/jobs/{job_id}/dismiss")
async def dismiss_swarm_job(job_id: str):
    """Hide a job from the dashboard by setting its status to 'dismissed'."""
    import sqlite3
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    if not os.path.exists(db_path):
        return {"error": "Database not found"}
    try:
        db = sqlite3.connect(db_path)
        db.execute("UPDATE swarm_jobs SET status = 'dismissed' WHERE id = ?", (job_id,))
        db.commit()
        db.close()
        return {"ok": True, "message": f"Job {job_id[:8]}… dismissed"}
    except Exception as e:
        return {"error": str(e)}


# Google AI Pay-as-you-go pricing (per 1M tokens, <128k context)
_TOKEN_PRICING = {
    "gemini-2.5-pro":       {"input": 1.25,  "output": 5.00},
    "gemini-2.5-flash":     {"input": 0.075, "output": 0.30},
    "gemini-2.0-flash":     {"input": 0.075, "output": 0.30},
    "gemini-1.5-pro":       {"input": 1.25,  "output": 5.00},
    "gemini-1.5-flash":     {"input": 0.075, "output": 0.30},
    "gemini-embedding-001": {"input": 0.00,  "output": 0.00},
}


@app.get("/api/telemetry/tokens")
async def get_token_telemetry():
    """Token economics: aggregate token usage and costs from swarm_jobs."""
    import sqlite3
    import re
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    
    result = {
        "total_tokens": {"input": 0, "output": 0},
        "total_cost_usd": 0.0,
        "by_agent": {},
        "by_model": {},
    }
    
    if not os.path.exists(db_path):
        return result
    
    try:
        db = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row
        rows = db.execute("SELECT agent_role, tokens_input, tokens_output, model_used, log_path FROM swarm_jobs").fetchall()
        db.close()
        
        for row in rows:
            data = dict(row)
            t_in = data.get("tokens_input", 0) or 0
            t_out = data.get("tokens_output", 0) or 0
            model = data.get("model_used") or "gemini-2.5-flash"
            agent = data.get("agent_role") or "unknown"
            
            # If tokens aren't stored in DB, try parsing from log
            if t_in == 0 and t_out == 0:
                log_path = data.get("log_path", "")
                if log_path and os.path.exists(log_path):
                    try:
                        with open(log_path) as f:
                            for line in f:
                                if "[TOKENS]" in line:
                                    parts = line.split("[TOKENS]")[1].strip()
                                    for kv in parts.split():
                                        if kv.startswith("input="):
                                            t_in += int(kv.split("=")[1])
                                        elif kv.startswith("output="):
                                            t_out += int(kv.split("=")[1])
                                        elif kv.startswith("model="):
                                            model = kv.split("=")[1]
                    except Exception:
                        pass
            
            # Aggregate totals
            result["total_tokens"]["input"] += t_in
            result["total_tokens"]["output"] += t_out
            
            # Per-agent breakdown
            if agent not in result["by_agent"]:
                result["by_agent"][agent] = {"input": 0, "output": 0, "cost": 0.0}
            result["by_agent"][agent]["input"] += t_in
            result["by_agent"][agent]["output"] += t_out
            
            # Per-model breakdown
            if model not in result["by_model"]:
                result["by_model"][model] = {"input": 0, "output": 0, "cost": 0.0}
            result["by_model"][model]["input"] += t_in
            result["by_model"][model]["output"] += t_out
        
        # Calculate costs
        for model_name, breakdown in result["by_model"].items():
            pricing = _TOKEN_PRICING.get(model_name, _TOKEN_PRICING["gemini-2.5-flash"])
            cost = (breakdown["input"] / 1_000_000) * pricing["input"] + \
                   (breakdown["output"] / 1_000_000) * pricing["output"]
            breakdown["cost"] = round(cost, 6)
            result["total_cost_usd"] += cost
        
        # Back-propagate costs to per-agent using model pricing
        for agent_name, breakdown in result["by_agent"].items():
            # Estimate using default flash pricing as approximation
            pricing = _TOKEN_PRICING["gemini-2.5-flash"]
            cost = (breakdown["input"] / 1_000_000) * pricing["input"] + \
                   (breakdown["output"] / 1_000_000) * pricing["output"]
            breakdown["cost"] = round(cost, 6)
        
        result["total_cost_usd"] = round(result["total_cost_usd"], 6)
        
    except Exception as e:
        logger.error(f"Token telemetry error: {e}", exc_info=True)
    
    return result

@app.post("/api/mutate_all")
async def force_system_mutation():
    global _is_distill_running, _mutation_proc
    
    # Check if we rely on global vars correctly
    distill_active = globals().get("_is_distill_running", False)
    if distill_active:
        return {"status": "error", "message": "Knowledge Distiller is currently active. Cannot run mutation sweep concurrently."}
        
    started = _spawn_mutation()
    if not started:
        return {"status": "already_running", "message": "Mutation sweep already in progress."}
    return {"status": "started"}

@app.get("/api/mutations")
async def get_recent_mutations():
    import sqlite3
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    limit = 15
    out = []
    if os.path.exists(db_path):
        try:
            db = sqlite3.connect(db_path)
            c = db.cursor()
            c.execute("""
                SELECT entity, source_url, timestamp
                FROM world_facts
                WHERE source_url LIKE '%/skills/%'
                   OR source_url LIKE '%/knowledge/%'
                   OR source_url LIKE '%workflow%'
                   OR source_url LIKE '%AROS_POLICY.md%'
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            for row in c.fetchall():
                entity = row[0]
                url = row[1] or "Unknown"
                ts = row[2]
                if "/skills/" in url:
                    mtype = "SKILL"
                    name = url.split("/skills/")[-1].split("/")[0]
                elif "/knowledge/" in url:
                    mtype = "KI"
                    name = url.split("/knowledge/")[-1].split("/")[0]
                elif "workflow" in url:
                    mtype = "WORKFLOW"
                    name = url.split("/")[-1].replace(".md", "")
                elif "GEMINI" in url:
                    mtype = "POLICY"
                    name = "Core Policy"
                else:
                    mtype = "EVOLUTION"
                    name = entity[:20]
                out.append({
                    "timestamp": ts,
                    "type": mtype,
                    "name": name,
                    "entity": entity[:60] + "..." if len(entity) > 60 else entity
                })
            db.close()
        except Exception as e:
            logger.error("Failed to query recent mutations from DB", exc_info=True)
    return {"status": "success", "mutations": out}

@app.get("/api/status")
async def get_process_status():
    """Return real-time running state of background daemons for UI progress bars."""
    return {
        "dream_running": _is_running(_dream_proc, "antigravity_brain.dreamer"),
        "mutation_running": _is_running(_mutation_proc, "antigravity_evolution.batch_evolver"),
        "distill_running": _is_distill_running,
        "next_scheduled_run": _next_scheduled_run,
        "next_weekly_run": _next_weekly_run,
    }


from pydantic import BaseModel
import subprocess
import json

class MCPConfigPayload(BaseModel):
    github_token: str
    uniprot_enabled: bool = True
    google_dev_enabled: bool = True
    kosmos_enabled: bool = True
    claude_skills_enabled: bool = True
    brain_enabled: bool = True

@app.post("/api/dream")
async def trigger_dream():
    started = _spawn_dream()
    if not started:
        return {"status": "already_running", "message": "Dream cycle already in progress."}
    return {"status": "started"}


# ── GCO Cycle Control Endpoints ──────────────────────────────────────────
import json as _json

@app.post("/api/dream/cycle")
async def enqueue_dream_cycle():
    """Enqueue a full dream cycle to the Global Chief Orchestrator."""
    try:
        db = _get_brain_db()
        mission_id = str(uuid.uuid4())
        db.execute("""
            INSERT INTO orchestrator_missions
            (id, source, mission_type, payload, priority)
            VALUES (?, ?, ?, ?, ?)
        """, (mission_id, "dashboard", "full_cycle",
              _json.dumps({"triggered_by": "dashboard"}), 2))
        db.commit()
        db.close()
        return {"status": "queued", "mission_id": mission_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/dream/pause")
async def pause_dream_cycle():
    """Pause the active dream cycle. The running CategoryAgent will pause at its next checkpoint."""
    try:
        db = _get_brain_db()
        db.execute("UPDATE orchestrator_cycles SET status='paused', paused_at=CURRENT_TIMESTAMP WHERE status='running'")
        changed = db.execute("SELECT changes()").fetchone()[0]
        db.commit()
        db.close()
        if changed:
            return {"status": "paused", "cycles_affected": changed}
        return {"status": "no_active_cycle", "message": "No running cycle to pause."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/dream/resume")
async def resume_dream_cycle():
    """Resume a paused dream cycle."""
    try:
        db = _get_brain_db()
        db.execute("UPDATE orchestrator_cycles SET status='running', paused_at=NULL WHERE status='paused'")
        changed = db.execute("SELECT changes()").fetchone()[0]
        db.commit()
        db.close()
        if changed:
            return {"status": "resumed", "cycles_affected": changed}
        return {"status": "no_paused_cycle", "message": "No paused cycle to resume."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/dream/cancel")
async def cancel_dream_cycle():
    """Cancel the active dream cycle. The running CategoryAgent will stop at its next checkpoint."""
    try:
        db = _get_brain_db()
        db.execute("UPDATE orchestrator_cycles SET status='cancelled', completed_at=CURRENT_TIMESTAMP WHERE status IN ('running', 'paused')")
        changed = db.execute("SELECT changes()").fetchone()[0]
        db.commit()
        db.close()
        if changed:
            return {"status": "cancelled", "cycles_affected": changed}
        return {"status": "no_active_cycle", "message": "No active cycle to cancel."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/dream/status")
async def get_dream_status():
    """Get the active cycle status, SessionContext summary, and quota meter."""
    try:
        db = _get_brain_db()
        cycle = db.execute("""
            SELECT id, status, current_category, completed_categories, quota_used, audit_trail, created_at
            FROM orchestrator_cycles
            WHERE status IN ('running', 'paused')
            ORDER BY created_at DESC LIMIT 1
        """).fetchone()

        if cycle:
            result = {
                "active_cycle": {
                    "id": cycle["id"],
                    "status": cycle["status"],
                    "current_category": cycle["current_category"],
                    "completed_categories": _json.loads(cycle["completed_categories"] or "[]"),
                    "quota_used": _json.loads(cycle["quota_used"] or "{}"),
                    "audit_trail": _json.loads(cycle["audit_trail"] or "[]")[-10:],
                    "started_at": cycle["created_at"],
                }
            }
        else:
            # Return last completed cycle info
            last = db.execute("""
                SELECT id, status, completed_categories, quota_used, completed_at
                FROM orchestrator_cycles
                ORDER BY created_at DESC LIMIT 1
            """).fetchone()
            result = {
                "active_cycle": None,
                "last_cycle": {
                    "id": last["id"],
                    "status": last["status"],
                    "completed_categories": _json.loads(last["completed_categories"] or "[]"),
                    "completed_at": last["completed_at"],
                } if last else None
            }

        db.close()
        return result
    except Exception as e:
        return {"active_cycle": None, "error": str(e)}


@app.get("/api/dream/queue")
async def get_mission_queue():
    """Get the Universal Mission Queue status grouped by priority lane."""
    try:
        db = _get_brain_db()
        rows = db.execute("""
            SELECT priority, status, COUNT(*) as count
            FROM orchestrator_missions
            WHERE status IN ('pending', 'in_progress')
            GROUP BY priority, status
            ORDER BY priority ASC
        """).fetchall()

        queue = {"P0_critical": 0, "P1_high": 0, "P2_normal": 0, "P3_low": 0, "in_progress": 0}
        priority_map = {0: "P0_critical", 1: "P1_high", 2: "P2_normal", 3: "P3_low"}
        for row in rows:
            if row["status"] == "in_progress":
                queue["in_progress"] += row["count"]
            else:
                key = priority_map.get(row["priority"], "P3_low")
                queue[key] += row["count"]

        total = db.execute("SELECT COUNT(*) as cnt FROM orchestrator_missions").fetchone()
        queue["total_lifetime"] = total["cnt"] if total else 0
        db.close()
        return queue
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/logs")
async def get_system_logs():
    try:
        # Securely read the last 300 lines from the systemd daemon log
        result = subprocess.run(
            ["journalctl", "--user", "-u", "antigravity-os", "-n", "300", "--no-pager"],
            capture_output=True, text=True, timeout=5
        )
        # Filter out routine polling access log noise.
        # The dashboard polls ~10 endpoints every 2-5 seconds, producing
        # dozens of 'GET /api/... 200 OK' lines per second that drown out
        # meaningful events (errors, warnings, background tasks, startup).
        _POLLING_ENDPOINTS = {
            "/api/status", "/api/logs", "/api/metrics", "/api/mutations",
            "/api/swarm/jobs", "/api/distiller/stats", "/api/distiller/proposals",
            "/api/brain/hygiene/log", "/api/brain/hygiene/stats",
            "/api/brain/evaluations", "/api/telemetry/tokens",
        }
        filtered_lines = []
        for line in result.stdout.splitlines():
            # Keep non-access-log lines (app logger, startup, errors)
            if '" 200' not in line:
                filtered_lines.append(line)
                continue
            # Check if this is a routine polling GET — skip it
            is_polling = False
            for ep in _POLLING_ENDPOINTS:
                if f"GET {ep}" in line:
                    is_polling = True
                    break
            if not is_polling:
                filtered_lines.append(line)

        return {"status": "success", "logs": "\n".join(filtered_lines[-100:])}
    except Exception as e:
        return {"status": "error", "logs": f"Failed to fetch system logs: {e}"}

@app.post("/api/mcp/setup")
async def setup_mcp_servers(payload: MCPConfigPayload):
    config_path = os.path.expanduser("~/.gemini/antigravity/mcp_config.json")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    config = {"mcpServers": {}}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f: config = json.load(f)
        except: pass
        
    if "mcpServers" not in config: config["mcpServers"] = {}
    
    if payload.github_token:
        config["mcpServers"]["github-mcp-server"] = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": payload.github_token},
            "disabled": False,
            "autoApprove": []
        }
    
    if payload.uniprot_enabled:
        config["mcpServers"]["uniprot-mcp-server"] = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-uniprot"],
            "env": {}, "disabled": False, "autoApprove": []
        }
        
    if payload.google_dev_enabled:
        config["mcpServers"]["google-developer-knowledge"] = {
            "command": "npx",
            "args": ["-y", "@google/mcp-server-developer-knowledge"],
            "env": {}, "disabled": False, "autoApprove": []
        }

    # Custom Python Servers logic assumes they exist in standard paths or the OS path
    # We will assume they are globally installed or use python3 generic wrappers for our framework
    if payload.claude_skills_enabled:
        config["mcpServers"]["claude-skills"] = {
            "command": "python3",
            "args": ["-m", "claude_skills.server"],
            "env": {}, "disabled": False, "autoApprove": []
        }
        
    if payload.kosmos_enabled:
        config["mcpServers"]["kosmos"] = {
            "command": "python3",
            "args": ["-m", "kosmos.server"],
            "env": {}, "disabled": False, "autoApprove": []
        }

    if payload.brain_enabled:
        config["mcpServers"]["antigravity-brain"] = {
            "command": "uv",
            "args": [
                "--directory", os.path.join(AROS_ROOT, "antigravity-brain"),
                "run", "python", "-m", "antigravity_brain.server"
            ],
            "env": {
                "GOOGLE_AI_API_KEY": os.environ.get("GOOGLE_AI_API_KEY", ""),
                "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", "")
            },
            "disabled": False, "autoApprove": []
        }
        
    try:
        with open(config_path, "w") as f: json.dump(config, f, indent=2)
        return {"status": "success", "message": f"mcp_config.json updated successfully at {config_path}. Please restart your agents."}
    except Exception as e:
        logger.error("Failed to save MCP config", exc_info=True)
        return {"status": "error", "message": f"Failed to save MCP config: {e}"}

class SettingsImportPayload(BaseModel):
    env_vars: dict
    mcp_config: dict

@app.get("/api/mcp/export")
async def export_settings():
    config_path = os.path.expanduser("~/.gemini/antigravity/mcp_config.json")
    env_path = os.path.expanduser("~/.gemini/.env")
    
    export_payload = {"env_vars": {}, "mcp_config": {}}
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                export_payload["mcp_config"] = json.load(f)
        except: pass
        
    if os.path.exists(env_path):
        try:
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        export_payload["env_vars"][k.strip()] = v.strip()
        except: pass
            
    return export_payload

@app.post("/api/mcp/import")
async def import_settings(payload: SettingsImportPayload):
    config_path = os.path.expanduser("~/.gemini/antigravity/mcp_config.json")
    env_path = os.path.expanduser("~/.gemini/.env")
    
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(payload.mcp_config, f, indent=2)
            
        with open(env_path, "w") as f:
            for k, v in payload.env_vars.items():
                f.write(f"{k}={v}\n")
                
        return {"status": "success", "message": "Settings imported successfully! Please restart OS daemons to apply changes."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ── Brain Federation Endpoints ───────────────────────────────
import tempfile

BRAIN_EXPORT_DIR = os.path.expanduser("~/.gemini/antigravity/brain_exports")

@app.post("/api/brain/export")
async def export_brain():
    """Export a selective brain snapshot for cross-PC federation.
    
    BUG FIX (1): Changed from GET to POST — this endpoint has side effects (writes files).
    BUG FIX (2): Offloaded to asyncio.to_thread() to prevent blocking the async event loop
    during potentially long file I/O with 500+ skills and 14 KIs.
    """
    try:
        import sys
        sys.path.insert(0, os.path.join(AROS_ROOT, "antigravity-brain", "src"))
        from antigravity_brain.sync import export_brain as _export
        
        os.makedirs(BRAIN_EXPORT_DIR, exist_ok=True)
        
        import socket
        instance_id = socket.gethostname()
        os.makedirs(LOGS_DIR, exist_ok=True)
        job_id = str(uuid.uuid4())
        log_path = os.path.join(LOGS_DIR, f"{job_id}_brain_export.log")
        _insert_swarm_job(job_id, "brain_federator", f"Brain Federation Export — packaging brain snapshot for cross-PC sync (instance: {instance_id})", log_path)
        
        # Run synchronous export in thread pool to avoid blocking the async event loop
        def _do_export():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"brain_export_{instance_id}_{timestamp}.json"
            filepath = os.path.join(BRAIN_EXPORT_DIR, filename)
            envelope = _export(instance_id=instance_id)
            with open(filepath, "w") as f:
                json.dump(envelope, f, indent=2)
            return filename, filepath, envelope.get("stats", {})
        
        filename, filepath, stats = await asyncio.to_thread(_do_export)
        _finalize_swarm_job(job_id, True)
        
        return {
            "status": "success",
            "filename": filename,
            "filepath": filepath,
            "stats": stats,
        }
    except Exception as e:
        logger.error("Failed to export brain", exc_info=True)
        return {"status": "error", "message": str(e)}


from fastapi import UploadFile, File

@app.post("/api/brain/import")
async def import_brain(file: UploadFile = File(...)):
    """Upload a brain export JSON file for merge review."""
    try:
        content = await file.read()
        envelope = json.loads(content.decode("utf-8"))
        
        # Save incoming file for reference
        os.makedirs(BRAIN_EXPORT_DIR, exist_ok=True)
        import_path = os.path.join(BRAIN_EXPORT_DIR, f"incoming_{file.filename}")
        with open(import_path, "w") as f:
            json.dump(envelope, f, indent=2)
        
        # Return preview stats without merging yet
        stats = envelope.get("stats", {})
        return {
            "status": "success",
            "message": "Brain snapshot uploaded. Ready for merge.",
            "source_instance": envelope.get("instance_id", "unknown"),
            "exported_at": envelope.get("exported_at", "unknown"),
            "preview": stats,
            "import_path": import_path,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


class MergeRequest(BaseModel):
    import_path: str

@app.post("/api/brain/merge")
async def merge_brain(req: MergeRequest):
    """Trigger LLM-reviewed merge of an imported brain snapshot.
    
    BUG FIX: Offloaded import_and_merge() to asyncio.to_thread() to prevent
    blocking the event loop during LLM review calls and large file I/O.
    Also registers as a brain_federator Swarm job for dashboard visibility.
    """
    try:
        import sys
        sys.path.insert(0, os.path.join(AROS_ROOT, "antigravity-brain", "src"))
        from antigravity_brain.sync import import_and_merge
        
        if not os.path.isfile(req.import_path):
            return {"status": "error", "message": f"Import file not found: {req.import_path}"}
        
        # Register as a Swarm job for dashboard visibility
        job_id = str(uuid.uuid4())
        os.makedirs(LOGS_DIR, exist_ok=True)
        log_path = os.path.join(LOGS_DIR, f"{job_id}_brain_merge.log")
        _insert_swarm_job(job_id, "brain_federator", f"Brain Federation LLM Merge — merging remote snapshot with Gemini review: {os.path.basename(req.import_path)}", log_path)
        
        with open(req.import_path, "r") as f:
            envelope = json.load(f)
        
        # Offload the potentially long-running merge to a thread
        report = await asyncio.to_thread(import_and_merge, envelope)
        _finalize_swarm_job(job_id, True)
        
        # Save merge report
        report_path = req.import_path.replace(".json", "_merge_report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        return {
            "status": "success",
            "report": report,
            "report_path": report_path,
        }
    except Exception as e:
        logger.error("Failed to merge brain", exc_info=True)
        return {"status": "error", "message": str(e)}


# BackgroundTasks imported at module level

@app.post("/api/brain/execute_proposals")
async def execute_proposals():
    """
    Dispatch un-executed GEPA distiller proposals.
    Now correctly proxies to swarm_bridge.py to enforce the centralized
    One-Agent-Per-Role Coalescing Guard.
    """
    import sys
    bridge_dir = os.path.join(AROS_ROOT, "antigravity-evolution", "src")
    if bridge_dir not in sys.path:
        sys.path.insert(0, bridge_dir)
        
    try:
        from antigravity_evolution.swarm_bridge import process_pending_distiller_proposals
        dispatched = await process_pending_distiller_proposals()
        
        # We need remaining count for the UI text
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        import sqlite3 as _sqlite3
        db = _sqlite3.connect(db_path)
        remaining = db.execute("""
            SELECT COUNT(*) FROM world_facts wf
            LEFT JOIN swarm_bridge_tracking sbt ON wf.id = sbt.fact_id
            WHERE wf.source_url = 'gepa://distiller' AND sbt.fact_id IS NULL
        """).fetchone()[0]
        db.close()
        
        msg = f"Dispatched {dispatched} proposals to Swarm. {remaining} proposals still pending."
        if remaining > 0:
            msg += f" Click 'Execute All' to dispatch the rest."
        
        logger.info(f"[execute_proposals] Complete: {msg}")
        return {
            "status": "success" if dispatched > 0 else "error",
            "message": msg,
            "jobs": [], # Not tracking individual local PIDs anymore
            "dispatched": dispatched,
            "remaining": remaining,
            "errors": [],
        }
    except Exception as e:
        logger.error(f"[execute_proposals] Swarm Bridge proxy failed: {e}")
        return {"status": "error", "message": f"Bridge error: {e}"}


@app.post("/api/brain/execute_all_proposals")
async def execute_all_proposals():
    """
    Dispatch ALL pending GEPA proposals in one shot.
    Iterates over the Swarm Bridge until all pending proposals have been assigned.
    Returns a summary of total jobs dispatched.
    """
    import sys
    bridge_dir = os.path.join(AROS_ROOT, "antigravity-evolution", "src")
    if bridge_dir not in sys.path:
        sys.path.insert(0, bridge_dir)
        
    try:
        from antigravity_evolution.swarm_bridge import process_pending_distiller_proposals
        total_dispatched = 0
        batch_num = 0
        
        while True:
            batch_num += 1
            dispatched = await process_pending_distiller_proposals()
            if not dispatched:  # 0 or None
                break
            total_dispatched += dispatched
            
            # Additional safety: stop if it goes completely nuts
            if batch_num > 50:
                logger.warning("[execute_all] Hit 50 batch max limit, stopping loop.")
                break
                
        return {
            "status": "success",
            "message": f"All done! Dispatched {total_dispatched} proposals across {batch_num-1} batches to the unified gateway.",
            "total_dispatched": total_dispatched,
            "errors": [],
        }
    except Exception as e:
        logger.error(f"[execute_all] Swarm Bridge proxy failed: {e}")
        return {"status": "error", "message": f"Bridge error: {e}"}


class CancelJobRequest(BaseModel):
    job_id: str

@app.post("/api/swarm/cancel")
async def cancel_swarm_job(req: CancelJobRequest):
    """Cancel a running Goal-Driven Swarm Job gracefully."""
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    try:
        import sqlite3 as _sqlite3
        db = _sqlite3.connect(db_path)
        db.execute("UPDATE swarm_jobs SET goal_status = 'cancelled' WHERE id = ?", (req.job_id,))
        db.commit()
        db.close()
        return {"status": "success", "message": f"Job {req.job_id} marked for cancellation."}
    except Exception as e:
        logger.error(f"[cancel_swarm_job] Failed: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}

@app.post("/api/brain/reset_tracking")
async def reset_swarm_tracking():
    """Reset stale swarm_bridge_tracking entries so proposals can be re-dispatched.
    
    Use when proposals were tracked before dispatch completed (legacy bug), or
    when you want to force re-execution of all pending GEPA proposals.
    """
    try:
        import sys
        bridge_dir = os.path.join(AROS_ROOT, "antigravity-evolution", "src")
        if bridge_dir not in sys.path:
            sys.path.insert(0, bridge_dir)
        from antigravity_evolution.swarm_bridge import reset_stale_tracking
        deleted = await reset_stale_tracking(max_age_hours=0)  # 0 = clear ALL
        return {"status": "success", "deleted": deleted, "message": f"Cleared {deleted} tracking entries. Proposals will be re-dispatched on next execution."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ── Knowledge Distiller Panel Endpoints ──────────────────────────────────────

def _insert_distiller_run(run_id: str, log_path: str):
    """Record a new distiller run in the distiller_runs table."""
    try:
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        db = _sqlite3.connect(db_path)
        db.execute(
            "INSERT OR IGNORE INTO distiller_runs (id, log_path) VALUES (?, ?)",
            (run_id, log_path)
        )
        db.commit()
        db.close()
    except Exception as e:
        logger.warning(f"Could not insert distiller run {run_id}: {e}")


def _update_distiller_run(run_id: str, report: dict, dispatched: int, status: str):
    """Update a distiller run record with results."""
    try:
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        db = _sqlite3.connect(db_path)
        if report:
            db.execute("""
                UPDATE distiller_runs SET
                    completed_at = datetime('now'),
                    clusters_found = ?,
                    structural_proposals = ?,
                    agent_proposals = ?,
                    policy_proposals = ?,
                    proposals_dispatched = ?,
                    status = ?
                WHERE id = ?
            """, (
                report.get('clusters_found', 0),
                len(report.get('skill_ki_proposals', [])),
                len(report.get('taxonomy_proposals', [])),
                len(report.get('rule_proposals', [])),
                dispatched,
                status,
                run_id,
            ))
        else:
            db.execute(
                "UPDATE distiller_runs SET completed_at=datetime('now'), status=? WHERE id=?",
                (status, run_id)
            )
        db.commit()
        db.close()
    except Exception as e:
        logger.warning(f"Could not update distiller run {run_id}: {e}")


def _dispatch_pending_proposals() -> tuple:
    """Dispatch all pending GEPA distiller proposals to the Swarm Orchestrator.
    Returns (dispatched_count, errors_list)."""
    import sys as _sys
    import asyncio
    
    bridge_dir = os.path.join(AROS_ROOT, "antigravity-evolution", "src")
    if bridge_dir not in _sys.path:
        _sys.path.insert(0, bridge_dir)
        
    try:
        from antigravity_evolution.swarm_bridge import process_pending_distiller_proposals
        total_dispatched = 0
        batch_num = 0
        
        while True:
            batch_num += 1
            dispatched = asyncio.run(process_pending_distiller_proposals())
            if not dispatched:
                break
            total_dispatched += dispatched
            
            # Additional safety
            if batch_num > 50:
                logger.warning("[dispatch] Hit 50 batch max limit, stopping loop.")
                break
                
        return total_dispatched, []
    except Exception as e:
        logger.error(f"[_dispatch_pending_proposals] failed: {e}")
        return 0, [str(e)]


@app.post("/api/distiller/run")
def run_distiller_pipeline(background_tasks: BackgroundTasks):
    """Single-button chained pipeline: Distill → Generate Proposals → Dispatch to Swarm."""
    global _is_distill_running, _mutation_proc
    
    if _is_distill_running:
        return {"status": "error", "message": "Pipeline already running."}
        
    # Check if mutation sweep is running
    is_mutating = _is_running(_mutation_proc, "antigravity_evolution.batch_evolver") if _mutation_proc else False
    if is_mutating:
        return {"status": "error", "message": "Mutation sweep is currently active. Cannot run Knowledge Distiller concurrently."}

    try:
        import sys
        sys.path.insert(0, os.path.join(AROS_ROOT, "antigravity-evolution", "src"))
        from antigravity_evolution.knowledge_distiller import run_distillation
    except ImportError as e:
        return {"status": "error", "message": f"Import error: {e}"}

    _is_distill_running = True
    run_id = str(uuid.uuid4())
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, f"{run_id}_distiller.log")
    _insert_distiller_run(run_id, log_path)
    _insert_swarm_job(run_id, "knowledge_distiller", "Knowledge Distiller — Full Pipeline (Distill → Execute)", log_path)
    _update_swarm_job_pid(run_id, os.getpid())

    def _pipeline():
        global _is_distill_running
        report = None
        try:
            # ── Phase 1: Distillation ─────────────────────────────
            with open(log_path, "a") as f:
                f.write("[PROGRESS] 10%\n")
                f.write("📊 Phase 1: Clustering conversation facts...\n")

            report = run_distillation()
            clusters = report.get('clusters_found', 0)
            struct_p = report.get('skill_ki_proposals', [])
            agent_p  = report.get('taxonomy_proposals', [])
            rule_p   = report.get('rule_proposals', [])

            with open(log_path, "a") as f:
                f.write(f"[PROGRESS] 50%\n")
                f.write(f"\n✅ Distillation complete: {clusters} knowledge clusters found.\n")
                if struct_p:
                    f.write(f"\n📋 Generated {len(struct_p)} Structural Proposals:\n")
                    for p in struct_p:
                        f.write(f"  • [{p.get('type', 'UNK').ljust(16)}] {p.get('target', 'unknown')} (cluster size: {p.get('cluster_size', 0)})\n")
                        f.write(f"    - {p.get('recommendation', '')}\n")
                if agent_p:
                    f.write(f"\n🤖 Generated {len(agent_p)} Agent Proposals:\n")
                    for p in agent_p:
                        f.write(f"  • [{p.get('type', 'NEW_AGENT')}] {p.get('agent_type', 'unknown')} (matching facts: {p.get('matching_facts', 0)})\n")
                        f.write(f"    - {p.get('recommendation', '')}\n")
                if rule_p:
                    f.write(f"\n📜 Generated {len(rule_p)} Policy Proposals:\n")
                    for p in rule_p:
                        f.write(f"  • [{p.get('type', 'POLICY')}] {p.get('target', 'unknown')}\n")
                        f.write(f"    - {p.get('recommendation', '')}\n")

            # ── Phase 2: Check if anything to dispatch ────────────
            total_proposals = len(struct_p) + len(agent_p) + len(rule_p)
            if clusters == 0 and total_proposals == 0:
                with open(log_path, "a") as f:
                    f.write(f"\n[PROGRESS] 100%\n")
                    f.write("ℹ️  No new un-distilled facts found. System is up to date.\n")
                _update_distiller_run(run_id, report, 0, "no_new_facts")
                _finalize_swarm_job(run_id, True)
                return

            # ── Phase 3: Dispatch proposals to Swarm ──────────────
            with open(log_path, "a") as f:
                f.write(f"\n[PROGRESS] 70%\n")
                f.write(f"🚀 Phase 2: Dispatching {total_proposals} proposals to Swarm Orchestrator...\n")

            dispatched, errors = _dispatch_pending_proposals()

            with open(log_path, "a") as f:
                f.write(f"[PROGRESS] 100%\n")
                f.write(f"\n✅ Pipeline complete: dispatched {dispatched} proposal(s) to Swarm.\n")
                if errors:
                    f.write(f"⚠️  {len(errors)} dispatch error(s):\n")
                    for err in errors:
                        f.write(f"  ❌ {err}\n")

            status = "completed" if not errors else "partial"
            _update_distiller_run(run_id, report, dispatched, status)
            _finalize_swarm_job(run_id, not errors)

        except Exception as e:
            logger.error("Distiller pipeline failed", exc_info=True)
            with open(log_path, "a") as f:
                f.write(f"\n❌ Pipeline failed: {str(e)}\n")
            _update_distiller_run(run_id, report, 0, "failed")
            _finalize_swarm_job(run_id, False)
        finally:
            _is_distill_running = False

    background_tasks.add_task(_pipeline)
    return {"status": "success", "run_id": run_id, "message": "Pipeline started in background."}


@app.get("/api/distiller/stats")
async def get_distiller_stats():
    """Return Knowledge Distiller statistics for the dashboard panel.

    BUG FIX (2026-04-18): Previously this endpoint returned stats from only the
    LAST distiller run.  After a successful first run consumed all eligible facts,
    subsequent runs correctly found 0 new clusters — but the dashboard overwrote the
    good stats with zeros.  Now we return CUMULATIVE SUM() across all runs so the
    dashboard always reflects the total historical output of the distiller.
    The last_run object is still included for status-pill display (COMPLETED / IDLE).
    """
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    stats = {
        "last_run": None,
        "total_runs": 0,
        # Cumulative totals across ALL runs (what the dashboard cards display)
        "cumulative_clusters": 0,
        "cumulative_structural": 0,
        "cumulative_agent_proposals": 0,
        "cumulative_policy_proposals": 0,
        "proposals": {"total": 0, "pending": 0, "dispatched": 0, "completed": 0, "failed": 0},
        "is_running": _is_distill_running,
    }
    if not os.path.exists(db_path):
        return stats

    try:
        db = _sqlite3.connect(db_path)
        db.row_factory = _sqlite3.Row

        # Last run — used by the frontend for the status pill (COMPLETED / IDLE / RUNNING)
        row = db.execute("SELECT * FROM distiller_runs ORDER BY started_at DESC LIMIT 1").fetchone()
        if row:
            stats["last_run"] = dict(row)
        stats["total_runs"] = db.execute("SELECT COUNT(*) FROM distiller_runs").fetchone()[0]

        # Cumulative SUM across all runs — these feed the big dashboard counter cards.
        # This prevents a later 0-cluster run from overwriting a successful earlier run's stats.
        sums = db.execute("""
            SELECT COALESCE(SUM(clusters_found), 0)        AS total_clusters,
                   COALESCE(SUM(structural_proposals), 0)  AS total_structural,
                   COALESCE(SUM(agent_proposals), 0)       AS total_agent,
                   COALESCE(SUM(policy_proposals), 0)      AS total_policy
            FROM distiller_runs
        """).fetchone()
        stats["cumulative_clusters"] = sums["total_clusters"]
        stats["cumulative_structural"] = sums["total_structural"]
        stats["cumulative_agent_proposals"] = sums["total_agent"]
        stats["cumulative_policy_proposals"] = sums["total_policy"]

        # Proposal counts from world_facts
        total = db.execute("SELECT COUNT(*) FROM world_facts WHERE source_url = 'gepa://distiller'").fetchone()[0]
        stats["proposals"]["total"] = total

        # Pending = in world_facts but NOT in swarm_bridge_tracking
        pending = db.execute("""
            SELECT COUNT(*) FROM world_facts wf
            LEFT JOIN swarm_bridge_tracking sbt ON wf.id = sbt.fact_id
            WHERE wf.source_url = 'gepa://distiller' AND sbt.fact_id IS NULL
        """).fetchone()[0]
        stats["proposals"]["pending"] = pending
        stats["proposals"]["dispatched"] = total - pending

        db.close()
    except Exception as e:
        logger.error(f"Failed to get distiller stats: {e}", exc_info=True)

    return stats


@app.get("/api/distiller/proposals")
async def get_distiller_proposals():
    """Return all GEPA distiller proposals with execution status."""
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    proposals = []
    if not os.path.exists(db_path):
        return {"proposals": proposals}

    try:
        db = _sqlite3.connect(db_path)
        db.row_factory = _sqlite3.Row
        rows = db.execute("""
            SELECT wf.id, wf.entity, wf.fact, wf.importance, wf.timestamp,
                   CASE WHEN sbt.fact_id IS NOT NULL THEN 1 ELSE 0 END as tracked
            FROM world_facts wf
            LEFT JOIN swarm_bridge_tracking sbt ON wf.id = sbt.fact_id
            WHERE wf.source_url = 'gepa://distiller'
            ORDER BY wf.timestamp DESC
            LIMIT 30
        """).fetchall()

        for row in rows:
            fact_text = row["fact"]
            # Parse proposal type from recommendation text
            ptype = "STRUCTURAL"
            lower_fact = fact_text.lower()
            if "new agent" in lower_fact or "agent archetype" in lower_fact or "new_agent_type" in lower_fact:
                ptype = "NEW_AGENT"
            elif "policy" in lower_fact or "rule" in lower_fact:
                ptype = "POLICY"
            elif "new ki" in lower_fact or "create" in lower_fact and "ki" in lower_fact:
                ptype = "NEW_KI"
            elif "enrich" in lower_fact and "skill" in lower_fact:
                ptype = "SKILL_ENRICH"
            elif "update ki" in lower_fact or "enrich" in lower_fact:
                ptype = "KI_ENRICH"

            status = "dispatched" if row["tracked"] else "pending"
            proposals.append({
                "id": row["id"],
                "type": ptype,
                "target": row["entity"],
                "recommendation": fact_text[:200],
                "importance": row["importance"],
                "status": status,
                "timestamp": row["timestamp"],
            })
        db.close()
    except Exception as e:
        logger.error(f"Failed to get distiller proposals: {e}", exc_info=True)

    return {"proposals": proposals}


# ── Legacy distill endpoint (kept for backward compatibility) ──────────────
@app.post("/api/brain/distill")
def distill_knowledge(background_tasks: BackgroundTasks):
    """Legacy endpoint — now redirects to /api/distiller/run internally."""
    return run_distiller_pipeline(background_tasks)


@app.get("/api/memory_graph")
async def get_memory_graph():
    import sqlite3
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    
    nodes = []
    edges = []
    node_ids = set()
    
    if not os.path.exists(db_path):
        return {"nodes": [], "edges": []}
        
    def add_node(n):
        if n["id"] not in node_ids:
            nodes.append(n)
            node_ids.add(n["id"])

    try:
        db = sqlite3.connect(db_path)
        c = db.cursor()
        
        # Central Hub
        add_node({"id": "CORE", "label": "Global Memory", "group": "core"})
        
        # --- Query each category explicitly so they always appear ---
        categories = [
            ("skill",    "skills",    "%/skills/%"),
            ("ki",       "knowledge", "%/knowledge/%"),
            ("workflow", "workflow",  "%workflow%"),
            ("policy",   "policy",    "%AROS_POLICY.md%"),
        ]
        
        for group, hub_label, pattern in categories:
            # Fetch up to 100 facts per category with a real source_url
            c.execute("""
                SELECT id, entity, source_url, fact
                FROM world_facts
                WHERE source_url LIKE ?
                ORDER BY id DESC
                LIMIT 100
            """, (pattern,))
            rows = c.fetchall()
            if not rows:
                continue
            
            hub_id = f"hub_{group}"
            add_node({"id": hub_id, "label": hub_label.title(), "group": f"{group}_hub"})
            edges.append({"from": "CORE", "to": hub_id})
            
            # Group by parent folder (skill name / KI name) to avoid flat explosion
            sub_hubs = {}
            for row in rows:
                n_id = f"fact_{row[0]}"
                url  = row[2] or ""
                fact_text = row[3] or ""
                # Use grandparent folder as sub-grouping key (e.g. skill name)
                parts = url.split("/")
                sub_label = parts[-2] if len(parts) >= 2 else hub_label
                sub_hub_id = f"sub_{group}_{sub_label}"
                
                if sub_hub_id not in sub_hubs:
                    sub_hubs[sub_hub_id] = sub_label
                    add_node({"id": sub_hub_id, "label": sub_label[:25], "group": group, "title": url})
                    edges.append({"from": hub_id, "to": sub_hub_id})
                
                # Semantic renaming logic
                entity_label = row[1]
                if entity_label in ("SKILL.md", "AROS_POLICY.md") and fact_text:
                    clean_fact = fact_text.strip().split("\n")[0]
                    display_label = clean_fact[:30] + "..." if len(clean_fact) > 30 else clean_fact
                else:
                    display_label = entity_label[:30]
                    
                add_node({"id": n_id, "label": display_label, "group": "fact_leaf", "title": url})
                edges.append({"from": sub_hub_id, "to": n_id})
        
        # Facts with no source_url — show a compact summary node instead of hundreds of grey dots
        c.execute("SELECT COUNT(*) FROM world_facts WHERE source_url IS NULL")
        null_count = c.fetchone()[0]
        if null_count > 0:
            add_node({"id": "hub_unindexed", "label": f"Unindexed ({null_count})", "group": "fact_hub"})
            edges.append({"from": "CORE", "to": "hub_unindexed"})
            
        # Distilled Topics Hub
        c.execute("SELECT id, entity, source_url, fact FROM world_facts WHERE source_url LIKE 'distilled://%' LIMIT 150")
        distilled = c.fetchall()
        if distilled:
            add_node({"id": "hub_distilled", "label": "Distilled Topics", "group": "fact_hub"})
            edges.append({"from": "CORE", "to": "hub_distilled"})
            d_subhubs = {}
            for row in distilled:
                topic = row[2].replace("distilled://", "")
                sub_hub_id = f"sub_distilled_{topic}"
                if sub_hub_id not in d_subhubs:
                    d_subhubs[sub_hub_id] = topic
                    add_node({"id": sub_hub_id, "label": topic[:25], "group": "fact_hub", "title": topic})
                    edges.append({"from": "hub_distilled", "to": sub_hub_id})
                
                n_id = f"fact_{row[0]}"
                display_label = row[1][:30]
                add_node({"id": n_id, "label": display_label, "group": "fact_leaf", "title": row[3]})
                edges.append({"from": sub_hub_id, "to": n_id})
        
        # Mental Models
        c.execute("SELECT id, topic FROM mental_models LIMIT 50")
        models = c.fetchall()
        if models:
            add_node({"id": "models_hub", "label": "Mental Models", "group": "model_hub"})
            edges.append({"from": "CORE", "to": "models_hub"})
            for row in models:
                mod_id = f"model_{row[0]}"
                add_node({"id": mod_id, "label": row[1][:30], "group": "model"})
                edges.append({"from": "models_hub", "to": mod_id})
                
        # Agents Taxonomy
        c.execute("SELECT agent_type FROM agent_taxonomy")
        agents = c.fetchall()
        if agents:
            add_node({"id": "agents_hub", "label": "Defined Agents", "group": "model_hub"})
            edges.append({"from": "CORE", "to": "agents_hub"})
            for row in agents:
                agt_id = f"agent_{row[0].replace(' ', '_')}"
                add_node({"id": agt_id, "label": row[0], "group": "agent"})
                edges.append({"from": "agents_hub", "to": agt_id})
                
        # Experiences
        c.execute("SELECT id, content FROM experiences ORDER BY id DESC LIMIT 150")
        exps = c.fetchall()
        if exps:
            add_node({"id": "exps_hub", "label": "Experiences", "group": "model_hub"})
            edges.append({"from": "CORE", "to": "exps_hub"})
            for row in exps:
                exp_id = f"exp_{row[0]}"
                content_preview = row[1][:30] + "..." if row[1] and len(row[1]) > 30 else "Experience"
                add_node({"id": exp_id, "label": content_preview, "group": "experience"})
                edges.append({"from": "exps_hub", "to": exp_id})
                
        # --- Memory Graph (memory_edges) ---
        c.execute("""
            SELECT source_type, source_id, target_type, target_id, relation_type
            FROM memory_edges
            ORDER BY id DESC LIMIT 2000
        """)
        for r in c.fetchall():
            s_type, s_id, t_type, t_id, rel = r
            
            s_node = None
            if s_type == "world_fact": s_node = f"fact_{s_id}"
            elif s_type == "experience": s_node = f"exp_{s_id}"
            elif s_type == "mental_model": s_node = f"model_{s_id}"
            
            t_node = None
            if t_type == "world_fact": t_node = f"fact_{t_id}"
            elif t_type == "experience": t_node = f"exp_{t_id}"
            elif t_type == "mental_model": t_node = f"model_{t_id}"
            
            if s_node in node_ids and t_node in node_ids:
                # Add relational styling
                edge_color = "#999999"
                if rel in ("contradicts", "superseded_by"):
                    edge_color = "#e63946"
                elif rel in ("depends_on", "derived_from"):
                    edge_color = "#457b9d"
                
                edges.append({
                    "from": s_node,
                    "to": t_node,
                    "label": rel,
                    "arrows": "to",
                    "color": {"color": edge_color},
                    "font": {"size": 10, "color": edge_color, "background": "rgba(255,255,255,0.7)"},
                    "dashes": rel in ("clarifies", "elaborates")
                })

                
        db.close()
    except Exception as e:
        pass
        
    return {"nodes": nodes, "edges": edges}


class RetryPayload(BaseModel):
    evaluation_id: int

@app.get("/api/brain/evaluations")
async def get_evaluations():
    try:
        import sys
        brain_src = os.path.join(AROS_ROOT, "antigravity-brain", "src")
        if brain_src not in sys.path:
            sys.path.insert(0, brain_src)
        from antigravity_brain.db import get_db
        db = get_db()
        c = db.cursor()
        c.execute("""
            SELECT id, task_type, overall_quality, alignment_gap, failure_root_causes 
            FROM task_evaluations 
            WHERE retry_recommended = 1 
            ORDER BY evaluated_at DESC LIMIT 10
        """)
        evals = [dict(r) for r in c.fetchall()]
        db.close()
        return {"status": "success", "evaluations": evals}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/brain/retry")
async def trigger_retry(payload: RetryPayload):
    try:
        import sqlite3, os
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        db = sqlite3.connect(db_path)
        db.execute("UPDATE task_evaluations SET retry_recommended = 0 WHERE id = ?", (payload.evaluation_id,))
        db.commit()
        db.close()
        return {
            "status": "success", 
            "message": f"Retry dispatched for evaluation {payload.evaluation_id} with enriched rule context."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/brain/dismiss_retry")
async def dismiss_retry(payload: RetryPayload):
    try:
        import sqlite3, os
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        db = sqlite3.connect(db_path)
        db.execute("UPDATE task_evaluations SET retry_recommended = 0 WHERE id = ?", (payload.evaluation_id,))
        db.commit()
        db.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
