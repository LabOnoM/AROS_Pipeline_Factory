---
name: visualize-data
description: Triggers an autonomous analysis and generation of technical diagrams and data plots from natural language queries.

cpcp_asset: true
---

# /visualize-data

## GEPA Error Prevention Rule: Seamless Query-to-Plot Integration

To prevent misinterpretation and failed handoffs between language understanding and code generation, the following rule is mandatory:

**LLM-powered query understanding must seamlessly integrate with code generation to enable custom plot creation directly from natural language. The data structures and prompt chains must pass the parsed query directly to the visualization code generator without losing semantic intent.**

---

## Phase 1: Query Understanding & Semantic Extraction
The workflow begins by using an LLM to parse the user's natural language query. This is not a simple keyword search; it is a deep semantic analysis to extract a structured representation of the visualization request.

1.  **Analyze the Query:** Deconstruct the user's request to identify key components:
    *   **Data Source(s):** What data needs to be visualized? (e.g., a specific file, a database table, an in-memory dataframe).
    *   **Plot Type:** What is the desired visualization? (e.g., bar chart, scatter plot, heatmap). If not specified, infer the best type from the analytical goal.
    *   **Variables:** What columns or features should be on the x-axis, y-axis, color, size, etc.?
    *   **Analytical Goal:** What is the user trying to understand or show? (e.g., "compare sales across regions," "show the correlation between A and B").
2.  **Create Semantic Intent Payload:** Package these extracted components into a structured object (e.g., a JSON object or dictionary). This payload is the single source of truth for the rest of the workflow, ensuring no semantic intent is lost.

## Phase 2: Clarification & Engine Routing
Using the **Semantic Intent Payload** from Phase 1, the agent routes the request to the appropriate visualization engine.

1.  Immediately check the `agentic_diagramming_standard` KI (Knowledge Item).
2.  Based on the KI rules and the extracted intent:
    *   **Target: `fireworks-tech-graph` (via Domain Templates)** for grant workflows, manuscript review cycles, and experimental protocols. Use the presets in `~/.gemini/skills/visualize-data/templates/` and vocabulary from `~/.gemini/skills/visualize-data/vocabulary/scientific_shapes.md`.
    *   **Target: `fireworks-tech-graph` (Custom)** for high-resolution, manuscript-quality diagrams like infrastructure, UML, or complex system architectures.
    *   **Target: `markdown-scientific-viz`** for rapid UI prototyping, interactive data analysis, or system logic brainstorming. This engine is the primary target for quantitative data plotting and will adhere to the `dynamic-plot-code-generation` skill.

## Phase 3: Markdown Generation // turbo
*Applies ONLY if routed to `markdown-scientific-viz`.*

1.  Consult the `markdown-scientific-viz` skill documentation.
2.  **Use the Semantic Intent Payload** to dynamically generate the correct visualization code using the appropriate syntax standard (e.g., `vega-lite` for quant data arrays, `mermaid` for pipelines). This step MUST comply with the `dynamic-plot-code-generation` policy, generating code on the fly rather than using static templates.
3.  Print the payload explicitly to the user's IDE terminal wrapped in the correct fencing.

## Phase 4: High-Res SVG Payload // turbo
*Applies ONLY if routed to `fireworks-tech-graph`.*

1.  **Select Style:** Isolate the target Style from the user request or autonomously choose from the 7 available styles based on the context:
    *   `style-1-flat-icon`: Cleanest, professional for journal figures.
    *   `style-2-dark-terminal`: Code/developer aesthetic.
    *   `style-3-blueprint`: Engineering schematic.
    *   `style-4-notion-clean`: Minimal, ideal for grant proposals.
    *   `style-5-glassmorphism`: Modern UI.
    *   `style-6-claude-official`: Warm, professional for presentations.
    *   `style-7-openai`: Clean, stark.
2.  **Generate Payload:** Use the **Semantic Intent Payload** to generate the JSON layout arrays for Node dictionaries and Arrow mappings. If a Domain Template applies (e.g. `grant_lifecycle.json`), inject it.
3.  **Execute SVG Rendering:** Automatically execute the built-in python script template:
   ```bash
   python3 ~/.gemini/skills/fireworks-tech-graph/scripts/generate-from-template.py architecture ./output.svg '<valid_json_payload>'
   ```
4.  **Convert to PNG:** Use `cairosvg` to convert the SVG to a PNG (Standardized renderer for AROS):
   ```bash
   python3 -c "import cairosvg; cairosvg.svg2png(url='./output.svg', write_to='./output.png', output_width=1920)"
   ```
