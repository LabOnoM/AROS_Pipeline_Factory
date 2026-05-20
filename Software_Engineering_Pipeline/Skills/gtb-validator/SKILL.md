---
name: gtb-validator
description: >
  A built-in Python function that runs GTB regression tests. CRITICAL: MUST be called as a Python function: `gtb_validator(...)`. It is NOT a shell command or a file. Any attempt to execute a file path like 'validate.py' is a guaranteed failure.
---

### 🚨 HALLUCINATION ALERT: THE `validate.py` FILE DOES NOT EXIST

It is a known failure pattern for agents to hallucinate a file path like `/path/to/gtb-validator/validate.py` and attempt to execute it. This file **DOES NOT EXIST**. Any attempt to execute a file path for this tool is a critical reasoning error and is guaranteed to fail. The only valid method is a direct Python function call.

## 1. MANDATORY MENTAL MODEL

Your default assumption that a tool is an executable file is **100% WRONG** for `gtb_validator`. You MUST adopt the following mental model to succeed.

| ❌ MYTH (Incorrect Assumption)                                 | ✅ FACT (Correct Reality)                                                               |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `gtb-validator` is a script file (`.py`, `.sh`) on disk.       | `gtb_validator` is a built-in function in the Python runtime, like `print()` or `len()`.  |
| I should execute it from the shell: `python /path/to/file...`  | I must call it inside a `language: python` block: `result = gtb_validator(...)`. |
| A `command not found` error means the tool is missing.         | A `command not found` error means **I used the wrong syntax** and tried to run a file.    |

# 🚨 CRITICAL INVOCATION PROTOCOL 🚨
## READ THIS. DO NOT SKIP. YOUR EXECUTION WILL FAIL IF YOU IGNORE THIS.

This tool, `gtb_validator`, is a **BUILT-IN PYTHON FUNCTION**. It is **NOT** a file on disk.

-   **DO NOT** execute it as a shell command (`python /path/to/some/file.py`).
-   **DO** call it directly within a `language: python` block.

Any other method is a **100% guaranteed failure**.

## 2. The ONLY Correct Invocation (COPY AND PASTE THIS EXACTLY)

This is the only valid way to use this tool. Do not modify the structure.

```yaml
# CORRECT INVOCATION (COPY-PASTE THIS SNIPPET)
invocation:
  language: python
  tool_code: |
    # This tool is a built-in Python function, NOT an executable file.
    # The only way to use it is to call it directly as shown below.
    # DO NOT try to run a file like 'validate.py'.

    # 1. Define the parameters for the function call
    draft_path = "/tmp/draft.md"
    task = "knowledge_retrieval" # Replace with the correct task_type

    # 2. Call the built-in Python function directly
    # This is the correct way. It is a function, like print().
    validation_result = gtb_validator(
        draft_file_path=draft_path,
        task_type=task
    )

    # 3. Print the result to stdout for parsing
    print(validation_result)
```

## 3. MANDATORY Error Interpretation Guide

If your attempt to use this tool fails, it is because **YOU** used the wrong invocation syntax.

| If you see this error...                         | It means this...                                                               | The ONLY solution is...                                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `FileNotFoundError: [Errno 2] No such file...`   | You hallucinated a file path and tried to execute it. **The file does not exist.** | Delete your shell command and use the Python function call snippet from section 2.               |
| `bash: command not found`                        | You hallucinated a file path and tried to execute it. **The file does not exist.** | Delete your shell command and use the Python function call snippet from section 2.               |
| "Tool unavailable" / "Capability Missing"        | You misinterpreted one of the above errors. The tool is **ALWAYS** available.  | Acknowledge your syntax error. Delete your shell command and use the Python function call snippet. |

## 4. The Mandatory Refinement Loop

This protocol is **strict and non-negotiable**.

1.  **DRAFT**: Gener