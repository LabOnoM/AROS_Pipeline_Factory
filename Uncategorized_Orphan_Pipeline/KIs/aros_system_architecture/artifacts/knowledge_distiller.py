# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

"""
Knowledge Distiller — Conversation Wisdom → GEPA Mutations

Closes the feedback loop between conversation-extracted facts (826 unindexed world_facts)
and the GEPA mutation engine. Instead of letting these facts sit passively,
the Distiller:

1. Clusters unindexed facts by embedding similarity
2. Detects gaps where clusters have no corresponding Skill/KI coverage
3. Proposes GEPA mutations to enrich Skills, create KIs, refine Policies,
   and evolve the Agent Taxonomy
"""

import os
import json
import struct
import sqlite3
import logging
from typing import Optional
from collections import defaultdict

logger = logging.getLogger("knowledge-distiller")

DB_PATH = os.environ.get(
    "BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db")
)
SKILLS_DIR = os.path.expanduser("~/.gemini/skills")
KI_DIR     = os.path.expanduser("~/.gemini/antigravity/knowledge")


def _get_db():
    import sqlite_vec
    db = sqlite3.connect(DB_PATH)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    db.row_factory = sqlite3.Row
    return db


def _unpack_embedding(blob: bytes) -> list[float]:
    n = len(blob) // 4
    return list(struct.unpack(f"{n}f", blob))


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    import math
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def cluster_unindexed_facts(similarity_threshold: float = 0.80) -> list[dict]:
    """
    Group unindexed world_facts into clusters based on embedding similarity.
    Returns a list of clusters, each containing related facts.
    
    Uses a simple greedy clustering approach:
    - Pick the highest-importance unclustered fact as a centroid
    - Absorb all facts with cosine_sim >= threshold into that cluster
    - Repeat until all facts are assigned
    """
    db = _get_db()
    c = db.cursor()

    # Load un-distilled CONVERSATION-EXTRACTED facts only.
    # Excludes:
    #   - gepa://distiller proposals (would cause infinite self-clustering loop)
    #   - Indexed KI metadata rows  (~/.gemini/antigravity/knowledge/)
    #   - Indexed workflow rows      (~/.gemini/antigravity/global_workflows/)
    #   - Indexed skill rows         (~/.gemini/skills/)
    # MUST INCLUDE:
    #   - Walkthrough facts          (~/.gemini/antigravity/brain/<id>/walkthrough.md)
    #   - NULL source_url facts      (extracted directly from conversation logs)
    #
    # BUG FIX (2026-04-18): The previous filter used NOT LIKE '%/.gemini/antigravity/%'
    # which matched *all* paths under .gemini/antigravity/ — including walkthrough.md
    # paths like /home/owner03/.gemini/antigravity/brain/<id>/walkthrough.md.
    # This caused 0 facts to be clustered on every run. Now we exclude only the
    # specific subdirectories that hold pre-structured index rows (knowledge/ and
    # global_workflows/), leaving the brain/ conversation extractions visible.
    c.execute("""
        SELECT wf.id, wf.entity, wf.fact, wf.importance, wf.confidence_score
        FROM world_facts wf
        WHERE wf.distilled_at IS NULL
          AND (wf.is_archived IS NULL OR wf.is_archived = FALSE)
          AND (wf.source_url IS NULL
               OR (wf.source_url NOT LIKE 'gepa://%'
                   AND wf.source_url NOT LIKE '%/.gemini/skills/%'
                   AND wf.source_url NOT LIKE '%/.gemini/antigravity/knowledge/%'
                   AND wf.source_url NOT LIKE '%/.gemini/antigravity/global_workflows/%'))
        ORDER BY wf.importance DESC
    """)

    facts_data = []
    for row in c.fetchall():
        fid = row[0]
        try:
            c.execute("SELECT embedding FROM vec_world_facts WHERE rowid = ?", (fid,))
            emb_row = c.fetchone()
            if emb_row:
                emb = _unpack_embedding(emb_row[0])
                facts_data.append({
                    "id": fid,
                    "entity": row[1],
                    "fact": row[2],
                    "importance": row[3],
                    "confidence": row[4],
                    "embedding": emb,
                })
        except Exception:
            continue

    db.close()

    # Greedy clustering
    assigned = set()
    clusters = []

    for fact in facts_data:
        if fact["id"] in assigned:
            continue

        cluster = {
            "centroid_entity": fact["entity"],
            "centroid_fact": fact["fact"],
            "max_importance": fact["importance"],
            "members": [fact],
        }
        assigned.add(fact["id"])

        for other in facts_data:
            if other["id"] in assigned:
                continue
            sim = _cosine_similarity(fact["embedding"], other["embedding"])
            if sim >= similarity_threshold:
                cluster["members"].append(other)
                assigned.add(other["id"])
                if other["importance"] > cluster["max_importance"]:
                    cluster["max_importance"] = other["importance"]

        clusters.append(cluster)

    # Sort by cluster size descending
    clusters.sort(key=lambda c: len(c["members"]), reverse=True)
    return clusters


