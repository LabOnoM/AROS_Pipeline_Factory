# Research Discovery — Extended Templates & References

This KI contains the bulky templates, examples, and persona guidelines extracted from
`/research-discovery` to keep the workflow within its 12 000-character limit.

---

## Phase 4 — Research Plan Template

Generate a structured plan in this exact format:

````markdown
# Research Plan: [Short Title]
*Generated: [date]*

---

## 1. Research Objective
[1-3 sentences. Precise. Citable.]

## 2. Hypotheses to Test
| ID | Hypothesis | Priority | Falsifiable prediction |
|----|-----------|----------|----------------------|
| H1 | ... | HIGH | ... |
| H2 | ... | MEDIUM | ... |

## 3. Literature Context
*What Kosmos should mine:*
- Key search terms: [list]
- Key prior papers to anchor on: [if user mentioned any]
- Key databases: PubMed, ArXiv, Semantic Scholar, [domain-specific]

## 4. Experiment Design
*What BFTS should optimize:*
- Stage 1 (preliminary): [what to validate first]
- Stage 2 (tuning): [what parameters to optimize]
- Stage 3 (creative): [what novel angles to explore]
- Stage 4 (ablation): [what components to test]

## 5. Success Criteria
| Metric | Minimum bar | Ideal outcome |
|--------|-------------|---------------|
| ... | ... | ... |

## 6. Anti-Goals (explicit out-of-scope)
- NOT investigating: [...]
- NOT using: [specific methods to exclude, if user stated]

## 7. super_scientist Execution Parameters
```python
from kosmos.workflow.super_scientist import SuperScientistWorkflow
import asyncio

ss = SuperScientistWorkflow(
    research_objective="[PASTE OBJECTIVE HERE]",
    domain="[domain]",
    artifacts_dir="./artifacts/[short_name]",
)

result = asyncio.run(ss.run(
    kosmos_cycles=[N],           # recommend: 2 (fast) / 3 (standard) / 5 (deep)
    tasks_per_cycle=[M],         # recommend: 3-5
    bfts_steps=[S],              # recommend: 9 (fast) / 21 (full)
    write_paper=[True/False],    # True only if user wants a paper output
))
```

## 8. Swarm Configuration (if multi-angle)
```python
sub_questions = [
    "H1: [...]",
    "H2: [...]",
]
# Use kosmos_swarm MCP tool or kosmos_swarm.py
```

## 9. Expected Timeline
| Phase | Engine | Estimated time |
|-------|--------|----------------|
| Literature mining | Kosmos | ~10–20 min |
| Hypothesis ranking | Kosmos | ~5 min |
| BFTS optimization | AIS-v2 | ~30–120 min |
| Validation | Kosmos ScholarEval | ~5 min |
| Paper writing | AIS-v2 | ~30 min (optional) |
| **Total** | | **~50 min – 3h** |

## 10. Post-Run Actions
- [ ] Run `/wiki-ingest` to index findings into LLM-Wiki
- [ ] Run `/lab-commit` to commit artifacts to project git
- [ ] If paper generated: run `/manuscript-write` for peer-review polish
````

---

## Phase 5 — Approval and Launch

**Goal:** Get explicit user approval, then fire `super_scientist`.

Present:
> *"Your research plan is ready above. You can:*
> - **Approve as-is** → I'll launch super_scientist now
> - **Edit any section** → Tell me what to change and I'll update
> - **Save for later** → I'll commit the plan to your LLM-Wiki for future use"*

**On approval:**

1. Confirm the exact `super_scientist` call parameters one more time:
   ```
   Objective: "..."
   Domain: ...
   Cycles: N, Tasks: M, BFTS: S steps
   Paper: yes/no
   Output: ./artifacts/[name]
   ```
2. Ask: *"Shall I launch now?"*
3. On confirmation → invoke `kosmos_super_scientist` MCP tool (or run CLI)
4. Report back with artifact location and next steps

---

## Agent Persona During This Workflow

- **Curious, not interrogating** — questions come from genuine interest, not a checklist
- **Intellectually bold** — willing to say "I think your framing is wrong because..."
- **Practically grounded** — always aware of compute/time constraints
- **Good memory** — explicitly reference what the user said 2 turns ago
- **Non-assuming** — do not fill in gaps with guesses; ask instead
- **Anti-scope-creep** — if the user keeps expanding the question, gently focus

---

## Example Brainstorm Angles (Biology)

- **Spatial context is causative, not correlative** — the repair outcome is determined by which microenvironmental niche cells land in, not intrinsic cell state
- **The failure mode is metabolic** — bone repair fails because of local ATP depletion, not immune infiltration
- **The key player is non-coding** — lncRNAs or miRNAs regulate the transition, and the protein-coding signal is secondary
- **Timing, not quantity** — the immune response is beneficial at day 3 but harmful at day 10; the problem is kinetics
- **A rare subpopulation drives everything** — 2% of osteoprogenitors account for 80% of the repair signal

---

## Integration Points

| Output | Where it goes |
|--------|--------------|
| Research plan markdown | `/wiki-ingest` → LLM-Wiki |
| super_scientist result | `./artifacts/[name]/` |
| Paper (if generated) | `/manuscript-write` workflow |
| Git commit | `/lab-commit` workflow |
