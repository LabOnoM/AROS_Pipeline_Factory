---
name: verification-result-reporting
description: "A mandatory policy for evaluating and reporting the outcomes of verification commands, ensuring all testing and validation steps produce a definitive, actionable result."
license: MIT
skill-author: AROS-Core
---

# Policy: Verification Result Reporting

This policy enforces the GEPA proposal that all verification, validation, or testing commands MUST be followed by a structured evaluation and a definitive report. This ensures that outcomes are never ambiguous and that subsequent actions are based on clear, evidence-backed results.

## Core Principles

1.  **No Silent Failures**: The output of any validation command must be explicitly checked. An absence of an error is not sufficient proof of success.
2.  **Binary Outcome**: Every verification step must conclude with a definitive `SUCCESS` or `FAILURE` state.
3.  **Evidence-Based Reporting**: The reported outcome must be directly supported by evidence captured from the command's output (`stdout`, `stderr`, exit code).
4.  **Actionable Feedback**: In case of failure, the report must include specific reasons to guide the necessary corrective actions (e.g., refinement, escalation).

## MANDATORY SKILL INSTRUCTIONS:

Any agent executing a command for the purpose of verification (e.g., running a linter, a test suite, or the `gtb-validator`) **MUST** perform the following sequence:

### 1. Execute and Capture

- **Execute** the verification command.
- **Capture** the entire `stdout`, `stderr`, and the exit code of the process. Do not proceed without this information.

### 2. Evaluate against Criteria

- **Analyze** the captured output to determine the outcome. The success criteria must be explicit and relevant to the command.
- **Examples of Criteria:**
    - For `gtb-validator`: `stdout` must be valid JSON containing `"passed": true`.
    - For a compiler or linter: The process must have an `exit code` of `0` and `stderr` must be empty.
    - For a data validation script: `stdout` must contain the string `"Validation Succeeded"`.

### 3. Generate a Definitive Report

- Following evaluation, the agent **MUST** generate an internal report in its logs or monologue before taking the next action. This report is crucial for traceability and debugging.
- The report **MUST** follow this structure:

```yaml
VerificationReport:
  VerificationStep: "Golden Test Battery (GTB) Validation"
  CommandExecuted: "python /home/owner03/.gemini/skills/gtb-validator/validate.py /tmp/draft.md knowledge_retrieval"
  Outcome: SUCCESS # SUCCESS or FAILURE
  Evidence: "Validator output contained '\"passed\": true'."
  NextAction: "Writing temporary file to the permanent knowledge base at ~/.gemini/antigravity/knowledge/new-policy.md"
```

### Example Failure Report

```yaml
VerificationReport:
  VerificationStep: "Python Syntax Check"
  CommandExecuted: "python -m py_compile /tmp/new_script.py"
  Outcome: FAILURE
  Evidence: "Process exited with code 1. Stderr: 'SyntaxError: invalid syntax on line 42'"
  NextAction: "Re-drafting the script to correct the reported syntax error."
```

## Integration

This policy is a foundational component of the `content-drafting-capability` and the `ki-quality-assurance-policy`. It provides the explicit reporting mechanism required to fulfill their validation loops. All agents must adhere to this reporting standard to ensure the integrity of the AROS ecosystem.
