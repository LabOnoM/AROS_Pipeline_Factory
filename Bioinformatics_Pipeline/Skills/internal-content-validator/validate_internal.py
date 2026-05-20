# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import sys
import json
import yaml
import re

def validate_content(file_path):
    """
    Validates the structural integrity of a drafted AROS component based on
    the rules defined in the 'internal-content-validator' skill.
    """
    passed = True
    reasoning = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return json.dumps({
            "passed": False,
            "reasoning": [f"File not found at path: {file_path}"]
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "passed": False,
            "reasoning": [f"Error reading file: {str(e)}"]
        }, indent=2)

    # 1. YAML Frontmatter Validation
    try:
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            passed = False
            reasoning.append("Missing or improperly formatted YAML frontmatter block (must be enclosed in '---').")
            frontmatter = None
        else:
            frontmatter_text = match.group(1)
            try:
                frontmatter = yaml.safe_load(frontmatter_text)
                if not isinstance(frontmatter, dict):
                    passed = False
                    reasoning.append("YAML frontmatter does not parse into a valid dictionary.")
                    frontmatter = None # Prevent further checks on invalid frontmatter
            except yaml.YAMLError as e:
                passed = False
                reasoning.append(f"Error parsing YAML frontmatter: {e}")
                frontmatter = None # Prevent further checks on unparsable frontmatter

        if frontmatter:
            # Check for required keys: name/title, description, skill-author
            if 'name' not in frontmatter and 'title' not in frontmatter:
                passed = False
                reasoning.append("Missing required YAML frontmatter key: 'name' or 'title'.")

            for key in ['description', 'skill-author']:
                if key not in frontmatter or not frontmatter.get(key):
                    passed = False
                    reasoning.append(f"Missing or empty required YAML frontmatter key: '{key}'.")

    except Exception as e:
        passed = False
        reasoning.append(f"An unexpected error occurred during YAML validation: {e}")

    # 2. Operational Context Validation
    operational_sections = [
        "## Workflow",
        "## Instructions",
        "## When to Use",
        "## Core Capabilities",
        "## Example Usage"
    ]
    
    found_section = False
    for section in operational_sections:
        # Match markdown headers, allowing for variations in whitespace
        if re.search(r'^\s*' + re.escape(section) + r'\s*', content, re.MULTILINE | re.IGNORECASE):
            found_section = True
            break
            
    if not found_section:
        passed = False
        reasoning.append("Missing operational context. Document must contain at least one of the following sections: " + ", ".join(operational_sections) + ".")

    result = {
        "passed": passed,
        "reasoning": reasoning
    }

    return json.dumps(result, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error_result = {
            "passed": False,
            "reasoning": ["Usage: python validate_internal.py <path_to_draft_file>"]
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

    draft_file_path = sys.argv[1]
    
    try:
        import yaml
    except ImportError:
        error_result = {
            "passed": False,
            "reasoning": ["Dependency missing. Please install 'pyyaml' (`pip install pyyaml`) to run this validator."]
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

    validation_result = validate_content(draft_file_path)
    print(validation_result)
