"""
AROS Evolution — GEPA Batch Mutation Sweep (batch_evolver.py)
==============================================================
Orchestrates the full Genetic-Pareto Evolutionary Prompt Algorithm pipeline.

Pipeline Phases:
  Phase 1 — Trace Analysis:
    Scans all walkthrough.md files for new/modified traces. Uses a DSPy
    TraceAnalyzer (Gemini 2.5 Pro) to classify failures and route mutations
    to the correct target type (skill, ki, workflow, policy).

  Phase 2 — Knowledge Distillation:
    After mutations, calls knowledge_distiller.run_distillation() to cluster
    conversation-extracted facts, detect skill/KI gaps, and surface proposals.

Key Components:
  - TraceAnalyzer:        DSPy signature for failure classification
  - _fuzzy_resolve_target(): Path resolver for hallucinated LLM target paths
  - _needs_processing():  Mtime-based deduplication to skip unchanged files
  - _update_telemetry():  Atomic counter increments in brain.db

Pre-flight: Calls preflight.run_preflight("mutation") before any work.

Part of: antigravity-evolution (AROS Self-Evolution Engine)
"""
import dspy
import os
import glob
import sqlite3
from antigravity_evolution.evolver import SystemEvolverPipeline

import logging
from logging.handlers import RotatingFileHandler

def setup_aros_logging(module_name: str):
    log_dir = os.path.expanduser("~/.gemini/antigravity/logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "aros.log")
    
    # Configure root logger so imported modules inherit it
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        fh = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger

logger = setup_aros_logging("batch-evolver")

def _load_env():
    """Load ~/.gemini/.env and alias all key name variants so litellm can find them."""
    env_path = os.path.expanduser("~/.gemini/.env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    # Alias: GOOGLE_AI_API_KEY → GEMINI_API_KEY (required by litellm gemini/ provider)
    google_ai_key = os.environ.get("GOOGLE_AI_API_KEY", "")
    if google_ai_key:
        os.environ.setdefault("GEMINI_API_KEY", google_ai_key)
        os.environ.setdefault("GOOGLE_API_KEY", google_ai_key)

def _update_telemetry(key: str, delta: int = 1):
    """Atomically increment a telemetry counter in brain.db."""
    try:
        db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
        if os.path.exists(db_path):
            db = sqlite3.connect(db_path)
            db.execute("""
                INSERT INTO system_telemetry (metric_key, metric_value)
                VALUES (?, ?)
                ON CONFLICT(metric_key) DO UPDATE SET metric_value = metric_value + ?
            """, (key, delta, delta))
            db.commit()
            db.close()
    except Exception as e:
        logger.warning(f"⚠️ Telemetry write failed for '{key}': {e}", exc_info=True)

class TraceAnalyzer(dspy.Signature):
    """
    You are a senior Antigravity OS reliability engineer analyzing an agentic session walkthrough.

    Read the walkthrough and judge whether the session contained a significant failure, bug,
    hallucination, or systematic issue that a mutation of an A.R.O.S system component could prevent.

    IMPORTANT: Base your judgment SOLELY on the content of the walkthrough.
    Do NOT assume failure based on keywords alone — read the narrative and decide holistically.

    A.R.O.S mutable component locations (use EXACTLY these path patterns):
    - Skills:    ~/.gemini/skills/<skill-name>/SKILL.md
      Example:   ~/.gemini/skills/spaceranger/SKILL.md
    - KIs:       ~/.gemini/antigravity/knowledge/<ki-name>/artifacts/<doc>.md
      Example:   ~/.gemini/antigravity/knowledge/aros_system_architecture/artifacts/architecture_guide.md
      Example:   ~/.gemini/antigravity/knowledge/spaceranger_pipeline/artifacts/overview.md
    - Workflows: ~/.gemini/antigravity/global_workflows/<workflow-name>.md
      Example:   ~/.gemini/antigravity/global_workflows/lab-commit.md
    - Policy:    ~/.gemini/antigravity/AROS_POLICY.md (this is a single file)

    ROUTING HEURISTICS — use these to pick target_type:
    - 'skill'    → The agent used a specific tool/skill incorrectly, or a skill's instructions were
                   incomplete, causing hallucinated parameters or wrong tool schemas.
    - 'ki'       → The agent lacked domain knowledge or background context that led to
                   factual errors, wrong assumptions, or missing API gotchas. KI mutations
                   add grounding wisdom so future agents don't repeat the same knowledge gap.
    - 'workflow'  → A multi-step orchestration sequence had ordering, dependency, or failover issues.
    - 'policy'   → A system-wide rule was missing (e.g., always use a specific model, always
                   validate paths before writing). Policy is the LAST resort for global issues.
    """
    conversation_log = dspy.InputField(desc="The walkthrough.md session summary from an agentic session.")

    did_fail = dspy.OutputField(desc=(
        "Your verdict: 'True' if the session had an actionable failure that a component mutation "
        "could prevent in future sessions, 'False' if the session was broadly successful. "
        "Be honest — not every session fails."
    ))
    judgment_rationale = dspy.OutputField(desc=(
        "1-2 sentence explanation of WHY you concluded did_fail = True or False."
    ))
    target_type = dspy.OutputField(desc=(
        "If did_fail is True: which A.R.O.S component type should be mutated? "
        "Must be exactly one of: 'skill', 'ki', 'workflow', 'policy'. Empty string if did_fail is False. "
        "Use the ROUTING HEURISTICS above to decide. Don't always default to 'policy'."
    ))
    target_file_path = dspy.OutputField(desc=(
        "If did_fail is True: the ABSOLUTE file path of the specific component to mutate. "
        "Use the EXACT path patterns from the component locations above. "
        "For KIs, the path MUST be: ~/.gemini/antigravity/knowledge/<ki-name>/artifacts/<doc>.md. "
        "Leave as empty string if did_fail is False or path is unknown."
    ))
    failure_reason = dspy.OutputField(desc="Concise summary of the root cause (1-2 sentences). Empty if did_fail is False.")

def _needs_processing(file_path: str) -> bool:
    """Return True if file is new or modified since last GEPA analysis."""
    if not os.path.exists(file_path):
        return False
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    if not os.path.exists(db_path):
        return True
    current_mtime = os.path.getmtime(file_path)
    try:
        db = sqlite3.connect(db_path)
        c = db.cursor()
        c.execute("SELECT mtime FROM processed_files WHERE file_path = ? AND processor = 'gepa'", (file_path,))
        row = c.fetchone()
        db.close()
        if row is None:
            return True
        return float(row[0]) < current_mtime
    except Exception:
        return True

def _mark_processed(file_path: str):
    """Record that GEPA has analyzed this file at its current mtime."""
    db_path = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))
    current_mtime = os.path.getmtime(file_path)
    try:
        db = sqlite3.connect(db_path)
        db.execute(
            """INSERT INTO processed_files (file_path, mtime, processor)
               VALUES (?, ?, 'gepa')
               ON CONFLICT(file_path) DO UPDATE SET mtime = ?, processed_at = CURRENT_TIMESTAMP""",
            (file_path, current_mtime, current_mtime)
        )
        db.commit()
        db.close()
    except Exception as e:
        logger.warning(f"⚠️ Failed to mark processed: {e}", exc_info=True)

