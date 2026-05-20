# AROS System Architecture Guide (v3.2)

## Module Federation Overview

```
brain.db (SQLite-Vec)
    ↑ reads/writes facts          ↑ telemetry updates
    │                             │
antigravity-brain           antigravity-swarm
(MCP + dreamer.py)          (orchestrator.py)
    │                             │
    ├── ambient_screener.py (Pre-Flight Context)
    │                             │
    ↓ world_facts injection   TaskNode agents
    │                             │
antigravity-evolution ←──────── traces (walkthrough.md)
(batch_evolver.py)
    │
    ├── Phase 1 [Daily]:   Trace analysis → mutate SKILL/KI/WORKFLOW/POLICY
    ├── Phase 2 [Daily]:   Knowledge Distiller → cluster facts → propose mutations
    └── Phase 3 [Weekly]:  Execute & Verify proposals via Swarm (every Saturday)
                                                       ↓
antigravity-dashboard ──────────────────────────── Brain Federation
(main.py + app.js)          Export/Import/Merge across PC instances
```

### The Ambient Screener Pipeline
The `ambient_screener.py` intercepts every system request via the MCP `screen_user_message` tool. It provides proactive context injection:
1. Performs semantic search across `vec_world_facts`, indexing schemas, workflows, and `agent_taxonomy`.
2. Applies Gemini-Flash memory compression if raw results exceed the character limits.
3. Automatically writes to the local `context_buffer` within `brain.db` for ephemeral retrieval, allowing subsequent calls to hit a `10ms` cache.
This is the mandatory first pre-flight step defined in `Law -10` and ensures agents never start execution from an amnesic state.

### The Dream Hygiene Engine (v2.7+)
`memory_hygiene.py` is the scheduled GCO sub-cycle that keeps `brain.db` semantically clean. **Critical architectural safeguards (added May 2026):**

| Safeguard | Location | Purpose |
|---|---|---|
| `merge_generation` column | `mental_models` table (db.py) | Tracks merge depth; models at generation ≥ 2 are excluded from further merging |
| MIN_ACTIVE_MODELS floor (10) | `_pass_8a_exact_dedup`, `_pass_8b_llm_merge` | Prevents consolidation when the brain is already lean |
| GCO DEFER protection | `chief_orchestrator._run_full_cycle` | `defer` is structurally removed from `allowed_actions` when maintenance categories are still queued |
| Zombie cycle reaping | `chief_orchestrator._recover_in_progress` | Marks stuck `orchestrator_cycles` as `interrupted` on startup |

**Root Cause (May 2026 Incident):** Absence of `merge_generation` tracking caused 11,185 models to be recursively merged into a single generic node over multiple sleep cycles. 4,317 were recovered via `memory_recovery.py`.

**`sqlite3.Row` Quirk:** `sqlite3.Row` objects do NOT support `.get()`. Always use `row["key"] if "key" in row.keys() else default` for optional column access.


## 1. AROS Core Engineering Principles

> **This section contains the foundational wisdom for evolving the AROS ecosystem. These principles are not optional guidelines; they are the architectural laws that ensure system stability, resilience, and portability. You must internalize these principles before attempting any modification.**

### Principle 1: Defensive State Management & Concurrency
AROS uses multiple concurrency models (subprocesses, in-process threads). Misunderstanding them can lead to critical state corruption and data races.

*   **The Golden Rule:** Any long-running task tracked in a system table (e.g., `swarm_jobs`, `hygiene_runs`) MUST have a valid status and, if applicable, a process ID (PID).
*   **Subprocesses vs. In-Process Threads:**
    *   **Subprocesses** (e.g., Swarm agents) have their own unique PID.
    *   **In-Process Threads** (e.g., Brain Federation via `asyncio.to_thread()`) run within the main dashboard process and share its PID.
