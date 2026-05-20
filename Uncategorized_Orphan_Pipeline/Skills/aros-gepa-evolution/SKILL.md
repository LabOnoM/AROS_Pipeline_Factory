---
name: aros-gepa-evolution
description: AROS GEPA Evolution Skill
---

# AROS GEPA Evolution Skill

Use this skill when you need to trigger, monitor, or understand the GEPA (Generative Evolutionary Python Architecture) engine that self-mutates AROS system components.

## When to Use
- A skill, KI, or workflow needs to be updated based on a failure or new knowledge
- You want to run the full autonomous mutation sweep
- You want to distill conversation knowledge into GEPA proposals
- You want to add a new agent archetype discovered through conversation patterns

## What GEPA Mutates
| Target | Location | Description |
|---|---|---|
| `SKILL` | `~/.gemini/skills/*/SKILL.md` | Tool usage docs and constraints |
| `KI` | `~/.gemini/antigravity/knowledge/*/` | Curated knowledge items |
| `WORKFLOW` | `~/.gemini/antigravity/global_workflows/*.md` | Multi-step agentic procedures |
| `POLICY` | `~/.gemini/antigravity/AROS_POLICY.md` | AROS swarm-level agent directives |
| `AGENT_TYPE` | `brain.db/agent_taxonomy` | Agent archetype registry |

## Quick Invocation (CLI)
```bash
# Full sweep: trace analysis + knowledge distillation
cd /mnt/Disk1/AntigravityInit/antigravity-evolution
uv run python -m antigravity_evolution.batch_evolver

# Distillation only (no trace sweep, faster)
uv run python -m antigravity_evolution.batch_evolver --distill-only
```

## Via Dashboard API
```bash
# Trigger full mutation sweep (async background process)
curl -X POST http://localhost:8000/api/mutate_all

# Trigger knowledge distillation only
curl -X POST http://localhost:8000/api/brain/distill
```

## Knowledge Distiller — What It Does
```python
from antigravity_evolution.knowledge_distiller import run_distillation

report = run_distillation()
# Returns:
# {
#   "clusters_found": 547,
#   "top_clusters": [...],
#   "skill_ki_proposals": [
#     {"type": "SKILL_ENRICHMENT", "target": "abba-python", ...},
#     {"type": "NEW_KI", "target": "wnt-pathway", ...}
#   ],
#   "taxonomy_proposals": [
#     {"type": "NEW_AGENT_TYPE", "agent_type": "neuroimaging", "matching_facts": 70}
#   ]
# }
```

## Adding a New Agent Archetype Manually
```python
import sqlite3, json

db = sqlite3.connect("~/.gemini/antigravity/brain.db")
db.execute("""
    INSERT OR REPLACE INTO agent_taxonomy
    (agent_type, description, skills, model_tier, updated_at)
    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
""", (
    "neuroimaging_analyst",
    "Specializes in brain atlas registration, ABBA Python, BrainGlobe, and Allen Atlas workflows.",
    json.dumps(["abba-python", "brainglobe-atlasapi", "brainreg"]),
    "analysis"
))
db.commit()
db.close()
```

## DSPy Evaluation Thresholds
- The batch evolver uses DSPy `Predicted(TraceAnalyzer)` with `gemini-2.5-pro`
- Verdict `"true"` = actionable failure → triggers component mutation
- Verdict `"false"` = benign or expected behavior → skipped

## Telemetry After Sweep
```bash
sqlite3 ~/.gemini/antigravity/brain.db "SELECT * FROM system_telemetry;"
# gepa_mutated_skills   | N
# gepa_mutated_kis       | N
# gepa_mutated_policies  | N
# gepa_mutated_workflows | N
# gepa_failed_traces     | N
```

## Key Rules
- **Error Prevention:** Critical sub-tasks must successfully complete for the overall agent orchestration goal to be achieved.
- **Daily schedule (03:00 local):** Dream cycle → GEPA mutation trace sweep
- **Weekly schedule (Saturday 03:00 local):** Dream → GEPA → Distill Knowledge → Execute & Verify via Swarm
- Phase 1: Trace analysis (walkthrough.md → mutation)
- Phase 2: Knowledge Distillation (conversation facts → proposals)
- Proposals that aren't acted on are saved as `world_facts` with `source_url='gepa://distiller'` for agent context injection
- Never modify `evolver.py` without updating `implementation_plan.md` first (per AGENTS.md rules)
