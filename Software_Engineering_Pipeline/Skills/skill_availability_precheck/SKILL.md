---
name: skill_availability_precheck
description: A mandatory pre-execution check to validate if a skill is available in the agent's authorized registry.
license: MIT
skill-author: AROS_code_generator
---

# Skill Availability Pre-Check

This skill implements the mandatory `Skill Availability Meta-Protocol`. It provides a script to verify that a requested skill is listed in the agent's `skill_registry.json`, ensuring the agent is authorized and equipped to execute it before any attempt is made.

## GEPA Rule: Pre-Task Capability Validation

This skill directly supports the "Pre-Task Capability Validation" GEPA rule by providing the mechanism to check for skill availability. An agent MUST use this validator before attempting to execute any skill.

## Core Component: `validate_skill.py`

The logic is contained within the `validate_skill.py` script.

### Workflow

1.  **Invoke Validator**: Before executing a skill (e.g., `gtb-validator`), the agent MUST first call the validation script with the target skill's name.
2.  **Read Registry**: The script reads the `~/.gemini/skills/skill_registry.json` file.
3.  **Check for Skill**: It checks if the target skill name exists in the "skills" list within the JSON file.
4.  **Return JSON Status**: The script prints a JSON object to standard output indicating the skill's status (`available` or `unavailable`) and a reason.

## Audit-Ready Commands

These commands demonstrate the core functionality for different scenarios.

```bash
# Example 1: Check for an available skill (should succeed)
python ~/.gemini/skills/skill_availability_precheck/validate_skill.py "gtb-validator"

# Example 2: Check for an unavailable skill (should report unavailable)
python ~/.gemini/skills/skill_availability_precheck/validate_skill.py "nonexistent-skill"

# Example 3: Run without a skill name (should report an error)
python ~/.gemini/skills/skill_availability_precheck/validate_skill.py
```
