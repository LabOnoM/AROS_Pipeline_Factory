---
name: pipeline-orchestrator
description: A Python-based tool for orchestrating and validating end-to-end operational pipelines.
license: MIT
skill-author: AROS-code-generator
status: alpha
---

# Pipeline Orchestrator

This skill provides a scaffolding for creating, running, and validating complex workflows. It enforces error prevention rules by checking inputs, outputs, and states at each step of a pipeline.

## When to Use

- Use this skill to define and execute multi-step operational pipelines.
- Use it when you need to ensure the integrity of a workflow by validating the state between steps.
- Ideal for automating complex sequences of commands where failure in one step should prevent subsequent steps from running.

## Core Features

-   **Workflow Definition**: Define pipelines as a series of steps in simple Python files.
-   **Step-by-Step Execution**: The orchestrator runs each step of the workflow in sequence.
-   **Stateful Validation**: Define pre-conditions and post-conditions for each step to validate the pipeline's state.
-   **Error Prevention**: Enforces the GEPA Error Prevention Rule by providing a framework for including validation and testing in all pipelines.

## Prerequisites

-   Python 3.8+

## Quick Check

```bash
python -m py_compile ~/.gemini/skills/pipeline-orchestrator/orchestrator/main.py
python ~/.gemini/skills/pipeline-orchestrator/orchestrator/main.py --help
```

## Workflow

1.  **Define a Workflow**: Create a Python file that defines a `Workflow` object. This object contains a list of `Step` objects.
2.  **Define Steps**: Each `Step` should have a name, a shell command to execute, and optional `pre_conditions` and `post_conditions`.
3.  **Define Validation Rules**: The conditions are functions that return `True` or `False`. The orchestrator provides a set of common validation functions (e.g., `file_exists`, `file_not_empty`).
4.  **Run the Orchestrator**: Execute the orchestrator from the command line, pointing it to your workflow definition file.

## Validation

To ensure the reliability of pipelines created with this orchestrator, the following validation practices are mandatory:

1.  **Unit and Smoke Tests**: All custom validation functions and complex workflows should be accompanied by tests in a `tests/` directory.
2.  **GEPA Readiness**: The orchestrator is designed to be compliant with the GEPA Readiness Check. Avoid using placeholders like `TODO` or `FIXME` in your workflow definitions.
3.  **Mandatory Validation Section**: Any new pipeline skill created using this orchestrator must include a "Validation" section in its `SKILL.md` file, detailing how to verify the pipeline's correctness.

This scaffolding tool itself includes a suite of unit tests to validate its own functionality. You can run them using:
`python -m unittest discover ~/.gemini/skills/pipeline-orchestrator/tests`
