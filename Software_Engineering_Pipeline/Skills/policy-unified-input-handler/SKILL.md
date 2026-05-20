---
name: policy-unified-input-handler
description: A comprehensive, unified AROS policy for handling missing, incomplete, or invalid inputs. This policy establishes a clear hierarchy of actions to ensure robust, resilient, and transparent skill execution. It supersedes and harmonizes `policy-missing-input-handler`, `missing-input-handling-and-improvisation`, and `MissingInputClarificationSkill`.
license: Apache 2.0
skill-author: AROS Self-Correction Subsystem
status: active
policy-type: execution-guardrail
---

# Policy: Unified Input Handler

This policy establishes the mandatory, system-wide protocol for handling missing, incomplete, or invalid inputs. It provides a tiered approach that prioritizes safe and predictable execution while maintaining task momentum where possible.

## 1. Unified GEPA Rules

These rules define a clear order of operations for input handling.

-   **GEPA-Rule-UIH-01: Validate First, Execute Later**
    The absolute first step of any skill, before any other action, MUST be the validation of all required inputs for presence, type, and sufficiency.

-   **GEPA-Rule-UIH-02: Actively Acquire Missing Data**
    If validation fails due to missing data, the agent MUST first attempt to acquire it. Use internal knowledge sources (`brain.db`, KIs) for system data or prompt the user for user-specific context.

-   **GEPA-Rule-UIH-03: Improvise Low-Risk Inputs Transparently**
    For **non-critical**, missing inputs where a reasonable, conventional default exists (e.g., a port number), the agent MAY make an assumption. This assumption and its justification MUST be explicitly stated to the user *before* proceeding.

-   **GEPA-Rule-UIH-04: Halt on Critical Missing Input**
    If a **critical** input is missing or invalid and cannot be acquired, the agent MUST halt execution. It must clearly report the specific gap to the user and request the necessary information. Fabrication of critical data is strictly prohibited.

## 2. Definitions

-   **Critical Input:** An input without which the skill's core function cannot be performed, or its absence would lead to a high risk of error, resource waste, or security issues.
    -   *Examples: API keys, source file paths, database credentials, user ID.*

-   **Non-Critical Input:** An input that has a widely accepted, safe, and conventional default, or one that modifies the output in a minor way.
    -   *Examples: Output port number, a boolean flag with a sane default, a color theme.*

## 3. Mandatory Workflow

1.  **Validate Inputs:** Check all inputs against the `## Input Validation` section defined in the skill's `SKILL.md`.

2.  **On Validation Failure, Triage by Criticality:**
    -   **If the input is CRITICAL:**
        1.  Attempt to acquire the data via **GEPA-Rule-UIH-02**.
        2.  If acquisition succeeds, resume the workflow.
        3.  If acquisition fails, **Halt** execution per **GEPA-Rule-UIH-04**. State the missing input, why it's needed, and provide an example of correct usage.
    -   **If the input is NON-CRITICAL:**
        1.  Attempt to infer a reasonable, high-confidence default.
        2.  If a default exists, **Improvise** per **GEPA-Rule-UIH-03**. Announce the improvisation and proceed.
        3.  If no high-confidence default exists, treat it as critical and **Halt** per **GEPA-Rule-UIH-04**.

## 4. Examples

### Scenario 1: Critical Missing Input

-   **User Request:** "Run the data analyzer on my latest upload." (The `--input-file` is missing).
-   **Compliant Agent Behavior:** "Execution halted. To analyze the data, I need the path to the input file. Please provide it using the `--input-file` parameter. For example: `run_analyzer --input-file /path/to/data.csv`."
-   **Non-Compliant Behavior:** "Error: Missing input." (Not specific or actionable).
-   **Critical Failure (Violation):** The agent guesses a file from the user's home directory and proceeds, potentially processing the wrong data.

### Scenario 2: Non-Critical Missing Input

-   **User Request:** "Deploy the new Flask web app." (The `--port` is not specified).
-   **Compliant Agent Behavior:** "I will deploy the Flask web app. The `--port` was not specified. Based on convention, I will use the default port `5000`. **Improvisation:** Proceeding with port `5000`. You can specify a different port using the `--port` argument in the future."
-   **Non-Compliant Behavior:** The agent starts the server on a random port without informing the user.
-   **Overly Strict Behavior:** "Execution halted. Missing `--port` parameter." (Blocks momentum for a non-critical, easily inferable value).
