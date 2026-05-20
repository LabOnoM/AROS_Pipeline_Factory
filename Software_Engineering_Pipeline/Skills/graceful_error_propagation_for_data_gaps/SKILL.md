---
name: graceful_error_propagation_for_data_gaps
description: A policy skill that defines how to gracefully handle task failures caused by missing critical input data, preventing downstream error cascades.
license: MIT
skill-author: AROS_code_generator
version: 1.0
---

# Policy: Graceful Error Propagation for Data Gaps

## 1. Preamble

This policy is a critical component of the AROS workflow management system. It provides a specific, mandatory protocol for handling task failures that are explicitly caused by the absence of critical input data, especially after proactive acquisition attempts (governed by the `missing_data_acquisition_mechanism` and `missing-input-handling-and-improvisation` skills) have failed.

## 2. Core Principle

When a task fails with the specific error tag `ERR_MISSING_CRITICAL_INPUT`, the workflow engine **MUST** prevent the execution of all downstream tasks that depend on the output of the failed task. This avoids wasting system resources on tasks that are guaranteed to fail and provides clearer, more concise error reporting for the entire workflow.

## 3. GEPA Error Prevention Rule: The Domino-Stop Rule

This policy enacts the "Domino-Stop Rule" to prevent error cascades. A single, well-defined failure due to missing data must halt the entire dependent chain immediately. Propagating vague or generic errors consumes resources and obscures the root cause. By failing fast and failing specifically, the system can more effectively pinpoint the exact data gap that needs to be resolved.

## 4. Mandatory Workflow Engine Behavior

1.  **Task Failure with Specific Tag**: A task must first attempt to resolve missing data using proactive policies. If it still cannot proceed, it MUST exit with a machine-readable state or error tag: `FAILED_MISSING_DATA`.

2.  **Engine Interception**: The AROS scheduler/workflow engine **MUST** intercept this specific `FAILED_MISSING_DATA` state.

3.  **Identify Dependencies**: Upon interception, the engine **MUST** query the workflow's dependency graph to identify all direct and indirect downstream tasks that depend on the failed task.

4.  **Update Downstream Status**: The engine **MUST** transition the state of all identified downstream tasks to `SKIPPED`. A metadata note must be attached to each skipped task indicating the root cause (e.g., `reason: "Skipped due to upstream failure of task [failed_task_name] with error FAILED_MISSING_DATA"`).

5.  **Finalization**: The workflow will then proceed until it hits the `finalization_workflow_gate`, which will correctly prevent the saving of partial or incomplete results, as some of its antecedent steps will be in a `SKIPPED` or `FAILED` state.

## 5. Example Scenario

-   **Workflow**: `Task A` -> `Task B` -> `Task C`
-   **Execution**:
    1.  `Task A` runs but cannot find a critical input file.
    2.  `Task A` fails with state `FAILED_MISSING_DATA`.
    3.  The AROS engine intercepts this state.
    4.  The engine identifies `Task B` and `Task C` as downstream dependencies.
    5.  The engine sets the state of `Task B` to `SKIPPED`.
    6.  The engine sets the state of `Task C` to `SKIPPED`.
    7.  The workflow concludes, and reporting clearly indicates `Task A` failed and `B` and `C` were skipped as a direct result.
