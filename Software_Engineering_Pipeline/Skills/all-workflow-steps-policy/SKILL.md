---
name: all-workflow-steps-policy
description: A policy that enforces strict context tracking for all artifacts processed in AROS workflows.
license: MIT
skill-author: AROS-Mutation-Sweeper
---

# Policy: Artifact Context Tracking in Workflows

This document outlines the 'Artifact Context Tracking' policy, a mandatory meta-protocol for all AROS agents executing multi-step workflows. The primary purpose is to ensure data lineage, prevent context-switching errors, and guarantee that each step in a workflow operates on the correct and intended artifact.

## GEPA Rule

**GEPA-Rule-ACT-001: Artifact-Context-Tracking**

Each step within a workflow **MUST** explicitly define its input and output artifact context. The context, including a unique identifier for the artifact (e.g., file path, KI name, database primary key), must be passed from the producing step to the consuming step. A step must fail if its required input artifact context is missing, invalid, or ambiguous.

## When to Use

- **Always:** This policy applies to every step of every automated workflow managed by the AROS orchestrator.
- It is triggered whenever a task is decomposed into a sequence of operations where the output of one operation becomes the input of another.

## Guiding Principles

- **Explicit is Better than Implicit:** Do not rely on assumptions about the "current" or "active" artifact. Each task step must declare what it is working on.
- **Context as a Parameter:** The artifact context should be treated as a mandatory parameter for any function or tool call that comprises a workflow step.
- **Chain of Custody:** The workflow orchestrator is responsible for maintaining the "chain of custody" by capturing the output context from a step and providing it as the input context to the subsequent step.

## Implementation and Enforcement

- **Tool & Skill Mutations:** All skills designed to be used in workflows must be updated to include a mandatory `artifact_context` parameter in their execution methods. This parameter will receive the identifier of the data/artifact to be processed.
- **Orchestrator Logic:** The AROS orchestrator will be mutated to enforce this policy. Before dispatching a task to a skill, it will verify that the `artifact_context` is present and valid. If a skill completes and produces a new artifact, the orchestrator will capture its context for the next step.
- **Error Handling:** If a skill is called without a valid `artifact_context`, it must raise a `ContextNotProvided` error. If a step receives a context that points to a non-existent or inaccessible artifact, it must raise an `ArtifactNotFound` error.

## Example Scenario

**Workflow:** `Code Generation -> QA -> Review`

1.  **Step 1: Code Generation**
    *   **Input:** User prompt.
    *   **Action:** Generates Python code.
    *   **Output Artifact Context:** `{"path": "/tmp/generated_code_abc123.py"}`.

2.  **Step 2: Automated QA**
    *   **Input Artifact Context:** `{"path": "/tmp/generated_code_abc123.py"}` (Received from Step 1).
    *   **Action:** Lints and tests the specified file.
    *   **Output:** Test results (no new artifact, so context is passed through or nullified).

3.  **Step 3: Review**
    *   **Input Artifact Context:** `{"path": "/tmp/generated_code_abc123.py"}` (Received from Step 1/2).
    *   **Action:** Loads the specified file for an agent to review.
    *   **Output:** Review comments.

**Non-Compliant Example:** The QA step assumes it should look for "the most recent file in /tmp". This is ambiguous and violates GEPA-Rule-ACT-001. The file path must be passed explicitly.