def detect_skill_gaps(clusters: list[dict], min_cluster_size: int = 3) -> list[dict]:
    """
    Compare knowledge clusters to existing Skills directory.
    Returns proposals for enrichment or new skill creation.
    """
    existing_skills = set()
    if os.path.isdir(SKILLS_DIR):
        existing_skills = {d.lower() for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))}

    existing_kis = set()
    if os.path.isdir(KI_DIR):
        existing_kis = {d.lower() for d in os.listdir(KI_DIR) if os.path.isdir(os.path.join(KI_DIR, d))}

    proposals = []

    for cluster in clusters:
        if len(cluster["members"]) < min_cluster_size:
            continue

        centroid = cluster["centroid_entity"].lower().replace(" ", "-")
        entities_in_cluster = {m["entity"] for m in cluster["members"]}

        # Check if any entity matches a skill name
        matching_skill = None
        for skill in existing_skills:
            for entity in entities_in_cluster:
                if skill in entity.lower() or entity.lower() in skill:
                    matching_skill = skill
                    break
            if matching_skill:
                break

        # Check if any entity matches a KI
        matching_ki = None
        for ki in existing_kis:
            for entity in entities_in_cluster:
                if ki in entity.lower().replace(" ", "_") or entity.lower().replace(" ", "_") in ki:
                    matching_ki = ki
                    break
            if matching_ki:
                break
                
        # --- GRAPH-AWARENESS: Consult memory_edges ---
        # If we didn't find a direct string match, check if the graph already knows about a relationship
        if not matching_skill and not matching_ki:
            db = _get_db()
            c = db.cursor()
            member_ids = [m["id"] for m in cluster["members"]]
            if member_ids:
                placeholders = ",".join(["?"] * len(member_ids))
                # Look for outgoing or incoming edges to/from world_facts that belong to a skill or KI
                c.execute(f"""
                    SELECT wf.source_url 
                    FROM memory_edges me
                    JOIN world_facts wf ON (
                        (me.target_type = 'world_fact' AND me.target_id = wf.id AND me.source_type = 'world_fact' AND me.source_id IN ({placeholders}))
                        OR 
                        (me.source_type = 'world_fact' AND me.source_id = wf.id AND me.target_type = 'world_fact' AND me.target_id IN ({placeholders}))
                    )
                    WHERE wf.source_url IS NOT NULL 
                      AND (wf.source_url LIKE '%/.gemini/skills/%' OR wf.source_url LIKE '%/.gemini/antigravity/knowledge/%')
                    LIMIT 1
                """, (*member_ids, *member_ids))
                edge_match = c.fetchone()
                if edge_match:
                    url = edge_match[0]
                    if "/skills/" in url:
                        matching_skill = url.split("/skills/")[-1].split("/")[0]
                    elif "/knowledge/" in url:
                        matching_ki = url.split("/knowledge/")[-1].split("/")[0]
            db.close()

        fact_summaries = [f"- [{m['importance']}] {m['entity']}: {m['fact'][:80]}" for m in cluster["members"][:8]]

        if matching_skill:
            proposals.append({
                "type": "SKILL_ENRICHMENT",
                "target": matching_skill,
                "cluster_size": len(cluster["members"]),
                "max_importance": cluster["max_importance"],
                "evidence": fact_summaries,
                "recommendation": f"Proposed: Enrich '{matching_skill}/SKILL.md' with {len(cluster['members'])} conversation-learned edge cases.",
            })
        elif matching_ki:
            proposals.append({
                "type": "KI_ENRICHMENT",
                "target": matching_ki,
                "cluster_size": len(cluster["members"]),
                "max_importance": cluster["max_importance"],
                "evidence": fact_summaries,
                "recommendation": f"Proposed: Update KI '{matching_ki}' with {len(cluster['members'])} newly discovered facts.",
            })
        else:
            proposals.append({
                "type": "NEW_KI",
                "target": centroid,
                "cluster_size": len(cluster["members"]),
                "max_importance": cluster["max_importance"],
                "evidence": fact_summaries,
                "recommendation": f"Proposed: Create new KI '{centroid}' from {len(cluster['members'])} conversation-extracted facts.",
            })

    return proposals


