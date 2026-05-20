---
name: secure_code_execution
description: SKILL: secure-code-execution
---

# SKILL: secure-code-execution

name: secure-code-execution
description: Implements the 'Secure Code Execution' skill, providing a concrete Python implementation for pre-execution environment verification.
license: MIT
skill-author: AROS_code_generator

# Secure Code Execution

## Overview

This skill provides a concrete implementation of the pre-flight checks mandated by the `agent-environment-provisioning` policy. It ensures that execution environments natively verify access to necessary data paths and libraries before running generated code, preventing common runtime errors.

## Key Capabilities

-   **Filesystem Validation:** Verifies the existence and read/write permissions of specified file paths.
-   **Shell Command Validation:** Checks for the availability of required shell commands in the system's PATH.
-   **Python Library Validation:** Ensures that all required Python libraries are installed and importable.

## Core Component: `EnvironmentValidator`

The logic is encapsulated in the `EnvironmentValidator` class within the `secure_code_execution.py` script.

### Workflow

1.  **Instantiate Validator**: An instance of the `EnvironmentValidator` is created.
2.  **Define Requirements**: The agent specifies lists of required read paths, write paths, shell commands, and Python libraries.
3.  **Execute Verification**: The `verify` method is called with the defined requirements.
4.  **Check Result**:
    -   If `verify` returns `True`, all checks have passed, and the agent can proceed with code execution.
    -   If `verify` returns `False`, the agent can retrieve a list of specific errors using the `get_errors` method and report them, halting execution as per the `agent-environment-provisioning` policy.

## Audit-Ready Command

This command demonstrates the functionality of the skill by running a self-test that simulates various success and failure scenarios for environment validation.

```bash
python ~/.gemini/skills/secure_code_execution/secure_code_execution.py
```
