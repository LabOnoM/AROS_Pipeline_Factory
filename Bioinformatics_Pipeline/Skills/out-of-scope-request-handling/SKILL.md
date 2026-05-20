---
name: out-of-scope-request-handling
description: A policy for gracefully handling user requests that fall outside the system's known capabilities by providing a list of supported alternatives and seeking additional context.
license: MIT
skill-author: AROS_code_generator
status: active
---

# Out-of-Scope Request Handling Policy

This policy governs how AROS agents respond when a user request does not map to any known skill or capability. The objective is to prevent silent failures, manage user expectations by clearly stating limitations, and proactively seek alternative ways to assist.

## GEPA Rules

**GEPA-Rule-003: Graceful Fallback for Unmatched Requests**

If a user's request cannot be confidently mapped to a specific skill or workflow, the agent MUST NOT attempt to improvise a solution with unrelated tools. Instead, it must gracefully inform the user that the request is out of scope and present a list of supported capabilities to guide them.

**GEPA-Rule-004: Context-Aware Assistance for Unmatched Queries**

Building on the graceful fallback, when a request is out of scope, the agent must also:
1.  **Explicitly State Limitations**: Clearly articulate what it cannot do and why (e.g., "I cannot directly browse websites or access live financial data.").
2.  **Offer In-Context Alternatives**: Suggest relevant, available skills or workflows that align with the user's likely intent.
3.  **Query for Additional Context**: Proactively ask the user if they have documentation, APIs, or other context (like a data file) that could enable the agent to assist with the task in a different way.

## Guiding Principles

- **Clarity over Ambiguity**: Never guess or proceed with a low-confidence tool match. It's better to admit a capability gap than to produce an incorrect result.
- **Acknowledge Limitations Explicitly**: Clearly state what cannot be done to manage user expectations and build trust.
- **Seek More Context**: Instead of terminating the conversation, invite the user to provide more information that might open up alternative solutions (e.g., "If you can provide a data export or API documentation, I can help you analyze it.").
- **Provide Actionable Alternatives**: The list of alternatives should be formatted clearly so the user can easily identify a relevant tool for their next query.
- **Dynamic Capability Discovery**: The list of supported functions should be generated dynamically by scanning the available skills, ensuring it's always up-to-date.

## Workflow

1.  **Analyze User Request**: The system first analyzes the incoming user request to understand its intent.
2.  **Match to Capabilities**: It then attempts to match this intent against a dynamically generated list of available skills.
3.  **Handle Match Failure**: If no high-confidence match is found, the system triggers this out-of-scope policy.
4.  **Generate Fallback Message**: The system generates a user-friendly message that:
    a.  Clearly states that the direct request cannot be fulfilled and briefly explains the limitation (e.g., "I am unable to access live web data.").
    b.  Queries the user for alternative documentation or data they might have (e.g., "Do you have a file with this data or access to an API I could use?").
    c.  Presents a list of dynamically discovered, relevant skills to guide the user toward a supported task.
5.  **Respond to User**: The comprehensive, helpful, and context-aware message is returned to the user.

## Example Response

**User Request:** "Can you check the current stock price of Google?"

**GEPA-Compliant Response:**

"I cannot access live financial data from the internet, so I am unable to check the current stock price for you. 

However, if you can provide me with a file (like a CSV) containing historical stock data, I can perform tasks like:
*   **analyze_data**: Analyze trends and statistics from the data.
*   **generate_report**: Create a summary report based on the provided information.

Do you have a data file or another form of documentation I could work with?"
