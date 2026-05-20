---
name: modular-task-execution
description: A policy for decomposing complex tasks into a sequence of smaller, manageable sub-tasks and defining an orchestration strategy for their execution, including conditional logic.
license: MIT
skill-author: AROS-Core
version: 2.0
original-source: addyosmani/agent-skills/incremental-implementation
---

# Modular Task Execution Policy

This document outlines the 'Modular Task Execution' policy, which governs how AROS agents should approach complex, multi-step tasks. The primary goal is to ensure that large objectives are broken down into a logical sequence of smaller, verifiable steps governed by a clear orchestration strategy.

## GEPA Rule: Task Decomposition

**The agent must decompose complex tasks into smaller, manageable sub-tasks and execute them in an organized and logical sequence to achieve the overall objective.**

### Guiding Principles

- **Think Step-by-Step:** Before execution, explicitly outline the sequence of sub-tasks. This plan should be communicated or logged.
- **Single Responsibility per Step:** Each sub-task should have a single, well-defined purpose. For example, a sub-task should be "Read the file content," not "Read the file and find the relevant lines."
- **Validate Intermediate Outputs:** After completing a sub-task, verify its output before proceeding to the next. This prevents the propagation of errors.
- **Logical Sequencing:** Ensure the order of sub-tasks is logical and dependencies are respected. A task that processes data must come after the task that reads the data.

---

## GEPA Rule: Orchestration Strategy Declaration

**For any workflow involving multiple dependent tasks, the agent MUST first define and declare an explicit orchestration strategy. This strategy must address dependencies, execution patterns, state management, and error handling.**

This rule extends the `dependent-task-sequencing-policy` by requiring a proactive plan for managing complex workflows beyond simple linear execution.

### 1. Define the Dependency Graph

The agent must identify all sub-tasks and map their relationships. This is the foundation of the execution plan.

- **Producer:** A task that creates an output (artifact, data, state).
- **Consumer:** A task that requires the output from one or more producers.

**Example:**
- **Task A (Producer):** Download dataset.
- **Task B (Producer):** Download data schema.
- **Task C (Consumer):** Validate dataset (depends on A and B).
- **Task D (Consumer):** Generate report (depends on C).

### 2. Select an Execution Pattern

Based on the dependency graph, the agent must select the most efficient and logical execution pattern.

- **Sequential Execution:** For strictly linear workflows where each step depends on the one immediately preceding it. This is the default for simple tasks.
    - **Example:** `Task A` -> `Task B` -> `Task C`

- **Parallel Execution:** For tasks that are not dependent on each other and can be run concurrently to improve performance.
    - **Example:**
      ```
      (Task A) ─┐
               ├─> (Task C)
      (Task B) ─┘
      ```
      *Tasks A and B can run in parallel before Task C begins.*

- **Fan-out / Fan-in:** For workflows where one task triggers multiple parallel processing tasks (fan-out), and a subsequent task consolidates their results (fan-in).
    - **Example:** A master task splits a large dataset into 5 chunks (fan-out), 5 parallel tasks process one chunk each, and a final task merges the 5 processed chunks back into a single result (fan-in).

- **Conditional Execution:** For workflows that require branching logic, where the execution path is determined by the outcome of a previous task. The agent must use conditional statements (e.g., if-then-else) to control the flow.
    - **Example:**
        1. **Task A:** Check if a file exists.
        2. **Condition:**
           - **If `True` (file exists):** Execute **Task B** (Process the file).
           - **If `False` (file does not exist):** Execute **Task C** (Download the file).
        3. **Task D:** Continue processing with the file from either Task B or C.

### 3. State Management

The agent must define how state (e.g., variables, file paths, intermediate results) is passed between tasks.

- **Implicit State:** For simple sequential workflows, the output of one step can be the implicit input for the next.
- **Explicit State Management:** For complex workflows (parallel, conditional), an explicit state object (like a dictionary or JSON object) must be maintained and passed to each task. This ensures data consistency and avoids ambiguity.

### 4. Error Handling and Recovery

The orchestration strategy must include a plan for handling task failures.

- **Retry:** For transient errors (e.g., network issues), a task can be retried a limited number of times.
- **Fallback:** If a task consistently fails, a fallback task or alternative strategy should be invoked. (See `gepa_error_prevention_patch`).
- **Compensating Transaction:** For stateful operations, if a later task fails, a compensating task may be needed to undo the actions of a previous successful task (e.g., delete a partially created resource).
- **Halt and Report:** If recovery is not possible, the workflow must halt cleanly and report the failure, including the state at the time of the error.


## Incremental Implementation (Merged from Osmani)

- **Thin-Slice Delivery:** Deliver full-stack features in the smallest possible increment.
- **Progress Checkpoints:** Verify functionality after every slice.
- **Rollback Guidance:** Always ensure a quick rollback path (e.g., `git reset --hard`) before starting a complex task.
