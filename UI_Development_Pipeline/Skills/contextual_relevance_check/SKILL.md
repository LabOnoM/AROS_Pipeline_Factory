---
name: contextual-relevance-check
description: "A mandatory GEPA policy that requires the agent to verify if a user's request is relevant to the provided walkthrough or instructional context before execution."
license: MIT
skill-author: AROS-GEPA
---

# Global Policy: Contextual Relevance Check

This is a mandatory meta-instruction that governs how user prompts are handled within a structured, multi-step context, such as a guided walkthrough or a tutorial. It was implemented as a result of a GEPA (Golden Experience Path Advancement) proposal to prevent user-induced deviations that lead to task failure.

## Core Principle

An agent must not proceed with a user's request if it deviates significantly from the established context of a guided process. The primary goal is to keep the user on the "golden path" to success by preventing out-of-scope actions that could corrupt the state or lead to confusion.

## Policy Directives

### 1. Assess Contextual Relevance

Before executing any user request, you MUST first assess if the request is relevant to the provided walkthrough context.

- **Context** is defined as the current step, the overall goal of the workflow, and the concepts introduced in the preceding instructions.
- **Relevance** is determined by whether the user's request logically follows from the current state or is an attempt to introduce an unrelated action.

### 2. Identify and Flag Deviations

If the user's request introduces new goals, tools, or concepts that are not part of the current instructional framework, it MUST be flagged as a potential deviation.

- **Example 1**: If the walkthrough is about "Deploying a Web Server", and the user suddenly asks, "How do I train a machine learning model?", this is a clear deviation.
- **Example 2**: If the current step is "Configure the firewall", and the user asks to "Install a new database", this is also a deviation.

### 3. Clarify and Confirm Before Proceeding

If a deviation is identified, you MUST NOT execute the user's request. Instead, you must:

1.  Acknowledge the user's request.
2.  State clearly that the request appears to be outside the scope of the current walkthrough (e.g., "That seems unrelated to our current goal of deploying a web server.").
3.  Ask the user for explicit confirmation to proceed with the out-of-context task. This requires a "yes" or "no" type of confirmation.

This policy ensures that users are made aware when they are stepping off the guided path, preventing common errors and improving the reliability of complex, guided tasks.
