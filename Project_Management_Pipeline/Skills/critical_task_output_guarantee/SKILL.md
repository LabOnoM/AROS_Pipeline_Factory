---
name: critical_task_output_guarantee
description: A Python implementation of the GEPA error prevention rule for tracking sub-task retries, distinguishing between fatal and intermediate failures, and triggering dynamic fallbacks.
license: MIT
skill-author: AROS_code_generator
---

# GEPA Error Prevention Rule: Codebase Patch

This component provides a Python implementation of the error prevention rule mandated by the AROS system. The core logic tracks retry counts for any given sub-task, dynamically triggers a fallback state when a failure threshold is reached, and strictly enforces the critical task output guarantee.

## Key Capabilities
- **Retry Tracking**: Monitors the number of consecutive failures for unique sub-tasks.
- **Configurable Threshold**: The number of retries before fallback is triggered can be configured (defaults to 2).
- **Dynamic Fallback Mechanism**:
    - **Alternative Skill**: If a fallback skill is specified, the system will attempt to execute it.
    - **Model Escalation**: If no alternative skill is available, the system will escalate to a 'larger model persona' for more complex reasoning.
- **Critical Task Handling**: Distinguishes between fatal and intermediate failures. Tasks marked as critical will halt the workflow immediately upon failure, preventing masked errors and infinite loops.

## Core Component: `SubTaskExecutionManager`

The logic is encapsulated in the `SubTaskExecutionManager` class within the `gepa_error_prevention_patch.py` script.

### Workflow
1.  **Instantiate Manager**: An instance of the manager is created, defining the retry threshold.
2.  **Execute Task**: The `execute_task` method is called with a unique `task_id`, the function to execute, an optional `fallback_skill`, and an `is_critical` boolean flag.
3.  **Attempt Execution**: The manager calls the task function.
4.  **On Success**: If the task returns `True`, the retry count for that `task_id` is reset, and the process completes.
5.  **On Critical Failure**: If `is_critical=True` or the task raises a `FatalError`, the workflow immediately halts and raises a `FatalError`.
6.  **On Intermediate Failure**: If the task returns `False` or raises a non-fatal exception, the retry count is incremented.
7.  **Check Threshold**: If the retry count is less than the threshold, the task is attempted again.
8.  **Trigger Fallback**: Once the retry count reaches the threshold, the manager triggers the fallback logic:
    - If a `fallback_skill` was provided, a message is logged to execute it.
    - Otherwise, a message is logged to escalate to a larger model persona.

## Audit-Ready Command

This command demonstrates the functionality of the patch by running a simulation of various task failure scenarios.

```bash
python ~/.gemini/skills/gepa_error_prevention_patch/gepa_error_prevention_patch.py
```
