---
name: skill-assignment-policy
description: AROS Policy: Skill Assignment & Task Definition Workflow
---

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

- **Guidance:** A skill is "functionally relevant" if its documented purpose, capabilities, and allowed tools directly map to the verbs and nouns of the task goal. Do not assign a data visualization skill to a file system cleanup task.
- **Validation:** Before execution, the orchestrator must perform a dry-run check comparing the task's requirements against the selected skill's `SKILL.md`. Mismatches must be flagged, and an alternative skill must be selected.

### 3.2 The Rule of Parsimony

**Assign the minimum number of skills required to complete the task.**

- **Guidance:** Avoid assigning multiple skills that have overlapping functionality. If a single skill can accomplish the task, it should be preferred over a combination of skills. This reduces complexity and potential for conflicts.
- **Validation:** The skill selection process should include a step to identify and prune redundant skills from the assignment list.

### 3.3 The Rule of Environmental Pre-Validation

**Before executing a task, an agent MUST validate that all environmental requirements are met.**

- **Guidance:** This is a mandatory pre-flight check to prevent runtime errors. The agent must use the `agent-environment-provisioning` skill to verify filesystem permissions, shell command availability, and network connectivity as required by the task.
- **Validation:** The AROS orchestrator MUST invoke the `agent-environment-provisioning` skill after skill assignment but before dispatching the task for final execution. Failure of any check MUST halt the task and trigger an error report as defined in the `agent-communication` policy.

### 3.4 The Rule of Orchestrated Execution (New)

**All operational pipelines, defined as a sequence of three or more skills intended for repeated use, MUST be executed via an approved AROS orchestrator tool.**

-   **Guidance:** This GEPA error prevention rule is designed to stop the creation of brittle, ad-hoc, and difficult-to-debug sequential skill executions. For any complex workflow, a dedicated orchestrator provides essential features like state management, error handling, and logging that are otherwise absent from simple, linear script-like execution.
-   **Validation:** The AROS execution environment will monitor for direct, sequential `invoke_skill` calls from a single agent process. If a sequence of three or more is detected without an orchestrator context, a policy violation warning will be logged, and future versions may halt execution.

### 3.5 The Rule of Persona Alignment

**The persona assigned to a sub-task MUST possess the necessary capabilities and specialization for that sub-task's domain.**

-   **Guidance:** To prevent execution errors and ensure high-quality output, the assigned agent persona must be appropriate for the task at hand. Assigning a generic persona to a specialized task is a policy violation. The orchestrator is responsible for this mapping.
    -   **Coding & Scripting Tasks:** MUST be assigned to a `code_generator` or `software_engineer` persona.
    -   **Verification & QA Tasks:** MUST be assigned to a `qa_engineer` or `code_reviewer` persona.
    -   **Data Analysis & Visualization Tasks:** MUST be assigned to a `data_analyst` persona.
    -   **System Administration & File System Tasks:** MUST be assigned to a `sysadmin` persona.
-   **Validation:** During task breakdown and before dispatching a sub-task, the orchestrator MUST verify that the target agent's persona matches the sub-task's metadata tags (e.g., `domain: 'coding'`, `domain: 'qa'`). A mismatch MUST halt the task and trigger a replanning cycle to assign a correct persona.
