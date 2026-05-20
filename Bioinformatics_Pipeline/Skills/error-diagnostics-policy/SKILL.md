---
name: error-diagnostics-policy
description: A policy that establishes the standard for generating and reporting detailed error diagnostics upon task failure.
license: MIT
skill-author: AROS-Mutation-Sweeper
version: 1.0
original-source: addyosmani/agent-skills/debugging-and-error-recovery
---

# Policy: Error Diagnostics

**Version:** 1.0
**ID:** AROS-POLICY-EDP-V1.0

---

## 1. Preamble

This document establishes the mandatory error reporting standards for all tasks within the Antigravity Research OS (AROS). Clear, detailed, and accessible error diagnostics are critical for the self-correction, robustness, and overall efficiency of the system. This policy ensures that failures are not just reported, but are made understandable and actionable.

## 2. Core Principle

When any task, tool, or process fails, the resulting error message must be sufficient to diagnose the root cause without requiring a full re-run or deep inspection of the source code. The goal is to make failures transparent and to provide enough context for an immediate and intelligent corrective action.

## 3. GEPA Error Prevention Rule: Comprehensive Diagnostics on Failure

To prevent recurring errors and to facilitate rapid recovery, this rule mandates the generation of rich, contextual error messages.

*   **Rule Rationale:** Task failures with vague or minimal error messages (e.g., "An error occurred," "Task failed") create ambiguity and lead to inefficient recovery loops. By enforcing detailed diagnostics, the system can more effectively apply self-correction policies or provide human operators with the necessary information to resolve the issue.

*   **Mandatory Action:** **Upon any task failure, detailed and diagnostic error messages, including relevant context or partial outputs, must be generated and made accessible.**

### 3.1. Implementation Guidelines

To comply with this rule, error reports MUST include:

*   **Clear Error Statement:** A human-readable message stating what failed.
*   **Original Goal/Command:** The specific action that was being attempted.
*   **Exit Codes:** Any numerical exit codes from failed shell commands.
*   **Standard Streams:** The complete `stdout` and `stderr` from the process.
*   **Partial Output:** If the task was generating content (e.g., a file, a data structure), the partial or incomplete output should be saved and its location referenced in the error message. This provides crucial context for debugging.
*   **Stack Traces:** For code-related failures, the full stack trace is mandatory.

## 4. Validation

Compliance with this policy is validated by inspecting the error report generated upon a task failure. A compliant report will contain all the elements listed in section 3.1. Automated auditors and peer-review agents MUST use these guidelines as a checklist when evaluating task failures.

*   **A "double failure" occurs if a task fails and its resulting error report does not comply with this policy.** Such an event should be treated with higher severity, as it represents a failure of the system's self-diagnostic capabilities.

## 5. Example

### 5.1. Non-Compliant Error Report (FAIL)

```json
{
  "error": "Task failed",
  "details": "An error occurred while processing the data."
}
```
**Reasoning for Failure:** This report is vague and unactionable. It lacks the original command, exit codes, standard streams, and any partial output that could be used for debugging.

### 5.2. Compliant Error Report (PASS)

```json
{
  "error": "Failed to compile the 'gravity-model' component.",
  "original_command": "python compile.py --model 'gravity-model'",
  "exit_code": 1,
  "stdout": "Starting compilation... Loading model assets...",
  "stderr": "Traceback (most recent call last):\n  File \"compile.py\", line 113, in <module>\n    main()\n  File \"compile.py\", line 98, in main\n    raise ValueError(\"Incompatible tensor dimensions\")\nValueError: Incompatible tensor dimensions",
  "partial_output_path": "/home/owner03/.gemini/antigravity/agent_sandbox/8ba2527e-2ca7-4506-aff0-96655a3a586a/logs/gravity-model-partial-build.log"
}
```
**Reasoning for Success:** This report is comprehensive. It clearly states the error, includes the exact command that failed, provides the exit code, captures both standard streams, and points to a log with the partial output, enabling efficient debugging.


## Debugging Checklist & Flowchart (Merged from Osmani)

**Triage Checklist:**
1. Reproduce -> 2. Isolate -> 3. Root Cause -> 4. Fix -> 5. Guard -> 6. Resume

**Stop-the-line Rule:** If you are guessing, stop. Formulate a hypothesis and test it before making widespread changes.
