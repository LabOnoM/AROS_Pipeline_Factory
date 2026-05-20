---
name: dependent-task-sequencing-policy
description: A NON-EXECUTABLE policy document that defines rules for task dependencies. To use, read this file for planning or edit it with file system tools.
skill-author: AROS-Core-Policy
version: 1.3
---

```IMPORTANT_NOTICE
================================================================================
           ATTENTION: THIS IS A CONFIGURATION FILE, NOT A TOOL
================================================================================

This document, `dependent-task-sequencing-policy`, is a declarative policy
guideline. It is NOT an executable program or a callable tool.

- DO NOT attempt to call or execute this skill.
- ANY attempt to call this skill as a function will result in a ToolNotFound error.

You can only interact with this document in two ways:
1. READ its contents to inform your planning logic.
2. WRITE to this file using a file system tool (e.g., `file.write`) to update the policy.
```

# Policy: Dependent Task Sequencing

## 1. Valid vs. Invalid Actions

To prevent execution failure, strictly adhere to the following interaction patterns.

### ✅ Valid Actions

*   **To understand the policy:** Read this document's contents.
    *   **Correct Thought Process:** "I need to create a plan with two steps. I will read `dependent-task-sequencing-policy` to make sure I order them correctly."
*   **To modify the policy:** Use a file system tool to overwrite this file.
    *   **Correct Tool Usage:** `file.write(path="path/to/dependent-task-sequencing-policy.md", content="New policy text...")`

### ❌ Invalid Actions

*   **DO NOT** call this skill as a function. It will always fail.
    *   **Incorrect Tool Usage:** `dependent-task-sequencing-policy(update="New rule...")` -> **GUARANTEED FAILURE**
    *   **Incorrect Tool Usage:** `dependent-task-sequencing-policy(validate="workflow")` -> **GUARANTEED FAILURE**

## 2. Common Failure Mode and Correction

A frequent error is attempting to call this skill to implement an update, as seen in a past failure (`Run ID: f4dd8b66...`).

*   **Failed Goal:** "Add an error prevention rule to the 'Dependent Task Sequencing' policy."
*   **Incorrect Action Taken:** The agent tried to use `dependent-task-sequencing-policy` as a tool in its `implement_policy_update` step.
*   **Root Cause:** The agent incorrectly assumed a "skill" must be an executable tool.
*   **Required Correction:** The agent should have used `file.read` to get the current content, modified the text, and then used `file.write` to save the updated policy.

## 3. Tool Schema: NOT APPLICABLE

This skill **DOES NOT** expose a callable tool interface. It has no functions, arguments, or entry points.

---

## 4. Core Policy Principle

A "consumer" task (a task that depends on the output of another task) **MUST NOT** begin execution until the "producer" task (the task it depends on) has successfully completed and its output has been validated and registered in the system.

This is a zero-tolerance policy. Bypassing this sequencing will result in immediate workflow termination and a policy violation error.

## 5. Enforcement Mechanism

The AROS scheduler and workflow engine are responsible for enforcing this policy automatically.

1.  **Dependency Declaration:** Workflows must explicitly declare dependencies between tasks.
2.  **Producer State Check:** Before scheduling a consumer task, the engine **MUST** verify the state of the producer task. The required state is `COMPLETED_SUCCESS`.
3.  **Output Artifact Verification:** The engine **MUST** confirm that the expected output artifact from the producer task exists and is accessible before starting the consumer task.
4.  **Execution Lock:** The consumer task will remain in a `WAITING` state until all its producer dependencies are met.

## 6. Example Scenario

Consider a workflow for generating a report from a dataset.

*   **Task A (Producer):** `data_extraction.py` - Extracts raw data from a database and saves it to `raw_data.csv`.
*   **Task B (Consumer):** `report_generator.py` - Reads `raw_data.csv`, analyzes it, and produces `report.pdf`.

### Correct Execution Sequence (Policy Adhered)
1.  Scheduler initiates **Task A**.
2.  **Task A** runs and successfully produces `raw_data.csv`.
3.  **Task A** is marked as `COMPLETED_SUCCESS`.
4.  Scheduler verifies that **Task A** is complete and `raw_data.csv` exists.
5.  Scheduler initiates **Task B**. **Task B** finds its input file and runs correctly.
6.  Workflow completes successfully.

### Incorrect Execution Sequence (Policy Violation)
1.  Scheduler initiates **Task B** before **Task A** is complete.
2.  **Task B** immediately fails because its input, `raw_data.csv`, does not exist.
3.  The workflow is terminated, and a policy violation is logged.