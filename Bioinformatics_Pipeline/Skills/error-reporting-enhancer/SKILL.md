---
name: error-reporting-enhancer
description: "Intercepts missing input halts and generates a precise, unambiguous JSON report detailing the missing input, its expected source, and type. This enhances the existing error reporting mechanism."
license: Apache 2.0
skill-author: AROS Self-Correction Subsystem
status: active
---

# Error Reporting Enhancer

This skill provides a robust mechanism for generating detailed JSON error reports when a process halts due to missing critical inputs. It standardizes the error format, making it easier for automated systems to parse and for developers to debug.

## When to Use

This skill should be integrated into any skill or workflow that performs input validation. When a required input is missing, instead of just logging a simple text message, you should call this skill to generate a structured JSON report. It is a direct implementation of the policy to provide precise, unambiguous error reports for missing inputs.

## How it Works

The core of this skill is the `scripts/generate_missing_input_report.sh` script.

### `generate_missing_input_report.sh`

This script takes three mandatory arguments and generates a JSON file in `~/.gemini/antigravity/logs/error_reports/`.

**Usage:**

```bash
~/.gemini/skills/error-reporting-enhancer/scripts/generate_missing_input_report.sh <missing_input> <expected_source> <expected_type>
```

**Arguments:**

1.  `missing_input`: The name of the parameter or variable that is missing (e.g., `API_KEY`, `input_file_path`).
2.  `expected_source`: Where the input was expected to be found (e.g., `environment_variable`, `skill_argument`, `config_file`).
3.  `expected_type`: The expected data type of the input (e.g., `string`, `integer`, `filepath`).

**Example Invocation:**

```bash
~/.gemini/skills/error-reporting-enhancer/scripts/generate_missing_input_report.sh 'OPENAI_API_KEY' 'environment_variable' 'string'
```

**Example Output JSON (`<report_id>.json`):**

```json
{
  "error_type": "MissingInput",
  "report_id": "...",
  "timestamp": "...",
  "severity": "High",
  "source_skill": "error-reporting-enhancer",
  "details": {
    "missing_input_name": "OPENAI_API_KEY",
    "expected_source": "environment_variable",
    "expected_type": "string"
  },
  "message": "Execution halted due to a missing critical input. The input 'OPENAI_API_KEY' (expected type: string) was not found in the expected source: 'environment_variable'."
}
```

## Integration into Policies

This skill should be referenced by policies like `policy-missing-input-handler`. The policy should mandate that instead of a simple halt, skills must invoke this reporting mechanism to ensure that the reason for the halt is captured in a structured and actionable format.
