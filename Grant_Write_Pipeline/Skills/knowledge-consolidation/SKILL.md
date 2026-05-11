---
name: pre-creation-planner
description: A mandatory planning skill for synthesizing information into a structured blueprint before authoring a new skill or Knowledge Item (KI). This skill produces a plan, not the final artifact.
license: MIT
skill-author: AROS-Code-Generator
---

# Pre-Creation Planner (Blueprint Generation)

This skill provides a systematic process for gathering, analyzing, and structuring information into a coherent plan. It is a **mandatory preparatory step** before using the `skill-creator` or authoring a new Knowledge Item. The goal is to produce a structured blueprint to guide the creation of a new AROS artifact.

## 🟥 HARD FAILURE CONSTRAINT: DO NOT MISUSE THIS SKILL 🟥

This skill will **IMMEDIATELY FAIL** if invoked for any task related to system memory, indexing, or database operations. It is a **PLANNING-ONLY** skill.

| Permitted Use (PLANNING)                                   | Forbidden Use (EXECUTION / MEMORY)                                                                |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| ✅ Outlining the structure of a new skill.                 | ❌ **Indexing** a KI into `brain.db` or vector memory.                                            |
| ✅ Synthesizing text from multiple sources into a summary. | ❌ Performing **memory consolidation** as part of the "AROS dream cycle".                           |
| ✅ Creating a temporary Markdown blueprint file.           | ❌ Interacting with any database, file system (except `/tmp`), or API.                            |
| ✅ Use by a `mutation_sweeper` or `developer` persona.     | ❌ Invocation by the **`dreamer` persona**. This persona's tasks are incompatible with this skill. |

**For memory, indexing, or "dream cycle" tasks, you MUST use a different skill, such as `knowledge-indexer`.**

## Tool Schema

This skill is purely conceptual and **has no executable tools**. Its only output is a structured Markdown document, which is the result of the agent's reasoning process following the mandatory workflow.
- **tools**: `none`

## When to Use

- **ALWAYS** use this skill as the first step before creating a new skill with `skill-creator`.
- Use when you need to synthesize research from a `literature-review` into a structured format for a new artifact.
- Use before drafting a new Knowledge Item that draws from multiple internal reports, logs, or external data sources.

## Constraints & Anti-Patterns (When NOT to Use)

- **DO NOT** use this skill to index, update, save, or manage KIs or skills. It lacks the necessary tools.
- **DO NOT** use this skill *after* an artifact has already been drafted. Its purpose is to create the plan, not to execute it.
- **DO NOT** use for any task involving the `dreamer` persona or the "AROS dream cycle." This is a planning skill, not a memory management skill.

## Mandatory Workflow

1.  **Identify Information Sources:**
    *   Explicitly list all potential sources of information relevant to the new artifact.
    *   Sources may include: results from `literature-review`, queries to `brain.db`, existing skills/KIs, system logs, user-provided documents, etc.

2.  **Extract Key Information:**
    *   From each source, extract the core facts, data points, process steps, and concepts essential for the new artifact's functionality.

3.  **Synthesize and Structure:**
    *   Organize the extracted information into a logical, coherent structure (e.g., a Markdown outline, process flow). This structure will serve as the blueprint for the new skill.

4.  **Produce the Final Blueprint:**
    *   Write a brief summary document that lists the sources consulted, key findings, and the final coherent structure.
    *   This summary **MUST** be saved as a temporary file (e.g., `/tmp/blueprint.md`).
    *   **This blueprint is the final and ONLY output of this skill.** The process of *creating* or *indexing* the artifact is handled by a different, subsequent skill (e.g., `skill-creator` or `knowledge-indexer`).

## Example Usage

**Goal:** Create a new skill for analyzing AROS system performance.

**Step 1: Identify Sources**
-   `aros-dashboard-control` skill (for API endpoints).
-   `brain.db` queries on `swarm_jobs` table (for historical task data).
-   AROS logs (`~/.gemini/antigravity/logs/aros.log`).

**Step 2: Extract Key Information**
-   From `aros-dashboard-control`: Get API endpoints like `/api/metrics`.
-   From `brain.db`: SQL query to get average job completion times.
-   From logs: Grep for common error patterns.

**Step 3: Synthesize and Structure**
-   Create an outline in a temporary file to serve as the blueprint:
    ```markdown
    # AROS Performance Analysis Skill Blueprint

    ## 1. Core Functions
    - `get_current_metrics()`: Hits `/api/metrics` endpoint.
    - `get_historical_performance()`: Queries `brain.db` for job stats.
    - `check_for_errors()`: Searches logs for critical failures.
    ```

**Step 4: Produce the Final Blueprint**
-   Save the blueprint to `/tmp/performance_skill_blueprint.md`. Now, you are ready to pass this file to the `skill-creator` skill to begin the actual creation process.