# DEPRECATED SKILL: text-to-technical-roadmap

> **Status**: DEPRECATED as of 2026-05-11
> **Replaced by**: `visualize-data` skill (global, `~/.gemini/skills/visualize-data/`)
> **SPEC Reference**: SPEC.md §10.1 (Unified Scientific Diagramming)

## Why Deprecated
This skill has been superseded by the unified `visualize-data` orchestrator, which provides the same Mermaid-to-flowchart functionality (via `markdown-scientific-viz`) plus the more powerful `fireworks-tech-graph` high-resolution SVG pipeline. The `visualize-data` skill can handle both rapid Mermaid prototypes AND publication-grade technical roadmap diagrams.

## Migration
Replace any call to `text-to-technical-roadmap` with:
- **For quick Mermaid prototypes**: `visualize-data` → `markdown-scientific-viz` engine
- **For publication-grade SVG/PNG**: `visualize-data` → `fireworks-tech-graph` engine

See `agentic_diagramming_standard` KI and `visualize-data` SKILL.md for full instructions.
