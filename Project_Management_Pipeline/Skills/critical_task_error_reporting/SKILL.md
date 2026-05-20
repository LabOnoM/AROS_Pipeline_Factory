---
name: critical_task_error_reporting
description: An advanced skill that intercepts failures in critical tasks to capture detailed error reports AND implements the GEPA error prevention rule by managing sub-task retries and triggering dynamic fallbacks.
license: MIT
skill-author: AROS_code_generator
---

# Critical Task Detailed Error Reporting with GEPA Prevention

This skill provides an advanced, decorator-based mechanism to wrap critical system tasks. It fuses two core AROS policies: detailed failure reporting and the GEPA error prevention rule for sub-task retries. When a wrapped task fails, this skill automatically attempts to retry the task up to a configurable threshold. If the task continues to fail, a rich, context-aware snapshot of the system state is captured, and a dynamic fallback is triggered.

## Key Capabilities
- **Failure Interception**: Uses a Python decorator (`@critical_task_handler`) to wrap functions and catch any exceptions they raise.
- **Retry Tracking (GEPA Rule)**: Implements the GEPA error prevention rule by monitoring and acting upon consecutive failures for unique tasks.
- **Configurable Threshold**: The number of retries before a task is considered failed can be configured directly in the decorator (e.g., `retry_threshold=3`). Defaults to 2.
- **Dynamic Fallback Mechanism**: On final failure, the system can trigger a specified alternative skill or escalate to a 'larger model persona' for more complex reasoning.
- **Rich Context Capture**: On final failure, it gathers a detailed report including the full traceback, local variables at the point of failure, and a snapshot of the system environment (OS, Python version, etc.).
- **Dedicated Logging**: Writes detailed error reports and retry attempts to a centralized log file (`~/.gemini/antigravity/logs/critical_errors.log`) for later analysis.

## Workflow
1.  **Decorator Application**: A developer or another agent applies the `@critical_task_handler` decorator from `~/.gemini/skills/critical_task_error_reporting/scripts/error_handler.py` to a function deemed critical.
2.  **Configuration**: The decorator is configured with a `retry_threshold` and an optional `fallback_skill` string. A unique `task_id` can also be passed to the decorated function's keyword arguments for precise tracking.
3.  **Task Execution**: The function is called as usual.
4.  **On Success**: If the task executes successfully, the process completes, and its retry counter is reset.
5.  **On Failure & Retry**: If the function raises an exception, the decorator catches it, logs the failed attempt, and increments the retry counter. If the count is below the threshold, the function is automatically executed again.
6.  **Final Failure & Reporting**: Once the retry count reaches the threshold, the full, detailed error report (traceback, state variables, environment) is generated and written to the critical error log.
7.  **Trigger Fallback**: After the report is logged, the fallback mechanism is triggered:
    - If a `fallback_skill` was provided, a message is logged to execute it.
    - Otherwise, a message is logged to escalate to a larger model persona.

## Audit-Ready Command

This command demonstrates the functionality of the patch by running a simulation of task failure and success scenarios.

```bash
python ~/.gemini/skills/critical_task_error_reporting/scripts/error_handler.py
```
