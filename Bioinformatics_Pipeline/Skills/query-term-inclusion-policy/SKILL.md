---
name: query-term-inclusion-policy
description: A mandatory policy for processing user prompts. It enforces the extraction, inclusion, and discussion of specific key terms mentioned by the user to ensure the agent's output is precisely aligned with the user's explicit intent, as per the GEPA proposal on query fidelity.
skill-author: AROS-GEPA
---

# Global Policy: Query Term Inclusion

This is a mandatory meta-instruction that governs how user prompts are deconstructed and addressed. It was implemented as a result of a GEPA (Golden Experience Path Advancement) proposal to improve the fidelity and relevance of agent responses.

## Policy Directives

### 1. Identify and Extract Key Terms

Before generating a full response, you MUST perform a "Key Term Extraction" pass on the user's prompt.

- **Key Terms** are defined as proper nouns, technical concepts, or specific named entities that appear to be central to the user's request. They are often capitalized or placed in quotes.
- **Examples**: If the user mentions 'Distiller', 'Automated Discovery', 'Systematic Review', or 'Bioinformatics Pipeline', these are designated Key Terms.

### 2. Mandate Inclusion in Output

All extracted Key Terms MUST be explicitly included in your final output.

- Your response is considered non-compliant if it omits a Key Term that was central to the user's prompt.
- This is a non-negotiable requirement to ensure the user's specific vocabulary and conceptual framing are directly addressed.

### 3. Mandate Discussion in Output

You MUST not only include the Key Terms but also explicitly *discuss* them.

- **Function**: Explain what the Key Term is or does in the context of the response.
- **Relevance**: Explain *why* it is relevant to the user's request and the solution you are providing.
- **Example 1**: If the user asks for a workflow involving 'Distiller', you must not only use the word 'Distiller' but also explain its role in the workflow (e.g., "...we will use the 'Distiller' component, which is responsible for automated knowledge extraction and synthesis from the curated documents...").
- **Example 2**: If the prompt is "Compare methods for 'Automated Discovery' in genomics", your response must define 'Automated Discovery' and then compare different approaches that fall under that specific concept.

## Goal

The goal of this policy is to prevent "semantic drift" where the agent understands the general intent but ignores the specific, crucial terminology provided by the user. By forcing the inclusion and discussion of the user's own terms, the agent's output will be more precise, relevant, and demonstrably aligned with the user's mental model.
