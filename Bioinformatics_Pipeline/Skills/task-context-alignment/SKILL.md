---
name: task-context-alignment
description: A meta-protocol for agent task planning that mandates the integration of explicit user-provided context (e.g., tool or method mentions) to ensure accurate interpretation of the user's underlying intent.
license: MIT
skill-author: AIPOCH (GEPA-derived)
---

## 1.0 Overview

This document specifies the **Task Contextualization and Intent Alignment Protocol**. It is a mandatory meta-skill governing the initial planning phase of any task undertaken by an AROS agent. Its purpose is to eliminate planning errors caused by misinterpreting user intent. The protocol ensures that explicit instructions, such as mentions of specific tools, skills, or methodologies, are not merely suggestions but are treated as primary directives that fundamentally shape the agent's execution plan.

This protocol is a direct implementation of a GEPA (Generative Evolutionary Policy Adaptation) proposal aimed at improving task fidelity and reducing redundant or incorrect actions.

## 2.0 Scope and Trigger

This protocol must be applied by any agent during the **PLANNING STAGE** of a task, immediately after receiving a user request and before executing any tool or action. It is a foundational layer of logic that precedes all other skill-specific execution.

## 3.0 Core Principle: The Intent Alignment Mandate

The central rule of this protocol is as follows:

> **The agent MUST integrate explicit user-provided context, including specific tool or method mentions, into its internal knowledge and planning to accurately interpret the user's underlying intent for the task.**

Failure to adhere to this principle constitutes a critical planning failure.

## 4.0 The Alignment Protocol (Execution Steps)

Agents must follow this sequence to ensure compliance with the mandate.

### Step 1: Context Identification and Extraction
- **Action:** Parse the user's prompt for explicit directives.
- **Checklist:**
    - [ ] Any mention of a specific `skill-name`?
    - [ ] Any mention of a specific shell command or tool (e.g., `python`, `git`, `docker`)?
    - [ ] Any reference to a specific file, KI, or workflow?
    - [ ] Any directive on methodology (e.g., "use a step-by-step approach," "create a markdown table")?
- **Output:** A structured list of all explicit context items.

### Step 2: Plan Scaffolding from Context
- **Action:** Construct the initial task plan *around* the extracted context items. The user's directives form the non-negotiable backbone of the plan.
- **Rule:** If a user specifies `skill-X`, the first operational step in the plan must be the invocation of `skill-X`. All other steps (e.g., finding files, reading data) are preparatory actions *for* that primary step.

### Step 3: Plan Verification and Self-Correction
- **Action:** Before execution, the agent must perform a self-check against the extracted context.
- **Verification Question:** "Does my final plan directly and explicitly use every tool, skill, and method specified by the user in their prompt?"
- **Correction Logic:**
    - If **YES**, proceed to execution.
    - If **NO**, discard the current plan and return to Step 2. The plan is invalid if it ignores a user directive in favor of an agent-derived alternative without explicit justification.

## 5.0 Examples of Protocol Application

### Example 1: Correct Application

**User Request:**
> "Review the new `aros-dashboard-control` skill and write a summary of its `Brain Federation` endpoints into a new KI named `brain-federation-api`."

**Agent Execution Log:**
1.  **Context Identification:**
    - Skill Mention: `aros-dashboard-control`
    - Keyword: `Brain Federation`
    - Action: Write new KI
    - KI Name: `brain-federation-api`
2.  **Plan Scaffolding:**
    a.  Read the `SKILL.md` for `aros-dashboard-control`.
    b.  Filter the content to find the "Brain Federation" section.
    c.  Extract and summarize the relevant endpoints (`/api/brain/export`, `/api/brain/import`, `/api/brain/merge`, `/api/brain/distill`).
    d.  Use the `write_local_file` tool to create `~/.gemini/antigravity/knowledge/brain-federation-api/summary.md` with the extracted information.
3.  **Verification:** The plan directly uses the specified skill for context, addresses the keyword, and creates the requested KI. **Proceed.**

### Example 2: Protocol Violation (Incorrect)

**User Request:**
> "I need a diagram of the agent's planning process. Use the `markdown-mermaid-writing` skill to create a flowchart."

**Agent Execution Log (VIOLATION):**
1.  **Context Identification:**
    - Topic: Agent planning process.
    - Output: Diagram/flowchart.
    - Skill Mention: `markdown-mermaid-writing`
2.  **Plan Scaffolding (INCORRECT):**
    a.  Understand the agent planning process.
    b.  Use Python `matplotlib` to generate a flowchart image.
    c.  Save the image to `/tmp/flowchart.png`.
    d.  Inform the user the image is ready.
3.  **Verification (FAILURE):** The plan ignores the explicit directive to use `markdown-mermaid-writing`. It substitutes an alternative (`matplotlib`) without justification. **This plan is invalid and must be corrected.**
