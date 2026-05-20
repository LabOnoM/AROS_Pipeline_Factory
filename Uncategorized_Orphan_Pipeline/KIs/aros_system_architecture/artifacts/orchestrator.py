# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

"""
Swarm Orchestrator v0.2 — Brain-Integrated, Skill-Aware, GEPA-Evolving

Architecture:
  Goal → Coordinator (gemini-3.1-pro) → DAG of TaskNodes
  Each TaskNode → Skill Router → Model Selector → Specialized Worker
  Results → Trace Writer → GEPA Mutation Engine (daily sweep)
"""
import asyncio
import os
import time
import struct
import sqlite3
import networkx as nx
from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from google import genai

from .model_selector import select_model, TIER_ORCHESTRATION, TIER_ANALYSIS, TIER_UTILITY
from .skill_router import find_matching_skills, load_skill_content
from .agent_taxonomy import seed_taxonomy, get_agent_type
from .trace_writer import save_execution_trace
from .coordinator import CoordinatorAgent, TaskNode, ExecutionPlan
from .tools.registry import global_registry
from .session import SwarmSession
from .harness import AgentHarnessContext


# ── Data Models ──────────────────────────────────────────────
# Data models imported from .coordinator

# ── Brain Integration ────────────────────────────────────────
DB_PATH = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))

_genai_client = None

def _get_client():
    global _genai_client
    if _genai_client is None:
        _genai_client = genai.Client()
    return _genai_client


async def _fetch_zero_shot_context(task_description: str, top_k: int = 3) -> Optional[str]:
    """Query brain.db for the most relevant context via vector similarity.
    Queries three tables in MTL priority order:
    1. vec_mental_models (Level-3 Insights) — highest transfer value
    2. vec_world_facts   (Level-2 Summaries) — domain knowledge
    3. vec_experiences   (Level-1 Walkthroughs) — episodic context
    """
    if not os.path.exists(DB_PATH):
        return None
    try:
        import sqlite_vec
        
        resp = await _get_client().aio.models.embed_content(
            model="models/gemini-embedding-001",
            contents=task_description,
            config=genai.types.EmbedContentConfig(output_dimensionality=768),
        )
        emb = resp.embeddings[0].values
        emb_bytes = struct.pack(f"{len(emb)}f", *emb)
        
        db = sqlite3.connect(DB_PATH)
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        db.enable_load_extension(False)
        
        try:
            cursor = db.cursor()

            # ── 1. Mental Models (Level-3 Insights — highest MTL priority) ──
            mental_model_texts = []
            try:
                cursor.execute("""
                    SELECT m.text, v.distance
                    FROM vec_mental_models v
                    JOIN mental_models m ON v.rowid = m.id
                    WHERE v.embedding MATCH ? AND k = ?
                    ORDER BY v.distance
                """, (emb_bytes, top_k * 2))
                for text, distance in cursor.fetchall():
                    if distance < 0.8:  # cosine threshold ~0.68
                        mental_model_texts.append(text)
            except Exception as e_mm:
                print(f"[Swarm] Mental models query skipped: {e_mm}", flush=True)

            # ── 2. World Facts (Level-2 Summaries — post-reranked by abstraction) ──
            cursor.execute("""
                SELECT d.fact, d.importance, d.source_url, v.distance
                FROM vec_world_facts v
                JOIN world_facts d ON v.rowid = d.id
                WHERE v.embedding MATCH ? AND k = ?
                ORDER BY v.distance
            """, (emb_bytes, top_k * 3))   # fetch 3x more, rerank in Python
            
            rows = cursor.fetchall()
            relevant_facts = []
            if rows:
                def _infer_abstraction(source_url, importance):
                    if source_url is None:
                        return 2 if (importance and importance >= 7) else 1
                    if 'knowledge/' in str(source_url):
                        return 3
                    if 'skills/' in str(source_url):
                        return 2
                    if 'brain/' in str(source_url) and 'walkthrough' in str(source_url):
                        return 1
                    return 1

                scored = []
                for fact, importance, source_url, distance in rows:
                    if distance >= 0.8:
                        continue
                    level = _infer_abstraction(source_url, importance)
                    adjusted_distance = distance - (level - 1) * 0.04
                    scored.append((fact, adjusted_distance))

                scored.sort(key=lambda x: x[1])
                relevant_facts = [s[0] for s in scored[:top_k]]

            # ── 3. Experiences (Level-1 Walkthroughs — episodic context) ──
            experience_texts = []
            try:
                cursor.execute("""
                    SELECT e.text, v.distance
                    FROM vec_experiences v
                    JOIN experiences e ON v.rowid = e.id
                    WHERE v.embedding MATCH ? AND k = ?
                    ORDER BY v.distance
                """, (emb_bytes, top_k))
                for text, distance in cursor.fetchall():
                    if distance < 0.8:
                        experience_texts.append(text[:300])  # truncate to 300 chars
            except Exception as e_exp:
                print(f"[Swarm] Experiences query skipped: {e_exp}", flush=True)

        finally:
            db.close()

        # ── Assemble context string in MTL priority order ──
        # Per SPEC §2.2: MTL_META_PROTOCOL → mental_models → experiences → aros_context
        context_parts = []
        MTL_META_PROTOCOL = (
            "=== AROS MTL Behavioral Protocol ===\n"
            "1. Inspect Before Act: read full state before modifying anything.\n"
            "2. Minimal Patch Discipline: smallest change that solves the problem.\n"
            "3. Self-Generated Verification: verify output even without external tests.\n"
            "4. Contract Compliance: respect API/output format specifications absolutely.\n"
            "5. Defensive I/O: wrap I/O in error handling, log failures explicitly."
        )
        context_parts.append(MTL_META_PROTOCOL)

        if mental_model_texts:
            context_parts.append(
                "=== PROCEDURAL WISDOM (Mental Models) ===\n"
                + "\n---\n".join(mental_model_texts[:top_k])
            )
        if relevant_facts:
            context_parts.append(
                "=== RELEVANT FACTS ===\n"
                + "\n---\n".join(relevant_facts)
            )
        if experience_texts:
            context_parts.append(
                "=== EPISODIC CONTEXT (Past Sessions) ===\n"
                + "\n---\n".join(experience_texts)
            )

        if len(context_parts) > 1:  # More than just the protocol
            return "\n\n".join(context_parts)
    except Exception as e:
        print(f"[Swarm] Zero-shot context unavailable: {e}", flush=True)
    return None


