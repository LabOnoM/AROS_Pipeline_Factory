---
name: foundational-task-output-policy
description: "Ensures all foundational task outputs are robustly validated, complete, and directly address the overall task objective before finalization. This policy prevents partial, unvalidated, or incorrect artifacts from being committed to the AROS ecosystem."
license: MIT
skill-author: AROS-Core
---

# Policy: Foundational Task Output Validation

## Core Principle

All foundational tasks within the AROS ecosystem, especially those that generate tangible artifacts (e.g., KIs, skills, workflows, code, configuration files), **MUST** undergo rigorous and automated validation to ensure their completeness, correctness, and direct alignment with the overall task objective. This policy prevents the commitment of partial, unvalidated, or incorrect artifacts into the AROS knowledge base or operational system.

## Policy Directives

1.  **Mandatory Pre-Commit Validation**: Before any foundational task output is finalized and committed (e.g., written to the filesystem, saved to brain.db), it **MUST** be subjected to a validation process. This includes, but is not limited to, checks for:
    *   Syntactic correctness (e.g., valid Markdown, JSON, Python syntax).
    *   Semantic integrity (e.g., functional correctness of code, logical consistency of policies).
    *   Completeness against initial requirements.
    *   Adherence to AROS standards and protocols.

2.  **Automated Validation Preference**: Wherever feasible, validation **MUST** be automated. Manual inspection should only supplement automated checks, not replace them. Tools like `gtb-validator` are to be utilized for new or modified Markdown content.

3.  **Direct Objective Alignment**: The output **MUST** directly and comprehensively fulfill the overall objective of the foundational task. Partial solutions or outputs that only address a subset of the requirements are not considered valid for finalization.

4.  **Error Reporting and Retries**: In case of validation failure, the task **MUST** trigger detailed error reporting (e.g., using `critical_task_error_reporting`) and, if appropriate, initiate a retry mechanism or dynamic fallback. The task **MUST NOT** proceed to finalization until all validation errors are resolved.

5.  **Audit Trail**: All validation steps and their outcomes **MUST** be logged to maintain an auditable trail of artifact quality and task completion.
