---
name: policy-missing-input-handler
description: Defines the standard AROS policy for handling missing or incomplete inputs during skill execution. This is a policy document, not an executable skill.
license: Apache 2.0
skill-author: AROS Self-Correction Subsystem
status: active
policy-type: execution-guardrail
---
# Policy: Missing Input Handler

This document outlines the mandatory AROS policy for handling missing critical inputs in all executable skills. Its purpose is to ensure robust, predictable, and safe skill execution by preventing workflows from proceeding with incomplete data.

## 1. Guiding Principle: "Validate First"

**The absolute first step** of any skill's workflow, before any computation, file I/O, or resource allocation, MUST be the validation of all required inputs.

## 2. Mandatory `SKILL.md` Section

Every executable skill MUST include an `## Input Validation` section in its `SKILL.md`. This section must clearly define:
- The scope of acceptable inputs.
- A list of critical, non-negotiable input parameters.
- The exact behavior and error message to be emitted if validation fails.

## 3. Execution Flow on Missing Input

When a critical input is found to be missing, the skill MUST immediately halt execution. It should not attempt to perform partial processing or make assumptions unless a specific improvisation policy (like `missing-input-handling-and-improvisation`) is explicitly applicable and documented for that skill.

## 4. Mandatory Reporting Action

Upon detecting a missing input and halting, the skill MUST NOT emit a simple text error message. Instead, it **is mandatory** to invoke the `error-reporting-enhancer` skill to generate a structured JSON report. This ensures that all input validation failures are logged in a consistent, machine-readable format for system-wide monitoring and debugging.

**Action:** Execute the following script with the appropriate details:

```bash
/home/owner03/.gemini/skills/error-reporting-enhancer/scripts/generate_missing_input_report.sh <missing_input_name> <expected_source> <expected_type>
```

### Parameters:
-   `<missing_input_name>`: The name of the parameter that is missing (e.g., `api_key`, `input_file`).
-   `<expected_source>`: Where the input was expected (e.g., `environment_variable`, `config_file`, `argument`).
-   `<expected_type>`: The expected data type (e.g., `string`, `filepath`, `integer`).

## 5. Implementation in Scripts

Skill scripts MUST implement this reporting logic at the beginning of their execution path.

**Python Example:**
```python
import argparse
import sys
import subprocess

def report_missing_input(name, source, type):
    """Invokes the standard AROS error reporting script."""
    script_path = "/home/owner03/.gemini/skills/error-reporting-enhancer/scripts/generate_missing_input_report.sh"
    try:
        # Halt execution and generate the standardized report
        subprocess.run([script_path, name, source, type], check=True)
    except subprocess.CalledProcessError as e:
        print(f"CRITICAL: Failed to invoke the error reporting skill: {e}", file=sys.stderr)
    except FileNotFoundError:
        print(f"CRITICAL: Error reporting script not found at {script_path}", file=sys.stderr)
    
    # Exit with a non-zero status code to indicate failure
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Path to the input file.')
    parser.add_argument('--output', help='Path to the output file.')
    args = parser.parse_args()

    if not args.input:
        # Instead of a simple print statement, call the mandatory reporting function.
        report_missing_input(name="--input", source="argument", type="filepath")

    # --- Main script logic begins here ONLY if validation passes ---
    print(f"Processing input file: {args.input}")

if __name__ == '__main__':
    main()
```

This updated policy ensures that all AROS skills are robust, fail predictably, and contribute to a structured, system-wide error logging mechanism, which is critical for autonomous operation and debugging.
