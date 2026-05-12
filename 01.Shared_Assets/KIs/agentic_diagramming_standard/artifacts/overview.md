---
cpcp_asset: true
---
# Agentic Diagramming & Visualization Standard

This standard dictates the correct methodology for Antigravity AI agents generating visual diagrams, plots, and charts based on user prompts.

## Dual-Modal Visualization Heuristic

**Do not guess the visualization method.** First evaluate the domain context and the target output environment.

### 1. Markdown Fencing (For IDE, UI, and Prototypes)
When the user is conducting interactive analysis within the Antigravity IDE, asking for quick flowcharts, or building data dashboards directly inside `.md` documentation files, use the **`markdown-scientific-viz`** composite skill.

This provides the agent with 15 fenced-block standards:
- **` ```mermaid `**: Quick process flows, state machines, API interactions.
- **` ```vega `**: Data quantitative charts (scatter, bar, density grids).
- **` ```plantuml `**: Deep UML structures, Cloud architectures, and BPMN pipelines.
- **`Raw HTML (infocard/architecture)`**: Editorial or structured UI layer representation.

*Advantage:* Instantly renders in compatible IDE previewers without background processing overhead or external library dependencies.

### 2. High-Res SVG/PNG Pipelines (For Final Reports & Manuscripts)
When the task requires polished, print-ready, or presentation-quality diagrams (e.g., LaTeX embedding, Journal figures, Slide decks, System Architecture Overviews), use the **`fireworks-tech-graph`** framework.

- **Process:** Generate structured XML nodes directly through the `fireworks-tech-graph` Python helper templates to avoid text clipping. For scientific workflows (grants, manuscripts), use the `visualize-data` skill to inject domain-specific JSON templates.
- **Export:** The system natively uses Python's `cairosvg` to render lossless SVGs into 1920px PNGs.
- **Ruleset:** Restrict the output to one of 7 official visual styles (e.g., Flat Icon, Claude Official, Dark Terminal), strictly adhering to structural semantic patterns (e.g., hexa=Agent, cylinder=Memory, beaker=Lab Experiment).

*Advantage:* Absolute aesthetic control, mathematically perfect alignment via Python templating, cross-platform compatibility, and true publication-grade deliverables.

> [!NOTE]
> High-Res exports **require** the user to have installed `cairosvg` (`pip install cairosvg`) on the host system. System-level `librsvg2-bin` is no longer the required standard due to cross-platform (macOS/Windows) inconsistencies.
