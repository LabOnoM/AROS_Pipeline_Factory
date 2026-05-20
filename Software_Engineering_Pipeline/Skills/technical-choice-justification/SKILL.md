---
name: technical-choice-justification
description: "A policy defining the mandatory protocol for justifying technical choices within the AROS ecosystem. This skill enforces clarity, traceability, and accountability in decision-making."
license: MIT
skill-author: AROS-Mutation-Sweeper
---

# Technical Choice Justification Policy

This skill defines the mandatory protocol that all AROS agents and developers must adhere to when making technical choices that have a significant impact on the system's architecture, performance, or maintainability.

## Core Principles

1.  **Clarity**: The justification for a technical choice should be easy to understand and unambiguous.
2.  **Traceability**: It should be possible to trace a technical choice back to the requirements or constraints that prompted it.
3.  **Accountability**: The person or team making a technical choice is responsible for justifying it.
4.  **Transparency**: The justification for a technical choice should be publicly available to all stakeholders.

## MANDATORY SKILL INSTRUCTIONS:

### GEPA Rule: Explicit Justification for Technical Choices

**When an agent or developer makes a technical choice, they must provide a clear, concise, and specific explanation of the exact reason for their choice.** This explanation should be actionable and informative for other agents and developers.

The justification must include the following information:

*   The technical choice that was made.
*   The alternatives that were considered.
*   The trade-offs that were made.
*   The reasons for the final decision.

### GEPA Rule: Justification Criteria for Error Prevention

To prevent integration failures and performance degradation, all technical choice justifications **must** explicitly address the following criteria:

*   **Robustness**: How does the choice enhance the system's ability to handle errors, edge cases, and unexpected inputs? What is the recovery strategy?
*   **Compatibility**: How does the choice integrate with existing AROS components, skills, policies, and data formats? Are there any breaking changes?
*   **Performance**: What is the expected impact on speed, resource consumption (CPU, memory), and scalability? Justifications should be supported by metrics or benchmarks where applicable.

**Failure to adhere to these rules will result in a policy violation.**

## Policy Enforcement

This policy is enforced at the agent's core logic level. The `make_technical_choice()` function within the agent's execution loop will incorporate this policy. When a technical choice is made, the agent will format the justification according to the GEPA rules before proceeding.
