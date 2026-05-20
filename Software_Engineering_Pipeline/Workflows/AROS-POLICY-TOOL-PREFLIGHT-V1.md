# Policy: External Tool Pre-Execution Verification
**Version:** 1.0
**ID:** AROS-POLICY-TOOL-PREFLIGHT-V1

---

## 1. Preamble

This document establishes the mandatory pre-execution verification policy for any external tools, binaries, or scripts invoked by an AROS agent. The purpose of this policy is to prevent common, foreseeable execution failures related to environmental and permission issues, thereby increasing system reliability and providing clear, actionable error reporting.

## 2. Core Principle

An agent MUST NOT attempt to execute an external tool without first successfully completing the pre-execution checklist defined in this policy. This is a zero-tolerance policy; invoking a tool without prior verification is a critical violation.

## 3. Pre-Execution Verification Checklist

Before invoking any external command-line tool (e.g., `git`, `python`, `curl`, `gtb-validator`), the agent MUST perform the following checks in order. If any check fails, the agent MUST immediately halt and report the failure without attempting to execute the tool for its primary task.

### Step 1: Tool Path Existence Check

*   **Objective:** Verify that the tool is present and locatable within the system's `PATH`.
*   **Action:** Execute the `command -v <tool_name>` shell command.
*   **Success:** The command returns a non-empty string containing the absolute path to the tool and exits with a status code of 0.
*   **Failure:** The command returns an empty string or a non-zero exit code.

### Step 2: Execute Permission Check

*   **Objective:** Verify that the agent possesses the necessary file system permissions to execute the tool.
*   **Action:** Using the path obtained from Step 1, execute the `[ -x "/path/to/tool" ]` shell command.
*   **Success:** The command exits with a status code of 0.
*   **Failure:** The command exits with a non-zero status code.

### Step 3: Operational Status Check

*   **Objective:** Perform a non-destructive "smoke test" to verify the tool is operational and not in a corrupted state.
*   **Action:** Execute the tool with a common, non-destructive flag that should always succeed on a healthy binary, such as `--version` or `--help`. The agent should prioritize `--version`.
*   **Success:** The command executes without hanging and returns a `0` exit code.
*   **Failure:** The command returns a non-zero exit code or exceeds a reasonable timeout (e.g., 5 seconds).

## 4. Standard Output Format for Verification Results

The results of the pre-execution checklist MUST be formatted into a standard JSON object for logging and inter-agent communication. This provides a structured and predictable format for reporting outcomes.

**Example of a SUCCESSFUL Verification:**
```json
{
  "tool_name": "gtb-validator",
  "pre_execution_check_passed": true,
  "checks": {
    "path_existence": {
      "passed": true,
      "details": "Resolved path: /home/owner03/.gemini/skills/gbt-validator/validate.py"
    },
    "execute_permissions": {
      "passed": true,
      "details": "File has execute permissions."
    },
    "operational_status": {
      "passed": true,
      "details": "Tool responded successfully to --help flag with exit code 0."
    }
  }
}
```

**Example of a FAILED Verification:**
```json
{
  "tool_name": "gtb-validator",
  "pre_execution_check_passed": false,
  "checks": {
    "path_existence": {
      "passed": true,
      "details": "Resolved path: /home/owner03/.gemini/skills/gbt-validator/validate.py"
    },
    "execute_permissions": {
      "passed": false,
      "details": "Error: Permission denied. File is not executable."
    },
    "operational_status": {
      "passed": false,
      "details": "Check not performed due to prior failure."
    }
  }
}
```

## 5. Agent Action Protocol

*   **On Success:** If `pre_execution_check_passed` is `true`, the agent is authorized to proceed with its primary task execution using the tool.
*   **On Failure:** If `pre_execution_check_passed` is `false`, the agent MUST NOT attempt to run the tool. It must report the failure explicitly, providing the structured JSON output as the reason, in accordance with the `agent-communication` policy.

## 6. Relationship to Self-Healing Environment Policy

This policy covers **Phase 1 (Detect)** of the three-phase Self-Healing Environment Pattern. For the complete lifecycle — including auto-installation (Phase 2: Repair) and graceful degradation (Phase 3: Degrade) — agents MUST also comply with the `self_healing_environment_policy` (`01.Shared_Assets/Policies/self_healing_environment_policy.md`).