def _fetch_ki_summaries(goal: str, max_items: int = 5) -> str:
    """Fetch relevant Knowledge Item summaries for the Coordinator."""
    import glob
    import json
    
    ki_path = os.path.expanduser("~/.gemini/antigravity/knowledge/")
    summaries = []
    
    for meta_file in glob.glob(f"{ki_path}/*/metadata.json"):
        try:
            with open(meta_file, "r") as f:
                meta = json.load(f)
            title = meta.get("title", "")
            summary = meta.get("summary", "")
            if title and summary:
                summaries.append(f"• {title}: {summary[:200]}")
        except Exception:
            continue
    
    if summaries:
        return "Available Knowledge Items:\n" + "\n".join(summaries[:max_items])
    return ""


# ── Coordinator ──────────────────────────────────────────────
# Moved to coordinator.py

def _update_swarm_telemetry(delta_active: int, increment_tasks: bool = False):
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    if not os.path.exists(db_path):
        return
    import sqlite3
    try:
        db = sqlite3.connect(db_path)
        cur_active = db.execute("SELECT metric_value FROM system_telemetry WHERE metric_key='swarm_active_nodes'").fetchone()
        if cur_active is not None:
            new_active = max(0, cur_active[0] + delta_active)
            db.execute("UPDATE system_telemetry SET metric_value=? WHERE metric_key='swarm_active_nodes'", (new_active,))
        else:
            new_active = max(0, delta_active)
            db.execute("INSERT INTO system_telemetry (metric_key, metric_value) VALUES ('swarm_active_nodes', ?)", (new_active,))
            
        if increment_tasks:
            cur_completed = db.execute("SELECT metric_value FROM system_telemetry WHERE metric_key='swarm_completed_tasks'").fetchone()
            if cur_completed is not None:
                db.execute("UPDATE system_telemetry SET metric_value=? WHERE metric_key='swarm_completed_tasks'", (cur_completed[0] + 1,))
            else:
                db.execute("INSERT INTO system_telemetry (metric_key, metric_value) VALUES ('swarm_completed_tasks', 1)")
        db.commit()
        db.close()
    except Exception:
        pass


