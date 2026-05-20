# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import argparse
import json
import sys

PERSONA_CAPABILITY_MAP = {
    "code_generator": [
        "implement", "write code", "develop", "create a script",
        "generate", "code", "program", "function", "module", "class", "patch"
    ],
    "qa_engineer": [
        "verify", "test", "validate", "ensure", "check", "QA", "review",
        "find bugs", "edge cases", "assert", "quality"
    ],
    "data_analyst": [
        "analyze", "data", "dataset", "visualize", "statistics",
        "report", "query", "insights"
    ],
    "research_specialist": [
        "research", "find information", "summarize", "investigate",
        "background", "literature review"
    ]
}

def get_required_persona(task_description):
    """
    Analyzes the task description to determine the required persona.
    It returns the persona with the most keyword matches.
    """
    task_lower = task_description.lower()
    scores = {persona: 0 for persona in PERSONA_CAPABILITY_MAP}

    for persona, keywords in PERSONA_CAPABILITY_MAP.items():
        for keyword in keywords:
            if keyword in task_lower:
                scores[persona] += 1

    # Find the persona with the highest score
    if any(s > 0 for s in scores.values()):
        best_persona = max(scores, key=scores.get)
        return best_persona

    return "generalist" # Default if no specific capability is identified

def validate_persona_assignment(task_description, assigned_persona):
    """
    Enforces the Persona-Capability Alignment rule.
    """
    required_persona = get_required_persona(task_description)

    if required_persona == "generalist" or assigned_persona == required_persona:
        return {
            "valid": True,
            "required_persona": required_persona
        }
    else:
        return {
            "valid": False,
            "reason": f"Persona '{assigned_persona}' does not match the required persona '{required_persona}' based on task analysis.",
            "required_persona": required_persona
        }

def main():
    """
    Main function to parse arguments and run the validation.
    """
    parser = argparse.ArgumentParser(
        description="Validate persona-capability alignment for a given task based on GEPA rules."
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="The description of the sub-task."
    )
    parser.add_argument(
        "--persona",
        type=str,
        required=True,
        help="The persona assigned to the agent for executing the task."
    )
    args = parser.parse_args()

    result = validate_persona_assignment(args.task, args.persona)
    print(json.dumps(result, indent=2))

    if not result["valid"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
