---
name: persona-assignment-policy
description: This policy governs the assignment of skills and personas to tasks to ensure efficient, reliable, and logically sound execution.
license: MIT
skill-author: AROS-Core
---

# AROS Policy: Skill & Persona Assignment Workflow

**Policy ID:** GEPA-POL-002
**Status:** Active
**Version:** 1.0

## 1.0 Purpose

This policy governs the assignment of skills and personas to tasks within the AROS ecosystem. Its primary purpose is to ensure that task execution is efficient, reliable, and logically sound by mapping tasks to the most appropriate and capable skills and agent personas available.

## 2.0 Scope

This policy applies to all agents and automated workflows operating within the Antigravity Research OS. It covers the entire lifecycle of task execution, from initial task definition and skill/persona selection to final review and validation.

## 3.0 Core Principles (GEPA Rules)

The following GEPA-derived rules are mandatory for all assignments:

### 3.1 The Rule of Functional Relevance

**Skills assigned to a task must be functionally relevant and capable of executing the task's explicit requirements.**

- **Guidance:** A skill is "functionally relevant" if its documented purpose, capabilities, and allowed tools directly map to the verbs and nouns of the task goal. Do not assign a data visualization skill to a file system cleanup task.
- **Validation:** Before execution, the orchestrator must perform a dry-run check comparing the task's requirements against the selected skill's `SKILL.md`. Mismatches must be flagged, and an alternative skill must be selected.

### 3.2 The Rule of Parsimony

**Assign the minimum number of skills required to complete the task.**

- **Guidance:** Avoid assigning multiple skills when a single, more comprehensive skill can achieve the same outcome. This reduces complexity and potential points of failure.
- **Validation:** The orchestrator should prefer skills that cover a broader range of the task's requirements.

### 3.3 The Rule of Persona-Capability Alignment (NEW)

**An agent's assigned persona MUST align with the primary capability required by the sub-task.**

- **Guidance:** Personas are specialized roles (e.g., `code_generator`, `qa_engineer`, `data_analyst`). When a task is deconstructed, each sub-task must be mapped to a persona that possesses the necessary context for that function. A task to write Python code must be assigned to a `code_generator`. A task to review and test that code must be assigned to a `qa_engineer`.
- **Validation:** Before dispatching a sub-task, the orchestrator **MUST** use the `persona_capability_validator` skill to verify the assignment. Mismatches must trigger a re-assignment to a suitable agent or halt the task if no capable agent is available. This prevents capability gaps and ensures high-quality execution.
