---
name: task-execution-engine
description: SKILL: TaskExecutionEngine
---

The TaskExecutionEngine file is located at `/home/owner03/.gemini/skills/TaskExecutionEngine/SKILL.md`.

Here is the full content of the file:

```markdown
---
name: TaskExecutionEngine
description: This skill provides a robust, error-handled mechanism for executing complex, multi-step tasks that involve code generation, file manipulation, and validation.
license: MIT
skill-author: AROS-Mutation-Sweeper
---

# SKILL: TaskExecutionEngine

## Description
This skill provides a robust, error-handled mechanism for executing complex, multi-step tasks that involve code generation, file manipulation, and validation. It ensures that critical operations produce verifiable outputs and prevents silent failures.

## MANDATORY SKILL INSTRUCTIONS
- **Ensure Verifiable Output**: All code generation or modification tasks executed through this engine MUST produce a verifiable output. This can be a file path to the generated code, a confirmation log, or a status object. The engine must check for the existence and validity of this output before reporting success.

## Example Usage
```python
task_engine = TaskExecutionEngine()
result = task_engine.execute(
    task_name="generate_new_skill",
    steps=[
        {"tool": "code_generator", "params": {"prompt": "Create a new skill...", "output_file": "/tmp/new_skill.py"}},
        {"tool": "file_validator", "params": {"filepath": "/tmp/new_skill.py"}}
    ]
)
if result.success:
    print(f"Task completed. Verifiable output at: {result.output}")
else:
    print(f"Task failed: {result.error}")
```

## SKILL IMPLEMENTATION

To execute this skill, use the following `ACTION` format:

```python
# ACTION: execute_task
# PARAMS:
#   task_name: "generate_new_skill"
#   steps:
#     - tool: "code_generator"
#       params:
#         prompt: "Create a new skill..."
#         output_file: "/tmp/new_skill.py"
#     - tool: "file_validator"
#       params:
#         filepath: "/tmp/new_skill.py"
```
```