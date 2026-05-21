import subprocess
import json
import os

VALIDATOR_PATH = "/home/owner03/.gemini/skills/gtb-validator/validate.py"

def run_validator(filepath):
    result = subprocess.run(["python", VALIDATOR_PATH, filepath, "knowledge_retrieval"], capture_output=True, text=True)
    return json.loads(result.stdout)

def test_invalid_ki_todo():
    filepath = "/tmp/invalid_ki_todo.md"
    content = """
# Test KI
This is a test KI.
## Validation
Validation will be done here.
## Section
TODO: add more text to make it longer than 150 characters.
Adding more text here to ensure the length is greater than 150 characters.
This is necessary to pass the length check.
Adding more text here to ensure the length is greater than 150 characters.
This is necessary to pass the length check.
    """
    with open(filepath, "w") as f:
        f.write(content)
    
    res = run_validator(filepath)
    assert not res["passed"], "Should fail due to TODO"
    assert "TODO" in res["reasoning"] or "placeholder" in res["reasoning"].lower()
    print("test_invalid_ki_todo passed.")

def test_invalid_ki_missing_validation():
    filepath = "/tmp/invalid_ki_missing_validation.md"
    content = """
# Test KI
This is a test KI.
## Section
Adding more text here to ensure the length is greater than 150 characters.
This is necessary to pass the length check.
Adding more text here to ensure the length is greater than 150 characters.
This is necessary to pass the length check.
Adding more text here to ensure the length is greater than 150 characters.
This is necessary to pass the length check.
    """
    with open(filepath, "w") as f:
        f.write(content)
    
    res = run_validator(filepath)
    assert not res["passed"], "Should fail due to missing validation section"
    assert "Validation" in res["reasoning"] or "validation" in res["reasoning"].lower()
    print("test_invalid_ki_missing_validation passed.")

def test_valid_ki():
    filepath = "/tmp/valid_ki.md"
    content = """
# Test KI
This is a valid test Knowledge Item. It is designed to pass all the checks in the GTB Validator.

## Description
This is a very informative section that contains more than enough characters to satisfy the length requirement. The quick brown fox jumps over the lazy dog multiple times.

## Validation
To validate this KI, simply read through its contents and confirm that there are no placeholders and that all sections have content.
    """
    with open(filepath, "w") as f:
        f.write(content)
    
    res = run_validator(filepath)
    assert res["passed"], f"Should pass, but failed with: {res.get('reasoning')}"
    assert res.get("judgment_score", 0) >= 7.0, "Score should be >= 7.0"
    print("test_valid_ki passed.")

if __name__ == "__main__":
    test_invalid_ki_todo()
    test_invalid_ki_missing_validation()
    test_valid_ki()
    print("All tests passed successfully.")
