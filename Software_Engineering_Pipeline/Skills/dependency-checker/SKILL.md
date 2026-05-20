---
name: dependency-checker
description: Checks for the existence of file-based dependencies before running a command.
license: MIT
skill-author: AROS_code_generator
---

# Dependency Checker

This skill provides a simple way to verify that all required file dependencies are present before executing a command. It helps prevent downstream errors by failing fast if an expected input or output from a previous step is missing.

## Workflow

1.  **Define Dependencies**: Identify the list of files or directories that must exist for a subsequent command to succeed.
2.  **Run Checker**: Execute the `check.py` script, passing the list of required paths as arguments.
3.  **Conditional Execution**: Only if the checker script exits with a status code of 0, proceed to run the main command.

## Usage

```bash
# Check for a single file
python ~/.gemini/skills/dependency-checker/scripts/check.py --paths /path/to/required/file.txt

# Check for multiple files
python ~/.gemini/skills/dependency-checker/scripts/check.py --paths /path/to/file1.txt /path/to/file2.csv

# Use in a script with conditional execution
python ~/.gemini/skills/dependency-checker/scripts/check.py --paths /tmp/input.csv && \
    echo "Dependency met, running next command" || \
    echo "Dependency check failed"
```

## Quick Check

```bash
# Create a dummy file for testing
touch /tmp/test_file.txt

# This should succeed
python ~/.gemini/skills/dependency-checker/scripts/check.py --paths /tmp/test_file.txt

# This should fail and print an error
python ~/.gemini/skills/dependency-checker/scripts/check.py --paths /tmp/non_existent_file.txt

# Clean up the dummy file
rm /tmp/test_file.txt
```
