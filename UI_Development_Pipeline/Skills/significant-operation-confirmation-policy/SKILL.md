---
name: significant-operation-confirmation-policy
description: A mandatory policy requiring agents to seek explicit user confirmation before executing significant, irreversible, or resource-intensive system operations.
license: MIT
skill-author: AROS-Mutation-Sweeper
---

# Policy: Significant Operation Confirmation

This document outlines the 'Significant Operation Confirmation' policy. This is a critical safety and user alignment protocol that mandates agents to identify high-impact requests, explain their potential consequences, and obtain explicit user confirmation before proceeding with execution. This policy acts as a final safeguard against unintended system changes.

## GEPA Error Prevention Rule

**GEPA-Rule-006: Pre-Execution Confirmation for Significant System Operations**

Before executing any operation classified as "significant," an agent **MUST**:
1.  Explicitly state its understanding of the requested operation.
2.  Clearly and concisely describe the potential consequences (e.g., data loss, resource consumption, system state changes).
3.  Request and receive an affirmative confirmation from the user before proceeding.

## Definition of a Significant System Operation

An operation is considered "significant" if it meets one or more of the following criteria:

1.  **Irreversible Data Modification:** Any action that deletes, overwrites, or moves files or data in a way that is difficult or impossible to undo.
    *   **Examples:** `rm`, `mv`, `write_local_file` to an existing path, database record deletion.

2.  **Resource-Intensive Processes:** Any task that consumes a substantial amount of computational resources (CPU, memory, time), potentially impacting system performance or incurring costs.
    *   **Examples:** Triggering a full GEPA mutation sweep (`/api/mutate_all`), initiating a dream cycle (`/api/dream`), running large-scale data analysis.

3.  **System Configuration Changes:** Any action that modifies the agent's or the system's operational parameters or configuration.
    *   **Examples:** Installing new software (`install_package`), changing MCP server settings (`/api/mcp/setup`).

4.  **Execution of External Code:** Running scripts or commands that are not part of the core AROS toolset, where the full impact may not be known.
    *   **Examples:** Executing a user-provided shell script, running a Python script that interacts with external APIs.

## Mandatory Dialogue Flow & Implementation

When a user request is identified as a significant system operation, the agent must engage in the following dialogue:

1.  **Acknowledge and Identify:** State the understood task and classify it as a significant operation.
2.  **Warn and Explain:** Describe the consequences.
3.  **Request Confirmation:** Ask for a clear "yes" or "proceed" confirmation.

## Example Application

**Scenario: User requests to trigger a GEPA mutation sweep.**

**User Request:** "Run the GEPA mutation sweep now."

**CORRECT / GEPA-COMPLIANT Response:**
"Acknowledged. I will initiate a full GEPA mutation sweep.

**Warning:** This is a resource-intensive process that may take a significant amount of time and will consume considerable computational resources.

Please confirm that you want to proceed."

---
*User confirms: "Yes, go ahead."*
---

**Agent's Next Action:**
`POST /api/mutate_all`

**INCORRECT / NON-COMPLIANT Response:**
"Acknowledged. Triggering the GEPA mutation sweep now."
*(This is a policy violation as it does not explain the consequences or wait for confirmation.)*
