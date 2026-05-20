# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

"""
AROS Brain — MCP Server (server.py)
=====================================
The Model Context Protocol (MCP) server that exposes AROS Brain capabilities
to the Antigravity IDE and external agents.

Exposed MCP Tools:
  - screen_user_message():     Eight-field MTL pre-flight oracle (SPEC v2.6).
                                Injects: Mental Models, Policies, Skills, Facts,
                                Experiences, KIs, Workflows, Agent suggestions.
                                Non-blocking via asyncio.to_thread (fixes EOF crashes).
                                Cache key = session_id + SHA-256(msg)[:6]
                                (prevents cross-prompt cache staleness).
  - query_memory():            Hybrid semantic search over world_facts, experiences,
                                mental_models. Non-blocking via asyncio.to_thread.
  - find_helpful_ki/workflow/agent/tool(): Semantic discovery endpoints (non-blocking)
  - read_ki_document():        Full-text KI artifact retrieval
  - raise_swarm_agent():       Background agent dispatch with Role Coalescing Guard
                                - Accepts task_list for batched payloads
                                - Enforces One-Agent-Per-Role: merges new tasks into
                                  the existing pending mission instead of spawning duplicates
  - check_agent_status():      Job status polling with log tailing
  - trigger_consolidation():   Force dream cycle (memory ingestion)

Background Services:
  - Swarm job sweeper (60s cycle): Detects crashed jobs → triggers self_healer
                                    Skips PID=0 entries (GCO-managed re-enqueued jobs)
  - Dream cycle watchdog: Real-time KI file monitoring

Concurrency design:
  All MCP tool handlers are async. Synchronous blocking calls (DB queries,
  embedding API, cosine search) are wrapped with asyncio.to_thread() so the
  event loop stays responsive. SQLite connections are always opened INSIDE the
  worker thread — never passed across thread boundaries — to respect SQLite's
  per-thread connection model (PEP 249 §2.2).

Part of: antigravity-brain (AROS Memory & Persistence Layer)
"""
import asyncio
import struct
import json
import logging
import time
import threading
from typing import Optional
from mcp.server.fastmcp import FastMCP

from .db import verify_and_init_db, get_db
from .dreamer import dream_cycle, get_embedding, get_client
from .ki_workflow_index import index as ctx_index
from .self_healer import heal_and_retry
import uuid
import subprocess
import os
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("antigravity-brain")

# FastMCP enables easy tool definitions and background tasks
mcp = FastMCP("antigravity-brain")


# ── Helper Functions ───────────────────────────────────────────────────

def _read_log_tail(log_path: str, lines: int = 50) -> str:
    """Read the last N lines from a log file."""
    if not log_path or not os.path.exists(log_path):
        return ""
    try:
        with open(log_path) as f:
            all_lines = f.readlines()
        return "".join(all_lines[-lines:])
    except Exception:
        return ""


def _parse_progress(log_path: str) -> str:
    """Parse the last [PROGRESS] marker from a log file."""
    if not log_path or not os.path.exists(log_path):
        return "unknown"
    try:
        with open(log_path) as f:
            all_lines = f.readlines()
        for line in reversed(all_lines):
            if "[PROGRESS]" in line:
                return line.split("[PROGRESS]")[1].strip()
        return f"{len(all_lines)} log lines emitted"
    except Exception:
        return "unknown"


def _parse_tokens_from_log(log_path: str) -> dict:
    """Parse [TOKENS] markers from log to aggregate token usage."""
    tokens = {"input": 0, "output": 0, "model": "unknown"}
    if not log_path or not os.path.exists(log_path):
        return tokens
    try:
        with open(log_path) as f:
            for line in f:
                if "[TOKENS]" in line:
                    parts = line.split("[TOKENS]")[1].strip()
                    for kv in parts.split():
                        if kv.startswith("input="):
                            tokens["input"] += int(kv.split("=")[1])
                        elif kv.startswith("output="):
                            tokens["output"] += int(kv.split("=")[1])
                        elif kv.startswith("model="):
                            tokens["model"] = kv.split("=")[1]
    except Exception:
        pass
    return tokens


