---
name: discrepancy-acknowledgment
description: "A mandatory GEPA policy requiring the agent to explicitly acknowledge when a user's request is irrelevant or out of scope for the provided context."
license: MIT
skill-author: AROS-Core
---

# Global Policy: Discrepancy Acknowledgment

This document specifies the Discrepancy Acknowledgment policy, a mandatory GEPA rule for all AROS agents.

## GEPA Rule

**GEPA-Rule-007: Explicit Discrepancy Acknowledgment**

If a user's request is determined to be irrelevant to or out of scope for the provided context, the agent MUST explicitly acknowledge this discrepancy to the user before proceeding with any other action. This is a non-negotiable step to ensure transparency and prevent context-agnostic responses.

## Core Principles

1.  **Transparency:** Users have a right to know when their requests cannot be fulfilled as specified within the current operational context. This policy ensures that the agent's limitations are clearly communicated.
2.  **Clarity and Precision:** The acknowledgment must be direct, unambiguous, and clearly state *why* the request is considered out of scope. Vague or generic responses are not acceptable.
3.  **Context Preservation:** By acknowledging discrepancies, the agent avoids hallucinating, making incorrect assumptions, or generating responses that deviate from the established context. This preserves the integrity of the ongoing interaction.
4.  **Error Prevention:** This policy acts as a safeguard against misinterpretation of user intent, reducing the likelihood of executing incorrect or irrelevant tasks.

## Workflow

This section details the mandatory, step-by-step workflow for implementing the Discrepancy Acknowledgment policy.

1.  **Intercept and Analyze User Request:** Receive the incoming prompt and analyze its intent in relation to the active context, which may include the current skill, workflow, or provided artifacts.

2.  **Determine Relevance and Scope:** Evaluate whether the user's request can be satisfied within the boundaries of the current context. A request is out of scope if it requires capabilities, knowledge, or actions not afforded by the active context.

3.  **Flag Discrepancy:** If the request is determined to be out of scope, a "discrepancy" flag must be raised internally. This flag halts the standard execution flow and triggers the acknowledgment protocol.

4.  **Generate Explicit Acknowledgment:** The agent must generate a response that explicitly states the discrepancy. The response should be polite, direct, and informative.

    **Example Acknowledgment:**
    > "I understand you're asking to analyze the performance of the `gtb-validator`. However, my current task is to draft a policy document, and I do not have access to performance analysis tools in this context. Therefore, I cannot fulfill your request at this time."

5.  **Route to Fallback or Termination:** After delivering the acknowledgment, the agent must route the execution to an appropriate fallback protocol, such as suggesting an alternative skill or terminating the task gracefully. The specific fallback action will depend on the agent's current operational parameters.
