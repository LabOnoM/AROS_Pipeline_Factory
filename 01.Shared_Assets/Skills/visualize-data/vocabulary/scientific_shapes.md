---
cpcp_asset: true
---
# Extended Scientific Shape Vocabulary

This vocabulary maps conceptual semantic meanings to SVG shapes supported by `fireworks-tech-graph`. When generating node data for diagrams, map the domain concept to the correct `shape` key.

| Shape Key | Primary Semantic Meaning | Example Usage |
|---|---|---|
| `rect` | Process Step / Action | "Draft Abstract", "Run Analysis" |
| `hexagon` | AI Agent / Actor | "Reviewer Agent", "Data Scraper" |
| `diamond` | Decision Gate / Quality Check | "Peer Review", "Editor Approval" |
| `cylinder` | Storage / Database | "Literature Corpus", "Results Archive" |
| `document` | Output / Manuscript / File | "Draft.md", "Funder Profile", "CV" |
| `shield` | Validation / Security | "Ethics Review", "Secure Delivery" |
| `beaker` | Lab Experiment / Method | "PCR", "Cell Culture", "Imaging" |
| `clock` | Deadline / Timeline Milestone | "Submission Due", "Phase 1 Complete" |
| `currency` | Budget / Allocation | "Grant Budget", "Personnel Cost" |
| `double_rect` | LLM Model / External API | "Gemini 2.5 Pro", "OpenAI Router" |

## Edge Types (Inherited)
- `write` (solid line, main flow)
- `read` (dashed line, data retrieval)
- `async` (dotted line, parallel tasks)
- `loop` (curved solid line, feedback/iteration)