def _calc_elapsed(data: dict) -> float:
    """Calculate elapsed seconds since job creation."""
    try:
        created = data.get("created_at", "")
        if created:
            from datetime import datetime
            # Handle SQLite datetime format
            ct = datetime.fromisoformat(created.replace("Z", "+00:00") if "T" in created else created)
            return round((datetime.now() - ct.replace(tzinfo=None)).total_seconds(), 1)
    except Exception:
        pass
    return 0.0


# Google AI pricing per 1M tokens (<128k context window)
PRICING = {
    "gemini-2.5-pro":       {"input": 1.25,  "output": 5.00},
    "gemini-2.5-flash":     {"input": 0.075, "output": 0.30},
    "gemini-2.0-flash":     {"input": 0.075, "output": 0.30},
    "gemini-1.5-pro":       {"input": 1.25,  "output": 5.00},
    "gemini-1.5-flash":     {"input": 0.075, "output": 0.30},
    "gemini-embedding-001": {"input": 0.00,  "output": 0.00},
}


def _estimate_cost(tokens: dict) -> float:
    """Estimate USD cost from token counts and model name."""
    model = tokens.get("model", "gemini-2.5-flash")
    pricing = PRICING.get(model, PRICING["gemini-2.5-flash"])
    input_cost = (tokens.get("input", 0) / 1_000_000) * pricing["input"]
    output_cost = (tokens.get("output", 0) / 1_000_000) * pricing["output"]
    return round(input_cost + output_cost, 6)


def _build_rich_response(data: dict) -> dict:
    """Construct the full response envelope with log tail, progress, tokens, summary."""
    log_path = data.get("log_path", "")
    tokens = _parse_tokens_from_log(log_path)
    tokens["estimated_cost_usd"] = _estimate_cost(tokens)

    return {
        "id": data.get("id"),
        "agent_role": data.get("agent_role"),
        "task": data.get("task", "")[:200],  # truncate for context savings
        "status": data.get("status"),
        "elapsed_seconds": _calc_elapsed(data),
        "progress": _parse_progress(log_path),
        "log_tail": _read_log_tail(log_path, lines=50),
        "healing_history": json.loads(data.get("healing_history") or "[]"),
        "tokens_used": tokens,
        "result_summary": data.get("result"),
    }


# ── Auto-Summary Generation ───────────────────────────────────────────

def _generate_summary_sync(job_id: str, log_path: str):
    """Generate a brief LLM summary when a job completes (runs in thread)."""
    try:
        with open(log_path) as f:
            log_content = f.read()[-4000:]

        client = get_client()
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                "Summarize this agent execution log in 2-3 sentences. "
                "Focus on what was accomplished, what changed, and any issues:\n\n"
                + log_content
            ),
        )
        summary = resp.text

        db = get_db()
        db.execute(
            "UPDATE swarm_jobs SET result = ?, status = 'completed', "
            "completed_at = CURRENT_TIMESTAMP WHERE id = ?",
            (summary, job_id),
        )
        db.commit()
        db.close()
        logger.info(f"Auto-summary generated for job {job_id}")
    except Exception as e:
        logger.error(f"Auto-summary failed for {job_id}: {e}")
        # Still mark as completed even if summary fails
        try:
            db = get_db()
            db.execute(
                "UPDATE swarm_jobs SET status = 'completed', "
                "completed_at = CURRENT_TIMESTAMP WHERE id = ?",
                (job_id,),
            )
            db.commit()
            db.close()
        except Exception:
            pass


# ── Startup Reaper ─────────────────────────────────────────────────────

