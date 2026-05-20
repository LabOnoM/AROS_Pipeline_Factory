---
name: pipeline-diagnostic-reporting
description: Pipeline Diagnostic Reporting Skill
---


---
name: pipeline-diagnostic-reporting
description: Generates a structured diagnostic report for a pipeline run, detailing successes, failures, and actionable recommendations.
license: MIT
skill-author: AROS_code_generator
---

# Pipeline Diagnostic Reporting Skill

This skill provides a standardized, machine-readable diagnostic report for automated pipeline executions. It uses a structurally enforced schema to ensure that critical information about a pipeline's status is always present.

## Key Capabilities
- **Structured Schema**: Utilizes Python dataclasses to define and enforce a strict JSON output schema.
- **Dynamic Simulation**: Simulates a pipeline run, including potential random failures, to generate realistic report data.
- **Required Fields**: Guarantees the presence of `execution_status`, `successes`, `failures`, and `actionable_recommendations` in every report.
- **Machine-Readable**: Outputs a JSON object, making it easy to integrate with monitoring dashboards, alerting systems, or other automated workflows.
- **Testable**: Includes a suite of unit tests to validate the script's functionality and schema compliance, adhering to AROS quality standards.

## Workflow
1.  **Execution**: The `generate_report.py` script is invoked.
2.  **Simulation**: A pipeline run is simulated with several steps. Some steps may randomly fail for demonstration purposes.
3.  **Data Structuring**: The results of the simulation are populated into a `DiagnosticReport` dataclass object.
4.  **Recommendation Generation**: Based on any failures, a list of actionable recommendations is generated.
5.  **Serialization**: The populated dataclass object is serialized into a well-formatted JSON string.
6.  **Output**: The JSON string is printed to standard output.

## Output Schema
The skill outputs a JSON object with the following structure:
```json
{
  "pipeline_name": "string",
  "run_id": "string (uuid)",
  "execution_status": "string (SUCCESS or FAILURE)",
  "successes": [
    {
      "step_name": "string",
      "status": "string (SUCCESS)",
      "duration_seconds": "float",
      "details": "object"
    }
  ],
  "failures": [
    {
      "step_name": "string",
      "status": "string (FAILURE)",
      "duration_seconds": "float",
      "details": "object"
    }
  ],
  "actionable_recommendations": [
    "string"
  ]
}
```

## Quick Check

Use this command to verify that the packaged script is syntactically correct.
```bash
python -m py_compile ~/.gemini/skills/pipeline-diagnostic-reporting/scripts/generate_report.py
```

## Audit-Ready Commands

These commands demonstrate the core functionality and validation process.

### 1. Generate a sample report
This command executes the script to produce a simulated diagnostic report in JSON format.
```bash
python ~/.gemini/skills/pipeline-diagnostic-reporting/scripts/generate_report.py
```

### 2. Run Mandatory Unit and Smoke Tests
This command runs the built-in unit tests to verify the script's correctness and ensure it conforms to the required output schema. This is a mandatory step for skill validation.
```bash
python -m unittest ~/.gemini/skills/pipeline-diagnostic-reporting/tests/test_report_generation.py
```