# ── Main Orchestrator ────────────────────────────────────────
class SwarmOrchestrator:
    def __init__(self, job_id: Optional[str] = None):
        self.session = SwarmSession(job_id)
        self.results: Dict[str, str] = {}  # Now stores artifact paths, or raw strings if short
        self.task_metadata: Dict[str, dict] = {}
    
    async def execute_task(self, task: TaskNode, upstream_results: Dict[str, str], working_dir: str = "", ide_workspace: str = ""):
        """Execute a single task with skill-aware routing and brain integration."""
        if not working_dir:
            working_dir = str(self.session.root_dir)
        start_time = time.time()
        print(f"[TASK_START] {task.task_id} by {task.agent_persona}", flush=True)
        print(f"[{task.task_id}] Started by {task.agent_persona}…", flush=True)
        _update_swarm_telemetry(1, False)
        
        # ── 1. Zero-Shot Context from Brain (MTL Priority: Mental Models + Facts + Experiences) ──
        zero_shot = await _fetch_zero_shot_context(task.description)
        if zero_shot:
            task.zero_shot_context = zero_shot
            print(f"[{task.task_id}] ✅ Zero-shot context injected (mental models + facts + experiences)", flush=True)
        
        # ── 2. Skill Router — find matching skills ──
        matched_skills = find_matching_skills(task.description, top_k=5)
        skill_content = ""
        skills_used = []
        
        # Always include mandatory skills for evolution/KI/skill tasks
        evolution_keywords = ['ki', 'knowledge item', 'skill', 'policy', 'workflow', 'gepa', 'proposal', 'gtb', 'validate', 'enrich']
        is_evolution_task = any(kw in task.description.lower() for kw in evolution_keywords)
        if is_evolution_task:
            # Force-inject critical evolution skills that agents must have
            import glob as _glob
            mandatory_names = ['gtb-validator', 'ki-creation', 'skill-creation', 'aros-dashboard-control']
            skills_dir = os.path.expanduser('~/.gemini/skills')
            for mname in mandatory_names:
                mpath = os.path.join(skills_dir, mname, 'SKILL.md')
                if os.path.exists(mpath) and mname not in [s.get('name') for s in matched_skills]:
                    matched_skills.append({'name': mname, 'path': mpath, 'description': f'Mandatory: {mname}', 'score': 1.0})
        
        for skill in matched_skills:
            content = load_skill_content(skill["path"])
            if content:
                skill_content += f"\n\n--- SKILL: {skill['name']} ---\n{content}"
                skills_used.append(skill["name"])
        
        if skills_used:
            print(f"[{task.task_id}] 🎯 Skills matched: {', '.join(skills_used)}", flush=True)
        
        # ── 3. Model Selection — check taxonomy, then keyword fallback ──
        taxonomy_entry = get_agent_type(task.agent_persona)
        if taxonomy_entry:
            model_tier = taxonomy_entry.get("model_tier", "utility")
            tier_map = {
                "orchestration": TIER_ORCHESTRATION,
                "analysis": TIER_ANALYSIS,
                "utility": TIER_UTILITY,
            }
            model = tier_map.get(model_tier, TIER_UTILITY)
        else:
            model = select_model(task.description, task.agent_persona)
        
        print(f"[{task.task_id}] 🤖 Model: {model}", flush=True)
        
        # ── 4. Build Worker Prompt ──
        prompt = f"Goal: {task.description}\n\n"
        
        if task.zero_shot_context:
            prompt += f"Background Wisdom (from AROS Memory Bank):\n{task.zero_shot_context}\n\n"
        
        if skill_content:
            prompt += f"MANDATORY SKILL INSTRUCTIONS:\n{skill_content}\n\n"
        
        if upstream_results:
            prompt += "Input Context (Artifact References):\n"
            for k, v in upstream_results.items():
                if os.path.exists(v):
                    prompt += f"--- {k} (File) ---\nPath: {v}\n(Use your view_file tool to read this if needed)\n"
                else:
                    preview = v[:2000] if len(v) > 2000 else v
                    prompt += f"--- {k} ---\n{preview}\n"
        
        # ── 5. Spawn Worker with Tools & Context ──
        # Fetch appropriate tools based on taxonomy role
        role_tools = global_registry.get_tools_for_role(task.agent_persona)
        
        # ── Agentic Harness Pre-Flight Setup ──
        harness_context = AgentHarnessContext(
            working_dir=working_dir,
            role=task.agent_persona,
            job_id=self.session.job_id,
            evolution_mode=getattr(task, "requires_framework_evolution", False),
            ide_workspace=ide_workspace
        )
        
        # ── AROS System Context — gives every agent full environment awareness ──
        # NOTE: We intentionally do NOT expose WORKSPACE_ROOT or the project repo path here.
        # Agents must write outputs to their job sandbox only: working_dir.
        
        local_rules = ""
        if ide_workspace and os.path.exists(ide_workspace):
            for rule_file in ["AGENTS.md", ".cursorrules", "local.rules", "copilot-instructions.md"]:
                r_path = os.path.join(ide_workspace, rule_file)
                if os.path.exists(r_path):
                    with open(r_path, "r") as f:
                        rule_content = f.read()
                        local_rules += f"\n--- Local Context: {rule_file} ---\n{rule_content}\n"

        MTL_META_PROTOCOL = (
            "\n\n=== OPERATIONAL META-PROTOCOL (AROS Institutional Memory) ===\n"
            "These behavioral patterns are proven to transfer across all task domains:\n"
            "1. INSPECT FIRST: Before editing any file, read it completely. "
            "Never blind-overwrite. Tool sequence: view → understand → act.\n"
            "2. MINIMAL PATCH: Make the smallest change that solves the problem. "
            "No speculative refactoring beyond the task scope.\n"
            "3. SELF-VERIFY: After implementing, create a verification step, "
            "even if no external tests exist. Confirm the output matches expectations.\n"
            "4. CONTRACT COMPLIANCE: Respect API output format specifications, "
            "file naming conventions, and schema contracts absolutely.\n"
            "5. DEFENSIVE I/O: Anticipate tool failures. Wrap filesystem and API "
            "calls with error handling. Log failures; do not silently drop them.\n"
            "======================================================\n"
        )

        aros_context = (
            f"\n\n=== AROS SYSTEM ENVIRONMENT ===\n"
            f"You have READ permissions to the AROS knowledge directories.\n"
            f"You have WRITE permissions ONLY to your assigned working directory: {working_dir}\n"
            f"{local_rules}\n"
            f"READ-ONLY Knowledge Directories:\n"
            f"  Skills:    ~/.gemini/skills/ (each subdirectory has a SKILL.md)\n"
            f"  KIs:       ~/.gemini/antigravity/knowledge/ (each subdir has metadata.json + artifacts/)\n"
            f"  Workflows: ~/.gemini/antigravity/global_workflows/ (*.md files)\n"
            f"  Brain DB:  ~/.gemini/antigravity/brain.db (SQLite: world_facts, swarm_jobs tables)\n"
            f"  Logs:      ~/.gemini/antigravity/logs/\n\n"
            f"WRITE RULES (MANDATORY — violation causes workspace pollution):\n"
            f"  ✅ Write all output files and scratch work to: {working_dir}\n"
            f"  ✅ To create/update a KI: write to ~/.gemini/antigravity/knowledge/<ki_name>/\n"
            f"  ✅ To create/update a Skill: write to ~/.gemini/skills/<skill_name>/SKILL.md\n"
            f"  ❌ NEVER write to the project source code directory\n"
            f"  ❌ NEVER use os.getcwd() as an output path\n"
            f"  ❌ NEVER create files at relative paths — always use absolute paths\n\n"
            f"DATA ACCESS:\n"
            f"  - Query brain.db: SELECT entity, fact FROM world_facts WHERE entity LIKE '%<topic>%' LIMIT 20\n"
            f"  - Read skill/KI docs using Python open() with the absolute ~/.gemini/... path\n"
            f"=================================================\n"
        )
        
        worker = Agent(
            f'google-gla:{model}',
            deps_type=AgentHarnessContext,
            system_prompt=(
                f"You are the {task.agent_persona} agent in the Antigravity Research OS (AROS). "
                f"You have FULL ACCESS to the machine filesystem, all KIs, Skills, Workflows, Policies, and brain.db. "
                f"Execute the task accurately. Follow any SKILL INSTRUCTIONS precisely. "
                f"If a tool or skill is not in your context, READ it from the filesystem directly. "
                f"If source data is missing, QUERY brain.db for related facts. "
                f"Never report 'unavailable' — find it yourself. You are autonomous."
                f"{MTL_META_PROTOCOL}"
                f"{aros_context}"
            ),
            tools=role_tools,
        )
        
        try:
            result = await worker.run(prompt, deps=harness_context)
            # pydantic_ai compatibility mapping
            raw_output = getattr(result, "data", getattr(result, "output", ""))
            
            # Save output as a durable artifact
            artifact_path = self.session.save_artifact(task.task_id, raw_output)
            self.results[task.task_id] = artifact_path
            
            # Token Extractor
            usage = getattr(result, "usage", lambda: None)()
            t_in = 0
            t_out = 0
            if usage:
                t_in = getattr(usage, "request_tokens", getattr(usage, "prompt_tokens", 0))
                t_out = getattr(usage, "response_tokens", getattr(usage, "completion_tokens", 0))
            
            duration = time.time() - start_time
            print(f"[TASK_DONE] {task.task_id}", flush=True)
            print(f"[{task.task_id}] ✅ Completed in {duration:.1f}s", flush=True)
            print(f"[TOKENS] input={t_in} output={t_out} model={model}", flush=True)
            
            self.task_metadata[task.task_id] = {
                "model": model,
                "skills_used": skills_used,
                "duration_s": duration,
                "success": True,
                "tokens_input": t_in,
                "tokens_output": t_out,
            }
            _update_swarm_telemetry(-1, True)
        except Exception as e:
            duration = time.time() - start_time
            print(f"[{task.task_id}] ❌ Failed after {duration:.1f}s: {e}", flush=True)
            print(f"[TOKENS] input=0 output=0 model={model}", flush=True)
            self.task_metadata[task.task_id] = {
                "model": model,
                "skills_used": skills_used,
                "duration_s": duration,
                "success": False,
            }
            _update_swarm_telemetry(-1, False)
    
    def _update_goal_status(self, status: str, iteration: int, total_tokens: int = 0):
        if not self.session.job_id: return
        import sqlite3
        import os
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        if not os.path.exists(db_path): return
        try:
            db = sqlite3.connect(db_path)
            db.execute("UPDATE swarm_jobs SET goal_status=?, current_iteration=?, total_tokens_used=? WHERE id=?", 
                      (status, iteration, total_tokens, self.session.job_id))
            db.commit()
            db.close()
        except:
            pass

    async def _evaluate_criteria(self, goal: str, criteria: str, results: Dict[str, str]) -> dict:
        """Master agent evaluates goal completion against criteria."""
        import os, json
        result_summary = ""
        for tid, path in results.items():
            if os.path.exists(path):
                with open(path, "r") as f:
                    result_summary += f"\n--- {tid} ---\n{f.read()[:3000]}\n"
        
        master = Agent(
            f'google-gla:{TIER_ORCHESTRATION}',
            system_prompt=(
                "You are the Master Evaluator Agent. You MUST objectively evaluate "
                "whether the subagent's work meets ALL specified criteria. "
                "Return JSON: {\"met\": bool, \"failures\": [\"str\"], \"summary\": \"str\"}"
            )
        )
        prompt = (
            f"GOAL: {goal}\n\n"
            f"CRITERIA: {criteria}\n\n"
            f"SUBAGENT RESULTS:\n{result_summary}\n\n"
            f"Evaluate: Do the results meet ALL criteria? Be strict."
        )
        try:
            result = await master.run(prompt)
            raw = getattr(result, "data", getattr(result, "output", "{}"))
            if "```json" in raw:
                raw = raw.split("```json")[1].split("```")[0].strip()
            elif "```" in raw:
                raw = raw.split("```")[1].split("```")[0].strip()
            return json.loads(raw)
        except Exception as e:
            return {"met": False, "failures": [f"Evaluation parse error: {e}"], "summary": "Failed to parse master LLM output"}

    def _build_sliding_critique(self, new_failures: List[str], previous_result: str, existing_critiques: List[str], max_history: int = 2) -> Tuple[str, List[str]]:
        """DeerFlow-style Context Engineering to prevent token explosion.
        Truncates the previous result heavily and keeps only the last N critiques."""
        import copy
        updated_critiques = copy.deepcopy(existing_critiques)
        
        # Format the current attempt's critique
        critique_block = "[PREVIOUS ATTEMPT FAILED]\nMaster Evaluator identified the following objective criteria failures:\n"
        for failure in new_failures:
            critique_block += f"- {failure}\n"
            
        if previous_result:
            truncated_res = previous_result[:4000] + "\n[... truncated by orchestrator ...]" if len(previous_result) > 4000 else previous_result
            critique_block += f"\nYour previous result was:\n{truncated_res}\n\nFIX THESE ISSUES IN YOUR NEXT ATTEMPT."
            
        updated_critiques.append(critique_block)
        
        # Keep only the last `max_history` items
        if len(updated_critiques) > max_history:
            updated_critiques = updated_critiques[-max_history:]
            
        return "\n\n=== REVISION REQUEST HISTORY ===\n" + "\n\n".join(updated_critiques), updated_critiques

    def _log_node_attempt(self, task_id: str, attempt: int, status: str, result_summary: str):
        """Autoresearch-style experiment logging to swarm_jobs table for audit trails."""
        if not self.session.job_id: return
        import sqlite3
        import os
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        if not os.path.exists(db_path): return
        try:
            db = sqlite3.connect(db_path)
            # We log this into a JSON array in the tracing_data field of swarm_jobs, 
            # or to a generic node_logs table if we had one. Since we don't, we will append to stdout/system tools for now 
            # and let the existing telemetry handle it. BUT for autoresearch parity, we log to CLI explicitly in TSV format:
            print(f"[TSV_LOG] {self.session.job_id}\t{task_id}\t{attempt}\t{status}\t{result_summary[:100].replace(chr(10), ' ')}", flush=True)
            db.close()
        except:
            pass

    async def _check_cancellation(self) -> bool:
        """Dashboard integration: check if user clicked Cancel."""
        if not self.session.job_id: return False
        import sqlite3
        import os
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        if not os.path.exists(db_path): return False
        try:
            db = sqlite3.connect(db_path)
            row = db.execute("SELECT goal_status FROM swarm_jobs WHERE id=?", (self.session.job_id,)).fetchone()
            db.close()
            if row and row[0] == 'cancelled':
                return True
        except:
            pass
        return False

    async def execute_task_with_retry(self, task: TaskNode, upstream_results: Dict[str, str], max_attempts: int = 20, working_dir: str = "", ide_workspace: str = ""):
        """Goal-Driven Node Execution Loop."""
        accumulated_critique_str = ""
        critique_history = []
        best_result_path = ""
        
        original_description = task.description
        
        for attempt in range(max_attempts):
            print(f"\n[GoalDriven] --- Node {task.task_id} --- Attempt {attempt+1}/{max_attempts}", flush=True)
            
            # 1. Inject sliding critique directly into description
            task.description = original_description + accumulated_critique_str
            
            # 2. Worker executes
            await self.execute_task(task, upstream_results, working_dir=working_dir, ide_workspace=ide_workspace)
            
            # Restore original description for clean downstream tracing
            task.description = original_description
            
            if not self.task_metadata.get(task.task_id, {}).get("success", False):
                self._log_node_attempt(task.task_id, attempt+1, "crash", "Task execution crashed/threw exception")
                continue # Retry on crash
                
            best_result_path = self.results.get(task.task_id, "")
            
            # 3. Master Evaluate
            if not task.node_criteria:
                self._log_node_attempt(task.task_id, attempt+1, "keep", "No criteria - single shot")
                return # Safe single-shot bypass
                
            print(f"[{task.task_id}] Subagent done. Master Evaluator checking against criteria...", flush=True)
            evaluation = await self._evaluate_criteria(task.description, task.node_criteria, {task.task_id: best_result_path})
            
            if evaluation.get("met"):
                print(f"[{task.task_id}] ✅ Node Criteria Met!", flush=True)
                self._log_node_attempt(task.task_id, attempt+1, "keep", "Criteria met")
                return
                
            # 4. Context Engineering (DeerFlow)
            failures = evaluation.get("failures", ["Criteria not met."])
            print(f"[{task.task_id}] ❌ Criteria failed ({len(failures)} issues). Rethinking...", flush=True)
            
            # Read previous artifact for context truncation
            prev_result_content = ""
            import os
            if best_result_path and os.path.exists(best_result_path):
                with open(best_result_path, "r") as f:
                    prev_result_content = f.read()
                    
            accumulated_critique_str, critique_history = self._build_sliding_critique(
                failures, 
                prev_result_content, 
                critique_history, 
                max_history=2
            )
            
            self._log_node_attempt(task.task_id, attempt+1, "discard", f"Failed: {failures[0]}" if failures else "Criteria failed")

        print(f"[{task.task_id}] ⚠️ NODE_EXHAUSTED. All {max_attempts} attempts failed criteria. Keeping best effort and continuing DAG.", flush=True)
        self._log_node_attempt(task.task_id, max_attempts, "exhausted", "Max attempts reached, degrading gracefully.")


    async def run(self, goal: str, criteria: str = "", max_iterations: int = 50, max_token_budget: int = 5000000, max_wall_time_s: int = 86400, working_dir: str = "", ide_workspace: str = "") -> Dict[str, str]:
        """Execute the full swarm pipeline for a research goal using Goal-Driven loop."""
        import time
        import os
        print(f"[Swarm] Coordinator analyzing goal…", flush=True)
        print(f"[Swarm] Goal: {goal}", flush=True)
        
        # ── Ensure taxonomy is seeded ──
        await asyncio.to_thread(seed_taxonomy)
        
        # ── Check Context ──
        ki_summaries = await asyncio.to_thread(_fetch_ki_summaries, goal)
        coordinator = CoordinatorAgent(ki_summaries=ki_summaries)
        
        iteration = 0
        total_tokens = 0
        start_wall = time.time()
        
        # DeerFlow context engineering for DAG-level error loops
        critique_history = []
        accumulated_error_context = ""
        
        while iteration < max_iterations:
            # Check dashboard cancellation
            if await self._check_cancellation():
                print(f"[GoalDriven] 🛑 Dashboard Cancellation. Aborting.", flush=True)
                break
                
            iteration += 1
            print(f"[GoalDriven] === Iteration {iteration}/{max_iterations} ===", flush=True)
            self._update_goal_status("iterating", iteration, total_tokens)
            
            self.results = {}
            self.task_metadata = {}
            
            try:
                dag, G = await coordinator.generate_execution_plan(goal, external_feedback=accumulated_error_context)
            except Exception as e:
                print(f"[Swarm Coordinator] Generation Failed: {e}", flush=True)
                raise
                
            print(f"[Swarm] Generated {len(dag)} tasks.", flush=True)
            task_map = {t.task_id: t for t in dag}
            
            print("[Swarm] Executing MapReduce Swarm Generations…", flush=True)
            for generation in nx.topological_generations(G):
                coroutines = []
                for node in generation:
                    task = task_map[node]
                    upstream = {dep: self.results[dep] for dep in task.depends_on if dep in self.results}
                    coroutines.append(self.execute_task_with_retry(task, upstream, working_dir=working_dir, ide_workspace=ide_workspace))
                
                for coroutine in coroutines:
                    await coroutine
                    
                completed = len(self.results)
                total = max(1, len(dag))
                pct = int((completed / total) * 100)
                print(f"[PROGRESS] {pct}%", flush=True)
                
            for m in self.task_metadata.values():
                total_tokens += m.get("tokens_input", 0) + m.get("tokens_output", 0)
                
            # ── Safety checks & Criteria eval ──
            if not criteria:
                print(f"[GoalDriven] No criteria provided. Single-shot complete.", flush=True)
                self._update_goal_status("completed", iteration, total_tokens)
                break
                
            evaluation = await self._evaluate_criteria(goal, criteria, self.results)
            
            if evaluation.get("met"):
                print(f"[GoalDriven] ✅ Criteria MET on iteration {iteration}", flush=True)
                self._update_goal_status("completed", iteration, total_tokens)
                break
                
            failures = evaluation.get("failures", [f"Criteria not met. Iteration {iteration} Failed."])
            print(f"[GoalDriven] ❌ Criteria NOT met. {len(failures)} failure(s). Continuing...", flush=True)
            
            # Sliding window for DAG level errors too
            accumulated_error_context, critique_history = self._build_sliding_critique(
                failures,
                previous_result="" , # Entire results dict is too massive, we just send failures to coordinator
                existing_critiques=critique_history,
                max_history=3
            )
            
            elapsed = time.time() - start_wall
            if elapsed > max_wall_time_s:
                print(f"[GoalDriven] ⚠️ Wall time {max_wall_time_s}s exhausted. Stopping.", flush=True)
                self._update_goal_status("exhausted_time", iteration, total_tokens)
                break
            if total_tokens > max_token_budget:
                print(f"[GoalDriven] ⚠️ Token budget {max_token_budget} exhausted. Stopping.", flush=True)
                self._update_goal_status("exhausted_tokens", iteration, total_tokens)
                break

        try:
            save_execution_trace(goal=goal, tasks=dag, results=self.results, task_metadata=self.task_metadata)
        except Exception as e:
            print(f"[Swarm] ⚠️ Failed to save execution trace: {e}", flush=True)
        
        print(f"[Swarm] ✅ Execution complete. {len(self.results)} tasks executed in last iteration.", flush=True)
        print("[SWARM_COMPLETE]", flush=True)
        return self.results

