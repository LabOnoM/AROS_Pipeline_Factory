# 🧠 AROS Self-Evolution Roadmap

> **Status:** Active  
> **Created:** 2026-05-13  
> **Derived From:** Gap analysis vs. MTL (arXiv:2604.14004) & SkillOS (arXiv:2605.06614)  
> **Full Report:** See `literature_evaluation_report.md` in conversation artifacts  
> **AROS Current Level:** Level 2 (Heuristic Evolution)  
> **Target Level:** Level 5 (Autonomous RL-Trained Evolution)

---

## Architecture Context

```
Phase 1 (Insight Memory) ──► Phase 3 (Curator Decoupling)
Phase 2 (Skill Lifecycle)──► Phase 3 ──► Phase 4 (RL Training)
                                          Phase 5 (Agentic Retrieval)
```

**Key Principle:** Each phase is **additive** — it layers onto existing AROS infrastructure without breaking CPCP compliance, SAMS governance, or the re_gent audit trail. No ground-up refactoring required.

---

## Phase 1: Insight Memory Layer

**Priority:** 🟠 HIGH | **Effort:** 4–6 weeks | **Risk:** Low  
**Objective:** Upgrade the Dreamer to extract Insight-format memories alongside existing `world_facts` and `mental_models`.

### Tasks

- [ ] **1.1** Add `insights` table to `brain.db` schema (`db.py`)
  - Fields: `id`, `title`, `description`, `content`, `domain_origin`, `abstraction_score`, `embedding`, `created_at`
  - **File:** `antigravity-brain/src/antigravity_brain/db.py`
  - **Acceptance:** Table creation verified via `sqlite3 brain.db ".schema insights"`

- [ ] **1.2** Update Dreamer extraction prompts to generate Insight triples
  - Add a new extraction mode that produces `{title, description, content}` triples from conversation logs
  - **File:** `antigravity-brain/src/antigravity_brain/dreamer.py`
  - **Acceptance:** Running `trigger_consolidation` produces at least 1 Insight record per processed conversation

- [ ] **1.3** Update Ambient Screener to include top-K Insights in MTL payload
  - Add `insights` as a 10th field in the `screen_user_message` response
  - **File:** `antigravity-brain/src/antigravity_brain/ambient_screener.py`
  - **Acceptance:** `screen_user_message` returns non-empty `insights` field

- [ ] **1.4** Add abstraction-level weighting to skill retrieval
  - Priority order: Insights > Mental Models > World Facts
  - **File:** `antigravity-brain/src/antigravity_brain/server.py` (find_helpful_skills)
  - **Acceptance:** Retrieval results show Insight-type entries ranked higher

- [ ] **1.5** Integration test: Verify cross-domain retrieval
  - Create test Insights from one domain, verify retrieval in another domain context
  - **Acceptance:** Cross-domain Insight retrieval verified in at least 3 domain pairs

### Phase 1 Completion Criteria
- [ ] `insights` table exists and is populated
- [ ] Dreamer automatically extracts Insights during dream cycles
- [ ] Ambient Screener injects Insights into pre-flight context
- [ ] Retrieval weighted by abstraction level
- [ ] `/lab-commit` with all Phase 1 changes

### Key Learnings (fill during/after execution)
<!-- 
Document what you learned during Phase 1 here.
This section ensures Phase 2 starts with full context.
-->
- _Pending..._

---

## Phase 2: Full Skill Lifecycle Operations

**Priority:** 🔴 CRITICAL | **Effort:** 6–8 weeks | **Risk:** Medium  
**Depends On:** Independent (can run in parallel with Phase 1)  
**Objective:** Upgrade GEPA to support Update and Delete operations, not just Insert.

### Tasks

- [ ] **2.1** Add `skill_update` tool to `batch_evolver.py`
  - Enable in-place modification of existing SKILL.md files with version tracking
  - **File:** `antigravity-brain/src/antigravity_brain/batch_evolver.py`
  - **Acceptance:** `skill_update("task_decomposition", new_content)` modifies the file and increments version

