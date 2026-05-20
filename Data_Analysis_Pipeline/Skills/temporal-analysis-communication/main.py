# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import argparse
import json
import re

def validate_output_structure(output_text):
    """
    Validates the output text against the required structure for temporal evolution mapping.
    Uses regex to check for the presence of the mandatory sections.
    """
    patterns = {
        "initial_state": r"^\*\*1\.\s+Initial\s+State\s+\(T0\):\*\*",
        "intermediate_state": r"^\*\*2\.\s+Intermediate\s+State\(s\)\s+\(T1,\s+T2,\s+\.\.\.\):\*\*",
        "final_state": r"^\*\*3\.\s+Final\s+State\s+\(Tn\):\*\*",
        "trend_analysis": r"^\*\*4\.\s+Trend\s+Analysis:\*\*"
    }

    for section, pattern in patterns.items():
        if not re.search(pattern, output_text, re.MULTILINE):
            return {"passed": False, "reason": f"Missing section: {section}"}

    return {"passed": True}

def generate_temporal_analysis(data):
    """
    Generates a temporal analysis report based on the provided data.
    This function currently creates a basic report and can be extended for more complex analysis.
    """
    report = []
    # Initial State
    report.append("**1. Initial State (T0):**")
    report.append(f"- **Timestamp/Identifier:** {data[0]['timestamp']}")
    report.append(f"- **Description:** {data[0]['description']}")
    report.append("- **Key Metrics:**")
    for key, value in data[0]['metrics'].items():
        report.append(f"  - {key}: {value}")
    report.append("")

    # Intermediate States
    report.append("**2. Intermediate State(s) (T1, T2, ...):**")
    if len(data) > 2:
        for item in data[1:-1]:
            report.append(f"- **Timestamp/Identifier:** {item['timestamp']}")
            report.append(f"- **Description:** {item['description']}")
            report.append("- **Key Metrics:**")
            for key, value in item['metrics'].items():
                report.append(f"  - {key}: {value}")
    else:
        report.append("- No intermediate states provided.")
    report.append("")

    # Final State
    report.append("**3. Final State (Tn):**")
    report.append(f"- **Timestamp/Identifier:** {data[-1]['timestamp']}")
    report.append(f"- **Description:** {data[-1]['description']}")
    report.append("- **Key Metrics:**")
    for key, value in data[-1]['metrics'].items():
        report.append(f"  - {key}: {value}")
    report.append("")

    # Trend Analysis
    report.append("**4. Trend Analysis:**")
    report.append("- **Summary of Evolution:** A summary of the evolution should be generated here.")
    report.append("- **Identified Trends:** Trends should be identified here.")
    report.append("")

    return "\n".join(report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Temporal Analysis & Communication Skill")
    parser.add_argument("--data", type=str, required=True, help="JSON string with temporal data")
    args = parser.parse_args()

    try:
        input_data = json.loads(args.data)
    except json.JSONDecodeError:
        print("Error: Invalid JSON data provided.")
        exit(1)

    # Generate the analysis
    analysis_report = generate_temporal_analysis(input_data)
    print("--- Generated Report ---")
    print(analysis_report)

    # Validate the output
    validation_result = validate_output_structure(analysis_report)
    print("--- Validation Result ---")
    print(json.dumps(validation_result, indent=2))

    if not validation_result["passed"]:
        print("\nError: The generated report does not meet the structural requirements.")
        exit(1)

    print("\nSuccessfully generated and validated the temporal analysis report.")
