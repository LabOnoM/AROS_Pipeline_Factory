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

## 1. When to Use

- You need to quickly find arXiv preprints by keyword, phrase, author, or category (e.g., `cs.AI`, `cs.CL`).
- You want to collect paper metadata (title, authors, publication date, abstract/summary, PDF link) for review or indexing.
- You need the latest submissions in a topic area (sorted by submission date or last updated date).
- You want to download one or more PDFs from search results for offline reading or batch processing.
- You have a known arXiv identifier and want to retrieve the corresponding paper directly.

## 2. Key Features

- arXiv query-based search (supports category filters, author filters, phrases, and ID lookups).
- Configurable result limits (`--max-results`).
- Sort control (`--sort-by`: `Relevance`, `LastUpdatedDate`, `SubmittedDate`).
- Metadata output per result (title, authors, published date, abstract/summary, PDF URL; DOI when available via arXiv metadata).
- Optional PDF download for returned results (`--download`) with configurable output directory (`--dir`).

## 3. Dependencies

- Python 3.8+
- `arxiv` (Python package) — version depends on your environment; install a recent release (e.g., `arxiv>=1.4.0`)

## 4. Example Usage

### Install dependencies

```bash
pip install "arxiv>=1.4.0"
```

### Run searches and downloads

**Search for papers in `cs.AI` about reinforcement learning (top 5 results):**
```bash
python scripts/arxiv_search.py --query "cat:cs.AI AND reinforcement learning" --max-results 5
```

**Search for “Large Language Models” in `cs.CL`:**
```bash
python scripts/arxiv_search.py --query "cat:cs.CL AND \"Large Language Models\""
```

**Get the latest 5 papers on “quantum computing” (sorted by submission date):**
```bash
python scripts/arxiv_search.py --query "quantum computing" --sort-by SubmittedDate --max-results 5
```

**Download a specific paper by arXiv ID:**
```bash
python scripts/arxiv_search.py --query "id:2101.12345" --download
```

**Download results into a specific directory:**
```bash
python scripts/arxiv_search.py --query "cat:cs.LG AND diffusion" --max-results 3 --download --dir ./papers
```

## 5. Implementation Details

- **Entry point:** `scripts/arxiv_search.py` wraps the `arxiv` Python API to execute queries against the arXiv search endpoint.
- **Query syntax:** The `--query` string is passed to arXiv search and can include:
  - Category filters (e.g., `cat:cs.AI`)
  - Author filters (e.g., `au:Smith`)
  - Exact phrases using quotes (e.g., `"Large Language Models"`)
  - ID lookup (e.g., `id:2101.12345`)
  - Boolean operators such as `AND`
- **Result limiting:** `--max-results` controls how many entries are returned (default: `10`).
- **Sorting:** `--sort-by` selects the ordering of results:
  - `Relevance` (default)
  - `LastUpdatedDate`
  - `SubmittedDate`
- **Downloads:** When `--download` is set, the script downloads the PDF for each returned result using the provided PDF URL and saves it to `--dir` (default: current working directory).
- **Metadata fields:** Each result includes core arXiv metadata (title, authors, published date, summary/abstract, PDF URL). DOI is included when present in arXiv’s metadata for that record.

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://info.arxiv.org/help/api/index.html and to always check the
    license of the papers retrieved by the skill for any restrictions, then (2)
    create the file recording the notification text and timestamp.

## Core Rules

-   **Terms of Use**: You MUST respect arXiv's Terms of Use.
    -   Maximum 1 request every 3 seconds.
    -   The provided utility scripts handle rate limiting automatically. Always
        use these scripts rather than writing your own curl/python requests.
-   If this skill is used, ensure this is mentioned in the output AND list the
    URLs of all papers that were used in producing the output.

## Utility Scripts

**1. Search and Extract Metadata**

Search arXiv and return a clean JSON array of matching papers.

```bash
uv run scripts/search_arxiv.py --query "au:einstein AND ti:relativity" \
  --max_results 5 2>/dev/null > /tmp/arxiv_search_results.json
```

> **Important**: The tool outputs a large JSON result to stdout. Requesting 100+
> results will produce a massive JSON that might exceed your context length.
> Limit `--max_results` (e.g., 5-10) or paginate carefully using `--start`.
> Always redirect output to a file and parse it separately, otherwise terminal
> output will be truncated.

*Returned Metadata:* JSON results include `id`, `title`, `summary`, `published`,
`authors`, `pdf_url`, `primary_category`, `doi`, `journal_ref`, and `comment`.
Note: the `doi` field only contains DOI information in case the paper has an
external DOI and if only an arXiv-issued DOI exists, this is DOI is not
returned.

*Options:*

-   `--query`: Search string. See
    [references/query_syntax.md](references/query_syntax.md) for advanced
    syntax.
-   `--id_list`: Comma-separated list of arXiv IDs to fetch directly (e.g.,
    `1706.03762v5`).
-   `--start`: Pagination offset (default 0).
-   `--max_results`: Number of results to return (default 10).
-   `--sort_by`: `relevance`, `lastUpdatedDate`, or `submittedDate`. (Use
    `--sort_by submittedDate --sort_order descending` for the most recent
    papers).
-   `--sort_order`: `ascending` or `descending`.

**2. Download Paper (PDF or HTML)**

Download the full text of a paper to your local workspace for reading.

```bash
uv run scripts/download_paper.py --id 1706.03762 --format pdf --output attention.pdf
```

*Options:*

-   `--id`: The arXiv ID (e.g., `1706.03762` or `1706.03762v5`).
-   `--format`: `pdf` or `html`. Note: HTML is only available for newer papers.
-   `--output`: Filepath to save the downloaded document.

> **Important**: when downloading papers, make sure you download them to a
> location where you do not overwrite other files and do not clutter existing
> directory structure.

**3. Download Paper Source (tar.gz)**

Download the LaTeX source files of a paper to your local workspace. Note that
not all papers have source available.

```bash
uv run scripts/download_paper_source.py --id 2010.11645 --output source.tar.gz
```

*Options:*

-   `--id`: The arXiv ID (e.g., `2010.11645`).
-   `--output`: Filepath to save the downloaded tar.gz file.

> **Caution**: Care should be exercised when untar'ing the downloaded file for
> security and to avoid cluttering your filesystem, as archives may contain many
> files or unexpected directory structures.
>
> **Safe Extraction Requirements**: NEVER extract directly into your working
> directory! Always extract into a dedicated new directory: `bash mkdir
> paper_source && tar -xzf source.tar.gz -C paper_source`

## Reference

-   **Advanced Query Syntax**: See
    [references/query_syntax.md](references/query_syntax.md) for prefixes (au,
    ti, abs), booleans, and date filtering.

## Workflow

1.  Search for papers using `search_arxiv.py`. Review the JSON summaries.
2.  If full text is needed, use `download_paper.py` to fetch the PDF or HTML.
3.  If downloading a PDF, verify the PDF is not empty or corrupted.
4.  Read the downloaded file using standard file reading tools.
