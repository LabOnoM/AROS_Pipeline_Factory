---
name: textual-interpretability-policy
description: A meta-protocol mandating that all text explanations for figures and analytical findings are clear, concise, and effectively translate data into meaningful insights. This policy governs skills like graph-interpretation and literatureimages-interpretation.
license: MIT
skill-author: AROS-GEPA
---
# Textual Interpretability Meta-Protocol

This document outlines the **GEPA (Generative Evidence & Provenance Alignment)** rule for textual interpretability. It is a mandatory policy that governs all AROS skills and workflows responsible for generating human-readable text from data, figures, or analytical results.

## Core Principle (The GEPA Rule)

**Accompanying text explanations for figures and analytical findings must be clear, concise, and effectively translate complex data into meaningful, interpretable insights for the user.**

The primary goal is to move beyond mere description of data points and provide genuine understanding.

## Scope and Applicability

This policy applies to any skill that performs interpretive or explanatory tasks, including but not limited to:

- `graph-interpretation`
- `literatureimages-interpretation`
- `meta-results-forest-plot-analyzer`
- Any future skill that generates captions, summaries, or explanations of data visualizations or statistical outputs.

All outputs from these skills must adhere to the guidelines specified below.

## Requirements and Guidelines

### 1. Clarity
- **Avoid Jargon:** Use language that is accessible to the intended audience. If technical terms are necessary, provide a brief definition.
- **Simple and Direct Language:** Employ straightforward sentence structures. Prioritize clarity over complex prose.
- **Define an Audience:** Assume the audience is intelligent but not necessarily an expert in the specific domain.

### 2. Conciseness
- **State the Primary Insight First:** Lead with the main conclusion or trend shown in the data.
- **Eliminate Redundancy:** Avoid repetitive phrasing or stating the obvious (e.g., "The graph shows..." can often be omitted).
- **Focus on Significance:** Report on data that is significant or relevant to the main finding. Not every data point needs to be mentioned.

### 3. Meaningful Translation
- **Interpret, Don't Just Describe:** The explanation must go beyond a literal reading of the chart. Explain what the data *means*.
- **Highlight Relationships and Trends:** Explicitly state comparisons, correlations, trends, and significant differences (e.g., "Group A's performance doubled, while Group B's remained flat, indicating a strong treatment effect.").
- **Provide Context:** Briefly mention the 'why' if it's available from the source material. Connect the finding to the broader research question.

## Example of Adherence

**Scenario:** A bar chart shows that a new drug (Drug X) reduces tumor size by 75% on average, while the placebo reduces it by 10%.

#### **Non-Compliant Output (Poor Interpretation):**
> "The bar chart displays two bars. The bar for Drug X is at 75% and the bar for the placebo is at 10%."

#### **Compliant Output (Rich Interpretation):**
> "Drug X demonstrates a significant therapeutic effect, reducing tumor size by an average of 75%. This effect is substantial compared to the 10% reduction observed in the placebo group, suggesting the drug is a highly effective treatment."

## GEPA Error Prevention Rule

### Rule: Prevent Low-Information Outputs

To prevent outputs that are verbose but uninformative, the agent's explanation must actively synthesize information rather than merely describing it. The output must explicitly state the primary insight, trend, or conclusion derived from the data. Raw data points should only be used to support this primary insight, not replace it.

#### **Failure Condition Example:**
An agent generates a plot and the accompanying text is: "The plot shows sales data. On the X-axis is time, and on the Y-axis is sales in millions. In January, sales were 5.2M, in February they were 5.4M, and in March they were 5.3M."

*   **Reasoning for Failure:** This output is a low-level description of the data points and provides no actual insight or interpretation. It fails to identify the trend (i.e., that sales are stable).

#### **Compliant Output Example:**
"The analysis shows that sales remained stable and consistent during the first quarter, averaging 5.3M per month. This indicates a predictable market baseline with no significant fluctuations."
