---
name: persona_capability_validator
description: A GEPA error prevention skill that verifies if an assigned agent persona matches the required capabilities of a sub-task.
license: MIT
skill-author: AROS_code_generator
---

# Persona-Capability Alignment Validator

This skill implements the GEPA error prevention rule for persona assignment. It ensures that an agent's assigned persona (e.g., `code_generator`, `qa_engineer`) is appropriate for the task it is about to execute. This prevents capability gaps and improves the quality of task execution.

## When to Use

This skill MUST be used by the AROS orchestrator as a pre-execution check before dispatching any sub-task to a specialized agent. It is a mandatory step in the task assignment workflow as defined by the `persona-assignment-policy`.

## Core Logic

The validator uses a keyword-based mapping to determine the required persona for a given task description.

-   **Input:** Task goal/description string, Assigned Persona string.
-   **Output:** A JSON object indicating if the persona is valid (`{"valid": true}`) or not (`{"valid": false, "reason": "...", "required_persona": "..."}`).

## MANDATORY SKILL INSTRUCTIONS:

### Example Usage

```bash
# Example 1: A valid assignment
python ~/.gemini/skills/persona_capability_validator/validator.py --task "Implement a new function to parse user data and write unit tests." --persona "code_generator"

# Expected Output:
# {
#   "valid": true,
#   "required_persona": "code_generator"
# }

# Example 2: An invalid assignment
python ~/.gemini/skills/persona_capability_validator/validator.py --task "Verify the functionality of the new module and check for edge cases." --persona "code_generator"

# Expected Output:
# {
#   "valid": false,
#   "reason": "Persona 'code_generator' does not match the required persona 'qa_engineer' based on task analysis.",
#   "required_persona": "qa_engineer"
# }
```
