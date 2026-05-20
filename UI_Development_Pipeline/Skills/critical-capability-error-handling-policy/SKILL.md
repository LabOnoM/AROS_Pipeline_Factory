---
name: critical-capability-error-handling-policy
description: "A GEPA policy that mandates how agents must handle missing or non-functional critical capabilities. It requires pre-execution checks and a structured error reporting format to prevent silent or ungraceful failures."
license: MIT
skill-author: AROS-Code-Generator
status: active
policy-type: execution-guardrail
---

# Policy: Critical Capability Error Handling

This policy implements a core GEPA principle: **"Prevent execution failures by verifying prerequisites."** It establishes the mandatory protocol for all AROS agents to detect and report missing or non-functional capabilities *before* a task's primary logic is executed. This prevents silent, ambiguous, or ungraceful failures, replacing them with clear, actionable error reports.

## GEPA Rule: The Rule of Prerequisite Verification

An agent **MUST NOT** attempt to execute the core logic of a task without first verifying the existence and basic functionality of all critical capabilities it depends on. A critical capability is any tool, command, skill, file, or endpoint without which the task is guaranteed to fail.

If any prerequisite check fails, the agent **MUST** immediately halt the operation, generate a structured error message as defined below, and terminate gracefully. It is a critical policy violation to proceed with a task when a required capability is known to be missing.

## Guiding Principles

- **Fail Fast, Fail Explicitly:** Detect environmental and dependency errors as early as possible.
- **Clarity Over Ambiguity:** Never assume a capability exists. Always check.
- **Structured Reporting:** Provide error messages that are machine-readable and contain enough context for automated or human-led remediation.
- **No Improvisation for Core Tools:** An agent is strictly forbidden from attempting to find a "substitute" for a missing, explicitly requested capability (e.g., using `wget` when `curl` was required by the workflow).

## Mandatory Pre-Execution Workflow

Before running the main logic of any task, the agent must perform the following steps:

1.  **Identify Critical Capabilities:** From the task description and its internal plan, compile a list of all critical dependencies. This includes:
    *   Shell commands (e.g., `git`, `python`, `docker`)
    *   Internal AROS tools/skills (e.g., `gtb_validator`, `code_linter`)
    *   Required input files or directories
    *   Network endpoints or APIs

2.  **Execute Verification Checks:** For each identified capability, perform a simple, low-cost check to confirm its presence and functionality.
    *   **For Shell Commands:** Use `command -v <command_name>`. A non-zero exit code indicates the command is not available in the `$PATH`.
    *   **For AROS Skills/Tools:** Query the internal tool registry to confirm the tool is loaded and available.
    *   **For Files/Directories:** Use `test -f /path/to/file` or `test -d /path/to/dir`.
    *   **For Network Endpoints:** Perform a `HEAD` request or use `curl --fail -s -o /dev/null <url>` to check for a successful HTTP response (2xx).

3.  **Handle Verification Failure:** If any check from step 2 fails, the agent **MUST** immediately halt and generate a structured error message.

## Standardized Error Message Format

The error message generated upon failure **MUST** contain the following fields. This structured output is crucial for the AROS orchestrator to diagnose and potentially remediate the issue.

```json
{
  "PolicyViolation": "critical-capability-error-handling-policy",
  "Status": "HALTED",
  "MissingCapability": {
    "Type": "ShellCommand",
    "Name": "git",
    "VerificationMethod": "command -v git",
    "VerificationResult": {
      "ExitCode": 127,
      "Stderr": "/bin/sh: 1: command: not found"
    }
  },
  "OriginalGoal": "Clone the remote repository from https://github.com/example/project.git to /tmp/project",
  "RemediationRequest": "The required shell command 'git' is not installed or is not available in the system's PATH. Please install 'git' to proceed."
}
```

### Field Definitions:
- **`PolicyViolation`**: Always `critical-capability-error-handling-policy`.
- **`Status`**: Always `HALTED`.
- **`MissingCapability.Type`**: The type of dependency. One of `ShellCommand`, `AROSSkill`, `File`, `Directory`, `NetworkEndpoint`.
- **`MissingCapability.Name`**: The specific name of the missing item (e.g., "git", "gtb_validator", "/data/input.csv").
- **`MissingCapability.VerificationMethod`**: The exact command or check that was performed.
- **`MissingCapability.VerificationResult`**: An object containing the exit code, `stdout`, or `stderr` from the verification check.
- **`OriginalGoal`**: The high-level task the agent was trying to accomplish.
- **`RemediationRequest`**: A clear, human-readable instruction on how to fix the problem.

By adhering to this policy, AROS ensures that tasks fail in a predictable, informative, and recoverable manner, which is essential for a robust and autonomous system.
