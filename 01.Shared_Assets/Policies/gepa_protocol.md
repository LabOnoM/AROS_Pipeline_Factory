---
cpcp_asset: true
canonical_location: "01.Shared_Assets/Policies/gepa_protocol.md"
consumers:
  - Grant_Write_Pipeline
  - Manuscript_Write_Pipeline
last_cpcp_review: "2026-05-11"
---
# AROS Policy: GEPA Implementation and Iterative Refinement

**Policy ID:** AROS-POL-GEPA-001
**Status:** ACTIVE
**Applies to:** `evolution_agent` and any other agent participating in the modification or creation of AROS Skills, KIs, Workflows, or Policies.

## 1. Overview

This policy governs the implementation of GEPA (Genetic Evolution through Persona Augmentation) proposals. It ensures that all modifications to the AROS system are robust, validated against the Golden Test Battery (GTB), and integrated in a controlled manner. The cornerstone of this policy is the mandatory use of a validation and refinement loop with built-in safeguards.

## 2. Core Protocol: Plan-Draft-Validate-Commit

All agents tasked with implementing a GEPA proposal must follow this four-step process.

### Step 1: Draft Generation

Based on an approved GEPA proposal, the agent generates the new or modified content for the target artifact (e.g., a Skill's `SKILL.md`, a KI artifact, or a Workflow). This initial draft is held in a temporary memory or file location and MUST NOT be immediately written to the official AROS filesystem.

### Step 2: Iterative Validation & Refinement Loop

Before committing any changes, the agent MUST enter a validation loop.

**Logic:**
1.  **Initialize Safeguards:** A `retry_count` is initialized to `0`. The `max_retries` limit is set to `3`.
2.  **Persist Draft:** The current version of the draft content is written to a temporary file (e.g., `/tmp/gepa_draft.md`).
3.  **Execute Validation:** The agent executes the `gtb-validator` skill on the temporary file to assess its quality and compliance against the Golden Test Battery.
4.  **Evaluate Results:**
    *   **On Success (`passed: true`, `score >= 7.0`):** The draft is considered validated. The agent exits the loop and proceeds to **Step 3: Commit to Filesystem**.
    *   **On Failure (`passed: false`, `score < 7.0`):** The validation has failed. The agent proceeds to the refinement and retry logic below.

**Mandatory Refinement Clause:**
> The agent must implement an iterative refinement loop that triggers content rewriting or modification whenever validation tasks indicate failure or non-compliance. The agent MUST use the `reasoning` field from the GTB validation output as the primary driver for modifications.

**Circuit Breaker Logic:**
*   The `retry_count` is incremented by 1.
*   If `retry_count` is less than `max_retries`, the agent rewrites the draft based on the failure reasoning and repeats the loop from step 2.
*   If `retry_count` reaches `max_retries`, the loop is terminated, and the agent MUST trigger the **Step 4: Escalation Protocol**. This `circuit_breaker` is a critical safeguard to prevent infinite execution loops.

### Step 3: Commit to Filesystem

Upon successful validation from the loop, the agent is authorized to write the validated content from the temporary file to its final destination within the AROS filesystem (`~/.gemini/skills/`, `~/.gemini/antigravity/knowledge/`, etc.).

### Step 4: Escalation Protocol

If the Iterative Validation Loop fails `max_retries` times, the following escalation procedure is automatically triggered:

1.  **Halt Execution:** The current agent ceases its modification attempts.
2.  **Preserve Context:** The agent packages the original proposal, all failed drafts, and the full history of GTB validation feedback.
3.  **Escalate:** The task is re-assigned to a designated larger model persona. This senior persona has the explicit goal of resolving the complex validation failures using the preserved context.

## 3. Compliance

Adherence to this protocol is mandatory. Any direct modification of core AROS files without passing through this Plan-Draft-Validate-Commit cycle is a policy violation.