def _startup_reaper():
    """Run ONCE at MCP server boot to expire stale 'dispatched'/'running' jobs whose PIDs are dead.
    Prevents phantom 'active agent' counts from accumulating across server restarts."""
    try:
        db = get_db()
        rows = db.execute(
            "SELECT * FROM swarm_jobs WHERE status IN ('dispatched', 'running')"
        ).fetchall()

        reaped = 0
        for row in rows:
            data = dict(row)
            pid = data.get("pid")
            if not pid:
                continue

            is_dead = False
            try:
                os.kill(pid, 0)
                # Also check zombie
                if sys.platform == 'linux':
                    stat_path = f"/proc/{pid}/stat"
                    if os.path.exists(stat_path):
                        with open(stat_path, 'r') as f:
                            parts = f.read().split()
                            if len(parts) >= 3 and parts[2] == 'Z':
                                is_dead = True
                    else:
                        is_dead = True  # /proc entry gone
            except OSError:
                is_dead = True

            if is_dead:
                # Check if the log has [SWARM_COMPLETE] — if so, mark completed
                log_path = data.get("log_path", "")
                has_complete_marker = False
                if log_path and os.path.exists(log_path):
                    try:
                        with open(log_path) as f:
                            if "[SWARM_COMPLETE]" in f.read():
                                has_complete_marker = True
                    except Exception:
                        pass

                if has_complete_marker:
                    db.execute(
                        "UPDATE swarm_jobs SET status = 'completed', "
                        "completed_at = CURRENT_TIMESTAMP WHERE id = ?",
                        (data["id"],)
                    )
                else:
                    db.execute(
                        "UPDATE swarm_jobs SET status = 'failed_permanent', "
                        "last_error = 'Reaped at startup: PID dead' WHERE id = ?",
                        (data["id"],)
                    )
                reaped += 1

        if reaped > 0:
            db.commit()
            logger.info(f"[STARTUP REAPER] Expired {reaped} stale job(s)")
        db.close()
    except Exception as e:
        logger.error(f"[STARTUP REAPER] Error: {e}")


# ── Periodic Sweeper ───────────────────────────────────────────────────

def _run_sweeper():
    """Background thread: every 60s, scan for zombie PIDs and trigger self-healing."""
    while True:
        time.sleep(60)
        try:
            db = get_db()

            # 1. Check for dead processes in active states
            rows = db.execute(
                "SELECT * FROM swarm_jobs WHERE status IN ('dispatched', 'running')"
            ).fetchall()

            for row in rows:
                data = dict(row)
                pid = data.get("pid")
                if not pid:
                    continue

                try:
                    os.kill(pid, 0)  # alive check — throws OSError if dead
                    
                    # Also check for zombie processes (defunct)
                    if sys.platform == 'linux':
                        stat_path = f"/proc/{pid}/stat"
                        if os.path.exists(stat_path):
                            with open(stat_path, 'r') as f:
                                stat_content = f.read().split()
                                if len(stat_content) >= 3 and stat_content[2] == 'Z':
                                    raise OSError("Zombie process")
                except OSError:
                    # Dead process detected
                    log_path = data.get("log_path", "")
                    has_complete_marker = False
                    if log_path and os.path.exists(log_path):
                        try:
                            with open(log_path) as f:
                                if "[SWARM_COMPLETE]" in f.read():
                                    has_complete_marker = True
                        except Exception:
                            pass
                    
                    if has_complete_marker:
                        logger.info(f"[SWEEPER] PID {pid} dead, but job {data['id']} has [SWARM_COMPLETE]. Deferring to summary generator.")
                        continue

                    retry_count = data.get("retry_count", 0) or 0
                    if retry_count < 3:
                        # Set healing FIRST to prevent re-trigger on next sweep
                        db.execute(
                            "UPDATE swarm_jobs SET status = 'healing' WHERE id = ?",
                            (data["id"],),
                        )
                        db.commit()
                        logger.info(
                            f"[SWEEPER] Dead PID {pid} for job {data['id']} — triggering self-healing (attempt {retry_count + 1})"
                        )
                        # Run heal_and_retry in a daemon thread
                        threading.Thread(
                            target=lambda jid=data["id"]: asyncio.run(heal_and_retry(jid)),
                            daemon=True,
                        ).start()
                    else:
                        db.execute(
                            "UPDATE swarm_jobs SET status = 'failed_permanent' WHERE id = ?",
                            (data["id"],),
                        )
                        db.commit()
                        logger.warning(f"[SWEEPER] Job {data['id']} permanently failed (max retries)")
                except Exception:
                    pass  # PID check failed for unknown reason, skip

            # 2. Check for successfully completed processes
            active_rows = db.execute(
                "SELECT * FROM swarm_jobs WHERE status IN ('dispatched', 'running')"
            ).fetchall()

            for row in active_rows:
                data = dict(row)
                log_path = data.get("log_path", "")
                if log_path and os.path.exists(log_path):
                    try:
                        with open(log_path) as f:
                            content = f.read()
                        if "[SWARM_COMPLETE]" in content:
                            logger.info(f"[SWEEPER] Job {data['id']} completed — generating summary")
                            threading.Thread(
                                target=_generate_summary_sync,
                                args=(data["id"], log_path),
                                daemon=True,
                            ).start()
                    except Exception:
                        pass

            db.close()
        except Exception as e:
            logger.error(f"[SWEEPER] Error: {e}")