- [ ] **2.2** Add `skill_delete` tool to `batch_evolver.py`
  - Implement soft-delete with 7-day rollback window (archive, don't hard-delete)
  - **File:** `antigravity-brain/src/antigravity_brain/batch_evolver.py`
  - **Acceptance:** Deleted skills archived to `~/.gemini/skills/.archive/` with restore capability

- [ ] **2.3** Add skill versioning to SKILL.md metadata
  - New YAML fields: `version`, `parent_skill`, `deprecated_by`, `last_updated`
  - **File:** Pipeline Factory SKILL.md template
  - **Acceptance:** All existing skills have `version: 1.0` added to frontmatter

- [ ] **2.4** Update Knowledge Distiller to propose Update/Delete actions
  - Currently proposes: NEW_SKILL, SKILL_MERGE, NEW_KI
  - Add: SKILL_UPDATE (with diff), SKILL_DELETE (with rationale)
  - **File:** `antigravity-brain/src/antigravity_brain/knowledge_distiller.py`
  - **Acceptance:** Distiller output includes at least one UPDATE or DELETE proposal

- [ ] **2.5** Execute pending SKILL_MERGE proposals
  - 30+ merge proposals currently queued in `brain.db`
  - **Acceptance:** Redundant skill count reduced by ≥50%

- [ ] **2.6** Add `skill_lifecycle_log` audit table
  - Track every insert/update/delete with rationale, author, timestamp, rollback hash
  - **File:** `db.py`
  - **Acceptance:** Every lifecycle operation creates an audit record

- [ ] **2.7** Add governance policy section for skill lifecycle
  - `auto_update: allowed`, `auto_delete: requires_confirmation`, `rollback_window: 7_days`
  - **File:** `AROS_POLICY.md`
  - **Acceptance:** Policy documented and enforced in `batch_evolver.py`

### Phase 2 Completion Criteria
- [ ] Update and Delete tools functional
- [ ] Skill versioning in all SKILL.md files
- [ ] Knowledge Distiller proposes all 3 operation types
- [ ] Pending merges executed
- [ ] Audit trail operational
- [ ] `/lab-commit` with all Phase 2 changes

### Key Learnings (fill during/after execution)
- _Pending..._

---

## Phase 3: Curator/Executor Decoupling

**Priority:** 🟠 HIGH | **Effort:** 8–12 weeks | **Risk:** High  
**Depends On:** Phase 1 + Phase 2  
**Objective:** Formally decouple the skill curation agent from the task execution agent.

### Tasks

- [ ] **3.1** Define `SkillCurator` persona in `agent_taxonomy`
  - Dedicated persona with `skill_insert`, `skill_update`, `skill_delete` tools
  - **File:** `brain.db` agent_taxonomy table
  - **Acceptance:** `find_helpful_agent("skill curation")` returns SkillCurator

- [ ] **3.2** Implement grouped task evaluation loop
  - Group tasks by semantic similarity using existing embedding infrastructure
  - Execute grouped tasks → collect success/failure signals
  - **Acceptance:** Evaluation loop produces per-skill usage statistics

- [ ] **3.3** Implement Curator as specialized SwarmAgent
  - Runs as a periodic background job (like the Dreamer)
  - Receives task outcome signals as input
  - Produces skill lifecycle operations as output
  - **Acceptance:** Curator SwarmAgent executes at least one autonomous curation cycle

- [ ] **3.4** Freeze executor during Curator training cycles
  - Ensure active IDE sessions are not disrupted by Curator operations
  - **Acceptance:** IDE agent performance unaffected during Curator cycles

- [ ] **3.5** Implement reward signal pipeline
  - `r_corr`: Binary task success from Swarm execution
  - `r_cnt`: Content quality via LLM-as-a-judge
  - **Acceptance:** Reward signals logged to `brain.db` for every Curator action

### Phase 3 Completion Criteria
- [ ] SkillCurator persona operational
- [ ] Evaluation loop produces task-skill attribution
- [ ] Curator makes autonomous curation decisions
- [ ] Reward signals flowing from executor to curator
- [ ] `/lab-commit` with all Phase 3 changes

### Key Learnings (fill during/after execution)
- _Pending..._

---

## Phase 4: RL-Trained Curation

**Priority:** 🔴 CRITICAL (Long-Term) | **Effort:** 12–20 weeks | **Risk:** Very High  
**Depends On:** Phase 3  
**Objective:** Replace heuristic curation with GRPO-trained Skill Curator.

### Tasks

- [ ] **4.1** Implement GRPO reward computation
  - Composite reward: `r = r_corr + r_cnt`
  - **Acceptance:** Reward function produces meaningful gradients

- [ ] **4.2** Prepare training data from AROS task traces
  - Extract (task, trajectory, skill_usage, outcome) tuples from Swarm execution history
  - **Acceptance:** ≥1000 training examples prepared

- [ ] **4.3** Train lightweight Curator model
  - Candidates: Qwen3-8B, Gemma-3-9B (finetuned via GRPO)
  - **Acceptance:** Trained model outperforms prompt-only baseline on held-out tasks

- [ ] **4.4** Deploy trained Curator alongside existing pipeline
  - A/B test: trained Curator vs. heuristic Knowledge Distiller
  - **Acceptance:** Trained Curator demonstrates measurable improvement

- [ ] **4.5** Integrate with Brain Federation
  - Trained Curator weights/checkpoints sync across AROS instances
  - **Acceptance:** Federated instances share Curator improvements

### Phase 4 Completion Criteria
- [ ] GRPO training pipeline operational
- [ ] Trained model available
- [ ] A/B test shows improvement
- [ ] Federation-ready
- [ ] `/lab-commit` with all Phase 4 changes

### Key Learnings (fill during/after execution)
- _Pending..._

---

## Phase 5: Agentic Skill Retrieval

**Priority:** 🟡 MEDIUM | **Effort:** 20+ weeks | **Risk:** Low-Medium  
**Depends On:** Phase 1 (for abstraction-level routing)  
**Objective:** Upgrade from single-shot cosine similarity to multi-hop agentic search.

### Tasks

- [ ] **5.1** Implement iterative retrieval agent
  - Multi-hop: initial query → examine results → reformulate → re-query
  - **Acceptance:** Retrieval agent makes ≥2 queries per retrieval request

- [ ] **5.2** Add abstraction-level routing
  - Prefer Insights for unfamiliar domains, Skills for known domains
  - **Acceptance:** Routing logic verified across 5 domain pairs

- [ ] **5.3** Integrate with Ambient Screener context buffer
  - Cache retrieval results for 10ms hits on repeated queries
  - **Acceptance:** Cache hit rate ≥80% for intra-session queries

- [ ] **5.4** Benchmark retrieval quality
  - Compare single-shot vs. agentic retrieval on AROS task suite
  - **Acceptance:** Agentic retrieval shows measurable improvement in task-relevant skill retrieval

### Phase 5 Completion Criteria
- [ ] Agentic retrieval operational
- [ ] Abstraction-level routing working
- [ ] Cached and performant
- [ ] Benchmarked against baseline
- [ ] `/lab-commit` with all Phase 5 changes

### Key Learnings (fill during/after execution)
- _Pending..._

---

## Cross-Phase Invariants

These rules apply to **every** phase:

1. **CPCP Compliance:** All changes must pass through the canonical processing pipeline
2. **SAMS Governance:** All shared assets must be registered in `SHARED_ASSET_REGISTRY.md`
3. **Audit Trail:** Every modification must be traceable via `re_gent` and `skill_lifecycle_log`
4. **Brain Federation:** All changes must be federation-compatible (no machine-local paths)
5. **Key Learnings:** Each phase's "Key Learnings" section MUST be filled before starting the next phase
6. **Wiki Sync:** Each phase completion triggers a `/wiki-update` to ensure the knowledge base reflects the new state

---

## Quick Reference: Current AROS Architecture

| Component | File | Role |
|---|---|---|
| Memory DB | `brain.db` (SQLite-Vec) | world_facts, mental_models, experiences |
| Dreamer | `dreamer.py` | Background fact/model extraction |
| Screener | `ambient_screener.py` | Pre-flight context injection |
| Distiller | `knowledge_distiller.py` | Fact clustering → mutation proposals |
| Evolver | `batch_evolver.py` | Physical skill/policy mutation |
| Hygiene | `memory_hygiene.py` | Consolidation, dedup, forgetting |
| Orchestrator | `chief_orchestrator.py` | GCO cycle management |
| Federation | `sync.py` | Cross-instance merge protocol |
