---
name: subtask-context-propagation
description: A mandatory policy for the Swarm Orchestrator to ensure that high-level goals and critical context are propagated to all sub-tasks during decomposition.
license: MIT
skill-author: AROS-Core (GEPA-derived)
---

# Policy: Sub-task Context Propagation

## 1.0 Overview and GEPA Mandate

This document specifies the **Sub-task Context Propagation** policy, a core component of the AROS Swarm Orchestrator. It is a direct implementation of the GEPA proposal demanding that the division of a task into smaller parts must not dilute the original intent.

The central GEPA rule is as follows:

> **GEPA-Rule-011: Context Inheritance Mandate**
> Every sub-task, regardless of its depth in the execution hierarchy, MUST inherit the complete and immutable context of the original high-level task. This includes the user's verbatim goal and all explicitly identified constraints.

Failure to adhere to this mandate is a critical orchestration failure, leading to context drift, goal misalignment, and inefficient or incorrect task execution.

## 2.0 Scope and Integration

This policy governs the **Swarm Orchestrator's Data Propagation Mechanism**. It is triggered whenever a task is decomposed into sub-tasks, as required by the `modular-task-breakdown` and `modular-task-execution` policies.

This policy acts as the essential link between `task-context-alignment` (which *identifies* the context at the start) and `modular-task-breakdown` (which *executes* the sub-tasks).

## 3.0 The Specification: Task Context Object (TCO)

To enforce the Context Inheritance Mandate, the Swarm Orchestrator MUST create and propagate a data structure known as the **Task Context Object (TCO)**.

### 3.1 TCO Instantiation

- A single TCO is instantiated by the Orchestrator at the very beginning of a new high-level task.
- Its content is derived from the initial application of the `task-context-alignment` skill on the user's prompt.

### 3.2 TCO Structure

The TCO must be a structured object (e.g., JSON or dictionary) containing the following mandatory fields:

| Field | Type | Description |
| :--- | :--- | :--- |
| `task_id` | string | A unique identifier for the high-level task. |
| `high_level_goal` | string | The original, verbatim user request. This field is **immutable**. |
| `critical_context` | object | A structured object containing key constraints extracted during the initial planning phase. This field is **immutable**. |
| `parent_task_id` | string \| null | The `task_id` of the parent task, if this is a sub-task. `null` for the top-level task. |
| `current_subtask_goal` | string | A concise description of the specific objective for the *current* sub-task being executed. |

#### 3.2.1 `critical_context` Field Specification

The `critical_context` object must contain, at a minimum, the following sub-fields:

- `files`: A list of specific file paths mentioned.
- `tools`: A list of specific skills or shell commands mentioned.
- `methodology`: A description of any specific methods or formats requested (e.g., "create a markdown table", "use a step-by-step approach").
- `focus`: A list of key subjects, keywords, or entities to prioritize (e.g., "focus on 'login failures'").

### 3.3 TCO Propagation Mechanism

- When the Orchestrator decomposes a parent task into sub-tasks, it MUST pass a copy of the parent's TCO to each child sub-task.
- For each sub-task, the `parent_task_id` is set to the parent's `task_id`, and a new, unique `task_id` is generated.
- The `current_subtask_goal` is updated to reflect the specific purpose of that sub-task.
- The `high_level_goal` and `critical_context` fields are passed down **without modification**.

## 4.0 Agent Responsibility

Any agent executing a sub-task MUST use the received TCO to inform its execution plan. The agent's logic must prioritize alignment with the `high_level_goal` and `critical_context` over optimizing for the `current_subtask_goal` in isolation.

**Verification Question for Agents:** "Does my plan for this sub-task directly contribute to the `high_level_goal` and respect all constraints within the `critical_context`?"

## 5.0 Example of Compliant vs. Non-Compliant Propagation

**High-Level Goal:** "Review `/var/log/app.log`, find all errors related to 'database connection', and create a KI summarizing them."

### Non-Compliant Execution (Context is Lost)

1.  **Task 1:** Read `/var/log/app.log`.
    - *Problem:* The agent only knows its goal is to "read a file." It has no knowledge of *why* it's reading the file.
2.  **Task 2:** Find error lines in the log content.
    - *Problem:* The agent doesn't know to focus on 'database connection' and may return all errors, leading to incorrect final output.
3.  **Task 3:** Create a KI from the error lines.
    - *Problem:* The KI will be a generic summary of all errors, failing the user's specific request.

### Compliant Execution (Using TCO Propagation)

**Initial TCO Created:**
```json
{
  "task_id": "task_789",
  "high_level_goal": "Review /var/log/app.log, find all errors related to 'database connection', and create a KI summarizing them.",
  "critical_context": {
    "files": ["/var/log/app.log"],
    "tools": ["create_ki"],
    "methodology": "summarize",
    "focus": ["database connection"]
  },
  "parent_task_id": null,
  "current_subtask_goal": "Decompose high-level goal into executable steps."
}
```

**Sub-task 1: Read the log file**
- **Orchestrator Action:** A new TCO is passed to the executing agent.
- **TCO for Sub-task 1:**
  ```json
  {
    "task_id": "subtask_A",
    "high_level_goal": "...", // (immutable)
    "critical_context": { ... }, // (immutable)
    "parent_task_id": "task_789",
    "current_subtask_goal": "Read the content of the file specified in critical_context.files[0] to prepare for error analysis."
  }
  ```
- **Agent Action:** The agent reads `/var/log/app.log`. It understands this is the first step towards summarizing database errors.

**Sub-task 2: Filter for specific errors**
- **TCO for Sub-task 2:**
  ```json
  {
    "task_id": "subtask_B",
    "high_level_goal": "...", // (immutable)
    "critical_context": { ... }, // (immutable)
    "parent_task_id": "task_789",
    "current_subtask_goal": "Filter the log content to isolate lines containing the keywords from critical_context.focus."
  }
  ```
- **Agent Action:** The agent specifically searches for lines containing "database connection", ignoring other errors, perfectly aligning with the high-level goal.

This specification provides the formal framework required to implement the GEPA proposal, ensuring robust and context-aware task execution across the AROS swarm.
