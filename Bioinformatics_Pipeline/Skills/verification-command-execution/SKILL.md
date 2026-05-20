---
name: verification-command-execution
description: A policy that mandates the direct execution of verification commands with a structured retry-and-fallback mechanism to ensure the correctness and functionality of generated artifacts.
license: MIT
skill-author: AROS
---

# Verification Command Execution Policy

## 1. Preamble

This policy governs the finalization steps for any task that results in the creation or modification of an artifact (e.g., code, scripts, configuration files). Its primary goal is to ensure that all generated artifacts are validated and functional through direct, real-world execution of commands before a task is considered complete.

## 2. When to Use

- **ALWAYS** use this policy after generating or modifying any artifact.
- This is a mandatory, non-negotiable step to be performed before reporting task completion.

## 3. GEPA Error Prevention Rule: Mandatory Verification

This section codifies the mandatory verification process as a GEPA (Golden-set Evolution and Proliferation Algorithm) error prevention rule.

### 3.1. The Rule

The agent **MUST** execute all proposed verification commands to confirm the existence, correctness, and functionality of generated artifacts. This includes, but is not limited to:
-   Checking for file existence (`ls`, `test -f`).
-   Validating syntax and structure (linters, compilers, `jq`, `yaml.safe_load`).
-   Executing the artifact to test its functionality (running scripts, starting services).
-   Running unit tests or other automated checks.

### 3.2. Rationale

This rule is critical for preventing errors of omission where an agent generates a solution but fails to test it. By explicitly running verification commands, the agent creates a tight feedback loop, allowing it to catch and remediate issues immediately. This prevents the propagation of flawed artifacts and ensures that the final output is robust, reliable, and correct. Failure to verify is a direct violation of the core principle of quality assurance.

### 3.3. Procedure

1.  **Generate Artifact:** Create or modify the file(s) as required by the task.
2.  **Propose Verification Commands:** Before execution, explicitly state the sequence of commands that will be used to validate the artifact. This makes the verification plan clear.
3.  **Execute and Analyze:** Run each proposed command sequentially. Carefully analyze the output (stdout, stderr) and the exit code of each command.
4.  **Remediate or Conclude:**
    *   **On Success:** If all verification commands execute successfully, the agent is authorized to conclude the task.
    *   **On Failure:** If any command fails or produces unexpected output, the agent MUST initiate a structured retry and fallback procedure. This procedure replaces an indefinite loop with a bounded, resilient process:
        1.  **Diagnose and Retry:** The agent must diagnose the likely cause of the failure and attempt to remediate it. It may retry the verification command up to a maximum of **two (2) 

