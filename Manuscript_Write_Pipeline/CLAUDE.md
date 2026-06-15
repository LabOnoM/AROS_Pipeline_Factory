# Manuscript Write Pipeline Context

## 🧭 Domain Context
This pipeline is responsible for academic and scientific manuscript authoring. It orchestrates the dual-agent review cycle and method-writing logic.

## ⚖️ Component Rules
- **Markdown-First Policy**: All manuscripts must be drafted in Markdown. Direct LaTeX generation is prohibited (per `markdown_first_manuscript_policy.md`).
- **Citation-Before-Claim Protocol**: Agents must pull literature via `literature-close-read` before making scientific claims.
- **Graphical Abstracts**: Handled via `visualize-data` in phase A1.5.

## 🚀 Execution
- **Trigger**: The `/manuscript-write` workflow governs operations here.
