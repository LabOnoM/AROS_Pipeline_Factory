---
name: markdown-scientific-viz
description: Generates rapid, interactive visual data grids natively. Use for flowcharting, API mapping, data pipelines, analytical plotting, and UI layer visualizations. Trigger when user requests "data chart", "mind map", "uml layout", or "quick architecture diagram" inside the IDE without high-res SVG export requirements.
metadata:
  author: markdown-viewer & Antigravity Synthesis
---

# Markdown Scientific Visualization Stack

This composite skill empowers agents to draw beautiful diagrams, complex UML configurations, and analytical Data Science plots instantly using Markdown IDE fenced blocks.

**CRITICAL RULE:** Do NOT wrap HTML/CSS outputs (`architecture`, `infocard`) in code blocks. Fenced tools MUST use exact syntax markers.

## 1. Flowcharts & Sequences (Mermaid / PlantUML)
**Fences:** ` ```mermaid ` or ` ```plantuml `

Mermaid is preferred for rapid simplicity (State machines, APIs).
PlantUML is required for complex network modeling, cloud infra, and enterprise components.

*Example PlantUML:*
```plantuml
@startuml
skinparam handwritten true
node "Database" as db
node "Web Server" as web
web -> db: Query
@enduml
```

## 2. Quantitative Data / Analytics (Vega-Lite)
**Fence:** ` ```vega-lite ` or ` ```vega `
Use for plotting data points, distributions, heatmaps, and statistical comparisons natively without running python matplotlib scripts.

*Example:*
```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": { "values": [{"a": "A", "b": 28}, {"a": "B", "b": 55}] },
  "mark": "bar",
  "encoding": {
    "x": {"field": "a", "type": "nominal"},
    "y": {"field": "b", "type": "quantitative"}
  }
}
```

## 3. Spatial Mind Maps (Canvas)
**Fence:** ` ```canvas `
Outputs JSON format structured for semantic concept linking and brainstorm logging.

*Example:*
```canvas
{
  "nodes": [
    {"id": "n1", "x": -200, "y": -100, "width": 250, "height": 60, "type": "text", "text": "Core Hypothesis"}
  ],
  "edges": []
}
```

## 4. HTML/CSS Component Architecture 
**No Code Fence.** Emit raw HTML.
Used for representing internal app structure layers. Employs `class="layer"`, `data-theme="dark"`, etc., that the Markdown IDE Viewer natively scoops up and styles beautifully.

## 5. UI Dashboards / InfoCards
**Fence:** ` ```infographic `
YAML-driven KPI dash setups.

*Example:*
```infographic
type: kpi-cards
title: Model Assessment
cards:
  - label: Accuracy
    value: 98%
    color: green
```

> **Recommendation:** Favor interactive Vega-Lite for any metric-based visualization and Mermaid for quick step-by-step logic. Only use Python+matplotlib if specifically enforcing a `.png` dump format in the `/scratch/` directory.
