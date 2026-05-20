# Knowledge Item: GEPA Proposal Implementation

This document provides the authoritative workflow for an agent implementing a GEPA Proposal. It ensures that new capabilities are created in a structured, verifiable, and traceable manner, grounded in facts from the AROS Memory Bank. Adherence to this protocol is mandatory for system evolution tasks.

## Overview
This Knowledge Item (KI) governs the execution of GEPA Proposals. The core principles are: 1) **Mandate-Driven Creation** where new capabilities originate from an approved GEPA Proposal; 2) **Fact-Based Grounding** where the process is grounded in verifiable facts from the AROS Memory Bank to prevent hallucination; and 3) **Structured Output** where the final artifact is delivered in a machine-readable format like Markdown.

## Workflow
Agents must follow this sequential workflow to implement a GEPA Proposal:

1.  **Proposal Ingestion**: Receive and parse the GEPA Proposal, identifying the core objective (e.g., "create a new KI," "develop a new skill").
2.  **Fact Extraction**: Query the AROS Memory Bank to extract the specific, relevant facts or conversation snippets that form the knowledge base for the new capability.
3.  **Drafting**: Synthesize the extracted facts into a coherent draft, adhering to the required structure (e.g., Markdown KI format, SKILL.md format). The draft must explicitly reference the source facts.
4.  **Validation**: Subject the draft to the Golden Test Battery (GTB) validator to ensure it meets quality, clarity, and structural standards.
5.  **Integration**: Upon successful validation, commit the new KI or skill to the appropriate knowledge directory (`~/.gemini/antigravity/knowledge/` or `~/.gemini/skills/`).
6.  **Traceability Logging**: Log the successful implementation, linking the new artifact back to the originating GEPA Proposal to close the operational loop.
