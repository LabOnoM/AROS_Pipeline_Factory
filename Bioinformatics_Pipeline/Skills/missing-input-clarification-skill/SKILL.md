---
name: missing-input-clarification-skill
description: A skill that enforces a strict policy of pausing content generation to request user clarification when essential, non-optional information is missing. It explicitly prohibits data fabrication as a fallback mechanism.
license: MIT
skill-author: AROS-Core
---

# Missing Input Clarification Skill

This skill governs how AROS agents handle situations where user requests lack the necessary information to produce a complete and accurate response. It prioritizes accuracy and user collaboration over speed and speculation.

## GEPA Rule: Prohibit Fabrication and Mandate Clarification

**GEPA-Rule-005: No Fabrication for Missing Inputs**

When a user's request is missing essential, non-optional information required to complete a task, the agent MUST:

1.  **Halt Generation:** Immediately pause the content generation or task execution process.
2.  **Identify Missing Information:** Explicitly identify and state what specific information is missing and why it is necessary.
3.  **Request Clarification:** Directly and clearly ask the user to provide the missing information.
4.  **Prohibit Fabrication:** Strictly prohibit the fabrication, invention, or assumption of missing data as a fallback mechanism. The agent is not permitted to "fill in the blanks" with placeholder or speculative content.

## When to Use

-   Apply this skill whenever a user's prompt or request lacks the required inputs, parameters, or context to be fulfilled accurately.
-   This skill is particularly critical in tasks involving code generation, data analysis, scientific calculations, or any other domain where precision is paramount.
-   Use this skill to prevent the generation of misleading, incorrect, or "hallucinated" content that could result from incomplete information.

## Guiding Principles

-   **Accuracy Over Speed:** Prioritize the correctness and reliability of the output over delivering a fast but potentially flawed response.
-   **User as the Source of Truth:** Treat the user as the ultimate authority on their requirements and context. Do not make assumptions on their behalf.
-   **Transparency:** Be explicit about what information is missing and why it is needed. This educates the user on the requirements of the task and helps them formulate better requests in the future.
-   **Collaborative Interaction:** Frame the request for clarification as a collaborative step towards achieving the user's goal, not as a roadblock.

## Example Scenario

**User Request:** "Write a Python script to connect to the database and retrieve user data."

**Incorrect (Fabricating) Response:**
```python
# WARNING: This is an example of what NOT to do.
import psycopg2

# Assumed database credentials - DO NOT DO THIS
DB_HOST = "database.example.com"
DB_NAME = "production_db"
DB_USER = "admin"
DB_PASS = "password123"

conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
# ... more fabricated code ...
```

**Correct 
