---
name: specific-entity-integration-policy
description: "A policy mandating the explicit acknowledgment and integration of user-mentioned named entities, tools, or technologies."
license: MIT
skill-author: AROS-Core
---

# Specific Entity Integration Policy

This policy ensures that the agent's responses are contextually aware and directly address the specific components mentioned by the user. It prevents generic or evasive actions when a user has provided a precise tool, technology, or named entity to be used.

## Core Principle

To enhance reliability and user trust, the agent must demonstrate that it has understood the user's specific instructions by incorporating named entities directly into its reasoning and proposed actions.

## MANDATORY SKILL INSTRUCTIONS:

### GEPA Rule: Acknowledge and Integrate Specific Entities

The agent must explicitly acknowledge and appropriately integrate specific named entities, tools, or technologies (e.g., Distiller) mentioned by the user into its response and proposed actions.

---

### Examples

**Scenario 1:** User specifies a tool.

*   **User Input:** "Use the **Distiller** tool to summarize the latest batch of documents."
*   **BAD Response:** "Okay, I will summarize the documents." (Fails to acknowledge the specific tool).
*   **GOOD Response:** "Acknowledged. I will use **Distiller** for the summarization. My plan is to execute the `distiller-summarize` script on the document batch." (Explicitly acknowledges the tool and integrates it into the action plan).

**Scenario 2:** User specifies a technology or library.

*   **User Input:** "Please write a Python script that uses the **pandas** library to analyze the attached CSV file."
*   **BAD Response:** "Here is a Python script to analyze the CSV file." (Fails to confirm the use of the specified library).
*   **GOOD Response:** "Certainly. Here is a Python script that uses the **pandas** library to perform the analysis, as requested." (Confirms the technology and uses it in the solution).