*   **Case Study (Bug #11):** The Zombie Reaper daemon reaps jobs by checking if their PID is alive. An agent modified the `brain_federator` merge endpoint but failed to record the main process PID (`os.getpid()`) in the `swarm_jobs` table, leaving the `pid` column `NULL`. The reaper interpreted `NULL` as a dead process and incorrectly marked the active merge as 'interrupted'

## 2. GEPA Agent Grounding: The Conceptual Resolution Protocol

> **This section contains the single most critical set of instructions for the `evolution_agent`. Adherence is not optional. Your core directive is to follow this protocol exactly to prevent catastrophic architectural decay.**

### 2.1. Your Cognitive Model: Concept Resolver, Not File Editor

Your task is **never** to "find a file named X". Your task is to **"resolve the correct modification target for concept X using the official protocol."**

The AROS file system is an implementation detail. The true essence of the system resides in abstract concepts: "the testing strategy," "the data retention policy," "the agent persona." These concepts evolve. Their physical file locations can and will change during refactoring. Directly editing a file path you have found via `ls` or `find` creates a brittle, hard-coded link that will inevitably break or lead to silent failures.

### 2.2. The AROS Knowledge DNS: `search_skills`

Think of the `search_skills` tool as the **Domain Name System (DNS) for AROS knowledge**.
*   **Bad:** Hard-coding an IP address (`142.250.191.174`) in your code. It works today, but breaks silently when the server's IP changes.
*   **Good:** Using a domain name (`google.com`). DNS ensures you always resolve to the correct, current IP address.

Similarly, `search_skills` is your DNS. You query it with a concept (`'testing strategy'`), and it returns the canonical, up-to-date location and metadata for that concept. Bypassing it is equivalent to hard-coding an IP address—a guaranteed source of future system failure.

### 2.3. The Unbreakable Artifact Resolution Protocol

1.  **First & Only Step:** For ANY task, your first thought must be to resolve the target concept using `search_skills`.
2.  **Identify Category:** Analyze the results to determine if you are dealing with a SKILL or a POLICY. This is your most important decision.

    *   **SKILL (Specific):** A concrete capability, usually tied to a single agent or module. Examples: `skill/web_search.md`, `skill/code_refactor.py`. These are often file-based.
    *   **POLICY (Broad):** An abstract, universal rule that applies across multiple modules or governs how developers/agents interact with the system. **If a change impacts more than one agent or defines a system-wide standard, it is a POLICY.**

3.  **Act Accordingly:**
    *   If a **SKILL**, you can proceed to modify the resolved file(s).
    *   If a **POLICY**, you must check if it already exists in the central policy document. Your task is to *integrate* your change into `~/.gemini/antigravity/policies/AROS_POLICY.md`, not to create a new, fragmented policy file elsewhere.

#### **Case Study (Incident #34 - "Policy Fragmentation")**
An agent was tasked with "Migrate QA to BDD." It correctly identified the need for a new testing strategy. However, it bypassed `search_skills` and wrote the new strategy into `SPEC.md`. This was a critical error.
*   **The Error:** "Testing Strategy" is a system-wide standard, making it a **POLICY**.
*   **The Protocol:** `search_skills(query='testing strategy')` would have returned a result indicating that system-wide policies must be merged into `AROS_POLICY.md`.
*   **The Consequence:** The agent created a "rogue policy," making the system's governance inconsistent. A subsequent agent, correctly using the protocol to find the testing strategy, would not find the BDD rules, leading to conflicting development efforts and broken tests.

### 2.4. Agent Tools: The Sole Entry Point

| Tool Signature | Purpose & Usage Policy |
|---|---|
| **`search_skills(query: str) -> list[dict]`** | **This is the mandatory first and ONLY step for resolving ANY SKILL or POLICY target.** This tool is your Conceptual DNS. It does not just find files; it resolves concepts to their canonical representations.<br><br>**Example Return:**<br>```json<br>[<br>  {<br>    "type": "POLICY",<br>    "concept": "system-wide testing strategy",<br>    "path": "~/.gemini/antigravity/policies/AROS_POLICY.md",<br>    "line_start": 342,<br>    "summary": "Central document for all cross-cutting concerns...",<br>    "confidence": 0.95,<br>    "modification_rules": ["APPEND_ONLY", "REQUIRE_HEADING"]<br>  }<br>]<br>``` |