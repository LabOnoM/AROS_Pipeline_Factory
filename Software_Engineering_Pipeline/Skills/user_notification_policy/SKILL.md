---
name: user_notification_policy
description: A policy that gates user notifications for task completion behind a mandatory validation check to ensure accuracy and prevent premature reporting.
license: MIT
skill-author: AROS_code_generator
---

# Policy: User Notification Gating

## 1. Preamble

This document outlines the mandatory policy for sending notifications to users regarding the completion of tasks. The purpose of this policy is to ensure that users are only notified when a task's core objective has been verifiably and completely fulfilled, preventing premature or inaccurate success notifications.

## 2. Core Principle

All user-facing notifications regarding the completion of a task **MUST** be gated behind a strict, explicit, and verifiable validation check. Notifications of success are prohibited until this validation check has passed and produced a tangible artifact of success.

## 3. Validation Workflow

Before any skill, workflow, or agent can trigger a user notification of task completion, it must perform the following steps:

1.  **Identify Core Objective:** Explicitly state the primary, verifiable goal of the user's request.
2.  **Define Success Artifact:** Determine what tangible output constitutes proof of completion (e.g., a generated file, a passing test result, a database record).
3.  **Execute Validation:** Perform a check that confirms the success artifact exists and is correct. This check must be an active, not a passive, confirmation.
4.  **Gate Notification:** Only upon the successful generation and verification of the success artifact may a notification be sent to the user.

## 4. GEPA Rules

### Rule 1: Mandatory Validation Artifacts

The validation mechanism must produce a verifiable artifact. Notifications cannot be based on the absence of an error message alone. Examples of acceptable validation artifacts include:

*   **Code Generation:** A passing test suite report (e.g., from `pytest`) that confirms the code runs and meets requirements.
*   **File Manipulation:** A hash (e.g., SHA256) of the final file or a directory listing showing the file's existence and correct size.
*   **Data Retrieval:** A count of the records returned or a sample of the data that matches the user's query.
*   **System Configuration:** A confirmation message from the system showing the new configuration has been successfully applied (e.g., output from a CLI tool).

### Rule 2: Prohibited Notifications

The following types of notifications are explicitly forbidden as substitutes for a validated success message:

*   **"Process Completed Without Errors":** A lack of errors does not guarantee the desired outcome was achieved.
*   **"Script Ran Successfully":** The script may have run, but its output could be incorrect or empty.
*   **"It looks like it worked":** Notifications must be based on certainty, not inference.

## 5. Examples

**Compliant Notification Flow:**

1.  **User Request:** "Please write a Python script to parse `data.csv` and save the results to `output.json`."
2.  **Agent Action:**
    *   Writes `script.py`.
    *   Executes `python script.py`.
    *   **Validation Step 1:** Checks if `output.json` exists.
    *   **Validation Step 2:** Opens `output.json` and verifies it contains valid JSON and the expected data structure.
3.  **Notification:** "I have successfully parsed `data.csv` and saved the results to `output.json`. The new file contains 150 records."

**Non-Compliant Notification Flow:**

1.  **User Request:** "Please write a Python script to parse `data.csv` and save the results to `output.json`."
2.  **Agent Action:**
    *   Writes `script.py`.
    *   Executes `python script.py`. The script exits with code 0.
3.  **Notification:** "I have run the script to process your data." (This is a policy violation, as it doesn't confirm the actual outcome).
