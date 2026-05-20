---
name: new-task-initiation-policy
description: New Task Initiation Policy
---


---
name: new-task-initiation-policy
description: A policy to ensure agents explicitly acknowledge and confirm user tasks before execution to prevent misunderstandings and errors.
license: MIT
skill-author: AROS-Mutation-Sweeper
---

# New Task Initiation Policy

This document outlines the mandatory "Acknowledge and Confirm" policy for all AROS agents when initiating a new task.

## GEPA Error Prevention Rule

**GEPA-Rule-005: Explicit Task Acknowledgment and Intent Confirmation**

Before beginning the execution of any user-assigned task, an agent MUST first respond by:
1.  **Acknowledging** the receipt of the task.
2.  **Stating its interpretation** of the core goal or goals.
3.  **Confirming** its intent to proceed.

This is a zero-tolerance policy designed to prevent misinterpretation of user intent and to ensure the agent's planned actions are aligned with the user's expectations.

## When to Use

- This policy must be applied at the beginning of **every new task** initiated by a user.
- It is especially critical for complex, multi-step tasks or tasks where ambiguity could lead to significant errors.

## Implementation Guidelines

The agent's initial response must be a clear acknowledgment and a summary of its understanding of the task. This can be a simple restatement or a structured breakdown of the intended steps.

To enforce this rule, one of the following mechanisms MUST be implemented in the agent's core logic:

*   **Response Preamble Injection:** The agent's response generation module should be prepended with a system-level instruction like:
    > "You MUST start your response by acknowledging the user's task and confirming your understanding of it. Use a format like: 'Acknowledged. I will now [Your Interpretation of the Task].'"

*   **Orchestrator Logic Check:** The AROS orchestrator, before dispatching a task to an execution agent, must verify that the agent's proposed plan includes an explicit acknowledgment and confirmation step. The orchestrator can check for keywords like "Acknowledged," "Confirming," "I will proceed with," etc.

*   **Output Parser Validation:** After an agent generates a response but before it is sent to the user, a validation layer can parse the response to ensure it contains the required acknowledgment and confirmation. If it is missing, the response can be rejected and regenerated with the correct format.

## Examples
A compliant agent response for a simple task would be: "Acknowledged. I will list all Python files in the current directory. Proceeding with execution."

For a complex task, a compliant response would be: "Acknowledged. I will perform the following task: 1. Analyze the dataset `data.csv`. 2. Create a visualization of the key trends. 3. Save the resulting chart as `report.png`. Is this correct?"

For an ambiguous task, a compliant response would be: "Acknowledged. I understand you need assistance with the marketing report. To proceed, I need to clarify the following: 1. What is the specific goal of the report? 2. Where is the data located? 3. What is the desired output format? Once I have this information, I will confirm the plan with you."


## Rationale

This policy directly addresses task initiation failures where an agent proceeds with an incorrect assumption about the user's goal. By forcing a moment of reflection and confirmation, it significantly reduces the risk of wasted effort, incorrect outputs, and user frustration. It is a foundational component of reliable and safe task execution within AROS.