def propose_taxonomy_mutations(clusters: list[dict], min_cluster_size: int = 5) -> list[dict]:
    """
    Analyze knowledge clusters for domain patterns that suggest new agent archetypes.
    """
    db = _get_db()
    c = db.cursor()
    c.execute("SELECT agent_type FROM agent_taxonomy")
    existing_types = {r[0] for r in c.fetchall()}
    db.close()

    # Domain keyword patterns → candidate agent types
    domain_patterns = {
        "neuroimaging": ["brain", "atlas", "registration", "abba", "brainglobe", "elastix", "allen"],
        "flow_cytometry": ["fcs", "gating", "flow", "cytometry", "facs", "fluorescence"],
        "spatial_transcriptomics": ["spatial", "visium", "spaceranger", "spot", "barcode"],
        "metaproteomics": ["mass spec", "proteom", "peptide", "msms", "protein identification"],
        "clinical_trial_analyst": ["clinical trial", "irb", "protocol", "consent", "recruitment"],
    }

    proposals = []
    for agent_type, keywords in domain_patterns.items():
        if agent_type in existing_types:
            continue

        # Count how many cluster members mention these keywords
        matching_facts = 0
        for cluster in clusters:
            for member in cluster["members"]:
                text = (member["entity"] + " " + member["fact"]).lower()
                if any(kw in text for kw in keywords):
                    matching_facts += 1

        if matching_facts >= min_cluster_size:
            proposals.append({
                "type": "NEW_AGENT_TYPE",
                "agent_type": agent_type,
                "matching_facts": matching_facts,
                "recommendation": f"Proposed: New agent archetype '{agent_type}' — {matching_facts} conversation facts support this specialization.",
            })

    return proposals


