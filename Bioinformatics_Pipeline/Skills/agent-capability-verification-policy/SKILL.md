---
name: agent-capability-verification-policy
description: A policy that mandates agents verify their advertised capabilities align with their active skills, KIs, and workflows, preventing capability hallucination (GEPA Rule).
skill-author: AROS-GEPA
license: MIT
---

# Agent Capability Verification Policy

This document defines the 'Agent Capability Verification' policy. It is a mandatory skill that governs how all AROS agents must ensure their claimed capabilities are a true reflection of their currently enabled operational components.

## 1. Overview

This policy establishes a mandatory pre-execution check to prevent "capability hallucination," where an agent claims it can perform a task for which it lacks the necessary underlying skills, knowledge, or workflows. To ensure operational integrity and predictable performance, an agent's advertised or documented capabilities MUST be perfectly aligned with its actively deployed and accessible components.

This alignment check is a core component of the General Environment Pre-flight Assessment (GEPA) framework.

## 2. The GEPA Error Prevention Rule

**GEPA-Rule-ACV-001: Capability Alignment**

> An agent MUST NOT claim, advertise, or attempt to execute a capability unless the corresponding Skill, Knowledge Item (KI), or Workflow is present, enabled, and fully accessible in its immediate execution environment. A pre-task inventory check is mandatory to enforce this alignment.

## 3. Core Principle: No Capability Without Components

An agent's capabilities are not inherent; they are the direct result of the specific Skills, KIs, and Workflows it has loaded. If a component is missing, disabled, or inaccessible, the corresponding capability does not exist.

- **Skills:** Define *how* to perform a task (e.g., `autoresearch`, `gtb-validator`).
- **Knowledge Items (KIs):** Provide the specific data or facts required for a task (e.g., `uniprot-api-schema`, `blastn-parameters`).
- **Workflows:** Define the sequence of steps to orchestrate skills and KIs for a complex objective.

An agent cannot claim to "run autoresearch" if the `autoresearch` skill is not in its `~/.gemini/skills/` directory. It cannot claim to "query UniProt" if the `uniprot-api-schema` KI is unavailable.

## 4. Mandatory Verification Workflow

All agents must follow this sequence before beginning substantive work on a task.

1.  **Identify Required Capabilities:** Upon receiving a task, the agent must first parse the request to identify all the capabilities needed for successful completion. This includes specific skills mentioned (e.g., "run a `beesgo-spawn`"), knowledge domains (e.g., "using the latest bioinformatics data"), or complex workflows.

2.  **Conduct Self-Inventory:** The agent must programmatically query its own environment to build an inventory of currently available and enabled components. This involves:
    *   Listing the contents of `~/.gemini/skills/` to identify active skills.
    *   Listing the contents of `~/.gemini/antigravity/knowledge/` for available KIs.
    *   Listing `~/.gemini/antigravity/global_workflows/` for available workflows.

3.  **Perform Alignment Check:** The agent must compare the list of required capabilities from Step 1 against the inventory from Step 2.

4.  **Execute or Halt:**
    *   **If Aligned:** If all required components are present in the inventory, the agent may proceed with the task.
    *   **If Misaligned:** If any required component is missing, the agent **MUST HALT** execution immediately. It must report the specific capability gap, citing this policy (`GEPA-Rule-ACV-001`).

## 5. Examples of Policy Violations

- **Violation:** An agent accepts a task to "Optimize the model using the autoresearch loop" but the `autoresearch` skill has been disabled or deleted.
    - **Correct Action:** The agent must halt and report: "Cannot perform task. Required skill 'autoresearch' is not available in my current environment, violating GEPA-Rule-ACV-001."
- **Violation:** An agent claims it can configure a system according to a new policy, but the KI containing the policy text is not loaded.
    - **Correct Action:** The agent must halt and report: "Cannot apply the new policy. The Knowledge Item for the policy is not accessible."

---

## MANDATORY SKILL INSTRUCTIONS:

### Pre-Execution Check

1.  **List Required Capabilities:** From the user's prompt and your initial plan, create a list of all necessary skills, KIs, and workflows.
2.  **Scan Environment:**
    *   Use `ls ~/.gemini/skills/` to list available skills.
    *   Use `ls ~/.gemini/antigravity/knowledge/` to list available KIs.
    *   Use `ls ~/.gemini/antigravity/global_workflows/` to list available workflows.
3.  **Compare and Verify:** For each required capability, ensure it exists in the scanned lists.
4.  **Halt on Mismatch:** If any capability is missing, stop immediately and report the specific missing component. Do not attempt to work around it or proceed with the task.
