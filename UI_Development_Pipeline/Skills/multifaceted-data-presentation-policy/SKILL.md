---
name: multifaceted-data-presentation-policy
description: "A mandatory policy requiring all data presentations to include detailed results, an interactive visualization, and a summary document to ensure clarity, explorability, and robustness of findings."
skill-author: AROS-GEPA
license: MIT
---

# Policy: Multifaceted Data Presentation

This policy establishes a mandatory framework for presenting data within the AROS ecosystem. It is designed to prevent common errors of misinterpretation that arise from presenting data in a single, static format. By requiring a multi-faceted approach, it ensures that findings are transparent, explorable, and clearly communicated. This policy is enforced by the GEPA framework.

## When to Use

- This policy is mandatory for any skill or workflow that generates a final analytical output for a user.
- It applies to tasks involving data reporting, exploratory data analysis, and results summarization.
- This is a terminal output policy, meaning it governs the final package of information presented to the user.

## GEPA Error Prevention Rule: Mandate Integrated Multifaceted Presentation

To prevent incomplete or misleading data reporting, all AROS components that present analytical findings **MUST** deliver them in an integrated package containing three distinct facets:

1.  **Detailed Results View:** The raw or processed data underlying the analysis must be presented in a clear, non-aggregated format (e.g., a data table, a structured text file). This ensures transparency and allows for detailed inspection.
2.  **Interactive Exploration Tool:** An interactive visualization (e.g., a Plotly chart, a filterable dashboard component) must be provided to allow the user to explore the data dynamically. This facilitates deeper understanding and personal inquiry.
3.  **Summary Document:** A concise, human-readable summary must accompany the presentation. This document should interpret the key insights, explain the significance of the findings, and state any limitations, adhering to the `textual-interpretability-policy`.

### Core Requirements:

1.  **Integration:** The three facets must be presented together as a cohesive package. They should not be delivered as separate, disconnected outputs. They should be clearly linked (e.g., the summary references the interactive plot and the detailed data).
2.  **Tooling:** Use appropriate tools for each facet. For interactivity, prefer libraries like Plotly or Bokeh. For detailed results, prefer standard formats like CSV, JSON, or well-formatted Markdown tables.
3.  **Clarity and Purpose:** Each facet must have a clear purpose. The summary should explain what the user is looking at in the other two components and guide their interpretation.
4.  **No Exceptions for Simplicity:** This rule applies even if the dataset is small or the finding seems simple. The practice of providing all three facets is a fundamental principle of robust data communication.

### Rationale

-   **Prevents Oversimplification:** A summary alone can hide important nuances or outliers.
-   **Prevents Data Overload:** Raw data alone can be overwhelming and difficult to interpret.
-   **Enhances Trust and Transparency:** Providing the detailed data builds trust and allows for independent verification.
-   **Empowers User-Driven Discovery:** Interactive tools allow users to explore questions beyond the primary summary.
