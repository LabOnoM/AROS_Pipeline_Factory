# Policy: ToolAvailabilityPre-Verification

## 1. Purpose

This policy implements the GEPA (Goal-Oriented Evolutionary Programming Agent) rule requiring strict pre-verification of all explicitly and implicitly required skills and tools before commencing critical execution steps of a workflow or task.

## 2. GEPA Rule

**GEPA-RULE-004**: An agent must not attempt to execute a task without first verifying that all required tools, skills, and dependencies are available in its current environment. This prevents execution failures due to missing dependencies and ensures predictable and reliable task execution.

## 3. Policy Directives

### 3.1. Pre-Execution Verification

Before executing any workflow or skill, the agent MUST perform a pre-execution verification check. This check consists of two main steps:

1.  **Dependency Identification**: Identify all required tools and skills for the task at hand.
2.  **Availability Verification**: Verify that each identified dependency is available in the agent's environment.

### 3.2. Dependency Identification

The agent must inspect the `SKILL.md` file and any other relevant documentation for the skill to be used. The agent must look for the following indicators of dependencies:

*   **Explicit Tool Lists**: Look for sections like `allowed-tools`, `required-tools`, `dependencies`, or `prerequisites`.
*   **Explicit Mentions**: Look for phrases like "depends on", "requires", "needs", etc. For example, "Executing the gtb-validator skill critically depends on write_file and execute_bash".
*   **Code Blocks**: Inspect any shell command examples in sections like `Quick Check`, `Instructions`, `Example Usage`, etc. The commands themselves are dependencies. For example, if a `Quick Check` section contains `python -m py_compile scripts/main.py`, then `python` is a dependency.
*   **Installation Commands**: Look for commands like `pip install`, `apt-get install`, etc. These indicate dependencies that might need to be installed.

### 3.3. Availability Verification

Once the dependencies are identified, the agent must verify their availability. The verification method depends on the type of dependency:

*   **Internal Skills/Tools**: For internal AROS tools like `write_file`, `read_file`, `run_shell_command`, the agent should check against its list of loaded and available tools.
*   **Shell Commands**: For shell commands like `python`, `git`, `curl`, the agent should attempt to run a version or help command (e.g., `python --version`, `git --version`, `curl --version`). A successful execution with a return code of 0 indicates the tool is available.
*   **Python Packages**: For python packages, the agent should check if they can be imported. For example, to check for `pandas`, the agent can run `python -c "import pandas"`.

### 3.4. Enforcement

*   **If all dependencies are available**: The agent may proceed with the execution of the task.
*   **If any dependency is unavailable**: The agent MUST NOT proceed with the execution. Instead, it must:
    1.  Halt the current task execution.
    2.  Report the missing dependency or dependencies clearly to the user or the orchestrating agent.
    3.  If possible and permitted, attempt to install the missing dependency using the provided installation instructions.

## 4. Examples

### Example 1: `gtb-validator` skill

*   **Dependency Identification**: The skill description explicitly states: "Executing the gtb-validator skill critically depends on write_file ... and execute_bash". The tool name for executing shell commands is `run_shell_command`.
*   **Required Tools**: `write_local_file`, `run_shell_command`.
*   **Verification**: The agent checks if `write_local_file` and `run_shell_command` are in its list of available tools.
*   **Action**: If both are present, proceed. If not, halt and report.

### Example 2: `lab-inventory-predictor` skill

*   **Dependency Identification**: The `Quick Check` section contains the command `python -m py_compile scripts/main.py`. It also mentions `pip install -r requirements.txt`.
*   **Required Tools**: `python`, `pip`.
*   **Verification**: The agent runs `python --version` and `pip --version` using the `run_shell_command` tool. It should also check the python version as the skill requires 3.8+.
*   **Action**: If `python` and `pip` are available and the python version is sufficient, proceed. Otherwise, halt and report.

### Example 3: `infographics` skill

*   **Dependency Identification**: The skill's metadata contains `allowed-tools: [Read, Write, Edit, Bash]`.
*   **Required Tools**: `read_local_file`, `write_local_file`, `run_shell_command`.
*   **Verification**: The agent checks if `read_local_file`, `write_local_file`, and `run_shell_command` are in its list of available tools.
*   **Action**: If all are present, proceed. If not, halt and report.
