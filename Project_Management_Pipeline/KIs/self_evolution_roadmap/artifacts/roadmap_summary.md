# AROS Self-Evolution Roadmap — KI Summary

## Current State
AROS is at **Level 2** (Heuristic Evolution via GEPA/Distiller). Target: **Level 5** (Autonomous RL-Trained Evolution).

## Gap Analysis Summary (from MTL + SkillOS papers)
| Gap | Severity | Phase |
|---|---|---|
| No RL-Trained Curation | 🔴 Critical | Phase 4 |
| No Skill Update/Delete | 🔴 Critical | Phase 2 |
| No Insight-Level Memory | 🟠 Medium | Phase 1 |
| Static Retrieval | 🟡 Low-Medium | Phase 5 |

## AROS Competitive Advantages
- Multi-file hierarchical SKILL.md (SkillOS acknowledges this as their limitation)
- Production governance (CPCP/SAMS/GEPA) — neither paper addresses safety
- Brain Federation (cross-instance sync) — maps to SkillOS's open research question

## Phase Dependencies
```
Phase 1 ──► Phase 3
Phase 2 ──► Phase 3 ──► Phase 4
                        Phase 5
```

## Key Files to Modify Per Phase
| Phase | Primary Files |
|---|---|
| 1 (Insight Memory) | `db.py`, `dreamer.py`, `ambient_screener.py`, `server.py` |
| 2 (Skill Lifecycle) | `batch_evolver.py`, `knowledge_distiller.py`, `db.py`, `AROS_POLICY.md` |
| 3 (Curator Decoupling) | `agent_taxonomy`, `orchestrator.py`, Swarm Bridge |
| 4 (RL Training) | New training pipeline, Qwen3-8B/Gemma-3-9B finetuning |
| 5 (Agentic Retrieval) | `server.py`, `ambient_screener.py` |

## Master Tracking File
`/home/ubuntu4/GitHub/AROS_Pipeline_Factory/ROADMAP_SELF_EVOLUTION.md`

## Cross-Phase Invariants
1. CPCP compliance on every change
2. SAMS governance for all shared assets
3. re_gent audit trail
4. Brain Federation compatibility
5. Key Learnings documented before proceeding to next phase
6. Wiki sync after each phase completion