def run_distillation() -> dict:
    """
    Run the full Knowledge Distillation pipeline.
    Returns a summary report for GEPA consumption.
    """
    logger.info("Starting Knowledge Distillation...")

    # ── Pre-flight self-diagnosis ──
    try:
        # Import path: preflight.py lives in antigravity-brain
        import sys, importlib
        brain_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "antigravity-brain", "src")
        if os.path.isdir(brain_src) and brain_src not in sys.path:
            sys.path.insert(0, brain_src)
        from antigravity_brain.preflight import run_preflight
        report = run_preflight("distiller")
        if not report.passed:
            logger.error("[Distiller] Pre-flight FAILED. Returning empty report.")
            logger.error(f"  Blockers: {report.blockers}")
            return {
                "walkthroughs_processed": 0, "rules_extracted": 0,
                "clusters_found": 0, "top_clusters": [],
                "skill_ki_proposals": [], "taxonomy_proposals": [],
                "rule_proposals": [], "preflight_failed": True,
                "preflight_blockers": report.blockers,
            }
    except Exception as e:
        logger.warning(f"[Distiller] Pre-flight module unavailable ({e}), proceeding with caution...")

    # Phase 0: Process all un-evaluated walkthroughs via DSPy WisdomDistiller
    import glob
    from antigravity_evolution.wisdom_distiller import WisdomDistiller
    
    brain_dir = os.path.expanduser("~/.gemini/antigravity/brain")
    walkthroughs = glob.glob(os.path.join(brain_dir, "*", "walkthrough.md"))
    
    db = _get_db()
    c = db.cursor()
    
    # Try initializing WisdomDistiller for DSPy evaluation
    try:
        distiller = WisdomDistiller()
        import dspy
        from dotenv import load_dotenv
        load_dotenv(os.path.expanduser("~/.gemini/.env"))
        api_key = os.environ.get("GOOGLE_AI_API_KEY", "")
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key # Some DSPy/LiteLLM handlers use GEMINI_API_KEY
            lm = dspy.LM("gemini/gemini-2.5-flash", api_key=api_key, timeout=60.0) # Prevent infinite socket hang
            dspy.configure(lm=lm)
            logger.info("DSPy LM configured with gemini-2.5-flash (timeout=60.0s).")
        else:
            logger.warning("GOOGLE_AI_API_KEY not found in .env, DSPy might fail.")
            distiller = None
    except Exception as e:
        logger.error(f"Could not initialize WisdomDistiller: {e}")
        distiller = None
        
    processed_count = 0
    new_rules = []
    
    # Limit batch to prevent blocking the scheduler for too long
    batch_limit = 3 
    
    for w_path in walkthroughs:
        if processed_count >= batch_limit:
            logger.info(f"Reached walkthrough distillation batch limit ({batch_limit}). Breaking early to prevent thread blocking.")
            break
            
        # Check if evaluated
        try:
            c.execute("SELECT id FROM task_evaluations WHERE walkthrough_path = ?", (w_path,))
            if not c.fetchone() and distiller:
                logger.info(f"Running deep DSPy evaluation on {w_path}...")
                distiller.process_walkthrough(w_path, "Automated Discovery via Distiller")
                processed_count += 1
        except Exception as e:
            logger.error(f"Failed to process {w_path}: {e}")
                
    # Fetch all rules not promoted to gtb
    try:
        c.execute("SELECT rule_text, target_name FROM evaluation_rules WHERE promoted_to_gtb = 0")
        for row in c.fetchall():
            new_rules.append(row)
    except Exception as e:
        logger.error(f"Failed to fetch rules: {e}")
        
    db.close()
    
    logger.info(f"DSPy Wisdom Distillation processed {processed_count} new walkthroughs.")
    
    try:
        t_in = 0
        t_out = 0
        if 'lm' in locals() and hasattr(lm, 'history'):
            for call in lm.history:
                if isinstance(call, dict) and 'usage' in call:
                    u = call['usage']
                    if hasattr(u, "prompt_tokens"):
                        t_in += getattr(u, "prompt_tokens", 0)
                        t_out += getattr(u, "completion_tokens", 0)
                    elif isinstance(u, dict):
                        t_in += u.get('prompt_tokens', 0)
                        t_out += u.get('completion_tokens', 0)
        if t_in > 0 or t_out > 0:
            logger.info(f"[TOKENS] input={t_in} output={t_out} model=gemini-2.5-flash")
    except Exception:
        pass

    # 1. Cluster
    clusters = cluster_unindexed_facts(similarity_threshold=0.80)
    logger.info(f"Found {len(clusters)} knowledge clusters from unindexed facts.")
    
    # 1.5 DB Tracking Update: mark distilled facts with a timestamp so they don't re-cluster
    if clusters:
        db = _get_db()
        c = db.cursor()
        for cluster in clusters:
            member_ids = [m["id"] for m in cluster["members"]]
            if member_ids:
                placeholders = ",".join("?" * len(member_ids))
                c.execute(f"UPDATE world_facts SET distilled_at = CURRENT_TIMESTAMP WHERE id IN ({placeholders})", (*member_ids,))
        db.commit()
        db.close()
        logger.info("Marked clustered facts as distilled (via distilled_at timestamp) to prevent repeat processing.")

    # 2. Detect gaps
    skill_proposals = detect_skill_gaps(clusters, min_cluster_size=3)
    logger.info(f"Generated {len(skill_proposals)} skill/KI proposals.")

    # 3. Taxonomy mutations
    taxonomy_proposals = propose_taxonomy_mutations(clusters, min_cluster_size=5)
    logger.info(f"Generated {len(taxonomy_proposals)} taxonomy proposals.")
    
    # 4. Convert evaluation rules into GEPA proposals
    rule_proposals = []
    for r in new_rules:
        target = r["target_name"] if r["target_name"] else "System Policy"
        rule_proposals.append({
            "type": "POLICY_UPDATE",
            "target": target,
            "recommendation": f"Proposed: Add error prevention rule to '{target}' policy/skill. Rule: {r['rule_text']}"
        })
        
    all_proposals = skill_proposals + taxonomy_proposals + rule_proposals
    
    # 5. DB Insertion (THE PHYSICAL WRITING BUGFIX)
    if all_proposals:
        db = _get_db()
        c = db.cursor()
        inserted_count = 0
        for p in all_proposals:
            rec = p.get("recommendation", "")
            if not rec: continue
            
            # Ensure we don't insert duplicates.
            # distilled_at is pre-set to CURRENT_TIMESTAMP so these proposal rows
            # NEVER re-enter the clustering pool on the next distillation run.
            c.execute("SELECT id FROM world_facts WHERE source_url = 'gepa://distiller' AND fact = ?", (rec,))
            if not c.fetchone():
                c.execute(
                    """INSERT INTO world_facts
                           (entity, fact, importance, confidence_score, source_url, distilled_at)
                       VALUES (?, ?, ?, ?, 'gepa://distiller', CURRENT_TIMESTAMP)""",
                    (p.get("target", "System"), rec, int(p.get("max_importance", 10)), 0.99)
                )
                inserted_count += 1
        # Mark rules as promoted so they never re-enter the pipeline
        promoted_targets = [p.get("target", "") for p in rule_proposals if p.get("recommendation", "")]
        if promoted_targets:
            placeholders = ",".join("?" * len(promoted_targets))
            c.execute(
                f"UPDATE evaluation_rules SET promoted_to_gtb = 1 WHERE target_name IN ({placeholders})",
                tuple(promoted_targets)
            )

        db.commit()
        db.close()
        logger.info(f"Wrote {inserted_count} pending GEPA proposals to brain.db for Swarm consumption.")

    report = {
        "walkthroughs_processed": processed_count,
        "rules_extracted": len(new_rules),
        "clusters_found": len(clusters),
        "top_clusters": [
            {
                "centroid": c["centroid_entity"],
                "size": len(c["members"]),
                "max_importance": c["max_importance"],
            }
            for c in clusters[:15]
        ],
        "skill_ki_proposals": skill_proposals,
        "taxonomy_proposals": taxonomy_proposals,
        "rule_proposals": rule_proposals
    }

    return report
