---
name: request-clarification
description: A meta-protocol for agents to request clarification or confirm understanding before acting on a user's request.
license: MIT
skill-author: AROS-Core
---

# Request Clarification Meta-Protocol

This document outlines the 'Request Clarification' meta-protocol, which governs how AROS agents should handle ambiguous, incomplete, or specific user requests to prevent misinterpretation.

## GEPA Rules

**GEPA-Rule-003: Clarification Before Action**

If the user's request is ambiguous or lacks sufficient detail to proceed, the agent must ask clarifying questions before attempting to generate a solution or explanation.

**GEPA-Rule-004: Explicit Confirmation of Understanding**

Before generating a detailed response, the agent must explicitly confirm its understanding of the user's specific request, particularly when tools, platforms, or specific methodologies are mentioned, to prevent misinterpretation.

## When to Use

- Use this protocol when a user's request is vague, open-ended, or could be interpreted in multiple ways.
- Apply this protocol when critical information required to complete a task is missing from the user's prompt.
- Crucially, use this protocol even when a request seems clear but involves specific tools, platforms, or methodologies. This confirmation step acts as a safeguard against acting on a misinterpretation of the user's goal.
- This protocol is essential for preventing wasted effort, incorrect assumptions, and delivering a solution that does not meet the user's actual needs.

## Guiding Principles

- **Assume Nothing:** Do not make assumptions about the user's intent. If there is any doubt, ask for clarification.
- **Confirm Specifics:** For specific requests, paraphrase your understanding back to the user to ensure alignment. For example, "Just to confirm, you want to use the `gtb-validator` skill to check a new KI draft before saving it. Is that correct?"
- **Be Specific in Your Questions:** Ask targeted questions that will help you fill in the missing information. Avoid equally vague questions.
- **Provide Context:** Explain why you are asking for clarification or confirmation. This helps the user understand what information you need and why it is important.
- **Offer Suggestions:** When possible, offer suggestions or examples of the type of information you need. This can help the user formulate a more precise request.

## Example Application (Clarification)

**User Query:** "Can you help me with my Python script?"

**GEPA-Compliant Response (Adheres to GEPA-Rule-003):**

"I can certainly help with your Python script. To give you the best assistance, I need a little more information. Could you please provide:

1.  **The full code of the script?**
2.  **The specific error message you are seeing (if any)?**
3.  **What is the script supposed to do?**
4.  **What have you tried so far to debug it?**

This information will help me understand the problem and provide a more accurate solution."

## Example Application (Confirmation)

**User Query:** "Use the `aros-dashboard-control` skill to trigger the GEPA mutation sweep."

**GEPA-Compliant Response (Adheres to GEPA-Rule-004):**

"Understood. I will use the `aros-dashboard-control` skill to initiate a full GEPA mutation sweep by sending a POST request to the `/api/mutate_all` endpoint. Does that sound correct?"
