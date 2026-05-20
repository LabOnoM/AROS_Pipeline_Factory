---
name: finalization_workflow_gate
description: SKILL: finalization_workflow_gate
---

# SKILL: finalization_workflow_gate
---
name: finalization_workflow_gate
description: A mandatory policy and tool that gates the finalization steps of a workflow (e.g., saving artifacts, notifying users) until all critical preceding validation steps have successfully completed. This skill provides the central implementation for the GEPA Error Prevention Rule.
license: MIT
skill-author: AROS-Core
version: 2.0
---

# Policy: Finalization Workflow Gate (v2.0)

## 1. Core Principle: Validate Before You Finalize

This policy establishes a non-negotiable quality gate for all AROS workflows. The finalization actions of a workflow—such as writing an artifact to the filesystem (`write_local_file`), committing to a database, or notifying a user of completion—**MUST** be gated behind the successful, explicit, and verifiable completion of all critical antecedent steps, especially validation.

This skill provides the official tool for enforcing this policy and is a cornerstone of the GEPA (Genetic Evolution and Policy Adaptation) error prevention strategy. It prevents the system from saving partial, corrupt, or unvalidated results and ensures that downstream processes are not triggered by failed or incomplete tasks.

**This skill supersedes and consolidates the logic previously found in `finalization-prerequisite-check` and `user_notification_policy`. Those skills are now considered deprecated in favor of this unified implementation.**

## 2. Mandatory Procedure

All multi-step workflows that generate or modify artifacts MUST follow this precise sequence:

1.  **Generate Content:** The workflow executes its primary task, generating content, code, or data. The boolean outcome (`true`/`false`) of this step's success must be captured.

2.  **Run Validation:** The workflow **MUST** run all applicable validation steps on the generated artifact. This includes, but is not limited to:
    *   **GTB Validation:** Running the `gtb-validator` for any new Skill, KI, or Policy.
    *   **Unit/Smoke Tests:** Executing tests for any generated code.
    *   **Data Integrity Checks:** Verifying the correctness and completeness of data artifacts.
    The boolean outcome (`true`/`false`) of each validation step must also be captured.

3.  **Apply the Gate:** Before the finalization step, the workflow **MUST** invoke the `gate.py` tool provided by this skill. The captured outcomes from the preceding steps are passed as command-line arguments.

4.  **Conditional Finalization:** The workflow **MUST** check the exit code of the `gate.py` script.
    *   If the script exits with code `0`, the gate has passed, and the workflow is authorized to proceed with finalization (e.g., writing the file to its permanent location, sending a notification).
    *   If the script exits with a non-zero code, the gate has failed. The workflow **MUST** terminate immediately, clean up any temporary files, and report the failure. Bypassing a failed gate is a critical policy violation.

## 3. Tool: `gate.py`

The core logic is implemented in `scripts/gate.py`.

### Usage

```bash
python ~/.gemini/skills/finalization_workflow_gate/scripts/gate.py \
    --content-drafting-status <'true'|'false'> \
    --validation-status <'true'|'false'>
```

### Arguments

*   `--content-drafting-status` (Required): The success status of the content drafting/generation step.
*   `--validation-status` (Required): The success status of the validation step (e.g., from `gtb-validator`).

### Exit Codes

*   `0`: Success. All gates passed.
*   `1`: Failure. One or more critical steps failed.

### Audit-Ready Commands

These commands demonstrate the tool's functionality and can be used for compliance checks.

```bash
# SCENARIO 1: Success - Both drafting and validation passed.
# EXPECTED: Exit code 0. Workflow proceeds.
echo "Running success scenario..."
python ~/.gemini/skills/finalization_workflow_gate/scripts/gate.py --content-drafting-status true --validation-status true
echo "Exit code: $?" # Should be 0

# SCENARIO 2: Failure - Drafting passed, but validation failed.
# EXPECTED: Exit code 1. Workflow halts.
echo -e "\nRunning validation failure scenario..."
python ~/.gemini/skills/finalization_workflow_gate/scripts/gate.py --content-drafting-status true --validation-status false || true
echo "Exit code: $?" # Should be 1

# SCENARIO 3: Failure - Drafting failed.
# EXPECTED: Exit code 1. Workflow halts.
echo -e "\nRunning drafting failure scenario..."
python ~/.gemini/skills/finalization_workflow_gate/scripts/gate.py --content-drafting-status false --validation-status false || true
echo "Exit code: $?" # Should be 1
```
