---
name: error_handling_and_diagnostic_reporting
description: Intercepts ToolNotFoundError or PreconditionUnmetError, gathers environment diagnostic details, and explicitly returns a structured error message to the orchestration system.
license: MIT
skill-author: AROS_code_generator
---

# Error Handling and Diagnostic Reporting Skill

This skill provides a robust mechanism for agents to handle specific, recoverable errors by capturing detailed system diagnostics and generating a structured, actionable report. It is designed to intercept `ToolNotFoundError` and `PreconditionUnmetError` to help the orchestration layer or a human operator resolve environment and prerequisite issues.

## Key Capabilities
- **Targeted Exception Handling**: Specifically catches `ToolNotFoundError` and `PreconditionUnmetError`.
- **Rich Diagnostic Capture**: Gathers detailed information about the system (OS, Python version), environment (`PATH`, `CWD`), and installed packages.
- **Structured JSON Reporting**: Outputs a standardized JSON object containing the error details, diagnostics, and a recommended remediation step.
- **Actionable Recommendations**: Provides clear, actionable next steps in the report, aligned with the GEPA error prevention principles.

## Workflow
1.  **Wrap Critical Task**: An agent wraps a function call that might fail due to missing tools or unmet preconditions with the `execute_critical_task` handler from this skill's script.
2.  **Provide Goal Context**: The agent passes the original high-level goal to the handler.
3.  **Exception Interception**: If the wrapped function raises a `ToolNotFoundError` or `PreconditionUnmetError`, the `except` block in the handler is triggered.
4.  **Diagnostic Aggregation**: The handler calls functions to collect system, environment, and package information.
5.  **Report Generation**: It formats all the captured information into the structured `DiagnosticReport` schema.
6.  **Return Report**: The handler returns the JSON report to the calling agent, which can then pass it up to the orchestrator.

## Output Schema
The skill returns a JSON object with the following structure:
```json
{
  "error_type": "string",
  "error_message": "string",
  "original_goal": "string",
  "failing_tool": "string",
  "diagnostics": {
    "system": {
      "os_platform": "string",
      "os_version": "string",
      "python_version": "string"
    },
    "environment": {
      "path": "string",
      "pythonpath": "string",
      "user": "string",
      "cwd": "string"
    },
    "installed_packages": "array"
  },
  "actionable_recommendations": [
    "string"
  ]
}
```

## Audit-Ready Command

This command executes the script's built-in simulation to demonstrate how it handles both `ToolNotFoundError` and `PreconditionUnmetError`, printing the structured JSON reports to the console.
```bash
python ~/.gemini/skills/error_handling_and_diagnostic_reporting/scripts/main.py
```
