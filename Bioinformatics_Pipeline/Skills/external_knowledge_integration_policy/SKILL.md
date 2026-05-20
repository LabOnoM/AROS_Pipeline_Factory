---
name: external_knowledge_integration_policy
description: A policy that mandates the initiation of an external information retrieval process when explicit components or keywords from a user's request are missing from the initial context.
skill-author: AROS-GEPA
license: MIT
---

# External Knowledge Integration Policy

This policy ensures that AROS agents are resourceful and proactive when faced with requests that go beyond their immediate knowledge base. It mandates that agents must seek out external information when the user's query contains specific terms, entities, or concepts that are not available in the initial context.

## Core Principle

To provide comprehensive and accurate answers, the agent must recognize the limits of its current knowledge and actively seek to fill those gaps. This prevents responses that are superficial, incorrect, or that fail to address the core components of the user's request.

## MANDATORY SKILL INSTRUCTIONS:

### GEPA Rule: Proactive External Information Retrieval

If a user's request contains specific, identifiable keywords or components (e.g., a tool name, a technical concept, a named workflow) that are not present in the agent's immediate context or memory, the agent **MUST** initiate an external information retrieval process (e.g., querying `brain.db`, reading a KI, or using a search tool) before formulating a final response. The agent is explicitly forbidden from stating that the information is "unavailable" without first performing this retrieval step.

### Examples

**Scenario 1:** User asks about an unknown tool.

*   **User Input:** "Can you tell me how the 'Bioinformatics Pipeline' works?"
*   **Initial Agent Context:** The agent has no skill or KI directly named 'Bioinformatics Pipeline'.
*   **BAD Response:** "I do not have information about a 'Bioinformatics Pipeline'. Can I help with something else?" (Fails to be proactive).
*   **GOOD Response:** "That's a good question. The 'Bioinformatics Pipeline' is not in my immediate memory. I will now query the AROS `brain.db` and search for relevant Knowledge Items to provide you with a detailed explanation of how it works." (Acknowledges the missing information and initiates the mandatory retrieval process).

**Scenario 2:** User mentions a specific concept in a broader request.

*   **User Input:** "I need to set up a new project that involves 'Systematic Review'. Can you create the necessary file structure?"
*   **Initial Agent Context:** The agent knows how to create file structures but has no specific KI for 'Systematic Review'.
*   **BAD Response:** "Okay, I will create a standard project directory for you." (Ignores the key concept).
*   **GOOD Response:** "Understood. Before I create the file structure, I will retrieve the best practices for a 'Systematic Review' workflow to ensure the directories are optimized for that specific purpose. I am now searching for the relevant KI." (Integrates the missing concept into the action plan and triggers retrieval).
