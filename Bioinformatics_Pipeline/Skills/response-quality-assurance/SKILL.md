---
name: response-quality-assurance
description: "A mandatory policy for processing user prompts. It enforces the extraction, inclusion, and discussion of specific key terms mentioned by the user to ensure the agent's output is precisely aligned with the user's explicit intent, as per the GEPA proposal on query fidelity."
license: MIT
skill-author: AROS-GEPA
---

# Global Policy: Query Term Inclusion & Response Fidelity

This is a mandatory meta-instruction that governs how user prompts are deconstructed and addressed. It was implemented as a result of a GEPA (Golden Experience Path Advancement) proposal to improve the fidelity and relevance of agent responses by ensuring all explicit user requirements and named entities are directly addressed.

## Core Principle

A response is only considered complete and correct if it demonstrably satisfies all explicit requirements laid out in the user's original request. All ambiguity regarding specific products, features, or workflows must be resolved *before* execution.

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

### 4. Persona and Skill Relevancy

**The assigned persona and invoked skills must be appropriate and relevant to the specific sub-task's nature and required output.**

- **Guidance:** This is an error prevention rule to catch flawed reasoning. An agent assigned a `code-auditor` persona

### 5. Accurate Status Summarization

The agent's high-level summary statement regarding project completion status MUST accurately reflect the detailed breakdown of completed and remaining tasks within the report. This prevents overly optimistic or misleading summaries where a project is declared "complete" or "successful" while ignoring failed or incomplete sub-tasks.
