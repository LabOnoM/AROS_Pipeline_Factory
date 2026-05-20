---
name: ki-creation-protocol
description: A mandatory skill that enforces the Knowledge Item Quality Assurance policy, requiring a strict consolidation, validation, and refinement loop using the Golden Test Battery (GTB) before any KI is saved.
license: MIT
skill-author: AROS-Core
---

# KI Creation Protocol (incorporating AROS-POLICY-KI-QA-V2)

This skill defines the mandatory, non-negotiable protocol for creating or modifying any Knowledge Item (KI) in the AROS system. It directly implements `AROS-POLICY-KI-QA-V2`. This protocol is a *process* you must follow, not a single tool you can call.

## When to Use

- ALWAYS use this capability when the goal is to create or update a Knowledge Item (`~/.gemini/antigravity/knowledge/`).
- This protocol is a specialization of the `content-drafting-capability` and MUST be followed for all KI-related tasks.

---

## !! CRITICAL PREREQUISITE !!

> [!CAUTION]
> This protocol is for **SYNTHESIS ONLY**, not for research or information gathering. Before you begin, you, the agent, must already possess all the necessary facts, data, or source text required to create the KI.

Your first action **MUST** be to write this pre-existing information into a temporary file. If you do not have the information, you must use other skills to find it *before* starting this protocol.

> [!IMPORTANT]
> **LLM API Compliance:** Any KI that includes executable code examples making LLM calls
> MUST demonstrate proxy-aware client instantiation per the `content-drafting-capability` 
> GEPA Rule: "Mandatory Proxy-Aware LLM Client Instantiation".

---

## MANDATORY PROTOCOL

This protocol is divided into two phases. **Phase A is a strict prerequisite for Phase B.** This is a **zero-tolerance policy**. No KI may be committed to the permanent knowledge base without successfully completing both phases in order.

### Phase A: Content Consolidation

> [!WARNING]
> **Anti-Pattern:** Do not try to find new information during this protocol. The goal of this phase is only to take information you *already have* and place it in a single file for processing.

**Step 1: Consolidate Source Material**

Your first action is to gather all relevant source material you have been provided with (e.g., facts from a prompt, conversation history, or other documents) and write it to a single, temporary file: `/tmp/source_content.txt`.

**Example:** If you are given a task like "Create a KI from these 4 facts...", your first step is to write those facts to the file.
`ACTION: write_local_file(filepath="/tmp/source_content.txt", content="Fact 1: Elastix is a software for image registration.\nFact 2: It was created by Stefan Klein and Marius Staring.\n...")`

You MUST confirm that the file `/tmp/source_content.txt` exists and contains the necessary information before proceeding to Phase B.

---

### Phase B: Validation and Refinement Loop

> [!CAUTION]
> Do not begin this phase until Step 1 of Phase A is complete and `/tmp/source_content.txt` has been successfully created.

**Step 2: Draft to Temporary File**

Using the consolidated material from `/tmp/source_content.txt`, you MUST write the full, formatted content of the new or updated KI to a separate temporary file: `/tmp/draft_ki.md`.

The permanent knowledge directory (`~/.gemini/antigravity/knowledge/`) MUST NOT be written to at this stage.

**Example:**
`ACTION: write_local_file(filepath="/tmp/draft_ki.md", content="# KI: Elastix\n\n[Content synthesized from /tmp/source_content.txt]...")`

**Step 3: Validate with Golden Test Battery (GTB)**

You MUST execute the `gtb-validator` skill on the temporary draft file. For all Knowledge Items, the `task_type` parameter MUST be set to `"knowledge_retrieval"`. This validation step explicitly verifies the correctness, quality, and compliance of the drafted KI.

**Example Invocation:**
```python
# The agent MUST use the gtb_validator tool
gtb_validator(draft_file_path="/tmp/draft_ki.md", task_type="knowledge_retrieval")
```

**Step 4: Mandatory Refinement Loop**

If the validation fails (`"passed": false`), you MUST analyze the `reasoning` provided in the result and iteratively revise the content in `/tmp/draft_ki.md`. You MUST re-run the validator on the revised draft until the validation passes (`"passed": true`).

Bypassing this validation step is a critical policy violation. A KI is only considered complete and ready for permanent storage once it has passed the GTB validation. Only after a successful validation can you move the file from `/tmp/draft_ki.md` to its final destination in the knowledge directory.