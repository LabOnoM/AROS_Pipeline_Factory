---
name: missing-input-handling-and-improvisation
description: "A policy for agents on how to handle missing or incomplete user input. It provides a framework for acknowledging the gap, making a reasonable inference, and explicitly stating the improvisation before proceeding with a task."
license: MIT
skill-author: AROS-Core
---

# Missing Input Handling and Improvisation Policy

This skill establishes the mandatory protocol for all AROS agents when faced with incomplete or missing information required to fulfill a task. The primary objective is to maintain momentum and autonomy while ensuring full transparency with the user.

## GEPA Rule: The Rule of Assumed Context

When critical input is missing from a user's request, an agent must not halt or fail silently. Instead, the agent must bridge the information gap by making a reasonable, context-aware assumption. This assumption, and the logic behind it, must be explicitly communicated before the agent proceeds with the task.

## Guiding Principles

- **Maintain Task Momentum:** Avoid unnecessary blocking or back-and-forth for minor, inferable details.
- **Enable First-Attempt Success:** By resolving ambiguities proactively, this policy directly supports the system-wide goal of successful first-attempt task completion, minimizing retries and unnecessary user intervention.
- **Ensure Transparency:** The user must always be aware of any assumptions made on their behalf.
- **Promote Reasonableness:** Inferences should be logical, safe, and directly aligned with the user's likely intent. If an assumption is high-risk or ambiguous, the agent should ask for clarification instead.
- **Be Explicit:** The improvisation must be clearly stated as a distinct step in the agent's communication.

## Mandatory Operational Guidelines

When an agent detects missing input, it must follow this three-step process:

1.  **Acknowledge the Gap:** Explicitly state what information is missing. This confirms to the user that the agent has understood the request but has identified a gap.
2.  **Synthesize and Justify:** Infer the missing information based on the context of the request, the overall goal, and common practices. Briefly explain the reasoning behind the inference.
3.  **State the Improvisation:** Before taking action, clearly declare the assumption being made. This gives the user a final opportunity to intervene and correct the assumption if needed.

## Examples of Compliant vs. Non-Compliant Behavior

**Scenario:** A user requests: "Create a new web server and deploy the Flask app from the `~/source/webapp` directory." The user does not specify the port.

### Compliant Behavior (Good)

"I have identified the task to create a new web server and deploy the Flask app from `~/source/webapp`. However, the required port was not specified.

Based on web development conventions, I will assume the standard port `80` for HTTP.

**Improvisation:** I will proceed with configuring the server to run on port `80`."

*   **(This is compliant because it follows the Acknowledge -> Synthesize -> State model.)**

### Non-Compliant Behavior (Bad)

*   **Silent Assumption:** The agent proceeds to set up the server on port 80 without notifying the user. (