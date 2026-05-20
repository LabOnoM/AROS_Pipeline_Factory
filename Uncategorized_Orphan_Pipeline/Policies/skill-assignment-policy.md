# AROS Policy: Skill Assignment & Task Definition Workflow

**Policy ID:** GEPA-POL-001
**Status:** Active
**Version:** 1.4

## 1.0 Purpose

This policy governs the assignment of skills to tasks within the AROS ecosystem. Its primary purpose is to ensure that task execution is efficient, reliable, and logically sound by mapping tasks to the most appropriate and capable skills available in the AROS Skill library.

## 2.0 Scope

This policy applies to all agents and automated workflows operating within the Antigravity Research OS. It covers the entire lifecycle of task execution, from initial task definition and skill selection to final review and validation.

## 3.0 Core Principles (GEPA Rules)

The following GEPA-derived rules are mandatory for all skill assignments:

### 3.1 The Rule of Functional Relevance

**Skills assigned to a task must be functionally relevant and capable of executing the task's explicit requirements.**

- **Guidance:** A skill is "functionally relevant" if its documented purpose, capabilities, and allowed tools directly map to the verbs and nouns of the task goal.
- **Validation:** Before execution, the orchestrator must perform a dry-run check comparing the task's requirements against the selected skill's `SKILL.md`. Mismatches must be flagged.

### 3.2 The Rule of Parsimony

Assign the minimum number of skills required to complete the task. Avoid assigning redundant or overlapping skills.

### 3.3 The Rule of Resource Availability (GEPA Error Prevention)

**Before execution, the orchestrator MUST verify that all environmental and tool dependencies for a selected skill are met.**

- **Guidance:** This is an error-prevention rule designed to preemptively catch failures caused by missing tools, insufficient permissions, or invalid configurations. The skill's `SKILL.md` must contain a `Resource-Requirements` section that explicitly lists all dependencies.
- **Validation:** The orchestrator must parse the `Resource-Requirements` section of the skill's manifest and perform the following checks:
    - **Tool Availability:** Verify that any required command-line tools (e.g., `git`, `python`, `uv`) are present in the system's `$PATH`.
    - **File Permissions:** Check for read/write access to any required files or directories.
    - **API Keys & Environment Variables:** Ensure that necessary environment variables or API keys are set and non-empty.
- **Failure Condition:** If any check fails, the task MUST NOT be executed. The agent must report the failure using the `agent-communication` policy, specifying the exact unmet dependency.

### 3.4 The Rule of Objective Completion (GEPA Error Prevention)

**Ensure all explicit user objectives, such as writing a final artifact to the filesystem and providing user notifications, are completed as final steps once all dependencies are met and outputs are validated.**

- **Guidance:** This rule prevents premature task termination or incomplete fulfillment of user requests. Core logic and data processing should be completed and validated *before* final, user-facing actions are taken.
- **Validation:** The task workflow must be structured to place file-writing and notification steps at the end of the execution chain. The orchestrator should verify that these final steps are only triggered after all preceding validation and processing steps have passed successfully.

### 3.5 The Rule of Task Decomposition and Persona Specialization

**Objectives must be decomposed into logical, sequential tasks, with appropriate personas assigned to each task to leverage specialized capabilities effectively.**

- **Guidance:** For a multi-step task, decompose the objective into smaller sub-tasks. Then, assign different agent personas (e.g., 'code_generator', 'code_reviewer', 'tester') to each sub-task. This ensures that each step is handled by an agent with the most appropriate mindset and skills. For example, a 'code_generator' persona focuses on writing efficient code, while a 'code_reviewer' persona focuses on identifying potential bugs and improving code quality.
- **Validation:** The workflow definition must explicitly define the sub-tasks and the persona for each sub-task. The orchestrator must verify that the assigned agent for a sub-task assumes the specified persona.
