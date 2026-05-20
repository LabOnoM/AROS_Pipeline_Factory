---
name: ppt
description: Create and export PPTX decks using the local HTML/JS PPT framework in `D:\SKILL\project\ppt`. Use this when you need to generate slides from a topic/outline, edit slide content via `projects/*.js`, preview as HTML, or export a `.pptx` without relying on an existing template.
license: MIT
skill-author: AIPOCH
---

## When to Use

- You need to generate a new slide deck from a topic, brief, or outline (typically 6–10 sections).
- You want to iteratively edit slide content/structure in a code-first way using `D:\SKILL\project\ppt\projects\*.js`.
- You need a quick HTML preview of the deck before exporting to PowerPoint.
- You want to export a `.pptx` without starting from a pre-made PPT template.
- You need consistent, reusable slide components (e.g., timeline, comparison, stats) across decks.

## Key Features

- **Code-driven deck authoring** via a `const SLIDES = [...]` data model in `projects/*.js`.
- **Reusable slide components** such as `comparison`, `timeline`, `stats`, `valueCards`, `quote`, and `ending`.
- **Two-step output pipeline**: HTML preview generation and PPTX export.
- **Deterministic outputs** saved to `D:\SKILL\project\ppt\output\`.
- **Simple dependency management** via `requirements.txt`.

## Dependencies

- **Python 3.10+** (recommended)
- **pip** (matching your Python installation)
- **Python packages**: install from  
  `D:\SKILL\project\ppt\requirements.txt`  
  (exact versions are defined in that file)

## Example Usage

### 1) Create a project file

Create:

`D:\SKILL\project\ppt\projects\demo-20260227.js`

```javascript
const SLIDES = [
  {
    badge: { icon: "*", text: "DEMO" },
    title: { text: "PPT Framework Demo" },
    subtitle: "Build once in JS, preview in HTML, export to PPTX",
    clickHint: "2026-02-27 / v1",
    elements: [
      {
        step: 1,
        type: "quote",
        text: "A code-first slide model makes decks fast to iterate and easy to standardize.",
        author: { icon: "-", text: "Key takeaway" }
      }
    ]
  },
  {
    badge: { icon: "#", text: "OVERVIEW" },
    title: { text: "What You Will See" },
    subtitle: "A minimal multi-slide example",
    clickHint: "Agenda",
    elements: [
      {
        step: 1,
        type: "valueCards",
        items: [
          { title: "Authoring", value: "projects/*.js", note: "Edit SLIDES data" },
          { title: "Preview", value: "HTML", note: "Fast iteration loop" },
          { title: "Export", value: "PPTX", note: "Shareable output" }
        ]
      }
    ]
  },
  {
    badge: { icon: ">", text: "END" },
    title: { text: "Thank You" },
    subtitle: "Questions?",
    clickHint: "Export-ready",
    elements: [{ step: 1, type: "ending" }]
  }
];

module.exports = { SLIDES };
```

### 2) Install dependencies (if needed)

From `D:\SKILL\project\ppt`:

```bash
pip install -r requirements.txt
```

### 3) Preview as HTML

From `D:\SKILL\project\ppt`:

```bash
python build_html.py demo-20260227
```

### 4) Export to PPTX

From `D:\SKILL\project\ppt`:

```bash
python convert_to_pptx.py demo-20260227
```

Outputs are written to:

`D:\SKILL\project\ppt\output\`

## Implementation Details

- **Authoring model**: each deck is defined as `const SLIDES = [...]`, where each slide is an object containing:
  - `badge`: small label with `icon` and `text`
  - `title`: `{ text: "..." }` (keep short and specific)
  - `subtitle`: one-sentence context
  - `clickHint`: date/version or navigation hint
  - `elements`: ordered visual/content blocks; each element includes:
    - `step`: render/order index
    - `type`: component type (e.g., `quote`, `timeline`, `comparison`, `stats`, `valueCards`, `ending`)
    - component-specific fields (e.g., `items`, `text`, `author`)
- **Workflow**:
  1. Draft an outline (6–10 sections; one intent per section).
  2. Expand each section into 3–5 concise bullets.
  3. Encode slides in `projects/<topic>-YYYYMMDD.js`.
  4. Generate HTML for rapid review, then export to PPTX.
- **Design constraints (recommended)**:
  - Use a bold, topic-specific palette: **1 dominant color + 2 supporting colors + 1 accent**.
  - Ensure every slide includes a **visual component**; avoid text-only slides.
  - Keep spacing consistent; maintain margins **≥ 0.5 inch**.