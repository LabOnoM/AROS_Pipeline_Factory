---
name: textual-interpretability
description: A policy for ensuring that text explanations of figures and data are clear, concise, and translate complex information into meaningful insights.
license: MIT
skill-author: AROS-Code-Generator
---

# Textual Interpretability Policy

This document outlines the 'Textual Interpretability' policy, which governs how AROS agents should compose text to explain figures, data, and other analytical findings.

## GEPA Rule

**GEPA-Rule-002: Clarity and Conciseness in Textual Explanations**

Accompanying text explanations for figures and analytical findings must be clear, concise, and effectively translate complex data into meaningful, interpretable insights for the user.

## When to Use

- Use this policy when generating figure captions for charts, graphs, or diagrams.
- Apply this policy when summarizing analytical findings from a dataset, experiment, or simulation.
- This policy is critical when writing the main body of a report that refers to a data visualization.
- Use this policy whenever an agent's response includes data that requires interpretation for the user to understand its significance.

## Guiding Principles

- **Clarity over Jargon:** Use simple, direct language. Avoid technical jargon where possible, or explain it if it is essential for the context.
- **Conciseness:** Be direct and to the point. The explanation should be as long as necessary to convey the main insight, but no longer.
- **Insight-Oriented:** Do not simply describe what the data is; explain what it *means*. Focus on the key takeaway, trend, or conclusion.
- **Context is Key:** Ensure the explanation is grounded in the context of the user's query or the broader document.
- **Audience-Aware:** Tailor the level of detail and technical language to the intended audience (e.g., expert vs. general).

## Example Application

**Context:** An agent has generated a bar chart showing user engagement metrics for two different product features (Feature A and Feature B) over 30 days.

**Non-Compliant Explanation (Describes but doesn't interpret):**
"Figure 1 shows a bar chart of user engagement. The x-axis is the feature and the y-axis is the number of interactions. Feature A has a value of 1,500 and Feature B has a value of 450."

**GEPA-Compliant Explanation (Translates data into insight):**
"Figure 1. Feature A drives significantly higher user engagement. Over the 30-day period, Feature A received over three times more user interactions than Feature B (1,500 vs. 450), indicating it is a primary driver of user activity."

## Implementation Details

- **Execution Model:** This is a behavioral policy to be integrated into the agent's core response generation logic, particularly when performing data visualization or summarization tasks.
- **Input Controls:** This policy is triggered when a task requires the generation of text to accompany data, figures, or analytical results.
- **Output Discipline:** The output must be a textual explanation that adheres to the principles of clarity, conciseness, and insight, directly supporting the associated data.
