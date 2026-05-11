# Literature Directory

> **Managed by**: `literature-ingestion` Shared Skill (`01.Shared_Assets/Skills/literature-ingestion/`)

This directory stores all raw literature assets downloaded and processed by the Literature Ingestion Engine.

## Directory Structure

```
Literature/
├── 01_Target_DOIs.txt      # Input: one DOI/PMID per line
├── 02_Raw_PDFs/             # Downloaded PDFs (named: {DOI_slug}.pdf)
├── 03_Parsed_Markdown/      # opendataloader-pdf output (.md files)
├── 04_Parsed_JSON/          # opendataloader-pdf output (.json with bboxes)
├── 05_Metadata/             # Per-paper metadata JSON (title, authors, source tier)
└── failed_downloads.json    # Manifest of failed retrievals for human follow-up
```

## Naming Convention

- PDF files: `{DOI_with_slashes_replaced_by_underscores}.pdf`
- Metadata: `{DOI_slug}.json`
- Markdown: `{DOI_slug}.md`
