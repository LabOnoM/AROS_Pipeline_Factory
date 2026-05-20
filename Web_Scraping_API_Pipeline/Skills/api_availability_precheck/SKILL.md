---
name: api_availability_precheck
description: A policy and skill to perform a preliminary check on an external API's availability before initiating a task that relies on it.
license: MIT
skill-author: AROS_code_generator
---

# API Availability Pre-Check Policy

This skill implements the GEPA proposal for API availability checks. It provides a simple, robust way to verify if an external service is online before attempting to use it.

## GEPA Rule

**GEPA-Rule-004: Proactive API Availability Check**

Before initiating any task that relies on an external API, perform a preliminary check (e.g., via a ping or status endpoint) to ensure the required API is available and accessible to the executing persona. The check must handle timeouts and return a clear status.

## Key Capabilities
- **Endpoint Check**: Verifies API availability by sending a lightweight HTTP request.
- **Timeout Handling**: Gracefully handles and reports APIs that do not respond within a specified time.
- **Clear Status Reporting**: Returns a structured JSON output with the status (`available`, `unavailable`, `timeout`), HTTP status code, and reason.
- **Dependency**: Requires the `requests` Python library.

## Workflow
1.  **Receive Target**: The skill is invoked with a target URL and an optional timeout.
2.  **Perform Check**: The script sends an HTTP `HEAD` request to the URL. A `HEAD` request is used as it's more lightweight, fetching only headers.
3.  **Evaluate Response**:
    - If a 2xx status code is received, the API is considered 'available'.
    - If any other status code is received, it's marked as 'unavailable'.
    - If the request times out, it's marked as 'timeout'.
    - If a connection error occurs, it's marked as 'unavailable'.
4.  **Return JSON Status**: The script prints the final outcome in a machine-readable JSON format.

## Quick Check

Use this command to verify that the packaged script is syntactically correct.
```bash
python -m py_compile ~/.gemini/skills/api_availability_precheck/scripts/main.py
```

## Validation

The skill includes a test suite to ensure its reliability. To run the tests:
```bash
python -m unittest ~/.gemini/skills/api_availability_precheck/tests/test_main.py
```

## Audit-Ready Commands

These commands demonstrate the core functionality for different scenarios.

```bash
# Example 1: Check a known available endpoint (should succeed)
python ~/.gemini/skills/api_availability_precheck/scripts/main.py --url "https://api.github.com/zen"

# Example 2: Check a non-existent endpoint (should report unavailable)
python ~/.gemini/skills/api_availability_precheck/scripts/main.py --url "http://127.0.0.1:9999/nonexistent"

# Example 3: Check with a very short timeout to force a timeout status
python ~/.gemini/skills/api_availability_precheck/scripts/main.py --url "https://httpbin.org/delay/5" --timeout 2
```
