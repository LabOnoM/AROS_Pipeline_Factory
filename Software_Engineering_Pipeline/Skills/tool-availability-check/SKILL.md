---
name: tool-availability-check
description: A mandatory pre-execution check to validate if a tool or method is available in the skill registry, with an integrated GEPA patch for resilience and a mandatory confirmation step.
license: MIT
skill-author: AROS_code_generator
---

# Tool/Method Availability Check (with GEPA & Confirmation)

This skill enforces a critical AROS policy: **An agent MUST validate the availability of a tool AND receive explicit confirmation before execution.** It prevents errors from calling non-existent tools and ensures that all tool parameters are verified before any action is taken.

## GEPA Integration

This skill integrates the GEPA error prevention patch by:
1.  **Retry Mechanism**: If the `skill_registry.json` file is temporarily unavailable or corrupted, the script will retry reading it twice before failing.
2.  **Mandatory Halt**: If the tool is not found in the registry, or if the registry cannot be read, the skill instructs the agent to **HALT** execution immediately. This prevents hallucinated workarounds.

## Mandatory Workflow

To use any tool, you MUST follow this three-step process:

### Step 1: Validate Tool Availability

Invoke the `check.py` script with the target tool name.

**Example Command:**
```bash
python ~/.gemini/skills/tool-availability-check/check.py "gtb-validator"
```

### Step 2: Analyze Result & Formulate Call

Analyze the JSON output from the script.

*   **If `"available": false`**:
    *   **HALT** all further action.
    *   Report the error message provided in the output.
    *   DO NOT attempt to use the tool or find an alternative.

*   **If `"available": true`**:
    *   The output will contain `"confirmed": false`. This is a hard-coded reminder of the next step.
    *   Proceed to formulate the complete tool call with all necessary parameters.

### Step 3: Mandated Confirmation Before Execution

This is a critical, non-negotiable step.

1.  **Present the Formulated Call**: Display the full tool call you intend to execute, including the tool name and all its arguments.
2.  **Request Explicit Confirmation**: Ask for a "yes" or "proceed" confirmation.
3.  **Await Approval**: **DO NOT** execute the tool call until you receive an affirmative confirmation.
4.  **Execute on Confirmation**: Once confirmation is granted, you are permitted to execute the tool call.

**Example of Confirmation Interaction:**

```text
PROPOSED ACTION:
I will now execute the following tool call:
- Tool: `gtb_validator`
- Parameters:
  - `draft_file_path`: "/tmp/draft_skill.md"
  - `task_type`: "skill_generation"

Is this correct? Please confirm to proceed.
```

Only after receiving a positive response to this prompt can the tool be executed. Bypassing this confirmation step is a critical policy violation.
