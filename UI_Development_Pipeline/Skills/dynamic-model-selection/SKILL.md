---
name: dynamic-model-selection
description: A policy for dynamically selecting the optimal AI model for a given sub-task based on complexity, cost, and required quality.
license: MIT
skill-author: AROS_code_generator
status: active
---

# Dynamic Model Selection Policy

This policy governs how AROS agents select AI models for executing sub-tasks. The primary objective is to optimize for efficiency, cost, and quality by matching the computational requirements of a task to the most appropriate model available.

## GEPA Rule: Tiered Model Routing

**For any given sub-task, the agent MUST evaluate its complexity, computational cost, and required quality. Based on this evaluation, the agent MUST route the task to a model from the appropriate tier, rather than relying on a single default model. The selection rationale must be logged.**

## Guiding Principles

- **Efficiency and Cost-Effectiveness**: Avoid using powerful, expensive models for simple, low-level tasks.
- **Quality and Accuracy**: Ensure that complex, high-stakes tasks are routed to models capable of delivering the required level of reasoning and accuracy.
- **Task-Centric Evaluation**: The choice of model should be determined by the nature of the task (e.g., simple data extraction vs. complex code generation), not by a fixed system-wide default.
- **Transparent Logging**: The decision-making process for model selection should be transparent and auditable by logging which model was chosen and why.

## Model Tier System

AROS defines a tier system to categorize available AI models based on their capabilities and cost. Agents must use this system for routing decisions.

*   **Tier 1 (Lightweight & Fast):**
    *   **Description:** Small, highly-efficient models, often running locally.
    *   **Use Cases:** Simple text formatting, data extraction, keyword analysis, routing, simple classification, or basic user intent recognition.
    *   **Examples:** `Llama 3 8B`, `Gemma 2`, `Phi-3-mini`.

*   **Tier 2 (Balanced - General Purpose):**
    *   **Description:** Capable, general-purpose models that offer a good balance between performance and cost.
    *   **Use Cases:** General content summarization, standard code generation, complex instruction following, multi-step reasoning.
    *   **Examples:** `Gemini 1.5 Flash`, `Claude 3 Sonnet`, `GPT-4o-mini`.

*   **Tier 3 (High Quality & Advanced Reasoning):**
    *   **Description:** State-of-the-art models for tasks requiring maximum performance, creativity, and deep reasoning. These are the most expensive models and should be used judiciously.
    *   **Use Cases:** Complex problem-solving, novel algorithm design, scientific analysis, in-depth code review, or high-stakes creative generation.
    *   **Examples:** `Gemini 1.5 Pro`, `Claude 3 Opus`, `GPT-4 Turbo`.

## Workflow

1.  **Task Decomposition**: Following the `modular-task-breakdown` policy, the agent first decomposes a complex objective into a sequence of sub-tasks.
2.  **Sub-Task Analysis**: For each sub-task, the agent analyzes its requirements:
    *   **Complexity:** Is the task simple (e.g., find a date) or complex (e.g., write a new Python class)?
    *   **Risk/Stakes:** Is the output critical and requires high accuracy, or is it a low-impact intermediate step?
    *   **Creativity:** Does the task require generating novel content or just processing existing data?
3.  **Tier Assignment**: Based on the analysis, the agent assigns a Tier (1, 2, or 3) to the sub-task.
4.  **Model Selection & Routing**: The agent selects an available model from within the assigned tier and executes the sub-task.
5.  **Log Rationale**: The agent logs the sub-task, the chosen model, the assigned tier, and a brief justification for the choice (e.g., "Sub-task 'Extract email addresses' assigned to Tier 1 for efficiency.").
