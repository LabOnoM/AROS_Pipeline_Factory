---
name: tool-method-availability-check
description: A mandatory pre-execution check to validate tool availability and enforce the GEPA confirmation-before-execution policy.
license: MIT
skill-author: AROS_code_generator
---

# Tool/Method Availability Check (GEPA Mandated)

This skill implements a critical GEPA Error Prevention rule: **An agent MUST confirm the availability of a tool or method before attempting to use it.** It provides a programmatic check that prevents execution errors by halting the workflow if a required tool is unavailable.

## Core Principle

To prevent `command not found` errors and ensure predictable task execution, this skill validates a tool against a central registry (`tool_registry.json`) and verifies its presence in the system's PATH. The output explicitly states whether execution is permitted, and agents **MUST** adhere to this directive.

## Workflow

1.  **Identify Required Tool**: Before using a shell command or external tool, identify its name (e.g., `git`, `gtb-validator`).
2.  **Invoke the Checker**: Execute the `checker.py` script with the tool name as an argument.
    ```bash
    python ~/.gemini/skills/tool-method-availability-check/checker.py "git"
    ```
3.  **Analyze the Result**: The script returns a JSON object. You **MUST** check the `execution_permitted` field.
    *   **If `true`**: You may proceed with using the tool.
    *   **If `false`**: You **MUST NOT** attempt to use the tool. Halt the current task and report the reason provided in the `reason` field. Bypassing this check is a critical policy violation.

## Example Success Output

```json
{
  "tool_name": "git",
  "registered": true,
  "executable": true,
  "execution_permitted": true,
  "reason": "Tool 'git' is registered and available. Execution is permitted."
}
```

## Example Failure Output

```json
{
  "tool_name": "non-existent-tool",
  "registered": false,
  "executable": false,
  "execution_permitted": false,
  "reason": "Tool 'non-existent-tool' is not listed in the tool registry. Execution is forbidden as per GEPA policy."
}
```

## Associated Files

*   `~/.gemini/skills/tool-method-availability-check/checker.py`: The validation script.
*   `~/.gemini/skills/tool-method-availability-check/tool_registry.json`: The list of authorized tools.