# ── MCP Tools ──────────────────────────────────────────────────────────

@mcp.tool()
async def query_memory(query: str, memory_type: str = "world_facts", limit: int = 5) -> str:
    """
    Search the hybrid memory banks of the active agent.
    Use memory_type = 'world_facts' for semantic truths, 'experiences' for episodic episodic chat history,
    or 'mental_models' for cognitive skills and reflections.
    """
    try:
        import asyncio
        from .graph_query import query_graph_enhanced
        # IMPORTANT: DB connection must be opened INSIDE the worker thread.
        # SQLite connections are not safe to use across threads (PEP 249 §2.2).
        def _run():
            db = get_db()
            try:
                return query_graph_enhanced(db, query, memory_type, limit)
            finally:
                db.close()
        results = await asyncio.to_thread(_run)
        return json.dumps(results, indent=2)
    except Exception as e:
        logger.error(f"Error querying memory: {e}")
        return f"Error querying memory: {str(e)}"

@mcp.tool()
async def screen_user_message(user_message: str) -> str:
    """
    AROS Ambient Screener: Pre-flight oracle that injects the full 8-field MTL
    (Memory Transfer Learning) context payload before reasoning starts.
    Fields: Mental Models, Policies, Skills, Facts, Experiences, KIs, Workflows, Agents.
    MUST be the first tool called in every IDE session.

    Implementation: calls screen_message() via asyncio.to_thread() to prevent
    blocking the MCP event loop during embedding API calls (fixes EOF crashes).
    Cache key = session_id + SHA-256(user_message)[:6] (prevents cross-prompt staleness).
    """
    try:
        import os
        import asyncio
        from .compliance_auditor import tracker
        from .ambient_screener import screen_message
        session_id = os.environ.get("ANTIGRAVITY_SESSION_ID", "default")
        tracker.record_tool_call(session_id, "screen_user_message")
        
        res = await asyncio.to_thread(screen_message, user_message, session_id=session_id)
        tracker.record_preflight_result(session_id, res)
        
        return json.dumps(res, indent=2)
    except Exception as e:
        logger.error(f"screen_user_message error: {e}")
        return f"Error: {e}"

@mcp.tool()
async def trigger_consolidation() -> str:
    """
    Forces the background dream cycle to instantly process any pending logs 
    and consolidate them into the memory graphs.
    """
    return "Forced consolidation initiated."

