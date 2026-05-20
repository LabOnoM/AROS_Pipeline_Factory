# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import sys
import json
import os
import re

def check_placeholder_completeness(content):
    """
    Checks for placeholder text that indicates incomplete work. Returns a list of findings.
    """
    findings = []
    # More comprehensive anti-patterns
    anti_patterns = [
        "TODO", "FIXME", "implement here", "...", "your logic here", "to be implemented",
        "TBD", "placeholder", "add details later", "coming soon", "under construction"
    ]
    for pattern in anti_patterns:
        # Use word boundaries for whole words, but not for "..."
        search_pattern = r'\b' + re.escape(pattern) + r'\b' if pattern != "..." else r'\.\.\.'
        if re.search(search_pattern, content, re.IGNORECASE):
            findings.append(
                f"GEPA Readiness Check Failed: Found placeholder text '{pattern}'. "
                "Skills and KIs must be complete and actionable."
            )
    return findings

def check_structural_completeness(content):
    """
    Performs checks on the markdown structure. Returns a list of findings.
    """
    findings = []
    if len(content.strip()) < 150:
        findings.append(
            "Content Completeness Check Failed: The content is too short to be a valid Skill, KI, or Policy. "
            "Ensure all required sections are present and contain meaningful information."
        )

    # Check for empty sections
    sections = re.split(r'(^#+\s.*)', content, flags=re.MULTILINE)
    if len(sections) > 1:
        for i in range(1, len(sections), 2):
            header = sections[i].strip()
            # Ensure there is content for the section
            section_content = sections[i+1].strip() if (i+1) < len(sections) else ""
            if not section_content:
                findings.append(
                    f"Content Completeness Check Failed: The section '{header}' is empty. "
                    "All sections must contain descriptive content."
                )

    # Check for mandatory 'Validation' or 'Instructions' or 'Usage' section
    # This ensures the artifact is actionable.
    if not re.search(r'#+\s(Validation|Instructions|Usage|Example|Protocol|Workflow)', content, re.IGNORECASE):
         findings.append(
             "GEPA Readiness Check Failed: A 'Validation', 'Instructions', 'Usage', 'Example', 'Protocol', or 'Workflow' section is mandatory "
             "to describe how to verify or use the artifact's correctness."
         )
    return findings

def main():
    """
    Main validation function that aggregates all findings.
    """
    if len(sys.argv) < 2:
        print(json.dumps({
            "passed": False,
            "score": 0.0,
            "reasoning": "Usage: python validate.py <filepath>"
        }))
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(json.dumps({
            "passed": False,
            "score": 0.0,
            "reasoning": f"File not found at path: {filepath}"
        }))
        sys.exit(1)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(json.dumps({
            "passed": False,
            "score": 0.0,
            "reasoning": f"Error reading file: {str(e)}"
        }))
        sys.exit(1)

    all_findings = []
    all_findings.extend(check_placeholder_completeness(content))
    all_findings.extend(check_structural_completeness(content))

    if not all_findings:
        result = {
            "passed": True,
            "score": 10.0,
            "reasoning": "All validation checks passed."
        }
    else:
        # Aggregate all findings into a single report
        reasoning_text = "Validation failed with the following issues:\n- " + "\n- ".join(all_findings)
        result = {
            "passed": False,
            "score": 1.0, # Hard failure score
            "reasoning": reasoning_text
        }

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
