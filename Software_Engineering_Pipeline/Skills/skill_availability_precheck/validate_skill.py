# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import json
import os
import sys

# The canonical path to the agent's skill registry.
REGISTRY_PATH = os.path.expanduser("~/.gemini/skills/skill_registry.json")

def create_response(skill_name, status, reason):
    """
    Generates a structured JSON response and prints it to stdout.

    Args:
        skill_name (str): The name of the skill being checked.
        status (str): The result of the check ('available', 'unavailable', 'error').
        reason (str): A human-readable explanation of the result.
    """
    response = {
        "skill_name": skill_name,
        "status": status,
        "reason": reason
    }
    print(json.dumps(response, indent=2))

def main():
    """
    Main execution logic for the skill availability validator.
    """
    # 1. Validate that a skill name was provided as a command-line argument.
    if len(sys.argv) < 2:
        create_response("unknown", "error", "No skill name provided. Usage: python validate_skill.py <skill_name>")
        sys.exit(1)

    target_skill = sys.argv[1]

    # 2. Ensure the skill registry file exists before attempting to read it.
    if not os.path.exists(REGISTRY_PATH):
        create_response(target_skill, "error", f"Skill registry not found at: {REGISTRY_PATH}")
        sys.exit(1)

    # 3. Read and parse the JSON registry file, with robust error handling.
    try:
        with open(REGISTRY_PATH, 'r') as f:
            registry_data = json.load(f)
    except json.JSONDecodeError:
        create_response(target_skill, "error", f"Failed to decode JSON from registry file: {REGISTRY_PATH}")
        sys.exit(1)
    except Exception as e:
        create_response(target_skill, "error", f"An unexpected error occurred while reading the registry file: {e}")
        sys.exit(1)

    # 4. Validate the structure of the registry data.
    if "skills" not in registry_data or not isinstance(registry_data.get("skills"), list):
        create_response(target_skill, "error", "Registry file is malformed: must contain a 'skills' key with a list of skill names.")
        sys.exit(1)

    # 5. Perform the availability check and report the result.
    if target_skill in registry_data["skills"]:
        create_response(target_skill, "available", "Skill is registered and available for execution.")
    else:
        create_response(target_skill, "unavailable", "Skill is not found in the agent's registry.")

if __name__ == "__main__":
    main()
