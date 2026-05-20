---
name: antecedent_task_output_validation_policy
description: A policy mandating that consumer tasks validate the integrity, completeness, and non-placeholder status of outputs from producer tasks.
license: MIT
skill-author: AROS_code_generator
---

# Policy: Antecedent Task Output Validation

## 1. GEPA Rule

This policy codifies a new Global Evolution & Policy Architecture (GEPA) rule: **"All consumer tasks MUST perform an initial validation step to confirm the integrity, completeness, and non-placeholder status of critical outputs from their antecedent producer tasks before beginning their own core logic."**

## 2. Core Principle

This policy prevents error cascades and preserves data integrity within multi-step workflows. A "consumer" task (e.g., `save_file`) that depends on the output of a "producer" task (e.g., `rewrite_content`) must not blindly trust the producer's output. Even if the producer task completes without throwing an error, its output may be incomplete, empty, or contain placeholder values. This "distrustful" check at each handoff point ensures that downstream tasks do not operate on invalid data.

This policy works in concert with, but is distinct from, `dependent-task-sequencing-policy`. While that policy ensures a producer task is marked `COMPLETED_SUCCESS` before a consumer starts, this policy requires the consumer to inspect the *actual artifact* produced.

## 3. Mandatory Procedure

Before executing its core logic, any task that consumes the output of a preceding task MUST perform the following checks on that output:

1.  **Integrity Check:** Verify that the output is not corrupt and is in the expected format (e.g., the file exists and is readable, JSON is parsable, etc.).
2.  **Completeness Check:** Verify that the output is not empty or trivially small. It should meet a minimum size threshold and contain expected data structures.
3.  **Placeholder Check:** Scan the output for common placeholder strings that indicate incomplete work (e.g., "TBD", "TODO", "FIXME", "To be supplemented", "Not provided"). The presence of such placeholders MUST be treated as a validation failure.

## 4. Execution Logic

-   **On Success:** If all validation checks pass, the consumer task is authorized to proceed with its core functions.
-   **On Failure:** If any check fails, the consumer task MUST immediately HALT. It should report a specific error detailing which check failed (e.g., "Validation failed: Antecedent task output contains placeholder 'TBD'.") and terminate the current workflow to prevent the propagation of erroneous data.

## 5. Example Application

**Workflow: `validate_rewrite_save_notify`**

1.  **Producer Task (`rewrite_content`):** An agent rewrites a file, `draft.md`. It completes successfully.
2.  **Consumer Task (`save_file`):** This task is intended to save `draft.md` to a permanent location.
    -   **BEFORE saving**, it applies this policy.
    -   It reads `draft.md` and checks if it's empty (Completeness).
    -   It scans `draft.md` for "TODO" (Placeholder).
    -   **Scenario A (Pass):** The file is not empty and has no placeholders. The `save_file` task proceeds to save the file.
    -   **Scenario B (Fail):** The file contains "TODO". The `save_file` task halts, logs a policy violation, and the workflow terminates, preventing the incomplete file from being saved.