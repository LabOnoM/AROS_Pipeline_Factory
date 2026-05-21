---
cpcp_asset: true
name: ppt
description: Create and export PPTX decks using the local HTML/JS PPT framework in `D:\SKILL\project\ppt`. Use this when you need to generate slides from a topic/outline, edit slide content via `projects/*.js`, preview as HTML, or export a `.pptx` without relying on an existing template.
license: MIT
skill-author: AIPOCH
---

## Validation Shortcut

Run this minimal command first to verify the supported execution path:

```bash
python scripts/validate_skill.py --help
```

## When to Use

- You need to generate a new slide deck from a topic, brief, or outline (6-10 sections) and want a consistent visual style.
- You want to iteratively edit slide content and structure in code (`projects/*.js`) rather than in PowerPoint.
- You need a fast HTML preview loop before exporting a final `.pptx`.
- You must export a `.pptx` without starting from an existing PowerPoint template.
- You want to standardize slide layouts using predefined component types (e.g., comparison, timeline, stats).

## Key Features

- Code-driven deck authoring via `const SLIDES = [...]` in `projects/*.js`.
- Built-in slide element/component types (e.g., `comparison`, `timeline`, `stats`, `valueCards`, `quote`, `ending`).
- HTML preview generation for quick review and iteration.
- PPTX export pipeline producing a PowerPoint-compatible `.pptx`.
- Consistent layout rules (spacing, margins) and guidance for palette selection.

## Dependencies

- Python (3.10+ recommended)
- Python packages listed in: `D:\SKILL\project\ppt\requirements.txt`

## Example Usage

### 1) Create a project file

Create: `D:\SKILL\project\ppt\projects\demo-20260227.js`

```javascript
const SLIDES = [
  {
    badge: { icon: "*", text: "DEMO" },
    title: { text: "PPT Framework Demo" },
    subtitle: "Build in JS, preview in HTML, export to PPTX",
    clickHint: "2026-02-27 / v1",
    elements: [
      {
        step: 1,
        type: "quote",
        text: "A code-first workflow makes decks reproducible and easy to iterate.",
        author: { icon: "-", text: "Key takeaway" }
      }
    ]
  },
  {
    badge: { icon: "*", text: "AGENDA" },
    title: { text: "What We Will Cover" },
    subtitle: "A simple outline slide",
    clickHint: "Section 1/3",
    elements: [
      { step: 1, type: "valueCards", title: "Authoring", items: ["Edit `projects/*.js`", "Use `const SLIDES`"] },
      { step: 2, type: "valueCards", title: "Preview", items: ["Generate HTML", "Review layout quickly"] },
      { step: 3, type: "valueCards", title: "Export", items: ["Convert to PPTX", "Share the deck"] }
    ]
  },
  {
    badge: { icon: "*", text: "END" },
    title: { text: "Next Steps" },
    subtitle: "Export and refine",
    clickHint: "Section 3/3",
    elements: [
      { step: 1, type: "ending", title: "Export the deck", bullets: ["Run HTML build", "Run PPTX conversion"] }
    ]
  }
];

module.exports = { SLIDES };
```

### 2) Preview as HTML

From `D:\SKILL\project\ppt`:

```bash
python build_html.py demo-20260
```