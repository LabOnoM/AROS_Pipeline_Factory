---
name: finalization-prerequisite-check
description: A mandatory logical gate to verify that all critical prerequisites (like successful GTB validation) have been met before committing a resource to the filesystem or notifying a user.
license: MIT
skill-author: AROS_code_generator
version: 1.0
---

# Finalization Prerequisite Check

This skill acts as a critical safety and quality gate in AROS workflows. It programmatically enforces the policy that certain prerequisites MUST be met before a state-modifying action (like writing a file or sending a notification) can be executed. It is a key component of the "Error Prevention Rule".

## When to Use

- **ALWAYS** use this skill immediately before any workflow step that writes a Skill, KI, or Policy to the filesystem.
- **ALWAYS** use this skill before a notification is sent regarding the completion of a content generation task.

This skill should be the **last check** before the final action.

## Core Principle: Validate Before You Finalize

The primary purpose of this skill is to prevent the execution of `write_local_file` or user notifications if the preceding validation steps have not passed. It provides a clear, enforceable logical gate that halts a workflow if quality or safety criteria are not met.

## Workflow

1.  **Generate Content**: A workflow generates a new KI, Skill, etc., and saves it to a temporary file (e.g., `/tmp/draft.md`).
2.  **Run Validation**: The workflow runs the appropriate validator (e.g., `gtb-validator`) on the temporary file. The JSON output of the validator is captured.
3.  **Invoke Prerequisite Check**: The workflow calls this skill, passing the validation result and any other required checks.
4.  **Gatekeeper Logic**:
    - If all checks pass, the script exits silently with code 0. The workflow is now authorized to proceed with its final step (e.g., moving the draft from `/tmp/` to its permanent location).
    - If any check fails, the script prints an error to stderr and exits with code 1. This non-zero exit code MUST be used to halt the workflow immediately, preventing the invalid content from being saved or acted upon.

## Available Checks

The `--checks` argument accepts a list of one or more of the following:

-   `gtb_validation`: Checks the result of a `gtb-validator` run. Requires the `--validation-passed` argument.
-   `user_auth`: Checks if the user is authenticated. Requires the `--user-auth` argument.
-   `file_exists`: Checks if a file exists at a given path. Requires the `--filepath` argument.
-   `file_not_empty`: Checks if a file at a given path is not empty. Requires the `--filepath` argument.

## Audit-Ready Commands

These commands demonstrate how to use the check.

```bash
# Simulate a successful validation
# The script will exit with code 0, allowing the workflow to continue.
python ~/.gemini/skills/finalization-prerequisite-check/scripts/main.py --checks gtb_validation --validation-passed true

# Simulate a failed validation
# The script will print an error to stderr and exit with code 1, halting the workflow.
python ~/.gemini/skills/finalization-prerequisite-check/scripts/main.py --checks gtb_validation --validation-passed false

# Check if a file exists and is not empty
touch /tmp/test_file.txt
python ~/.gemini/skills/finalization-prerequisite-check/scripts/main.py --checks file_exists file_not_empty --filepath /tmp/test_file.txt
# This will fail because the file is empty.

# Check multiple prerequisites at once
python ~/.gemini/skills/finalization-prerequisite-check/scripts/main.py --checks gtb_validation user_auth --validation-passed true --user-auth false
# This will fail because user_auth is false.
```
