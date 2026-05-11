---
name: md-html-docx-generator
description: A section-by-section generator for converting large Markdown manuscripts into high-fidelity, single-file HTML reports and optional DOCX exports, bypassing LLM output token limits.
---

# /md-html-docx-generator

## Overview
This skill solves the recurring issue of LLM output truncation when generating large reports. Instead of prompting the LLM to generate an entire HTML document at once, this skill uses a Python orchestrator to chunk the input Markdown by section (`##`), iteratively converts each section to styled HTML using Gemini, and then bundles them into a standalone, offline-ready HTML file. It can optionally export a `.docx` version using Pandoc.

The skill employs the **Huashu Design** philosophy for scientific reports, ensuring high-fidelity typography, styling, and data presentation without hallucinating boilerplate styles every time.

## Requirements
- `google-generativeai` (for LLM API calls)
- `python-dotenv` (for API key resolution)
- `pandoc` (only if using the `--docx` flag)

## Execution Syntax // turbo
Trigger the skill via CLI using the Python orchestrator:

```bash
python3 ~/.gemini/skills/md-html-docx-generator/scripts/build_report.py \
    /path/to/input.md \
    -o /path/to/output_report.html \
    [--docx] \
    [--api-key YOUR_API_KEY] \
    [--model gemini-2.5-flash]
```

## API Key Resolution
The script uses a portable 4-tier API key resolution chain. It checks in this order:
1. The `--api-key` CLI argument.
2. The `GOOGLE_AI_API_KEY` or `GEMINI_API_KEY` environment variables.
3. A `.env` file in the current directory or script directory.
4. The global AROS `.env` file at `~/.gemini/.env`.

## Anti-AI-Slop Checklist (For Agents using this output)
When integrating the output of this skill into a workflow, ensure the following constraints are met:
- **No Style Hallucinations**: Do not prompt the LLM to invent its own CSS inline styles; the orchestrator handles styles using the predefined `scientific_report.css`.
- **Markdown Purity**: Ensure the source `.md` file is well-formed with standard markdown tables, image references, and `##` level section breaks.
- **Image Referencing**: All images referenced in the markdown should be accessible via relative or absolute paths. The orchestrator will automatically base64 encode them for HTML.
