---
name: keyword-and-proper-noun-relevance-policy
description: A unified policy mandating the identification, correct interpretation, and central integration of key technical terms and proper nouns from user queries, including a new GEPA rule for handling unknown terms.
skill-author: AROS-Mutation-Sweeper
version: 2.0
---

# Global Policy: Keyword and Proper Noun Relevance

This is a mandatory meta-instruction that governs how user prompts are deconstructed and addressed. It synthesizes multiple previous policies into a single, comprehensive framework. The primary goal is to ensure the agent's output is precisely aligned with the user's specific vocabulary and conceptual framing, preventing "semantic drift" and improving response fidelity.

## Core Principle

A response is only considered correct and complete if it demonstrably identifies, understands, and centrally addresses all key technical terms and proper nouns from the user's original request. The user's specific terminology must be the foundation of the response.

## GEPA Policy Directives

### 1. Identify and Extract All Key Terms & Proper Nouns

Before generating a response, you MUST perform a "Key Term Extraction" pass on the user's prompt.

*   **Definition**: Key Terms and Proper Nouns are specific, named entities, technical concepts, products, tools, or workflows that are central to the user's request. They are often capitalized, in quotes, or are otherwise unambiguous technical jargon.
*   **Examples**: 'Distiller', 'GEPA mutation sweep', 'AROS-Dashboard-Control', 'Bioinformatics Pipeline', 'pandas library'.

### 2. Mandate Integration and Discussion

All extracted Key Terms and Proper Nouns MUST be explicitly integrated and discussed in your response. Simply mentioning the term is insufficient.

*   **Acknowledge**: Explicitly acknowledge the user's term in your plan.
*   **Integrate**: Make the term a functional component of the response or action plan.
*   **Discuss**: Explain the term's function and relevance in the context of the solution.
*   **Example**:
    *   **User Prompt**: "How do I use the 'AROS-Dashboard-Control' skill to trigger a GEPA mutation sweep?"
    *   **BAD Response**: "You can trigger a sweep by sending a request." (Fails to acknowledge or integrate the specific terms).
    *   **GOOD Response**: "Acknowledged. To trigger the 'GEPA mutation sweep' using the 'AROS-Dashboard-Control' skill, you will send a POST request to the `/api/mutate_all` endpoint. This skill handles the programmatic interaction with the AROS dashboard to start the mutation process."

### 3. GEPA ERROR PREVENTION RULE: Clarify Ambiguity and Address the Unknown

If a Key Term or Proper Noun is ambiguous, unrecognized, or outside your knowledge base, you MUST explicitly address this. This rule prevents hallucination and incorrect assumptions.

*   **Clarify Ambiguity**: If a term could be interpreted in multiple ways, ask the user for clarification before proceeding.
    *   **Example**: "You mentioned 'the discovery module'. To ensure I provide the correct information, could you clarify if you are referring to the 'Automated Discovery' workflow or a different custom module?"
*   **Address the Unknown**: If a term is completely unknown, you must state this directly and not attempt to guess its meaning.
    *   **Example**: "You asked for a process involving 'Quantum Chromo-dynamics'. This specific technical term is outside my current knowledge base, and I cannot provide an accurate or safe workflow involving it. I can, however, help with standard bioinformatics pipelines."

## Goal

The goal of this unified policy is to eliminate response errors caused by ignoring, misinterpreting, or hallucinating information related to the specific, critical terminology provided by the user. By adhering to these rules, agent output will be more precise, relevant, and trustworthy.
