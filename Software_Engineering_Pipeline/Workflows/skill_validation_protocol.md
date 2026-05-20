# System Instruction: Skill Availability Meta-Protocol

## 1. Overview

To ensure system stability and predictable behavior, all agents MUST validate the availability of a skill before attempting to execute it. This protocol outlines the mandatory procedure for cross-referencing a selected skill against the agent's predefined `skill_registry`.

## 2. The Skill Registry

Each agent is provisioned with a `skill_registry.json` file, located at `~/.gemini/skills/skill_registry.json`. This file contains an explicit list of all skills the agent is authorized and equipped to use. The agent's capabilities are strictly limited to the skills defined in this registry.

**Example `skill_registry.json`:**
```json
{
  "skills": [
    "gtb-validator",
    "lab-inventory-predictor",
    "adverse-event-narrative",
    "agent-communication",
    "aros-dashboard-control"
  ]
}
```

## 3. Mandatory Validation Logic

Before executing any skill, the agent MUST perform the following validation check:

1.  **Identify the Target Skill**: Determine the name of the skill to be executed (e.g., `lab-inventory-predictor`).
2.  **Invoke the Validator**: Execute the `validate_skill.py` script with the target skill name as an argument.
    ```bash
    python ~/.gemini/skills/validate_skill.py "lab-inventory-predictor"
    ```
3.  **Analyze the Output**: The script will return a JSON object with the validation result.
    *   **Success:**
        ```json
        {
          "skill_name": "lab-inventory-predictor",
          "available": true,
          "message": "Skill is available."
        }
        ```
    *   **Failure:**
        ```json
        {
          "skill_name": "non_existent_skill",
          "available": false,
          "message": "Error: Skill 'non_existent_skill' not found in the registry. Please select an available skill."
        }
        ```
4.  **Enforce the Result**:
    *   If `"available": true`, the agent may proceed with skill execution.
    *   If `"available": false`, the agent MUST NOT attempt to execute the skill. It must report the error to the user, citing the reason provided in the `"message"` field, and suggest alternative, available skills if possible.

## 4. Policy Enforcement

-   **Strict Adherence**: This protocol is not optional. Bypassing this validation check is a policy violation.
-   **Error Handling**: Any attempt to call an unregistered skill must be caught and handled gracefully, as per the instructions in section 3.
-   **Immutable Registry**: Agents are not permitted to modify their own `skill_registry.json` file. The registry is managed at the system level to ensure governance and control.

By adhering to this protocol, agents contribute to a robust and reliable AROS ecosystem, preventing execution errors and clearly communicating their capabilities.
