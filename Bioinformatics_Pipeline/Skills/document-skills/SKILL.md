---
name: document-skills
description: Create and manipulate Office documents (DOCX, PDF, PPTX, XLSX) programmatically using Python. Covers generating Word documents, PDF reports, PowerPoint presentations, and Excel spreadsheets with formatting, tables, charts, and images.
original-source: addyosmani/agent-skills/documentation-and-adrs
---

# Document Skills

## Overview

This skill provides guidance for creating and manipulating common document formats programmatically using Python. Each sub-skill covers a specific format:

- **docx** — Word documents via `python-docx`
- **pdf** — PDF generation via `reportlab`, `fpdf2`, or `weasyprint`
- **pptx** — PowerPoint presentations via `python-pptx`
- **xlsx** — Excel spreadsheets via `openpyxl`

## Sub-Skills

For format-specific instructions, refer to:

- `~/.gemini/skills/document-skills/docx/SKILL.md`
- `~/.gemini/skills/document-skills/pdf/SKILL.md`
- `~/.gemini/skills/document-skills/pptx/SKILL.md`
- `~/.gemini/skills/document-skills/xlsx/SKILL.md`

## When to Use

Use this skill when:
- Generating reports, manuscripts, or summaries as downloadable Office files
- Automating document creation pipelines
- Converting analysis results into formatted documents
- Creating presentation slides or spreadsheets from data


## Architecture Decision Records (ADRs) (Merged from Osmani)

When documenting significant decisions, use the ADR format:
1. **Title:** Short noun phrase
2. **Context:** What is the issue?
3. **Decision:** What is the change?
4. **Status:** Proposed/Accepted/Deprecated
5. **Consequences:** What becomes easier or harder?
