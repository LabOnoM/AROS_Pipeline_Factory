---
name: context-request-alignment-policy
description: A policy to ensure user requests align with the temporal scope and implied action of the provided context.
license: MIT
skill-author: AROS-Core
---

# Policy: Context-Request Alignment

This document outlines the 'Context-Request Alignment' policy, a mandatory meta-protocol for all AROS agents. The primary goal of this policy is to prevent erroneous actions and factual hallucinations by ensuring the agent's response and actions are logically consistent with the provided context.

## GEPA Rules

**GEPA-Rule-004: Context-Request Coherence**

The agent must verify that the user's request, particularly its temporal scope and implied action, aligns with the nature and purpose of the provided context. If a mismatch is detected, the agent must refuse the specific action and explain the discrepancy to the user.

**GEPA-Rule-005: Assume Context is Complete and Accurate**

The agent must not make assumptions about the completeness or accuracy of the provided context. If the context appears to be truncated, corrupted, or ambiguous, the agent must notify the user and ask for a complete and valid context before proceeding with any analysis or action. This prevents the agent from providing answers based on incomplete data.

**GEPA-Rule-006: Request Reframing and Clarification**

After acknowledging a discrepancy (as per Rule 2), the agent must either attempt to reframe the user's request within the provided context or explicitly ask for clarification to align the request with the available information.

## When to Use

- **Always:** This policy is a foundational check that must be applied before executing any task that is based on a specific, bounded context (e.g., a file, a log snippet, a previous command's output).
- It is especially critical when the user's request implies a state change, a real-time observation, or an action that the context's nature does not support.

## Guiding Principles

- **Analyze the Context's Nature:** First, determine the type of context you are working with. Is it a static file, a real-time data stream, a historical log, a read-only document, or a draft?
- **Analyze the Request's Verb:** Scrutinize the primary action verb in the user's request (e.g., "monitor", "add", "update", "show live", "delete").
- **Compare and Identify Mismatches:** Compare the requested action with the context's limitations. Can a static log be "monitored"? Can a read-only policy be "updated"?
- **Refuse and Clarify:** If a mismatch exists, the agent's primary duty is to refuse the impossible action. Immediately follow up with a clear explanation of *why* the action is impossible, citing the nature of the context as the reason. Offer a valid alternative action if one exists.

## Example Applications

The following scenarios demonstrate how to enforce context-request coherence, handle discrepancies, and apply the rules for clarification.

### Scenario 1: Temporal Mismatch

**Context Provided:** The agent has just read the contents of `/var/log/system-2023-10-26.log`.

**User Request:** "Okay, monitor this log and show me the live error rate."

**INCORRECT / NON-COMPLIANT Response:**
"Okay, I will monitor the log. The current error rate is 5%." (This is a hallucination, as the agent can only calculate the rate from the static, historical file).

**CORRECT / GEPA-COMPLIANT Response:**
"I cannot fulfill that request. The provided context is a static log file from a past date. Therefore, I cannot 'monitor' it for live changes. Would you like me to calculate the error rate based on the contents of this historical file instead?"

### Scenario 2: Action Mismatch

**Context Provided:** The agent has just read the contents of the `context-request-alignment-policy` (this very document), which is a read-only skill file.

**User Request:** "Add a new rule to this policy about asking for clarification."

**INCORRECT / NON-COMPLIANT Response:**
"Okay, I have added the new rule to the policy." (This is impossible, as the agent does not have write access to its own skill files).

**CORRECT / GEPA-COMPLIANT Response:**
"I cannot directly modify my own skill files as they are read-only. However, I can draft a revised version of the policy with your suggested rule and save it in my working directory. Would you like me to proceed with that?"
