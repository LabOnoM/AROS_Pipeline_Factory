# Data Analysis Pipeline Context

## 🧭 Domain Context
This pipeline handles statistical modeling, data plotting, flow cytometry gating (flowcypy), and quantitative analyses.

## ⚖️ Component Rules
- **Visualization**: All scientific diagrams and graphs must funnel through the unified `visualize-data` shared skill (utilizing fireworks-tech-graph and cairosvg).
- **Execution Sandboxing**: Agents performing deep data analysis MUST execute code using the established Sandbox rules to prevent environment corruption.

## 🚀 Execution
- **Trigger**: The `/visualize-data` workflow governs diagrammatic and statistical charting operations.
