---
name: articulate_failure_reasons
description: A skill to catch exceptions and construct detailed, specific, and actionable failure reports in compliance with AROS communication policies.
license: MIT
skill-author: AROS_code_generator
---

# Articulate Failure Reasons

This skill provides a standardized mechanism for agents and tools to report failures. It ensures that when an operation fails, the resulting error message is not vague but instead provides clear, concise, and actionable information, adhering to the "Explicit Reason for Failure" GEPA rule defined in the `agent-communication` policy.

## Key Capabilities
- **Standardized Reporting**: Generates failure reports in a consistent format.
- **Exception-Driven**: Directly translates caught exceptions into user-friendly, informative messages.
- **Context-Aware**: Incorporates the operational context into the report to specify what was being attempted during the failure.
- **Actionable Suggestions**: Provides helpful next steps for common, identifiable errors like `FileNotFoundError` or `PermissionError`.

## Workflow
1.  **Wrap Operation**: An agent wraps a potentially failing operation (e.g., a file access attempt, an API call) in a `try...except` block.
2.  **Catch Exception**: Upon failure, the `except` block catches the exception object.
3.  **Invoke Skill**: The agent calls the `articulate_failure` function from this skill's script.
4.  **Provide Context**: The agent passes the exception object and a string descr