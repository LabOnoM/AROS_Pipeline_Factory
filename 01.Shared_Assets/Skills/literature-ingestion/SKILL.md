---
name: literature-ingestion
description: Centralized shared skill for retrieving academic PDFs via a tiered cascade (OA APIs -> Institutional Proxies -> LibGen -> Sci-Hub) and batch converting them to Markdown using opendataloader-pdf in hybrid mode.
license: MIT
cpcp_asset: true
---

## When to Use

- The user or a workflow needs to ingest academic papers based on a list of DOIs, PMIDs, or free-text reference lists.
- A workflow (e.g., `/wiki-ingest`) encounters PDF files that need to be parsed into Markdown for the LLM-Wiki.
- You need to download literature while respecting the AROS fallback cascade (Open Access APIs first, then shadow libraries).

> [!WARNING]
> **DEPRECATION NOTICE**: This skill supersedes and replaces the global `research-paper-downloader` skill within the AROS Pipeline Factory. Agents MUST use `literature-ingestion` instead of `research-paper-downloader` to ensure SAMS/CPCP compliance and automatic Markdown conversion.

## Key Features

- **6-Tier Retrieval Cascade**:
  1. Semantic Scholar (Open Access)
  2. Unpaywall (Open Access)
  3. PubMed Central (Open Access)
  4. Publisher Landing Page (with optional Institutional Proxy injection)
  5. LibGen / Anna's Archive (Shadow Library Fallback)
  6. Sci-Hub (Shadow Library Fallback)
- **Full Performance Parsing**: Uses `opendataloader-pdf` in hybrid mode to extract text, tables, formula LaTeX, and generate image descriptions using SmolVLM.
- **Dual-Format Output (Markdown + JSON)**: Enforces simultaneous output of Markdown for LLM efficiency and JSON for structural validation.
- **Batch Processing**: Converts all PDFs efficiently in a single JVM pass.
- **Idempotent**: Skips DOIs that have already been downloaded or converted.

## Downstream Usage

- **Markdown (`03_Parsed_Markdown/`)**: Used for LLM context, RAG integration, and `/wiki-ingest` processing. Fast and token-efficient.
- **JSON (`04_Parsed_JSON/`)**: Used for rigorous structural verification, extracting precise bounding boxes, and validating metadata.
- **Deep Reading**: For structured evidence extraction and strict grounding, pass the parsed Markdown file to the `literature-close-read` skill.

## Dependencies

- Python `>= 3.10`
- `requests >= 2.28`
- `beautifulsoup4 >= 4.12`
- `opendataloader-pdf[hybrid] >= 0.2` (Requires Java 11+)

## Example Usage

### Download and Convert DOIs

```bash
python 01.Shared_Assets/Skills/literature-ingestion/scripts/fetch_and_convert.py --input 00.RawData/Literature/01_Target_DOIs.txt
```

### Convert Existing PDFs

If PDFs are already in `00.RawData/Literature/02_Raw_PDFs/`, you can just run the converter. It will automatically apply the `-f markdown,json` flag from `config.json`:

```bash
python 01.Shared_Assets/Skills/literature-ingestion/scripts/pdf_converter.py
```

## Output Artifacts

All outputs are routed to `00.RawData/Literature/`:
- `02_Raw_PDFs/`: The raw downloaded `.pdf` files.
- `03_Parsed_Markdown/`: The `.md` text outputs from `opendataloader-pdf`.
- `04_Parsed_JSON/`: The `.json` outputs containing bounding boxes.
- `05_Metadata/`: Clean JSON metadata for each paper (Title, Authors, DOI, Source Tier).
- `failed_downloads.json`: A manifest of DOIs that failed all retrieval tiers.
