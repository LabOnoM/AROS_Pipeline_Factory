---
name: report_missing_input_error
description: A specialized error reporting skill to generate precise, unambiguous JSON reports for missing input halts.
license: MIT
skill-author: AROS_code_generator
---

# Report Missing Input Error

This skill provides a standardized mechanism for agents and tools to report failures specifically caused by missing or incomplete input data. It complies with the AROS policy for clear and actionable error reporting by generating a structured JSON report.

This mechanism is a specialization of the `articulate_failure_reasons` skill, tailored for input validation failures.

## GEPA Rule: Precise Missing Input Reporting

When a task halts due to missing input, the agent or tool **MUST** generate a JSON report containing the following fields:
- `missing_data`: The name or identifier of the missing piece of information (e.g., "api_key", "file_path").
- `expected_source`: Where the information was expected to be found (e.g., "user input", "environment_variable", "brain.db").
- `expected_type`: The expected data type of the missing information (e.g., "string", "integer", "list").

This ensures that the reason for failure is unambiguous and can be programmatically analyzed or presented to a user for correction.

## Key Capabilities
- **Structured JSON Output**: Generates reports in a consistent, machine-readable JSON format.
- **Exception-Driven**: Designed to work with a custom `MissingInputError` exception to capture all necessary details.
- **Precise and Unambiguous**: Clearly identifies what data is missing, where it was expected from, and what its type should be.

## Workflow
1.  **Input Validation**: A tool or agent validates its required inputs at the start of execution.
2.  **Raise Custom Exception**: If a required input is missing, the component raises a `MissingInputError`, passing the details of the missing data.
3.  **Catch and Report**: A global error handler or a `try...except` block catches the `MissingInputError`.
4.  **Invoke Skill**: The handler calls the `report_missing_input` function from this skill's implementation to generate the standardized JSON report.
5.  **Propagate Report**: The JSON report is logged or returned as the failure reason.

## Example Implementation

See `/mnt/Disk1/AntigravityInit/src/error_reporting_service.py` for the reference implementation.

```python
# from error_reporting_service import report_missing_input, MissingInputError

# try:
#     if "username" not in data:
#         raise MissingInputError(
#             message="User identifier is missing.",
#             missing_data="username",
#             expected_source="User-provided configuration",
#             expected_type="string"
#         )
# except MissingInputError as e:
#     error_report = report_missing_input(e)
#     print(error_report)
#
# Output:
# {
#     "error_type": "MissingInput",
#     "missing_data": "username",
#     "expected_source": "User-provided configuration",
#     "expected_type": "string"
# }

```
