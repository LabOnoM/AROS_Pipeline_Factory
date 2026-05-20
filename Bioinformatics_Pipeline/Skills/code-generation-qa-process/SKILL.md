---
name: code-generation-qa-process
description: Policy: Code Generation Quality Assurance
original-source: addyosmani/agent-skills/code-review-and-quality
---

# Policy: Code Generation Quality Assurance

**Version:** 1.2
**ID:** AROS-POLICY-CG-QA-V1.2

---

## 1. Preamble

This document outlines the mandatory quality assurance (QA) process for all code generation tasks performed within the Antigravity Research OS (AROS). Adherence to this policy is critical for maintaining system stability, preventing regressions, and ensuring that all generated code is robust, secure, and fit for purpose.

## 2. GEPA Rule: Multi-Stage Verification

To enforce the highest standards of quality, the following GEPA rule is now in effect:

**GEPA-Rule-CG-QA-001: Implement a multi-stage verification process (generation, QA, review) for all code outputs.**

All code generation tasks MUST implement this multi-stage verification process. No code may be considered 'complete' or committed to a production-like environment until it has successfully passed all three stages.

## 3. The Multi-Stage Verification Process

This workflow is mandatory for any agent or process that generates executable code, scripts, or configuration files.

### 3.1. Stage 1: Generation

The agent generates the initial code based on the user's request, source data, and relevant skills. The primary focus of this stage is to create functionally correct code that meets the specified requirements.

### 3.2. Stage 2: Automated QA & Refinement

This stage is a **non-negotiable** automated validation and refinement gate, executed by the `iterative-validator` skill. The agent responsible for generation MUST subject the code to this process before proceeding.

*   **A. Linting and Static Analysis:**
    *   **Action:** The code MUST be checked for stylistic errors, bugs, and suspicious constructs using standard linters (e.g., `pylint`, `flake8` for Python; `shellcheck` for shell scripts). This is typically part of the `gtb-validator`'s task-specific checks.
    *   **Success Condition:** The code must pass linting with zero critical errors.

*   **B. Unit & Smoke Testing:**
    *   **Action:** In accordance with the `gtb-validator` policy, the generating agent MUST also write and execute unit tests that validate the core functionality of the code. A smoke test should also be performed to ensure the code runs without immediately crashing.
    *   **Success Condition:** All unit tests must pass. The smoke test must complete successfully.

*   **C. Automated Refinement Loop:**
    *   **Action:** If the automated checks fail, the `iterative-validator` skill will automatically attempt to fix the code based on the feedback from the validator, up to a maximum of two times.

### 3.3. Stage 3: Mandatory External Review

If the code fails to pass the Automated QA & Refinement stage, it must undergo a mandatory external review.

*   **A. Peer Agent Review (Default):**
    *   **Trigger:** This stage is automatically triggered by the `iterative-validator` skill if its automated correction attempts fail.
    *   **Process:** The `iterative-validator` requests a review from a separate, specialized QA agent. The QA agent's role is to check for logical errors, missed edge cases, and adherence to architectural principles that automated tests might miss.
    *   **Mechanism:** This review is programmatically invoked by the `iterative-validator` skill as part of its multi-tiered validation process. The validator uses the external feedback for one final attempt at correction. If this last attempt fails, the process is escalated for expert review.


## Five-Axis Review Framework (Merged from Osmani)

When reviewing code, evaluate against these five axes:
1. **Correctness:** Does the code do what it's supposed to do? Are edge cases handled?
2. **Readability:** Is the code easy to understand? Are names descriptive?
3. **Architecture:** Does the code fit into the overall system design?
4. **Security:** Are there vulnerabilities? (e.g., shell injection, unescaped inputs)
5. **Performance:** Are there bottlenecks? (e.g., N+1 queries, unoptimized loops)


## TDD Fix Plans & Interactive Reporting (Merged from Pocock)

- Ask the user to reproduce the bug in an interactive session if logs are insufficient.
- Write a failing test for the bug BEFORE changing the implementation code.
- Ensure the test passes after the fix is applied.
