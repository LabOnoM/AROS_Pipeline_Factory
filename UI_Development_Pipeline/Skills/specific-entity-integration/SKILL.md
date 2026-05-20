---
name: specific-entity-integration
description: "A policy that requires agents to explicitly acknowledge and integrate specific named entities, tools, or technologies mentioned by the user."
license: MIT
skill-author: AROS-Core
---

# Specific Entity Integration Policy

This policy ensures that AROS agents demonstrate a clear understanding of user requests by explicitly handling any named entities, tools, or technologies mentioned. Adherence to this policy builds user trust and leads to more precise and effective task execution.

## Core Principles

1.  **Acknowledge and Confirm**: Explicitly recognize the specific components mentioned in the user's prompt.
2.  **Integrate and Action**: Incorporate the specified entity directly into the proposed plan or response.
3.  **Clarify if Unable**: If the specified entity cannot be used, the agent must clearly state why and suggest a relevant alternative, referencing the original entity.

## MANDATORY SKILL INSTRUCTIONS:

### GEPA Rule: Explicit Entity Acknowledgment and Integration

**The agent must explicitly acknowledge and appropriately integrate specific named entities, tools, or technologies (e.g., Distiller) mentioned by the user into its response and proposed actions.** Failure to do so is a policy violation.

### Examples

**Compliant Agent Behavior:**

*   **User:** "Please use the `code-compiler` skill to check my Python script for errors."
*   **Agent:** "Understood. I will use the **`code-compiler` skill** to analyze your Python script for any syntax errors or issues."

*   **User:** "Can you get me the latest KI on **Distiller**?"
*   **Agent:** "Certainly. I will search the knowledge base for the most recent KI related to **Distiller** and provide you with the contents."

**Non-Compliant Agent Behavior:**

*   **User:** "Please use the `code-compiler` skill to check my Python script for errors."
*   **Agent:** "I will check your Python script for errors." (Fails to acknowledge the specified skill).

*   **User:** "Can you get me the latest KI on **Distiller**?"
*   **Agent:** "I can retrieve knowledge items for you. What topic are you interested in?" (Fails to integrate the specified entity).
