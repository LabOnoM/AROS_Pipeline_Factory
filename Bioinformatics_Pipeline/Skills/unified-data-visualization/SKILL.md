---
name: unified-data-visualization
description: "Generates insightful, portable, and dynamically-created data visualizations using Vega-Lite, adhering to AROS policies for illustrative power and artifact portability."
skill-author: AROS-GEPA-System
license: MIT
---

# Unified Data Visualization Skill

## 1. Overview

This skill defines the standard for generating all data visualizations within the AROS ecosystem. It synthesizes multiple policies to create a robust, flexible, and effective data interpretation process. The core mandate is to produce self-contained, interactive, and contextually appropriate visualizations that are paired with clear textual insights.

This skill supersedes and integrates the principles from `dynamic-plot-code-generation`, `illustrative-power-policy`, and `artifact-portability-policy`.

## 2. GEPA Rule: Dynamic and Portable Visualization Generation

To prevent brittle, non-portable outputs, this rule is mandatory and non-negotiable.

1.  **MUST Dynamically Generate Vega-Lite:** Agents **MUST** dynamically generate visualization specifications using the Vega-Lite JSON format. This ensures the output is a portable, self-contained artifact that can be rendered in any modern markdown viewer or web browser without requiring a Python kernel or external libraries. The generation logic must be based on an in-context analysis of the input data and the user's analytical goal.

2.  **MUST NOT Use Python Scripts for Plotting:** Agents **MUST NOT** generate Python code (e.g., using Matplotlib, Seaborn) for visualization as the primary output. This practice violates the `artifact-portability-policy`. Python plotting is only permissible when a specific, non-portable file format (like a `.png` dump) is explicitly requested for a legacy system.

3.  **MUST NOT Use Static Templates:** Agents **MUST NOT** use static, pre-written Vega-Lite templates. The JSON specification must be constructed dynamically to adapt to the specific data schema (column names, data types, etc.).

## 3. GEPA Rule: Visual Richness and Textual Interpretability

To prevent errors of misinterpretation, all visualizations must be both visually effective and textually explained.

1.  **Select the Right Visualization for the Task:** Do not default to simplistic charts. The choice of `mark` and `encoding` in the Vega-Lite specification must be driven by the analytical goal, adhering to the `illustrative-power-policy`:
    *   **Correlations:** Use `mark: "point"` (scatter plots) or `mark: "rect"` (heatmaps).
    *   **Distributions:** Use `mark: "bar"` with binning (histograms) or `mark: "boxplot"`.
    *   **Comparisons:** Use `mark: "bar"` or `mark: "arc"` (donuts, with caution).
    *   **Time Series:** Use `mark: "line"`.

2.  **Provide a Textual Insight Summary:** The `vega-lite` JSON block **MUST** be immediately followed by a concise, human-readable summary explaining the primary insight revealed by the visualization. Simply describing the chart is non-compliant. The text must explain what the data *means*.

## 4. Mandatory Workflow & QA

All visualization generation must follow a strict, multi-stage process:
1.  **Analyze:** Examine the input data and the user's goal.
2.  **Select & Design:** Choose the most effective visualization type and design the Vega-Lite spec.
3.  **Generate:** Create the Vega-Lite JSON and the textual insight summary.
4.  **Validate:** The combined output (JSON + text) **MUST** be validated using the `gtb-validator` with the `task_type="data_analysis"` before being shown to the user.

---

### Correct Usage Example (Compliant)

**Goal:** "Show me the relationship between horsepower and fuel efficiency in this dataset."

**Agent's Process:**
1.  **Analyze:** The goal is to find a correlation between two quantitative variables: `horsepower` and `miles_per_gallon`.
2.  **Select & Design:** A scatter plot is the ideal visualization for this task.
3.  **Generate:** Create the Vega-Lite JSON for a scatter plot and write the insight summary.
4.  **Validate:** Pass the complete markdown output to the `gtb-validator`.

**Final Output:**
```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "description": "A scatter plot showing the negative correlation between Horsepower and Miles per Gallon.",
  "data": { "url": "data/cars.json" },
  "width": "container",
  "height": "container",
  "mark": "point",
  "encoding": {
    "x": {
      "field": "Horsepower",
      "type": "quantitative",
      "title": "Engine Horsepower"
    },
    "y": {
      "field": "Miles_per_Gallon",
      "type": "quantitative",
      "title": "Fuel Efficiency (MPG)"
    },
    "tooltip": [
      {"field": "Name", "type": "nominal"},
      {"field": "Horsepower", "type": "quantitative"},
      {"field": "Miles_per_Gallon", "type": "quantitative"}
    ]
  }
}
```

**Insight Summary:** The visualization clearly shows a negative correlation between horsepower and fuel efficiency. As a car's horsepower increases, its miles per gallon (MPG) tends to decrease, indicating a trade-off between power and efficiency.

### Incorrect Usage Example (Non-Compliant)

**Goal:** "Show me the relationship between horsepower and fuel efficiency."

**Agent's Output:**
```python
# NON-COMPLIANT: Violates portability policy
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_json("data/cars.json")
plt.scatter(df['Horsepower'], df['Miles_per_Gallon'])
plt.xlabel('Engine Horsepower')
plt.ylabel('Fuel Efficiency (MPG)')
plt.title('Horsepower vs. MPG')
plt.show()
```
**(Fails because it generates a Python script and provides no insight summary.)**
