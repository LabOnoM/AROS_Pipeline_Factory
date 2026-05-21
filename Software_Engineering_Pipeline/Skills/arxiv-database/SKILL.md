---
name: arxiv-database
description: Search for scientific papers, preprints, and publications on arXiv. Extract
  metadata, abstracts, and download full-text PDFs or HTML versions of papers. Use
  when the user asks to find research papers, literature, or specific arXiv IDs.
license: MIT
skill-author: AIPOCH
---
# ArXiv Database Skill

## When to Use

- Use this skill when you need search and retrieve scientific preprints from arxiv; use it when you need to find papers by keyword/author/category, fetch metadata (abstract, doi, pdf url), or download pdfs for offline reading in a reproducible workflow.
- Use this skill when a evidence insight task needs a packaged method instead of ad-hoc freeform output.
- Use this skill when the user expects a concrete deliverable, validation step, or file-based result.
- Use this skill when `scripts/arxiv_search.py` is the most direct path to complete the request.
- Use this skill when you need the `arxiv-database` package behavior rather than a generic answer.

## Key Features

- Scope-focused workflow aligned to: Search and retrieve scientific preprints from arXiv; use it when you need to find papers by keyword/author/category, fetch metadata (abstract, DOI, PDF URL), or download PDFs for offline reading.
- Packaged executable path(s): `scripts/arxiv_search.py`.
- Reference material available in `references/` for task-specific guidance.
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

- `Python`: `3.10+`. Repository baseline for current packaged skills.
- `Third-party packages`: `not explicitly version-pinned in this skill package`. Add pinned versions if this skill needs stricter environment control.

## Example Usage

```bash
cd "20260316/scientific-skills/Evidence Insight/arxiv-database"
python -m py_compile scripts/arxiv_search.py
python scripts/arxiv_search.py --help
```

Example run plan:
1. Confirm the user input, output path, and any required config values.
2. Edit the in-file `CONFIG` block or documented parameters if the script uses fixed settings.
3. Run `python scripts/arxiv_search.py` with the validated inputs.
4. Review the generated output and return the final artifact with any assumptions called out.

## Implementation Details

- Execution model: validate the request, choose the packaged workflow, and produce a bounded deliverable.
- Input controls: confirm the source files, scope limits, output format, and acceptance criteria before running any script.
- Primary implementation surface: `scripts/arxiv_search.py`.
- Reference guidance: `references/` contains supporting rules, prompts, or checklists.
- Parameters to clarify first: input path, output path, scope filters, thresholds, and any domain-specific constraints.
- Output discipline: keep results reproducible, identify assumptions explicitly, and avoid undocumented side effects.