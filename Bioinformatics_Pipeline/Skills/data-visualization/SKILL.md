---
name: data-visualization
description: Dynamically generates Python plotting code using an LLM to create visualizations tailored to specific data structures and analytical goals, enhancing analytical scope and flexibility.
license: MIT
skill-author: AROS-GEPA-System
---

# Data Visualization

## Overview

This skill governs the generation of data visualizations. It ensures that plotting code is always dynamically created to fit the specific context of the data and the analytical objective, rather than relying on inflexible, pre-defined templates. The goal is to maximize analytical insight and adapt to novel data structures.

## GEPA Error Prevention Rule: No Static Templates

This is a mandatory, non-negotiable error prevention rule to avoid brittle, non-adaptive plotting logic that fails when data schemas change.

1.  **MUST Dynamically Generate Code:** Agents **MUST** use a large language model (LLM) to write Python plotting code (e.g., using Matplotlib, Seaborn, Plotly) based on an analysis of the input data's structure and the user's analytical goal. The code should be generated in-context during the task execution.

2.  **MUST NOT Use Static Templates:** Agents **MUST NOT** use static, pre-written code templates where variables are simply filled in. This practice is strictly forbidden as it limits the analytical scope and leads to errors when data deviates from the template's expected format.

### Rationale

-   **Flexibility:** Dynamic generation allows the system to create novel plot types (e.g., heatmaps, pair plots, 3D plots) that a static template could never anticipate.
-   **Robustness:** The skill can adapt to any tabular data structure, regardless of column names, data types, or dimensions, preventing failures when data schemas evolve.
-   **Insight:** By reasoning about the analytical goal, the LLM can generate visualizations that are more likely to reveal meaningful patterns in the data.

## Implementation

The core logic is implemented in `scripts/main.py`. It accepts a pandas DataFrame and a user's natural language goal, interfaces with an LLM to generate plotting code, and then executes that code.


## D3.js and Interactive Web Visualizations (Merged from Benchflow)

- When targeting standalone HTML reports, prefer D3.js over static Matplotlib PNGs for interactive data exploration.
- Ensure JSON data is embedded correctly into the D3 state without CORS issues.