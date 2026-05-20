---
name: ki-quality-assurance-policy
description: Policy: Knowledge Item Quality Assurance
---

# Policy: Knowledge Item Quality Assurance
**Version:** 2.5
**ID:** AROS-POLICY-KI-QA-V2.5

---

## 1. Preamble

This document outlines the mandatory quality assurance policy for the creation and modification of all Knowledge Items (KIs) within the Antigravity Research OS (AROS). Adherence to this policy ensures that the AROS knowledge base remains accurate, coherent, and useful.

This version incorporates the GEPA proposal rule regarding a multi-tiered validation and refinement loop, including an external feedback step.

## 2. Core Principle

All knowledge creation or modification tasks MUST implement a robust, multi-tiered validation and refinement loop to ensure quality before being saved to the permanent knowledge base. This is a zero-tolerance policy; no KI may be committed without passing this validation process.

## 3. GEPA Error Prevention Rule: Minimum Viable Structure

To prevent the creation of severely truncated, incomplete, or "stub" Knowledge Items, all KI drafts are subject to a minimum completeness and quality threshold. This rule is automatically enforced by the `gtb-validator` skill.

*   **Rule Rationale:** Early GEPA cycles sometimes produced fragmented or empty KI drafts that polluted the knowledge base. This rule establishes a baseline for what constitutes a viable draft, ensuring that only reasonably complete thoughts are subjected to the full validation loop.

*   **Mandatory Checks:**
    *   **Minimum Length:** The draft content MUST exceed **250 characters**.
    *   **Structural Integrity:** The draft MUST contain at least **two distinct level-2 Markdown headers** (`##`). This enforces a basic structure, such as a summary followed by details, preventing monolithic blocks of text.

*   **Failure Condition:** If a draft fails to meet these criteria, the `gtb-validator` will immediately return `"passed": false` with a `reasoning` message indicating a structural or length failure. The agent MUST then revise the draft to meet these minimums before proceeding with further validation.

## 4. The Validation and Refinement Loop

The following process is mandatory for all agents and workflows that handle KI authoring or updates. The canonical implementation of this loop is the `iterative-validator` skill.

### 4.1. Triggers

This loop is triggered by:

*   **New KI Creation:** When a new Knowledge Item is being drafted.
*   **KI Modification:** When an existing Knowledge Item is updated or amended.

### 4.2. Evaluation Criteria

The primary tool for evaluation is the **Golden Test Battery (GTB)**, accessed via the `gtb-validator` skill.

*   **Success Condition:** The evaluation is considered successful if and only if the `gtb-validator` script returns a JSON output containing `"passed": true`.
*   **Task Type:** For all Knowledge Items, the `task_type` parameter for the validator MUST be set to `"knowledge_retrieval"`.

### 4.3. Multi-Tiered Refinement Process

Upon drafting the initial content, the agent MUST invoke the `iterative-validator` skill, which orchestrates the following process:

1.  **Tier 1: Automated Self-Correction (2 Attempts)**
    *   The `iterative-validator` first runs the `gtb-validator` on the draft.
    *   If it fails, the validator's feedback is used to automatically regenerate and improve the content.
    *   This automated cycle is repeated up to **two** times.

2.  **Tier 2: External Feedback and Final Correction (1 Attempt)**
    *   If the content still fails validation after two automated attempts, the `iterative-validator` **must** solicit feedback from an external source (e.g., a "Peer Review Agent" or another specialized validation service).
    *   This external feedback is then used to perform **one final regeneration** of the content.
    *   The `gtb-validator` is run a final time on this externally-informed draft.

### 4.4. Final State Determination

*   **On Success:** If the content passes validation at any point in the loop, the `iterative-validator` will save it to its final destination in the knowledge base, and the process is complete.
*   **On Failure:** If the content fails the third and final validation check (the one informed by external feedback), the `iterative-validator` will trigger a **fail-safe escalation protocol**. The content will not be saved, and the task will be flagged for review by a larger model persona or a human operator to prevent loops and resolve complex failures.
