import os
import subprocess
import json
import unittest

VALIDATOR_SCRIPT = "/home/owner03/.gemini/skills/gtb-validator/validate.py"

class TestGTBValidator(unittest.TestCase):

    def setUp(self):
        self.bad_draft_path = "/tmp/bad_draft.md"
        self.good_draft_path = "/tmp/good_draft.md"
        
        # Negative test draft: attempts to complete without using validation findings
        # For instance, missing "Validation" section and containing TODO
        bad_content = """# Bad Draft Skill
This is a bad draft because it does not have a validation section.
It also has a placeholder: TODO: implement this.
"""
        with open(self.bad_draft_path, "w") as f:
            f.write(bad_content)
            
        # Positive test draft: refined based on findings (added validation section, removed TODOs, long enough, no empty sections)
        good_content = """# Good Draft Skill

This is a good draft that meets all the requirements of the GTB validator.

## Overview
This skill does wonderful things and is complete.

## Implementation Details
Here are the implementation details. It is very robust and well tested.

## Practical Utility
This section is practical.

## Validation
To validate this skill, run the test suite and ensure all tests pass.
The validation process is thorough and ensures no regressions occur.
"""
        with open(self.good_draft_path, "w") as f:
            f.write(good_content)

    def tearDown(self):
        if os.path.exists(self.bad_draft_path):
            os.remove(self.bad_draft_path)
        if os.path.exists(self.good_draft_path):
            os.remove(self.good_draft_path)

    def run_validator(self, draft_path):
        result = subprocess.run(
            ["python", VALIDATOR_SCRIPT, draft_path, "knowledge_retrieval"],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)

    def test_negative_validation(self):
        # Negative test: task attempts to complete without using validation findings
        print("\nRunning Negative Test...")
        output = self.run_validator(self.bad_draft_path)
        self.assertFalse(output["passed"], "Negative test failed: Validator should have failed the draft.")
        print(f"Validation correctly failed. Reason: {output['reasoning']}")

    def test_positive_validation(self):
        # Positive test: task completes after successfully executing validation and refining based on findings
        print("\nRunning Positive Test...")
        output = self.run_validator(self.good_draft_path)
        self.assertTrue(output["passed"], "Positive test failed: Validator should have passed the draft.")
        print(f"Validation correctly passed. Reason: {output['reasoning']}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
