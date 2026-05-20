---
name: conditional-logic-execution
description: A skill ensuring agents accurately evaluate conditions and execute appropriate branches of logic.
license: MIT
skill-author: AROS-Core
version: 1.0
---

# Conditional Logic Execution Skill

This skill mandates that agents accurately evaluate conditions and execute appropriate branches of logic or actions based on the evaluation outcomes, ensuring dynamic and adaptive task execution.

## GEPA Error Prevention Rule: Accurate Conditional Evaluation

### Rule: Evaluate Conditions Accurately

The agent **MUST** accurately evaluate conditions and execute appropriate branches of logic or actions based on the evaluation outcomes, ensuring dynamic and adaptive task execution.

### Rationale:
Incorrect conditional evaluation leads to flawed decision-making, incorrect task flow, and ultimately, system errors. This rule ensures that agents rigorously verify the truthfulness of conditions before proceeding with any conditional actions.

### Procedure:
1.  **Identify Conditional Statements:** Recognize all explicit and implicit conditional statements within a task or workflow.
2.  **Evaluate Conditions:** Rigorously evaluate each condition to determine its truth value (true/false).
3.  **Execute Appropriate Branch:** Based on the evaluated truth value, execute only the logic or actions associated with the correct branch.
4.  **Verify Outcome:** After execution, verify that the outcome aligns with the expected result of the correctly evaluated condition.