@mcp.tool()
async def find_helpful_ki(task_description: str) -> str:
    """
    Search Knowledge Items semantically. 
    Returns top-3 KI names, summaries, and artifact paths.
    """
    try:
        import asyncio
        results = await asyncio.to_thread(ctx_index.search_kis, task_description)
        return json.dumps(results, indent=2)
    except Exception as e:
        logger.error(f"find_helpful_ki error: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def read_ki_document(ki_name: str, document_path: str = "") -> str:
    """
    Read the full content of a KI's artifact. 
    If document_path is empty, returns all artifacts concatenated.
    """
    import asyncio

    def _run():
        artifacts = ctx_index.get_ki_artifacts(ki_name)
        if not artifacts:
            return f"No artifacts found for KI: {ki_name}"

        content = ""
        for path in artifacts:
            if document_path and not path.endswith(document_path):
                continue
            try:
                with open(path, 'r', errors='ignore') as f:
                    content += f"\n--- {os.path.basename(path)} ---\n{f.read()}\n"
            except Exception as e:
                content += f"\n--- Error reading {path}: {e} ---\n"

        return content if content else f"Could not match document_path '{document_path}' in KI."

    return await asyncio.to_thread(_run)

@mcp.tool()
async def find_helpful_workflow(task_description: str) -> str:
    """
    Search workflows semantically. 
    Returns top-3 workflow names and descriptions.
    """
    try:
        import asyncio
        results = await asyncio.to_thread(ctx_index.search_workflows, task_description)
        return json.dumps(results, indent=2)
    except Exception as e:
        logger.error(f"find_helpful_workflow error: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def read_workflow(workflow_name: str) -> str:
    """
    Read the full markdown content of a workflow file.
    """
    import asyncio

    def _run():
        path = ctx_index.get_workflow_path(workflow_name)
        if not path:
            return f"Workflow not found: {workflow_name}"
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading workflow: {str(e)}"

    return await asyncio.to_thread(_run)

@mcp.tool()
async def find_helpful_agent(task_description: str) -> str:
    """
    Query agent_taxonomy in brain.db. 
    Returns matched agent personas with their skills and model tiers.
    """
    try:
        import asyncio
        results = await asyncio.to_thread(ctx_index.search_agents, task_description)
        return json.dumps(results, indent=2)
    except Exception as e:
        logger.error(f"find_helpful_agent error: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def find_helpful_tool(task_description: str) -> str:
    """
    Query the AROS Swarm ToolRegistry to find available execution tools.
    Returns matched tools with their descriptions and assigned persona roles.
    """
    try:
        # Connect to swarm src to dynamically load the unified registry
        import sys
        import os
        
        _CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        _AROS_ROOT = os.path.abspath(os.path.join(_CURRENT_DIR, "..", "..", ".."))
        swarm_src = os.path.join(_AROS_ROOT, "antigravity-swarm", "src")
        
        if swarm_src not in sys.path:
            sys.path.append(swarm_src)
            
        from antigravity_swarm.tools.registry import global_registry
        
        # Build tool serialization
        tools_info = []
        with global_registry._lock:
            for name, tool in global_registry._tools.items():
                roles = [r for r, tlist in global_registry._roles.items() if name in tlist]
                tools_info.append({
                    "name": name,
                    "description": tool.description or "",
                    "roles": roles
                })
                
        # Future: Rank by get_embedding(task_description) cosine distance
        return json.dumps(tools_info, indent=2)
    except Exception as e:
        logger.error(f"find_helpful_tool error: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def raise_swarm_agent(agent_role: str, task: str = "", task_list: list = None, working_dir: str = "", ide_workspace: str = "") -> str:
    """
    Dispatch a background Swarm agent. Returns a job_id immediately (non-blocking).
    working_dir defaults to the IDE's current workspace if empty.
    ide_workspace (optional): The absolute path to the user's current project workspace.
                              As the IDE AI, use this to grant the swarm agent read/write permissions 
                              to the project and automatically inject the project's local rules (e.g. AGENTS.md).
    task_list (optional): Bypass single-task mode and directly pass a batch of tasks.
    
    COMPLIANCE: Before calling this tool, you must:
    (a) Have called screen_user_message in this session.
    """
    from dotenv import load_dotenv
    import os
    load_dotenv(os.path.expanduser("~/.gemini/.env"), override=False)

    from .compliance_auditor import tracker
    session_id = os.environ.get("ANTIGRAVITY_SESSION_ID", "default")
    tracker.record_tool_call(session_id, "raise_swarm_agent")
    
    compliance_tracker_res = tracker.check_compliance(session_id)
    warning_prefix = ""
    if not compliance_tracker_res["compliant"]:
        warning = (
            "⚠️ PROTOCOL NOTE: Pre-flight not completed for this session. "
            "Consider calling screen_user_message first. "
            "Proceeding anyway per agent judgment.\n\n"
        )
        logger.warning(f"[COMPLIANCE] {warning.strip()}")
        warning_prefix = warning

    job_id = str(uuid.uuid4())
    mission_id = job_id  # 1:1 mapping for simplicity

    # Enforce strict agent isolation for working directory.
    # CRITICAL: Internal AROS system agents MUST NEVER inherit WORKSPACE_ROOT (the project repo).
    # They must always use an isolated per-job sandbox under ~/.gemini/antigravity/agent_sandbox/.
    # Only explicitly user-facing agents may use WORKSPACE_ROOT as a fallback.
    _SYSTEM_INTERNAL_ROLES = {
        "knowledge_distiller", "dreamer", "gepa_evolver", "evolution_agent",
        "self_healer", "graph_reflection", "conflict_resolution",
        "memory_compaction", "ki_ingestion", "log_distillation",
        "taxonomy_rebuild", "qa_agent", "test_agent",
    }
    per_job_sandbox = os.path.expanduser(f"~/.gemini/antigravity/agent_sandbox/{job_id}")
    os.makedirs(per_job_sandbox, exist_ok=True)
    if not working_dir:
        if agent_role in _SYSTEM_INTERNAL_ROLES:
            # System agents are always sandboxed — NEVER touch the project repo
            working_dir = per_job_sandbox
        else:
            # User-facing agents: prefer explicit WORKSPACE_ROOT, else sandbox
            working_dir = os.environ.get("WORKSPACE_ROOT", per_job_sandbox)

    # ── Role Coalescing Guard ─────────────────────────────────────────────────────
    # Principle: At most ONE pending or active agent per agent_role type.
    # If a same-role mission is already PENDING in the UMQ (not yet picked up by GCO),
    # merge the new task into it instead of creating a new job.
    # We only coalesce into 'pending' missions — not 'in_progress' ones, since
    # in_progress missions are already executing and cannot receive new work.
    db_check = get_db()
    pending_same_role = None
    try:
        all_pending = db_check.execute(
            "SELECT id, caller_job_id, payload FROM orchestrator_missions WHERE status = 'pending'"
        ).fetchall()
        for row in all_pending:
            try:
                p = json.loads(row["payload"])
                if p.get("agent_role") == agent_role:
                    pending_same_role = dict(row)
                    pending_same_role["_parsed_payload"] = p
                    break
            except Exception:
                continue
    except Exception as e:
        logger.warning(f"[Coalescing Guard] DB read failed: {e} — proceeding with new job")
    finally:
        db_check.close()

    if pending_same_role:
        p = pending_same_role["_parsed_payload"]
        # Build or extend the task_list
        existing_tasks = p.get("task_list", [p.get("task", "")])
        existing_tasks = [t for t in existing_tasks if t]  # filter empty strings
        
        tasks_to_add = task_list if task_list is not None else ([task] if task else [])
        existing_tasks.extend([t for t in tasks_to_add if t])
        
        p["task_list"] = existing_tasks
        # Update display task — use first non-empty task for readability
        first_task = next((t for t in existing_tasks if t), "")
        p["task"] = f"[BATCH {len(existing_tasks)} tasks] {first_task[:80]}"

        db_merge = get_db()
        db_merge.execute(
            "UPDATE orchestrator_missions SET payload = ? WHERE id = ?",
            (json.dumps(p), pending_same_role["id"])
        )
        existing_job_id = pending_same_role["caller_job_id"]
        if existing_job_id:
            db_merge.execute(
                "UPDATE swarm_jobs SET task = ? WHERE id = ?",
                (p["task"], existing_job_id)
            )
        db_merge.commit()
        db_merge.close()

        logger.info(
            f"[Coalescing Guard] Merged new task(s) into pending '{agent_role}' mission "
            f"{pending_same_role['id'][:8]}. Total tasks: {len(existing_tasks)}"
        )
        return json.dumps({
            "job_id": existing_job_id or pending_same_role["id"],
            "mission_id": pending_same_role["id"],
            "status": "coalesced",
            "message": (
                f"{warning_prefix}Task merged into existing pending '{agent_role}' mission. "
                f"{len(existing_tasks)} tasks now queued."
            )
        })
    # ── End Role Coalescing Guard ─────────────────────────────────────────────────

    try:
        db = get_db()
        
        # Resolve initial task_list mapping for a new job
        initial_tasks = task_list if task_list is not None else ([task] if task else [])
        display_task = f"[BATCH {len(initial_tasks)} tasks] {initial_tasks[0][:80]}" if len(initial_tasks) > 1 else task

        # 1. Create swarm_jobs record (backward compat for check_agent_status)
        db.execute(
            "INSERT INTO swarm_jobs (id, agent_role, task, working_dir, status) "
            "VALUES (?, ?, ?, ?, ?)",
            (job_id, agent_role, display_task, working_dir, 'queued')
        )

        # 2. Enqueue to Universal Mission Queue — GCO will pick this up
        payload = json.dumps({
            "agent_role": agent_role,
            "task": display_task,
            "task_list": initial_tasks,
            "working_dir": working_dir,
            "ide_workspace": ide_workspace,
        })
        db.execute("""
            INSERT INTO orchestrator_missions
            (id, source, caller_job_id, mission_type, payload, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            mission_id, "ide_ai", job_id, "babysitter",
            payload, 0  # P0_CRITICAL: IDE/user-facing requests are highest priority
        ))
        db.commit()
        db.close()

        return json.dumps({
            "job_id": job_id,
            "mission_id": mission_id,
            "status": "queued",
            "message": f"{warning_prefix}Mission queued for '{agent_role}'. GCO will execute sequentially. Use check_agent_status('{job_id}', wait_seconds=300) to monitor."
        })
    except Exception as e:
        logger.error(f"raise_swarm_agent error: {e}")
        return f"Error raising swarm: {e}"

@mcp.tool()
async def check_agent_status(job_id: str, wait_seconds: int = 0) -> str:
    """
    Check the status and result of a dispatched Swarm agent job.
    If wait_seconds > 0, blocks until the job reaches a terminal state
    (completed/failed_permanent) or the timeout expires — similar to
    the IDE's command_status tool with WaitDurationSeconds.
    Returns structured JSON with progress, log tail, healing history,
    token usage, and auto-generated result summary.
    """
    TERMINAL_STATES = ("completed", "failed_permanent")
    deadline = time.time() + wait_seconds

    while True:
        try:
            db = get_db()
            row = db.execute("SELECT * FROM swarm_jobs WHERE id = ?", (job_id,)).fetchone()
            if not row:
                db.close()
                return json.dumps({"status": "not_found", "message": "No matching job_id."})
            
            data = dict(row)
            
            # Zombie detection (only if NOT already healing)
            if data["status"] in ("dispatched", "running") and data.get("pid"):
                try:
                    os.kill(data["pid"], 0)  # Throws OSError if dead
                except OSError:
                    retry_count = data.get("retry_count", 0) or 0
                    if retry_count < 3 and data["status"] != "healing":
                        # Trigger self-healing in background
                        db.execute(
                            "UPDATE swarm_jobs SET status = 'healing' WHERE id = ?",
                            (job_id,),
                        )
                        db.commit()
                        threading.Thread(
                            target=lambda: asyncio.run(heal_and_retry(job_id)),
                            daemon=True,
                        ).start()
                        data["status"] = "healing"
                    elif retry_count >= 3:
                        db.execute(
                            "UPDATE swarm_jobs SET status = 'failed_permanent' WHERE id = ?",
                            (job_id,),
                        )
                        db.commit()
                        data["status"] = "failed_permanent"

            db.close()

            # If terminal state or wait expired, build response and return
            if data["status"] in TERMINAL_STATES or time.time() >= deadline:
                break

            # If no wait requested, return immediately
            if wait_seconds <= 0:
                break

            await asyncio.sleep(5)  # Poll every 5 seconds

        except Exception as e:
            logger.error(f"check_agent_status error: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    return json.dumps(_build_rich_response(data), indent=2, default=str)


# ── Main Entry Point ──────────────────────────────────────────────────

def main():
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.gemini/.env"))
    
    logger.info("Initializing Brain DB...")
    verify_and_init_db()
    
    logger.info("Running Startup Reaper (one-time stale job cleanup)...")
    _startup_reaper()
    
    logger.info("Building Context Arrays in background...")
    indexer_thread = threading.Thread(target=ctx_index.build_index, daemon=True)
    indexer_thread.start()
    
    # Start the periodic sweeper in a background daemon thread
    logger.info("Starting Sweeper (60s interval)...")
    sweeper_thread = threading.Thread(target=_run_sweeper, daemon=True)
    sweeper_thread.start()

    logger.info("Starting MCP stdio interface...")
    mcp.run("stdio")

if __name__ == "__main__":
    main()
