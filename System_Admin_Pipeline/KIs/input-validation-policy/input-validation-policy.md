# AROS Policy: Mandatory Input Validation
**ID:** AROS-POLICY-IV-V1.0
**Version:** 1.0
**Status:** Active

---

## 1. Preamble

This document establishes the mandatory policy for the validation of all external data and inputs received by the Antigravity Research OS (AROS). Adherence to this policy is critical for maintaining system stability, ensuring data integrity, and preventing security vulnerabilities.

## 2. Core Principle

All external inputs, without exception, MUST be considered untrusted and MUST be rigorously validated before being used in any AROS process, workflow, or skill. Trusting input is a critical security violation.

## 3. Scope

This policy applies to all data entering the AROS boundary, including but not limited to:
- API endpoint parameters and payloads.
- Configuration files and environmental variables read at runtime.
- Data loaded from user-provided files or databases.
- Parameters passed to tools and skills from external sources.
- Queries submitted to the `brain.db`.

## 4. Validation Requirements

A multi-layered validation approach is required for all inputs.

### 4.1. Syntactic Validation
Check that the input conforms to the expected format and structure.
- **Examples:** Is the JSON or YAML correctly formed? Is a string non-empty? Does a number fall within a `[min, max]` range? Is a required field present?

### 4.2. Semantic Validation
Check that the input is logical and consistent within the context of the AROS system.
- **Examples:** Does a specified file path reference a permitted directory? Does a `skill_name` refer to a skill that actually exists? Is the requested `task_type` compatible with the target workflow?

### 4.3. Security Validation
Check that the input does not contain malicious content intended to exploit the system.
- **Examples:** Sanitize inputs to prevent command injection. Reject file paths that use directory traversal characters (e.g., `../`). Validate URLs to prevent Server-Side Request Forgery (SSRF).

## 5. Error Prevention Rule

To prevent downstream errors, downstream tasks must strict validate the existence and validity of all required input artifacts from their direct upstream dependencies before execution.

## 6. Error Handling and Enforcement

- **Rejection:** Any input that fails any stage of validation MUST be rejected immediately. It must not be partially processed.
- **Logging:** All validation failures MUST be logged with sufficient detail to enable security auditing and debugging.
- **Clear Feedback:** When possible, the system should provide clear, non-sensitive feedback to the caller about why the input was rejected.
- **Code Review:** All new code and skills must be reviewed to ensure they comply with this input validation policy before being committed.