def _fuzzy_resolve_target(target_path: str, target_type: str) -> str:
    abs_target = os.path.realpath(os.path.expanduser(target_path))
    if os.path.exists(abs_target):
        return abs_target

    import re
        
    if target_type == "skill":
        parts = target_path.split("/")
        if len(parts) >= 2:
            guess_dir = parts[-2].lower()
            skills_dir = os.path.expanduser("~/.gemini/skills")
            
            if os.path.exists(skills_dir):
                dirs = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
                best_match = None
                best_score = 0
                g_words = set(re.findall(r'[a-z0-9]+', guess_dir))
                
                for d in dirs:
                    d_words = set(re.findall(r'[a-z0-9]+', d.lower()))
                    overlap = len(d_words.intersection(g_words))
                    if overlap > best_score:
                        best_score = overlap
                        best_match = d
                        
                if not best_match:
                    for d in dirs:
                        clean_d = d.lower().replace('-python', '').replace('-skill', '')
                        if clean_d in guess_dir:
                            best_match = d
                            break

                if best_match:
                    candidate = os.path.join(skills_dir, best_match, "SKILL.md")
                    if os.path.exists(candidate):
                        logger.info(f"  → 🔍 Fuzzy resolved hallucinated skill path to: {candidate}")
                        return candidate

    elif target_type == "ki":
        # KI paths follow: ~/.gemini/antigravity/knowledge/<ki-name>/artifacts/<doc>.md
        # The LLM often hallucinates the ki-name or doc name. Try fuzzy matching.
        ki_root = os.path.expanduser("~/.gemini/antigravity/knowledge")
        if os.path.exists(ki_root):
            # Extract the KI name guess from the path
            # e.g. /home/user/.gemini/antigravity/knowledge/my_ki_name/artifacts/overview.md
            parts = target_path.replace("\\", "/").split("/")
            ki_name_guess = None
            doc_name_guess = None
            for i, part in enumerate(parts):
                if part == "knowledge" and i + 1 < len(parts):
                    ki_name_guess = parts[i + 1]
                if part == "artifacts" and i + 1 < len(parts):
                    doc_name_guess = parts[i + 1]
            
            if not ki_name_guess:
                # Fallback: use the second-to-last path component
                ki_name_guess = parts[-3] if len(parts) >= 3 else parts[-1]

            ki_dirs = [d for d in os.listdir(ki_root) 
                       if os.path.isdir(os.path.join(ki_root, d))]
            
            # Exact match first
            if ki_name_guess in ki_dirs:
                best_ki = ki_name_guess
            else:
                # Fuzzy word-overlap match
                g_words = set(re.findall(r'[a-z0-9]+', ki_name_guess.lower()))
                best_ki = None
                best_score = 0
                for d in ki_dirs:
                    d_words = set(re.findall(r'[a-z0-9]+', d.lower()))
                    overlap = len(d_words.intersection(g_words))
                    if overlap > best_score:
                        best_score = overlap
                        best_ki = d
            
            if best_ki:
                artifacts_dir = os.path.join(ki_root, best_ki, "artifacts")
                if os.path.exists(artifacts_dir):
                    # Try exact doc name first
                    if doc_name_guess:
                        candidate = os.path.join(artifacts_dir, doc_name_guess)
                        if os.path.exists(candidate):
                            logger.info(f"  → 🔍 Fuzzy resolved hallucinated KI path to: {candidate}")
                            return candidate
                    # Fallback to first .md file in artifacts
                    md_files = [f for f in os.listdir(artifacts_dir) if f.endswith(".md")]
                    if md_files:
                        candidate = os.path.join(artifacts_dir, md_files[0])
                        logger.info(f"  → 🔍 Fuzzy resolved hallucinated KI path to: {candidate}")
                        return candidate
                        
    return abs_target

