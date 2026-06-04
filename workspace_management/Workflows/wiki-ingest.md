---
description: Ingest new experimental results, papers, or data into the project's LLM-Wiki
---

# Wiki Ingest Workflow

// Note: All commands must execute from the active project root.

Run this workflow whenever a new paper is downloaded or a new experiment is completed, to ensure knowledge compounds inside the `.wiki/` directory.

## Step 1: Identify Target

Determine the file(s) that need to be ingested.
```bash
# E.g., recent articles added in the last 7 days
find Articles 00.RawData -type f -mtime -7
```

## Step 1.5: Auto-Convert PDFs (If Applicable)

If the identified target files include `.pdf` files, invoke the `literature-ingestion` shared skill to convert them to Markdown before proceeding:

1. Copy new PDFs to `00.RawData/Literature/02_Raw_PDFs/`.
2. Run `python ~/.gemini/skills/literature-ingestion/scripts/pdf_converter.py`.
3. The resulting `.md` files in `03_Parsed_Markdown/` become the ingestion targets for Step 2.

## Step 2: Extract Content (Human-in-the-Loop)

According to the LLM-Wiki philosophy, **avoid fully automated mass ingestion**. Process one or a few documents at a time and involve the user.

- **PDFs and Images**: Since standard python environments might lack PDF/image parsing libraries locally, use the **browser subagent** to read PDFs and images.
- **Office Documents (.docx, .pptx)**: Extract text content using Python via the `run_command` tool (e.g., using `python-docx`, `python-pptx`, or parsing the `word/document.xml` directly via `zipfile`).
- **Spreadsheets (.xlsx, .csv)**: To prevent context window bloat, **DO NOT extract all rows**. Instead, write a quick python snippet using `pandas` or `openpyxl` to extract only the metadata: Sheet names, column headers, data shape (rows/cols), and the top 5 rows. In the source page, describe its purpose and embed a direct file link to the raw data file.

Prompt the agent with the specific strategy required for the given file type.

## Step 3: Create Source Page

1. Create a new markdown file in `.wiki/sources/[Author]-[Year]-[Topic].md`.
2. Format using the standard YAML frontmatter defined in `.wiki/SCHEMA.md`.
3. Synthesize the findings into English.

## Step 4: Update Entities and Concepts

1. Scan the new source page for biological entities (e.g., [[SP7]], [[RUNX2]], [[Alternative Splicing]]).
2. Open the corresponding `.wiki/entities/` or `.wiki/concepts/` pages.
3. Update them to reflect the new evidence. Do not just rewrite them; *compound* the knowledge.

## Step 5: Log the Ingestion

Open `.wiki/log.md` and append a new entry:
`- **YYYY-MM-DD HH:MM**: INGESTED [[Source Page Link]]. Updated [[Entity1]] and [[Entity2]].`

## Step 6: Auto-Commit

Delegate to the canonical `/lab-commit` workflow. Do NOT write inline `git add` / `git commit` commands here — the lab-commit workflow handles staging, Obsidian symlink verification, project registry updates (e.g., INDEX.csv or PIPELINE_REGISTRY.md), and commit message formatting automatically.
