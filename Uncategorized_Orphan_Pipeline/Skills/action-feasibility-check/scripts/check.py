import json
import os
import sys
import re

PROHIBITED_PLACEHOLDERS = [
    'TODO',
    'FIXME',
    'implement here',
    '...',
    'your logic here',
    'to be implemented'
]

def check_placeholders(filepath):
    """Scans a file for prohibited placeholders."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple string matching is case-sensitive and fast
        for placeholder in PROHIBITED_PLACEHOLDERS:
            if placeholder in content:
                return f"Failed: Prohibited placeholder '{placeholder}' found."

        # Special case for '...' to avoid matching ellipses in prose
        if re.search(r'\.\s*\.\s*\.', content):
             # This is a weak check, but let's assume for now it's for code placeholders
             pass # Let's be more specific, maybe look for it on its own line or with code comments
    except Exception as e:
        return f"Error reading file {filepath}: {e}"
    return None

def check_validation_section(filepath):
    """Checks for a '## Validation' section in a Markdown file."""
    if not (filepath.endswith('.md') or filepath.endswith('.MD')):
        return None # Only apply this check to markdown files

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use regex to find a markdown header '## Validation'
        # This is case-insensitive and allows for variations in whitespace
        if not re.search(r'^\s*##\s+Validation\s*$', content, re.MULTILINE | re.IGNORECASE):
            return "Failed: Markdown file must contain a '## Validation' section."
            
    except Exception as e:
        return f"Error reading file {filepath}: {e}"
    return None

def find_skill_root(filepath):
    """Finds the root directory of a skill from a given filepath."""
    current_path = os.path.abspath(filepath)
    # Walk up until we find the directory that is a direct child of 'skills'
    while True:
        parent = os.path.dirname(current_path)
        if os.path.basename(parent) == 'skills':
            return current_path
        if parent == '/' or parent == current_path: # Reached the top
            return None
        current_path = parent

def check_tests_directory(filepath):
    """Checks for the existence of a 'tests/' subdirectory in the skill's root."""
    try:
        skill_root = find_skill_root(filepath)
        if not skill_root:
             return f"Failed: Could not determine the skill's root directory from path '{filepath}'."
        
        tests_dir = os.path.join(skill_root, 'tests')
        if not os.path.isdir(tests_dir):
            return f"Failed: Skill must have a 'tests/' directory at '{skill_root}'."

    except Exception as e:
        return f"Error checking for tests directory: {e}"
    return None


def main(filepath):
    """Runs all feasibility checks on the given file."""
    results = {
        "passed": True,
        "reasoning": []
    }

    # Check 1: Prohibited Placeholders
    placeholder_result = check_placeholders(filepath)
    if placeholder_result:
        results["passed"] = False
        results["reasoning"].append(placeholder_result)

    # Check 2: Mandatory Validation Section (for .md files)
    validation_result = check_validation_section(filepath)
    if validation_result:
        results["passed"] = False
        results["reasoning"].append(validation_result)

    # Check 3: Mandatory tests/ directory
    tests_dir_result = check_tests_directory(filepath)
    if tests_dir_result:
        results["passed"] = False
        results["reasoning"].append(tests_dir_result)
        
    if not results["reasoning"]:
        results["reasoning"].append("Success: All feasibility checks passed.")

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({
            "passed": False,
            "reasoning": ["Usage: python check.py <filepath>"]
        }, indent=2))
        sys.exit(1)
        
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(json.dumps({
            "passed": False,
            "reasoning": [f"Error: File not found at '{filepath}'"]
        }, indent=2))
        sys.exit(1)

    main(filepath)
