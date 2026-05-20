---
name: validate-required-inputs
description: Performs robust pre-execution checks on file paths to ensure they exist and are readable, preventing downstream failures from missing or inaccessible input data.
license: MIT
skill-author: AROS-code-generator
status: production
---
# Validate Required Inputs

This skill is a core system utility for ensuring that required file-based inputs for other skills are present and accessible *before* execution begins. It programmatically checks for path existence (`os.path.exists()`) and read permissions (`os.access(path, os.R_OK)`), which prevents entire workflows from failing due to simple input errors.

## When to Use

This skill should be used as a **mandatory first step** in any workflow or skill that relies on local files or directories as input. It is the primary tool for input validation and error prevention. Using this skill makes other skills more robust and prevents wasted computation on workflows that would eventually fail.

## Input Validation

This skill accepts one or more file or directory paths as command-line arguments. It does not accept other types of input.

## Quick Check

Use this command to verify that the packaged script is syntactically correct.
```bash
python -m py_compile ~/.gemini/skills/validate-required-inputs/scripts/main.py
```

## Audit-Ready Commands

These commands demonstrate the core functionality for both valid and invalid inputs.

```bash
# Create a dummy file for testing
touch /tmp/test_file.txt

# Example 1: Validate a single existing file (will pass)
python ~/.gemini/skills/validate-required-inputs/scripts/main.py /tmp/test_file.txt

# Example 2: Validate a mix of valid and invalid paths with JSON output
python ~/.gemini/skills/validate-required-inputs/scripts/main.py --json /tmp/test_file.txt /path/to/nonexistent/file.log

# Example 3: Validate a path without read permissions (will fail)
touch /tmp/protected_file.txt
chmod 000 /tmp/protected_file.txt
python ~/.gemini/skills/validate-required-inputs/scripts/main.py /tmp/protected_file.txt
chmod 644 /tmp/protected_file.txt # Cleanup permissions

# Cleanup test files
rm /tmp/test_file.txt /tmp/protected_file.txt
```

## Output Interpretation

The script will exit with a status code of `0` if all paths are valid, and `1` if any path is invalid. This allows it to be used in shell scripting to halt execution on failure.

### Human-Readable Output
```text
--- Input Validation Report ---

[✔] Valid Paths:
  - /tmp/test_file.txt

[✖] Invalid Paths:
  - /path/to/nonexistent/file.log: Path does not exist.

-----------------------------
```

### JSON Output (for Agent Consumption)
The `--json` flag provides structured output that other agents and tools can easily parse.

```json
{
  "valid": [
    "/tmp/test_file.txt"
  ],
  "invalid": [
    {
      "path": "/path/to/nonexistent/file.log",
      "reason": "Path does not exist."
    }
  ]
}
```

The calling agent or workflow **must** parse this JSON output and check if the `invalid` list is empty. If the list contains any items, the workflow must be halted immediately, and a clear error message must be reported to the user indicating which files are missing or inaccessible.