def run_mutation_sweep():
    # Load env keys first — must happen before any LLM init
    _load_env()

    # ── Pre-flight self-diagnosis ──
    try:
        import sys as _sys
        brain_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "antigravity-brain", "src")
        if os.path.isdir(brain_src) and brain_src not in _sys.path:
            _sys.path.insert(0, brain_src)
        from antigravity_brain.preflight import run_preflight
        report = run_preflight("mutation")
        if not report.passed:
            logger.error("[GEPA] Pre-flight FAILED. Aborting mutation sweep.")
            logger.error(f"  Blockers: {report.blockers}")
            return
    except Exception as e:
        logger.warning(f"[GEPA] Pre-flight module unavailable ({e}), proceeding with caution...")

    api_key = os.environ.get("GEMINI_API_KEY", "")
    logger.info(f"[GEPA] GEMINI_API_KEY present: {bool(api_key)} (first 8 chars: {api_key[:8] if api_key else 'NONE'})")

    gemini_lm = dspy.LM('gemini/gemini-2.5-pro', api_key=api_key)
    dspy.settings.configure(lm=gemini_lm)

    analyzer = dspy.Predict(TraceAnalyzer)
    evolver = SystemEvolverPipeline()

    brain_dir = os.path.expanduser("~/.gemini/antigravity/brain")
    all_logs = sorted(glob.glob(f"{brain_dir}/*/walkthrough.md"))

    # Filter to only new/modified files
    log_files = [lf for lf in all_logs if _needs_processing(lf)]
    skipped_unchanged = len(all_logs) - len(log_files)

    logger.info(f"[GEPA] Found {len(all_logs)} total traces. {skipped_unchanged} unchanged → analyzing {len(log_files)} new/modified.")

    if not log_files:
        logger.info("[GEPA] Nothing new to analyze. Sweep complete.")
        return

    mutated = 0
    skipped = 0
    failed  = 0
    
    pending_mutations = {} # dict mapping abs_target: {"type": target_type, "traces": list}

    for log_path in log_files:
        conv_id = os.path.basename(os.path.dirname(log_path))
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                content = f.read()[-10000:]

            if len(content.strip()) < 100:
                logger.info(f"[SKIP] {conv_id}: walkthrough too short, skipping.")
                _mark_processed(log_path)  # Don't re-check next time
                skipped += 1
                continue

            logger.info(f"[ANALYZE] {conv_id}...")
            diagnosis = analyzer(conversation_log=content)

            verdict   = str(diagnosis.did_fail).strip().lower()
            rationale = str(diagnosis.judgment_rationale).strip()
            logger.info(f"  → verdict={verdict} | {rationale}")

            if verdict == "true":
                target_type = str(diagnosis.target_type).lower().strip()
                target_path = str(diagnosis.target_file_path).strip()
                reason      = str(diagnosis.failure_reason).strip()

                _update_telemetry("gepa_failed_traces")
                logger.info(f"  → Failure: {reason}")

                if target_type in ["skill", "ki", "workflow", "policy"] and target_path:
                    abs_target = _fuzzy_resolve_target(target_path, target_type)
                    if os.path.exists(abs_target):
                        if abs_target not in pending_mutations:
                            pending_mutations[abs_target] = {"type": target_type, "traces": []}
                        pending_mutations[abs_target]["traces"].append(content)
                        logger.info(f"  → Queued {target_type.upper()} mutation for {abs_target}...")
                    else:
                        logger.warning(f"  → 🚫 LLM proposed non-existent path: '{abs_target}'. Skipping.")
                        skipped += 1
                else:
                    logger.warning(f"  → No valid mutable target identified. Logging failure only.")
                    skipped += 1
            else:
                skipped += 1

            # Mark as processed regardless of outcome so we don't re-analyze
            _mark_processed(log_path)

        except Exception as e:
            logger.error(f"  → ❌ Failed to process {log_path}: {e}", exc_info=True)
            failed += 1
            _update_telemetry("gepa_failed_traces")

    # Now execute the accumulated mutations once per target file
    for abs_target, data in pending_mutations.items():
        try:
            target_type = data["type"]
            traces = data["traces"]
            with open(abs_target, "r", encoding="utf-8") as doc_f:
                current_doc = doc_f.read()
            
            # Constrain to last 3 traces to avoid blowing context windows
            agg_trace = "\n\n--- ADDITIONAL FAILURE SESSION ---\n\n".join(traces[-3:])
            logger.info(f"  → Triggering aggregated {target_type.upper()} mutation on {abs_target} ({len(traces)} sessions)...")
            
            evolver(
                target_type=target_type,
                current_doc=current_doc,
                execution_trace=agg_trace,
                target_file_path=abs_target
            )
            mutated += 1
        except Exception as e:
            logger.error(f"  → ❌ Failed to mutate {abs_target}: {e}", exc_info=True)
            failed += 1

    try:
        t_in = 0
        t_out = 0
        if hasattr(gemini_lm, 'history'):
            for call in gemini_lm.history:
                if isinstance(call, dict) and 'usage' in call:
                    u = call['usage']
                    if hasattr(u, "prompt_tokens"):
                        t_in += getattr(u, "prompt_tokens", 0)
                        t_out += getattr(u, "completion_tokens", 0)
                    elif isinstance(u, dict):
                        t_in += u.get('prompt_tokens', 0)
                        t_out += u.get('completion_tokens', 0)
        if t_in > 0 or t_out > 0:
            logger.info(f"[TOKENS] input={t_in} output={t_out} model=gemini-2.5-pro")
    except Exception:
        pass

    logger.info(f"\n[GEPA] Sweep complete. Mutated={mutated}, Skipped={skipped}, Errors={failed}")

    # ── Phase 2: Knowledge Distillation ─────────────────────────
    # After trace-based mutations, cluster conversation-extracted facts and surface proposals
    logger.info("\n[GEPA] Running Knowledge Distiller (Phase 2)...")
    try:
        from antigravity_evolution.knowledge_distiller import run_distillation
        distill_report = run_distillation()
        n_clusters = distill_report.get("clusters_found", 0)
        proposals  = distill_report.get("skill_ki_proposals", [])
        tax_props  = distill_report.get("taxonomy_proposals", [])

        logger.info(f"[GEPA/Distiller] {n_clusters} knowledge clusters found")
        for p in proposals[:10]:
            logger.info(f"  [{p['type']}] {p['target']} ({p['cluster_size']} facts, importance={p['max_importance']})")
        for tp in tax_props:
            logger.info(f"  [NEW_AGENT] {tp['agent_type']} — {tp['matching_facts']} supporting facts")


        # Note: Proposals are already persisted directly inside run_distillation()
    except Exception as e:
        logger.error(f"[GEPA/Distiller] ⚠ Distillation failed (non-fatal): {e}", exc_info=True)

    logger.info("[GEPA] Full pipeline complete.")


if __name__ == "__main__":
    import sys
    if "--distill-only" in sys.argv:
        _load_env()
        logger.info("[GEPA] Running Knowledge Distiller standalone...")
        from antigravity_evolution.knowledge_distiller import run_distillation
        import json
        report = run_distillation()
        print(json.dumps(report, indent=2))
    else:
        run_mutation_sweep()
