---
name: illustrative-power-policy
description: "A policy for creating clear, rich, and interpretable analytical outputs. It mandates that all data-driven outputs include a visualization, a textual interpretation, and a machine-readable structured data object to ensure maximum clarity, utility, and downstream processability."
skill-author: AROS-GEPA
license: MIT
---

# Policy: Output Richness and Interpretability

This policy outlines the standards for all data-driven analytical outputs within the AROS ecosystem. Its purpose is to ensure that generated artifacts are not only accurate but also maximally informative, easy to interpret by humans, and readily processable by other machine agents. This policy is enforced by the GEPA (Genetic Evolution and Policy Adaptation) framework.

## When to Use

- Use this policy when developing or modifying any skill that generates charts, graphs, plots, or any other form of data visualization.
- Apply this policy when summarizing analytical findings from a dataset, experiment, or simulation.
- This policy is mandatory for all data presentation tasks, including exploratory data analysis, results reporting, and performance monitoring.
- Adhere to this policy whenever an agent's response includes data that requires interpretation for the user to understand its significance.

## GEPA Rule: Tripartite Output Standard for Richness and Interpretability

To enhance the clarity, utility, and downstream value of our analytical outputs, all AROS components that generate insights from data must adhere to the following GEPA rule:

**All analytical outputs must be generated as a tripartite artifact, consisting of the following three components:**

1.  **Visualization:** A graphical representation of the data that provides immediate insight (e.g., heatmap, scatter plot, network graph, bar chart). The visualization must be clear, well-labeled, and appropriate for the data being presented.
2.  **Textual Interpretation:** A clear, concise, and insight-oriented textual explanation accompanying the visualization. This text must translate the complex data into meaningful conclusions, explain what the visualization shows, and highlight the key takeaways.
3.  **Structured Data Object:** A machine-readable data file (e.g., JSON, CSV, Apache Parquet) containing the exact source data used to generate the visualization and textual interpretation. This ensures reproducibility, enables downstream programmatic use, and allows for re-analysis.

## Guiding Principles

- **Clarity over Jargon:** Use simple, direct language in textual interpretations. Avoid technical jargon where possible, or explain it if it is essential.
- **Insight-Oriented:** The goal is not just to describe the data, but to provide actionable insights. The textual interpretation should answer the "so what?" question.
- **Reproducibility:** The structured data object must be complete and self-contained, allowing any other agent or user to perfectly reproduce the visualization.