def _update_job_status(job_id: str, status: str, pid: Optional[int] = None):
    try:
        import sqlite3
        import os
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        conn = sqlite3.connect(db_path)
        if pid is not None:
            conn.execute("UPDATE swarm_jobs SET status = ?, pid = ? WHERE id = ?", (status, pid, job_id))
        else:
            conn.execute("UPDATE swarm_jobs SET status = ? WHERE id = ?", (status, job_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Swarm Status Monitor] Could not update job {job_id} to {status}: {e}")

def main():
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="Antigravity Swarm Orchestrator")
    parser.add_argument("--job-id", type=str, default="", help="UUID for DB tracking")
    parser.add_argument("--criteria", type=str, default="", help="Goal-driven success criteria")
    parser.add_argument("--max-iterations", type=int, default=50, help="Goal-driven max DAG iterations")
    parser.add_argument("--max-wall-time-s", type=int, default=86400, help="Max wall time in seconds")
    parser.add_argument("--max-token-budget", type=int, default=5000000, help="Max token budget")
    parser.add_argument("goal", nargs="+", help="Research goal or task prompt")
    
    args = parser.parse_args()
    goal = " ".join(args.goal)
    job_id = args.job_id
    
    if job_id:
        import os
        _update_job_status(job_id, "running", pid=os.getpid())

    try:
        orchestrator = SwarmOrchestrator(job_id=job_id)
        results = asyncio.run(orchestrator.run(
            goal=goal,
            criteria=args.criteria,
            max_iterations=args.max_iterations,
            max_wall_time_s=args.max_wall_time_s,
            max_token_budget=args.max_token_budget
        ))
        
        print("\n" + "=" * 60)
        print("FINAL RESULTS (Artifact Previews)")
        print("=" * 60)
        import os
        for task_id, path in results.items():
            print(f"\n--- {task_id} ---")
            if os.path.exists(path):
                with open(path, "r") as f:
                    content = f.read(1000)
                    print(content + ("..." if len(content) >= 1000 else ""))
            else:
                print(f"[Artifact not found: {path}]")
        
        if job_id:
            _update_job_status(job_id, "completed")
            
    except Exception as e:
        print(f"\n❌ FATAL SWARM ERROR: {str(e)}")
        if job_id:
            _update_job_status(job_id, "failed_permanent")
        sys.exit(1)

if __name__ == "__main__":
    main()

