---
cpcp_asset: true
name: literature-close-read
description: Produce a structured close-reading report from a paper's full PDF-to-Markdown text (with `## Page XX` pagination and image references) when you need to systematically extract background, research questions, methods, results, limitations, and reproducible experimental details.
license: MIT
skill-author: AIPOCH
---

# Literature Close Reading

## When to Use

- When you have a full paper converted from PDF to Markdown and need a structured, in-depth interpretation rather than a brief abstract-style summary.
- When you must extract reproducible experimental details (datasets, settings, controls, metrics, statistics) for replication or reimplementation.
- When you need to map the paper's logical chain (motivation → problem → method → experiments → conclusions) and identify missing links or ambiguities.
- When you want a systematic list of limitations, threats to validity, and follow-up research questions grounded strictly in the text.
- When figures/tables are referenced via Markdown images and you need them incorporated into the interpretation without guessing beyond what is shown.

## Key Features

- Reads the entire Markdown paper text, prioritizing **Methods** and **Results** for technical fidelity.
- Produces a **structured close-reading report** in Markdown (UTF-8), following a predefined template.
- Extracts and organizes:
  - research background and problem statement
  - methodological details and experimental design
  - key results and statistical evidence (as explicitly stated)
  - limitations and threats to validity
  - reproducible points and follow-up questions
- Supports Markdown inputs that include pagination headers like `## Page XX` and image references such as `![page-01](...)`.
- Enforces a strict constraint: **summarize only what is explicitly present in the text/images; do not infer or speculate**.
- Uses external guidance and templates:
  - Requirements/checklist: `references/guide.md`
  - Output template: `assets/deep_reading_template.md`

## Dependencies

- `literature-ingestion` (shared skill) — MANDATORY. Used to fetch and convert PDFs into the canonical 4-artifact set. No direct use of `pdf-extract` or `pdftotext` is permitted.

## Example Usage

```bash
# 1) Download and convert the full-text PDF into the canonical 4-artifact set
# MANDATORY: To comply with AROS LAW 3 (Universal PDF Processing Mandate), you must use the shared skill:
# Make sure the target DOIs/PMIDs are in the 01_Target_DOIs.txt file.
python <PROJECT_ROOT>/01.Shared_Assets/Skills/literature-ingestion/scripts/fetch_and_convert.py --input <PROJECT_ROOT>/00.RawData/Literature/01_Target_DOIs.txt --base-dir <PROJECT_ROOT>

# 2) Run the close-reading process (manual or via your orchestration tool):
# Input: paper.md (full text converted from PDF, may include `## Page XX` and images)
# Guidance: references/guide.md
# Template: assets/deep_reading_template.md

# 3) Save the final report as UTF-8 Markdown under outputs/
mkdir -p outputs
# Example output file name:
# outputs/paper_close_reading.md
```

Minimal expected I/O contract:

- **Input**: a single `.md` file containing the full paper text (PDF-to-Markdown), optionally with:
  - page headers like `## Page 01`
  - image references like `![page-01](...)`
- **Output**: one UTF-8 encoded `.md` file (the close-reading report).
