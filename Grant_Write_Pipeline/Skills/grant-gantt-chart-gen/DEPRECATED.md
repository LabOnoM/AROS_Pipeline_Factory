# DEPRECATED SKILL: grant-gantt-chart-gen

> **Status**: DEPRECATED as of 2026-05-11
> **Replaced by**: `visualize-data` skill (global, `~/.gemini/skills/visualize-data/`)
> **SPEC Reference**: SPEC.md §10.1 (Unified Scientific Diagramming)

## Why Deprecated
This skill has been superseded by the unified `visualize-data` orchestrator, which uses the `fireworks-tech-graph` Python framework with `cairosvg` rendering to produce publication-grade SVG/PNG diagrams. The `visualize-data` skill supports Gantt chart generation via domain templates in `~/.gemini/skills/visualize-data/templates/`.

## Migration
Replace any call to `grant-gantt-chart-gen` with:
```
visualize-data → fireworks-tech-graph → grant lifecycle / Gantt domain template
```

See `agentic_diagramming_standard` KI and `visualize-data` SKILL.md for full instructions.
