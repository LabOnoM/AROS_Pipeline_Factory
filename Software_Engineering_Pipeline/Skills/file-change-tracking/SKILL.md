---
name: file-change-tracking
description: A policy and skill for tracking, validating, and managing file changes within the AROS system, incorporating GEPA error prevention and mandatory file identification.
license: MIT
skill-author: AROS_System_Architect
original-source: addyosmani/agent-skills/git-workflow-and-versioning
---

# File Change Tracking Policy and Skill

This document outlines the mandatory policy and the supporting skill for tracking, validating, and managing all file system changes initiated or observed by AROS agents. This is a critical component for system integrity, auditability, and error prevention.

## Core Principles

-   **Integrity**: All file modifications must be intentional and validated.
-   **Auditability**: Every change must be traceable to its origin and purpose.
-   **Error Prevention**: Proactive measures are in place to prevent unintended or corrupt file changes.

## GEPA Error Prevention Rule Integration

This skill directly integrates with the `gepa_error_prevention_patch` skill to ensure that any attempts to modify critical system files or operations that result in validation failures are subjected to the GEPA retry and fallback mechanism.

-   **Sub-Task Monitoring**: File modification operations (e.g., `write_local_file`, `run_shell_command` involving file system writes) are treated as sub-tasks managed by `gepa_error_prevention_patch`.
-   **Validation Integration**: If a file modification fails internal validation (e.g., checksum mismatch, schema validation for KIs/Skills, or the `gtb-validator` for content), it will trigger a retry through GEPA.
-   **Dynamic Fallback**: Upon reaching the GEPA retry threshold, this skill will coordinate with `gepa_error_prevention_patch` to either attempt an alternative file management strategy or escalate to a larger model persona for deeper analysis and resolution.

## Mandatory File Identification Rule

All file operations, especially writes, MUST include explicit identification of the file's purpose and expected content structure.

-   **Purpose Declaration**: When creating or modifying a file, the agent MUST internally declare the intended purpose of the file (e.g., "KI update," "new skill," "temporary log").
-   **Content Schema Adherence**: For structured files (e.g., `SKILL.md`, `metadata.json`, `workflow.md`), the agent MUST ensure the content adheres to the expected schema or format. Failure to do so will trigger GEPA error prevention.
-   **Unique Naming**: Temporary files, drafts, and backups MUST use clearly identifiable naming conventions to prevent conflicts and ensure clarity.

## Workflow

1.  **Initiate File Operation**: An agent intends to create, modify, or delete a file.
2.  **Pre-Validation (if applicable)**: If the operation involves content creation (e.g., writing a new Skill or KI), the content MUST first pass `gtb-validator` checks, as enforced by `content-drafting-capability`.
3.  **GEPA Management**: The file operation is wrapped by the `SubTaskExecutionManager` from `gepa_error_prevention_patch`.
4.  **Exec