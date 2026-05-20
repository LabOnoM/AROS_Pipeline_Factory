---
name: missing_input_reporting
description: Missing Input JSON Reporting
---


---
name: missing_input_reporting
description: Intercepts missing input halts and generates a precise, unambiguous JSON report detailing the missing input, its expected source, and type.
license: MIT
skill-author: AROS_code_generator
---

# Missing Input JSON Reporting

This skill provides a standardized mechanism for handling "missing input" halts. When a task cannot proceed because a required piece of data is missing, this skill ensures that the failure is reported in a precise, machine-readable JSON format, in compliance with AROS error handling policies.

## Key Capabilities
- **Custom Exception**: Defines a specific `MissingInputError` to clearly distinguish this halt condition from other exceptions.
- **Precise Reporting**: Generates a JSON object detailing exactly which data is missing.
- **Context-Aware**: The report includes the expected source (e.g., user input, database) and the expected data type (e.g., string, integer) of the missing data.
- **Unambiguous Format**: The structured JSON output is easy for other agents or monitoring systems to parse and act upon.

## Workflow
1.  **Raise Exception**: A function or process that validates its inputs raises the `MissingInputError` when a required piece of data is absent. The exception must be instantiated with the name of the missing data, its expected source, and its expected type.
2.  **Catch Exception**: A `try...except` block higher up in the call stack catches the `MissingInputError`.
3.  **Generate Report**: The `except` block calls the `generate_missing_input_report` function from this skill's script, passing the caught exception object to it.
4.  **Return JSON**: The function returns a formatted JSON string, which can then be logged, returned as an API response, or used for further automated decision-making.

## Audit-Ready Command

This command executes the `reporter.py` script, which runs a built-in simulation. The simulation attempts to run a process with incomplete data, catches the resulting `MissingInputError`, and prints the generated JSON report to standard output, demonstrating the full workflow.

```bash
python ~/.gemini/skills/missing_input_reporting/scripts/reporter.py
```
