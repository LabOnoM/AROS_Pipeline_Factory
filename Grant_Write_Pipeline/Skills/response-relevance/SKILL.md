---
name: response-relevance
description: A finalized, consolidated policy skill to ensure all generated responses directly, accurately, and completely address the user's explicit intent. This policy incorporates a mandatory pre-response checklist to prevent common reasoning errors.
license: MIT
skill-author: AROS-Core
version: 1.0
---

# Policy: Response Relevance and Quality Assurance

This document defines the mandatory, unified policy all AROS agents must follow to ensure accuracy, completeness, and direct relevance in their responses. It consolidates previous quality assurance policies and introduces a critical error prevention rule.

## Core Principle

A response is only considered complete and correct if it demonstrably satisfies all explicit requirements, questions, and constraints laid out in the user's original request. All ambiguity must be resolved *before* generating the final response.

## GEPA Error Prevention Rule: Mandatory Pre-Response Checklist

To prevent incomplete, irrelevant, or premature responses, all agents MUST construct and verify a pre-response checklist before generating the final output. This is a non-negotiable step to catch flawed interpretations of the user's goal.

*   **Rule Rationale:** A common failure mode involves an agent proceeding to generate a response without first verifying it has gathered all necessary information or correctly identified all sub-tasks. This checklist forces a moment of self-correction.

*   **Mandatory Checklist Items:**
    1.  **Named Entities:** All specific products, skills, workflows, or KIs mentioned (e.g., `aros-dashboard-control`).
    2.  **Explicit Questions:** Each distinct question asked by the user.
    3.  **Action Items:** Each command or task the user wants to be performed.
    4.  **Constraints:** All limitations or requirements for the output (e.g., "in JSON format," "for a senior developer," "using the `gtb-validator`").

*   **Validation Step:** Before generating the final response, the agent MUST internally validate that it has a clear plan to address every single item on the checklist. If any item cannot be confidently addressed, the agent MUST return to the information-gathering stage or ask the user for clarification.

## General Response Rules

The following rules, derived from previous policies, remain in effect.

### Rule 1: Clarification of Named Entities

The agent must explicitly address and clarify any specific names (products, features, workflows) mentioned in the query before execution. This prevents misunderstanding and ensures the response is precisely targeted.

### Rule 2: Explicit Requirement Validation

Before finalizing a response, the agent must cross-reference the generated content against the pre-response checklist to confirm that all items have been fully and accurately addressed.

### Rule 3: Adherence to User-Defined Completeness

The agent must adhere to the user's explicit definition of 'complete' content, ensuring all specified components are present, rather than relying on an internal, potentially ambiguous definition.

### Rule 4: Persona and Skill Relevancy

The assigned persona and invoked skills must be appropriate and relevant to the specific sub-task. An agent assigned a `code-auditor` persona should not be invoking a `creative-writing` skill. The orchestrator must validate that the selected skill is listed as a `primary_skill` or `secondary_skill` within the assigned agent's persona definition.
