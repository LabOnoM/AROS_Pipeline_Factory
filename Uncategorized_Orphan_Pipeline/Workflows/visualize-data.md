---
description: Triggers an autonomous analysis and generation of technical diagrams
---

# /visualize-data 

## Phase 1: Clarification & Engine Routing
Begin by analyzing the data logic the user wants visualized (infrastructure, UML, analytics, processes).
Immediately check the `agentic_diagramming_standard` KI (Knowledge Item).
Based on the KI rules:
- Will this output be deployed into a final manuscript, LaTeX report, or high-level slide deck?
  **ACTION:** Target `fireworks-tech-graph`.
- Is this a rapid UI prototyping session, interactive data analysis, or a system logic brainstorm? 
  **ACTION:** Target `markdown-scientific-viz`.

## Phase 2: Markdown Generation // turbo
*Applies ONLY if routed to `markdown-scientific-viz`.*

1. Consult the `markdown-scientific-viz` skill documentation.
2. Formulate the correct logic using the appropriate syntax standard (e.g. `vega-lite` for quant data arrays, `mermaid` for pipelines).
3. Print the payload explicitly to the user's IDE terminal wrapped in the correct fencing.

## Phase 3: High-Res SVG Payload // turbo
*Applies ONLY if routed to `fireworks-tech-graph`.*

1. Isolate the target Style (e.g. Dark Terminal, Flat, Glassmorphism).
2. Generate the JSON layout arrays for Node dictionaries and Arrow mappings.
3. Automatically execute the built-in python script template:
   ```bash
   python3 ~/.gemini/skills/fireworks-tech-graph/scripts/generate-from-template.py architecture ./output.svg '<valid_json_payload>'
   ```
4. Request the CLI to run `rsvg-convert` to render the PNG equivalent if installed in the host OS.

## Phase 4: Walkthrough 
Once visualization is successfully dumped, present an artifact walkthrough mapping the generated graph to the raw logic strings. Emphasize exactly what the generated shapes map to in reality.
