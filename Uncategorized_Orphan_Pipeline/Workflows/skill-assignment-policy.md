# AROS Policy: Skill Assignment & Task Definition Workflow

**Policy ID:** GEPA-POL-001
**Status:** Active
**Version:** 1.2

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

- **Guidance:** Avoid chaining multiple skills together if a single, more comprehensive skill exists. If a task requires both data processing and visualization, and a single skill performs both, it is preferred over using two separate skills.
- **Validation:** The proposed execution plan should be checked for redundant skill assignments.

### 3.3 The Rule of End-to-End Pipeline Integrity

**Bioinformatics pipeline skills must manage the complete workflow from initial inputs to a final, analysis-ready output.**

- **Guidance:** A skill that runs a pipeline (e.g., RNA-seq, variant calling) must not be a "partial" wrapper around a single command. It must encompass the full, logical sequence of steps, including input validation, quality control, core processing, and final output generation. For example, an RNA-seq skill must handle everything from FASTQ validation to generating a count matrix, not just the alignment step.
- **Validation:** The `SKILL.md` for a pipeline skill must explicitly document its start and end points (e.g., "Input: FASTQ files, Output: Annotated VCF"). It must also list the sequence of core tools it orchestrates. Skills that wrap single sub-commands are only permissible if clearly defined as modular "helper" skills.

### 3.4 The Rule of Persona Specialization

**Assign and utilize distinct personas for different sub-tasks within a complex workflow to leverage specialized capabilities or perspectives.**

- **Guidance:** For a multi-step task, consider assigning different agent personas to each step. For example, in a "research and report" workflow, a 'researcher' persona could handle data gathering, a 'writer' persona could draft the report, and a 'critic' persona could review and refine the output. This leverages the specialized training of each persona.
- **Validation:** For any workflow involving more than two distinct steps, the execution plan must specify the persona assigned to each step. If no personas are specified, the plan must include a justification for using a single generalist persona.

### 3.5 The Rule of Contextual Appropriateness

**The assigned persona and invoked skills must be appropriate and relevant to the specific sub-task's nature and required output.**

- **Guidance:** A 'code_generator' persona should be assigned to tasks requiring code generation, not writing a research paper summary. Similarly, a 'data_scientist' persona should utilize data analysis and visualization skills, not system administration tools. The chosen persona and skills must form a logical and coherent pairing for the task at hand.
- **Validation:** The execution plan must be audited to ensure the persona assigned to each sub-task has a logical alignment with the skills being invoked for that sub-task. For instance, a 'Creative Writer' persona invoking a 'database_query' skill would be flagged for review.
