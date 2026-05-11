---
description: Centralized pipeline for retrieving academic PDFs via tiered cascade and batch-converting to Markdown using full-performance hybrid mode.
---

# Literature Ingest Workflow

Run this workflow when the user requests downloading and converting academic papers from DOIs, PMIDs, or reference lists.

## Step 1: Input Collection

Collect the target DOIs or PMIDs.
1. Save them to `00.RawData/Literature/01_Target_DOIs.txt` (one identifier per line).

## Step 2: Fetch and Convert

Execute the Shared Skill `literature-ingestion`:

```bash
python 01.Shared_Assets/Skills/literature-ingestion/scripts/fetch_and_convert.py --input 00.RawData/Literature/01_Target_DOIs.txt
```

This skill automatically:
- Retrieves PDFs via a 6-tier fallback cascade (OA APIs -> Proxies -> LibGen -> Sci-Hub).
- Converts them to Markdown and JSON via `opendataloader-pdf`.
- Saves output to `00.RawData/Literature/`.

## Step 3: Handle Failures

Review `00.RawData/Literature/failed_downloads.json`. If there are failed downloads, inform the user so they can manually retrieve the PDFs and place them in `02_Raw_PDFs/`.

## Step 4: Auto-Wiki Ingestion

For every successfully converted paper in `03_Parsed_Markdown/`, trigger the `/wiki-ingest` workflow to properly synthesize and integrate the knowledge into the LLM-Wiki `.wiki/` directory.

## Step 5: Commit

Trigger the `/lab-commit` workflow to persist the new raw data and metadata to the repository.
