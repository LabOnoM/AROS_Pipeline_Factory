---
name: out-of-scope-request-handler
description: A policy for gracefully handling user requests that do not map to a predefined set of supported functions, providing a helpful list of available alternatives.
license: MIT
skill-author: AROS_code_generator
---

# Out-of-Scope Request Handling Policy

This skill implements a system prompt rule and validation layer to map incoming user requests against a predefined dictionary of supported functions. If a request does not match, it returns a graceful fallback message that lists the supported alternatives.

## Key Capabilities
- **Request Validation**: Checks incoming requests against a dictionary of known, supported functions.
- **Graceful Fallback**: If a request is not supported, it provides a clear error message.
- **Alternative Discovery**: The fallback message includes a list of all supported functions, guiding the user toward a valid request.

## Workflow
1.  **Define Supported Functions**: A Python dictionary (`SUPPORTED_FUNCTIONS`) maps valid function names to their descriptions. This serves as the ground truth for the system's capabilities.
2.  **Receive User Request**: The system receives a request from the user, which is treated as a string to be validated.
3.  **Validate Request**: The script checks if the user's request string exists as a key in the `SUPPORTED_FUNCTIONS` dictionary.
4.  **Process or Reject**:
    *   If the request is **valid** (it exists in the dictionary), the system proceeds with the corresponding workflow.
    *   If the request is **invalid** (out of scope), the system triggers the fallback mechanism.
5.  **Return Fallback Message**: The fallback message informs the user that the request is not supported and provides a formatted list of all available functions and their descriptions.

## Quick Check

Use this command to verify that the packaged script is syntactically correct.
```bash
python -m py_compile ~/.gemini/skills/out-of-scope-request-handler/scripts/main.py
```

## Audit-Ready Commands

These commands demonstrate the core functionality for both a valid (in-scope) and an invalid (out-of-scope) request.

### In-Scope Request (Success Case)
This command simulates a valid user request that matches a key in the `SUPPORTED_FUNCTIONS` dictionary.
```bash
python ~/.gemini/skills/out-of-scope-request-handler/scripts/main.py "monitor_co2_tank"
```

### Out-of-Scope Request (Fallback Case)
This command simulates an invalid user request, triggering the graceful fallback message with a list of alternatives.
```bash
python ~/.gemini/skills/out-of-scope-request-handler/scripts/main.py "summarize_document"
```
