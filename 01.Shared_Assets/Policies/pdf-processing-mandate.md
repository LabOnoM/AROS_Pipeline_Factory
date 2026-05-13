# Universal PDF Processing Mandate

**ID**: `pdf-processing-mandate`
**Type**: Factory-Wide Enforcement Policy
**Scope**: All AROS Pipelines & Global Workflows

## 🔒 The Rule
> **Every PDF file encountered by any AROS workflow — whether downloaded, user-provided, or discovered during project onboarding — MUST be routed through the `literature-ingestion` shared skill before its content is consumed by any agent.**

## Protocol

1. **No Raw PDF Reading**: Agents MUST NOT use `pdftotext`, `pdfplumber`, browser subagent PDF viewing, or any other ad-hoc PDF extraction as the primary method. All PDFs must first be processed into the canonical 4-artifact set (Raw PDF → Markdown → JSON → Metadata) via `literature-ingestion`.
2. **Canonical Storage**: All processed PDFs reside in `<PROJECT_ROOT>/00.RawData/Literature/02_Raw_PDFs/`. Agents must not scatter PDFs across arbitrary directories.
3. **Universal Ingestion**: ALL PDFs are treated as knowledge assets and ingested into the Wiki. Non-literature PDFs (admin docs, manuals, forms) are processed equally so their contents are searchable and indexable by the AROS Brain.
4. **Idempotency**: If a PDF's parsed `.md` equivalent already exists in `03_Parsed_Markdown/`, skip re-processing to save compute.
5. **Self-Healing Fallback**: The `pdf_converter.py` script automatically installs its dependency (`opendataloader-pdf[hybrid]`). If the installation or execution fails, it gracefully degrades to extracting raw text via `pdftotext` and formatting it as a basic Markdown document, ensuring the workflow never hits a dead-end loop.
