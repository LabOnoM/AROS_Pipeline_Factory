---
name: input_validation
description: A skill that enforces strict input validation for all data entering the AROS system, particularly for tool and skill parameters.
license: MIT
skill-author: AROS-Security-Team
version: 1.0
---

# Skill: Input Validation

This skill provides a centralized and robust mechanism for validating all inputs passed to AROS tools, skills, and workflows. It is a critical component of the AROS security and stability framework, preventing injection attacks, malformed data, and unexpected behavior.

## Core Principle

All external and internal inputs must be treated as untrusted. This skill enforces a "deny-by-default" policy, where data is considered invalid unless it conforms to a strict, predefined schema. This aligns with the GEPA (Global Error Prevention Architecture) mandate for proactive error and vulnerability mitigation.

## Workflow

1.  **Schema Definition**: The developer or agent defining a new skill or tool MUST provide a validation schema for its input parameters. This schema should define data types, required fields, value ranges, and regex patterns.
2.  **Pre-Execution Check**: Before any skill or tool is executed, the AROS kernel invokes this `input_validation` skill.
3.  **Validation Execution**: This skill compares the provided input against the target tool's registered schema.
4.  **Decision**:
    *   **On Success**: If the input conforms to the schema, execution of the target tool is allowed to proceed.
    *   **On Failure**: If the input is invalid, the skill raises a critical exception, logs the malicious or malformed input, and blocks the execution of the target tool. This action prevents the corrupted data from propagating through the system.

## Example Invocation

Consider a tool `file_writer` that expects a `filepath` and `content`.

**Schema Definition (part of file_writer's SKILL.md):**
```yaml
parameters:
  - name: "filepath"
    type: "string"
    required: true
    validation:
      # Must be an absolute path within the agent sandbox
      pattern: "^/home/owner03/\\.gemini/antigravity/agent_sandbox/.*$"
  - name: "content"
    type: "string"
    required: true
    validation:
      # Content must not be empty
      min_length: 1
```

**Usage (internal AROS call):**

```python
# VALID INPUT
# This would be allowed by the input_validator
aros_kernel.run_skill(
    'file_writer',
    {
        'filepath': '/home/owner03/.gemini/antigravity/agent_sandbox/8ba2527e-2ca7-4506-aff0-96655a3a586a/output.txt',
        'content': 'This is valid content.'
    }
)

# INVALID INPUT
# This would be blocked by the input_validator, and an exception raised.
aros_kernel.run_skill(
    'file_writer',
    {
        'filepath': '../../etc/passwd', # Path traversal attempt
        'content': '' # Fails min_length check
    }
)
```

--- AUTO-CORRECTION BASED ON FEEDBACK ---
The content lacks depth and clarity. Automated check failed.
--- END CORRECTION ---

--- AUTO-CORRECTION BASED ON FEEDBACK ---
The content lacks depth and clarity. Automated check failed.
--- END CORRECTION ---

--- AUTO-CORRECTION BASED ON FEEDBACK ---
External review feedback: The structure is illogical and lacks a concluding summary. Please revise.
--- END CORRECTION ---