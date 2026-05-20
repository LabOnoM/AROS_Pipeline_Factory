---
name: content-parsing-accuracy
description: A policy that mandates the accurate and complete parsing of source documentation before executing a task.
license: MIT
skill-author: AROS-Mutation-Sweeper
---

# Content Parsing Accuracy Policy

This document outlines the 'Content Parsing Accuracy' policy, which governs how AROS agents must process instructional documents provided as input for a task.

## GEPA Rule

**GEPA-Rule-004: Comprehensive Content Ingestion**

Accurately parse and understand all relevant content from provided documentation or walkthroughs. An agent must not act upon partial or incomplete understanding of the provided materials.

## When to Use

- Use this policy at the beginning of any task where the primary input is a document containing instructions (e.g., a README, a walkthrough, a tutorial, or a set of operational procedures).
- Apply this policy before executing commands or scripts derived from documentation.
- This policy is critical for tasks involving system configuration, software deployment, and data processing, where misinterpretation can lead to errors.

## Guiding Principles

- **No Skimming:** Read and parse the entirety of the provided text. Do not stop at the first command or instruction.
- **Identify Critical Components:** Systematically extract key entities such as commands, file paths, configuration parameters, environment variables, success criteria, and error-handling procedures.
- **Acknowledge and Resolve Ambiguity:** If instructions are unclear, contradictory, or seem to be missing information, the agent must halt execution and flag the ambiguity.
- **Formulate a Plan:** Based on the comprehensive understanding of the document, formulate an execution plan. This plan should reflect the full sequence of steps, including any validation or cleanup actions mentioned.

## Example Application

**User Goal:** "Use the instructions in `walkthrough.md` to set up the new monitoring tool."

**`walkthrough.md` Content:**
"First, run `setup.sh`. This will install dependencies. IMPORTANT: after setup, you must edit `/etc/tool/config.yaml` and set `enabled: true`. Finally, verify the installation by running `tool --status`."

**Insufficient (Non-Compliant) Action:**
The agent reads the first line and immediately executes `setup.sh`, then reports the task as complete. This fails because the configuration was not edited and the status was not verified.

**GEPA-Compliant Action:**
1.  The agent parses the entire `walkthrough.md` file.
2.  It formulates the following plan:
    a. Execute `setup.sh`.
    b. Read the content of `/etc/tool/config.yaml`.
    c. Modify the content to set `enabled: true`.
    d. Write the modified content back to `/etc/tool/config.yaml`.
    e. Execute `tool --status` to verify the installation.
3.  The agent executes the plan step-by-step, ensuring all instructions from the document are followed correctly.

## Implementation Details

- **Execution Model:** This is a behavioral policy that must be integrated into the agent's core task-planning and interpretation logic.
- **Input Controls:** The trigger for this policy is the presence of instructional documentation as a primary input for a task.
- **Output Discipline:** The agent should be able to produce a multi-step execution plan derived from the document before taking action.
