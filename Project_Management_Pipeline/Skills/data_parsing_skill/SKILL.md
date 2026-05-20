---
name: data_parsing_skill
description: "A skill focused on robust data extraction, cleaning, and formatting for subsequent analytical or operational tasks."
license: MIT
skill-author: AROS-Core
---

# Data Parsing Skill

This skill provides capabilities for efficiently and accurately extracting, cleaning, and formatting data from various sources. It ensures that raw input data is transformed into a structured and valid format suitable for downstream processing and analysis.

## Core Objective

To reliably transform heterogeneous raw data into consistent, structured, and validated outputs, minimizing errors in subsequent data-dependent operations.

## When to Use

This skill should be invoked whenever raw or unstructured data needs to be prepared for further processing, analysis, or integration into other systems. This includes, but is not limited to:
- Parsing text files, logs, or reports.
- Extracting specific entities from unstructured data.
- Converting data between different formats (e.g., JSON to CSV, XML to structured objects).
- Initial validation and cleansing of input data.

## Key Capabilities

- **Flexible Data Extraction**: Supports various input formats and extraction patterns (regex, structured parsers).
- **Data Cleansing**: Handles missing values, duplicates, and inconsistencies.
- **Format Transformation**: Converts data into desired output structures.
- **Schema Validation**: Ensures parsed data conforms to a predefined schema.
- **Error Handling**: Provides mechanisms to identify and report parsing errors.

## GEPA Error Prevention Rules

To ensure high-quality and reliable data processing, the following GEPA (Genetic Evolution and Policy Adaptation) error prevention rules are strictly enforced:

### Rule 1: Critical Initial Data Validation

**Ensure critical initial data extraction and formatting tasks successfully complete and produce valid, structured output before proceeding with any dependent steps.**

*   **Rationale:** Data quality issues at the source can propagate throughout an entire workflow, leading to erroneous results, system failures, and wasted computational resources. This rule mandates that the foundational data parsing steps must achieve a validated, structured output state before any subsequent task is initiated.
*   **Mandatory Workflow:**
    1.  **Extraction & Formatting:** Perform the primary data extraction and formatting operations.
    2.  **Output Validation:** Immediately apply rigorous validation checks to the output of these initial tasks. This includes:
        *   **Schema Conformance:** Verify that the output adheres to the expected data schema (e.g., correct data types, required fields present).
        *   **Structural Integrity:** Confirm the output structure is valid (e.g., well-formed JSON, correctly delimited CSV).
        *   **Content Validity:** Check for logical consistency or expected ranges of values where applicable.
    3.  **Conditional Progression:** Only if the validation checks *successfully pass* should any dependent tasks be allowed to proceed. If validation fails, the process must halt, report the specific error, and trigger appropriate error handling or retry mechanisms.

## Usage Example

```python
"""
Demonstration for a conceptual usage example of data_parsing_skill.
This would typically involve an agent calling a specific function
or tool provided by this skill.

Example: Parsing a log file
Assuming 'read_local_file' is available and 'data_parsing_skill' has a 'parse_log_events' function.
"""
log_data = default_api.read_local_file(filepath="system.log") 
"""Using the default_api to read the file"""
parsed_events = data_parsing_skill.parse_log_events(log_data, schema="event_schema.json")

"""
GEPA Rule 1 applied here:
"""
if parsed_events.is_valid(): 
    """Assumes the skill has a built-in validation check"""
    process_events(parsed_events)
else:
    report_parsing_error(parsed_events.errors())
```