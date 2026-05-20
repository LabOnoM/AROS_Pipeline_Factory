---
name: diagnose_and_request_capabilities
description: diagnose_and_request_capabilities
---

# diagnose_and_request_capabilities

This is a meta-skill that provides a structured process for an agent to self-diagnose execution failures and request the necessary capabilities from the orchestrator. It embodies the GEPA (Goal-Execution-Prevention-Analysis) error prevention rule.

## When to Use

Use this skill immediately after a `run_shell_command` or any other tool execution fails unexpectedly. Instead of aborting the mission, use this skill to analyze the failure and request help.

## GEPA Error Prevention Rule

The core principle is to prevent recurring errors by clearly articulating the missing prerequisites for a given goal. When a command fails, do not simply report the failure. Instead, diagnose the root cause and request specific remediation.

## Workflow

1.  **Capture Execution Context:** When a command fails, capture the following information:
    *   **Original Goal:** What were you trying to achieve?
    *   **Command:** The exact command that was executed.
    *   **Exit Code:** The exit code from the command.
    *   **Stdout:** The standard output.
    *   **Stderr:** The standard error.

2.  **Diagnose the Root Cause:** Analyze the `stderr` and exit code to identify the type of error.

    *   **`command not found` (Exit Code 127):**
        *   **Diagnosis:** The required executable is not in the system's `PATH` or is not installed.
        *   **Remediation Request:** "Requesting installation of `<tool_name>`. Please make it available in the environment."

    *   **`Permission denied` (Exit Code 126):**
        *   **Diagnosis:** The agent does not have the necessary permissions to execute the file or access a resource.
        *   **Remediation Request:** "Requesting execute permissions for the file: `<file_path>`. Please run `chmod +x <file_path>`."

    *   **`ModuleNotFoundError` / `ImportError` (Python):**
        *   **Diagnosis:** A required Python library is not installed.
        *   **Action:** Check the `SKILL.md` of the failing skill for a `requirements.txt` or a list of dependencies.
        *   **Remediation Request:** "Requesting installation of Python package: `<package_name>`. Please run `pip install <package_name>`."

    *   **`FileNotFoundError`:**
        *   **Diagnosis:** A required file or directory does not exist at the specified path.
        *   **Action:** Verify the path. Was it constructed correctly? Is there a typo?
        *   **Remediation Request:** "Requesting confirmation that the file exists at `<file_path>`. The tool failed because this file could not be found."

    *   **Python Version Mismatch:**
        *   **Diagnosis:** The script failed with an error (e.g., `SyntaxError`, `ModuleNotFoundError` for a standard library module like `dataclasses`) that suggests an incorrect Python version.
        *   **Action:** Check the `SKILL.md` for Python version prerequisites (e.g., "Python 3.8+ is strictly required").
        *   **Remediation Request:** "The executed script requires Python version `<required_version>`, but the current environment seems to be using a different version. Please ensure the correct Python interpreter is used."

3.  **Communicate Clearly to Orchestrator:**
    *   Present the diagnosis and request in a clear, structured format. Do not be conversational. Be direct and precise.

## Example Communication

**Scenario:** The agent tries to run the `gtb-validator` skill, but `validate.py` fails.

**`run_shell_command` result:**
*   **command:** `python /home/owner03/.gemini/skills/gtb-validator/validate.py "/tmp/draft.md" "knowledge_retrieval"`
*   **exit_code:** 1
*   **stdout:** ""
*   **stderr:** `Traceback (most recent call last): File "/home/owner03/.gemini/skills/gtb-validator/validate.py", line 5, in <module> import antigravity_evolution ModuleNotFoundError: No module named 'antigravity_evolution'`

**Agent's Response (using this skill):**

> **Execution Failure Diagnosis:**
> *   **Goal:** Validate a draft KI against the Golden Test Battery.
> *   **Tool:** `gtb-validator` skill.
> *   **Command:** `python /home/owner03/.gemini/skills/gtb-validator/validate.py "/tmp/draft.md" "knowledge_retrieval"`
> *   **Diagnosis:** The execution failed with a `ModuleNotFoundError` for the `antigravity_evolution` package. This is a required dependency for the script.
> *   **Remediation Request:** Please install the `antigravity_evolution` Python package.
