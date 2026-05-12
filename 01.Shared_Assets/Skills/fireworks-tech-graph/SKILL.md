---
cpcp_asset: true
name: fireworks-tech-graph
description: High-fidelity, publication-ready SVG + PNG technical diagrams. Generates diagrams representing System Architectures, Cloud Deployments, Flows, and Neural Networks using rsvg-convert. Use when the user requests "high resolution", "publication-grade", "LaTeX export", "architecture diagram", or specifies styles like "dark terminal" or "glassmorphism".
metadata:
  author: yizhiyanhua-ai (Optimized for Antigravity)

cpcp_asset: true
---

# Fireworks Tech Graph

This skill enables the autonomous generation of visually stunning, publication-ready technical diagrams in SVG format, exported to high-resolution (1920x) PNGs.

## Execution Rules
1. Decide the diagram Layout: Architecture (Layers), Sequence (Lifelines), Flowchart (Grid+Diamonds).
2. Use Python to generate SVGs programmatically to avoid syntax errors inside the Antigravity Terminal.
3. Once the SVG is created, validate and generate the PNG using the helper script if `rsvg-convert` is available.

## Template Helpers (Recommended)
You can directly formulate your nodes, arrows, and styles, and pass them to the built-in python engine. 
*Path*: `~/.gemini/skills/fireworks-tech-graph/scripts/generate-from-template.py`

### Usage:
Execute via `run_command`:
```bash
python3 ~/.gemini/skills/fireworks-tech-graph/scripts/generate-from-template.py architecture ./output.svg '{"title":"System","nodes":[{"id":"app","label":"Frontend"}],"arrows":[{"source":"app","target":"db","label":"query"}]}'
```

## Raw SVG Generation
If building raw SVGs, use strict Semantic Vocabularies. 
**ALWAYS generate via Python list appends** (to prevent truncation):
```python
lines = []
lines.append('<svg viewBox="0 0 960 700" xmlns="...">')
lines.append('<!-- Draw Content -->')
lines.append('</svg>')
with open('/path/to/img.svg', 'w') as f: f.write('\n'.join(lines))
```

## Shapes & Styles
- Agent = Hexagon
- Vector DB = Cylinder with grid inside
- Memory = Dashed Rounded Rect
- LLM / Model = Double-border rounded rect

Styles:
1. Flat Icon (White, Minimal)
2. Dark Terminal (Neon, Mono)
3. Blueprint (Dark blue, Cyan grid)
4. Notion Clean
5. Glassmorphism
6. Claude Official (Anthropic brand palettes)
7. OpenAI Official (White + Green)

> To compile your SVG into a PNG required for final UI embedding:
> `rsvg-convert -w 1920 diagram.svg -o diagram.png`
