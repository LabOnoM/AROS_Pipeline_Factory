# Unified Scientific Diagramming

To eliminate fragmentation and redundant logic across different pipelines within the AROS Pipeline Factory, all scientific diagramming tasks MUST be routed through the unified `visualize-data` skill.

## 1. Engine Consolidation
- **Primary Engine**: `fireworks-tech-graph` is the canonical framework for generating high-resolution, publication-ready SVG and PNG diagrams (e.g., grant lifecycle timelines, dual-agent architecture workflows).
- **Renderer**: `cairosvg` is the mandated cross-platform renderer for PNG conversion. The legacy dependency on system-level `librsvg2-bin` has been permanently removed to ensure compatibility across macOS, Ubuntu, and Windows.
- **Legacy Deprecation**: Narrow-scope skills such as `grant-gantt-chart-gen` and `text-to-technical-roadmap` are deprecated. Their semantic templates have been absorbed into the `/visualize-data` orchestrator's domain templates directory (`~/.gemini/skills/visualize-data/templates/`).

## 2. Usage
Agents should use the `visualize-data` skill, which will load the appropriate scientific shape vocabulary and predefined JSON templates to generate aesthetically consistent and semantically correct visual artifacts.
