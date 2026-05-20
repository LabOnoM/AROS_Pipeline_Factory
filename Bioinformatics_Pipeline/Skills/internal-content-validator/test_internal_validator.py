# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import os
import sys
import json
import subprocess

VALIDATOR_SCRIPT = "/home/owner03/.gemini/skills/internal-content-validator/validate_internal.py"

TEST_CASES = [
    {
        "name": "valid_draft",
        "content": '''---
name: my-cool-skill
description: Does cool things.
skill-author: TestBot
---
# My Cool Skill

Some intro text.

## Example Usage
Here is how you use it.
''',
        "expected_pass": True,
        "expected_reason_substrings": []
    },
    {
        "name": "missing_yaml",
        "content": '''# Missing YAML Frontmatter

This file has no yaml at all.

## Workflow
Step 1.
''',
        "expected_pass": False,
        "expected_reason_substrings": ["Missing or improperly formatted YAML frontmatter block"]
    },
    {
        "name": "missing_yaml_keys",
        "content": '''---
name: missing-keys
description: Missing author
---
# Missing Keys

## Instructions
Do this.
''',
        "expected_pass": False,
        "expected_reason_substrings": ["Missing or empty required YAML frontmatter key: 'skill-author'."]
    },
    {
        "name": "missing_context",
        "content": '''---
name: no-context
description: Missing sections
skill-author: TestBot
---
# No Context

It has frontmatter but no operational headers.
''',
        "expected_pass": False,
        "expected_reason_substrings": ["Missing operational context."]
    },
    {
        "name": "missing_both",
        "content": '''# Nothing Here
Just random text.
''',
        "expected_pass": False,
        "expected_reason_substrings": [
            "Missing or improperly formatted YAML frontmatter block",
            "Missing operational context."
        ]
    }
]

def run_tests():
    all_passed = True
    
    for case in TEST_CASES:
        filename = f"/tmp/{case['name']}.md"
        with open(filename, 'w') as f:
            f.write(case['content'])
            
        print(f"Running test: {case['name']}...")
        result = subprocess.run(
            [sys.executable, VALIDATOR_SCRIPT, filename],
            capture_output=True,
            text=True
        )
        
        try:
            output = json.loads(result.stdout)
        except json.JSONDecodeError:
            print(f"  [FAIL] Could not parse JSON output for {case['name']}:\n{result.stdout}\nSTDERR:\n{result.stderr}")
            all_passed = False
            continue
            
        passed = output.get("passed")
        reasoning = output.get("reasoning", [])
        
        if passed != case['expected_pass']:
            print(f"  [FAIL] Expected pass={case['expected_pass']}, got {passed}")
            all_passed = False
            continue
            
        # Check reasons
        if not case['expected_pass']:
            reasoning_str = " ".join(reasoning)
            for sub in case['expected_reason_substrings']:
                if sub not in reasoning_str:
                    print(f"  [FAIL] Expected reason substring '{sub}' not found in: {reasoning_str}")
                    all_passed = False
                    break
            else:
                print(f"  [PASS] {case['name']}")
        else:
            print(f"  [PASS] {case['name']}")
            
    if all_passed:
        print("\nAll automated tests PASSED successfully.")
    else:
        print("\nSome automated tests FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
