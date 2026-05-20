---
name: biorxiv-database
description: Browse, filter, and download life sciences, biology, and medical preprints
  from bioRxiv and medRxiv. Supports fetching paper metadata by DOI, and browsing
  by date range with category and keyword filters. Keyword filtering is local, so
  date ranges MUST be narrow (1-4 weeks) with a category to prevent timeouts.
license: MIT
metadata:
  skill-author: AIPOCH & K-Dense Inc.
---

## Overview

This skill provides tools for searching and retrieving preprints from the bioRxiv database. It enables searches by keywords, authors, date ranges, and categories. It returns structured JSON metadata that includes titles, abstracts, DOIs, and citation information and supports PDF downloads for full-text analysis.

## When to Use This Skill

Use this skill when:

- Searching for recent preprints in specific research areas.
- Tracking publications by particular authors.
- Conducting systematic literature reviews.
- Analyzing research trends over time periods.
- Retrieving metadata for citation management.
- Downloading preprint PDFs for analysis.
- Filtering papers by bioRxiv subject categories.
- Building a literature monitoring pipeline that periodically searches bioRxiv.
- You need a simple CLI tool to quickly query bioRxiv.

## When Not to Use This Skill

- Do not use this skill when the required source data, identifiers, files, or credentials are missing.
- Do not use this skill when the user asks for fabricated results, unsupported claims, or out-of-scope conclusions.
- Do not use this skill when a simpler, direct answer is more appropriate than the documented workflow.

## Key Features

- Keyword-based search with a configurable lookback window (days).
- Author-based search.
- Date range search.
- Category filtering.
- DOI-based lookup.
- Structured metadata retrieval in JSON format (e.g., Title, Abstract, DOI, Authors).
- PDF download by DOI to a local file path.
- Scriptable Python API via `BioRxivSearcher`.
- Command-line interface for quick searches.

## Dependencies

- Python 3.8+
- `requests>=2.25.0`

## Installation

```bash
pip install requests
```

## Core Search Capabilities

### 1. Keyword Search

Search for preprints containing specific keywords in titles, abstracts, or author lists.

**Python Usage:**
```python
from scripts.biorxiv_search import BioRxivSearcher

searcher = BioRxivSearcher()
papers = searcher.search_by_keywords(keywords=["CRISPR", "gene editing"], days_back=30)
print(f"Found {len(papers)} papers")
```

**CLI Usage:**
```bash
python scripts/biorxiv_search.py --keywords "CRISPR" "gene editing" --days-back 30 --output results.json
```

**Search Fields:**
By default, keywords are searched in both title and abstract. Customize with `--search-fields`:
```python
python scripts/biorxiv_search.py --keywords "AlphaFold" --search-fields title --days-back 365
```

### 2. Author Search

Find all papers by a specific author within a date range.

**Python Usage:**
```python
from scripts.biorxiv_search import BioRxivSearcher

searcher = BioRxivSearcher()
papers = searcher.search_by_author(author_name="Smith", days_back=365)
print(f"Found {len(papers)} papers by Smith")
```

**CLI Usage:**
```bash
python scripts/biorxiv_search.py --author "Smith" --days-back 365 --output smith_papers.json
```

### 3. Date Range Search

Retrieve all preprints posted within a specific date range.

**Python Usage:**
```python
from scripts.biorxiv_search import BioRxivSearcher
from datetime import datetime, timedelta

searcher = BioRxivSearcher()
end_date = datetime.now()
start_date = end_date - timedelta(days=90)
papers = searcher.search_by_date_range(start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))
print(f"Found {len(papers)} papers in the last quarter.")
```

**CLI Usage:**
```bash
python scripts/biorxiv_search.py --start-date 2024-01-01 --end-date 2024-01-31 --output january_2024.json
```

**Days Back Shortcut:**
```bash
python scripts/biorxiv_search.py --days-back 30 --output last_month.json
```

### 4. Paper Details by DOI

Retrieve detailed metadata for a specific preprint.

**Python Usage:**
```python
from scripts.biorxiv_search import BioRxivSearcher

searcher = BioRxivSearcher()
paper = searcher.get_paper_details("10.1101/2024.01.15.123456")
print(paper)
```

**CLI Usage:**
```bash
python scripts/biorxiv_search.py --doi "10.1101/2024.01.15.123456" --output paper_details.json
```

**Full DOI URLs Accepted:**
```bash
python scripts/biorxiv_search.py --doi "https://doi.org/10.1101/2024.01.15.123456"
```

### 5. PDF Downloads

Download the full-text PDF of any preprint.

**Python Usage:**
```python
from scripts.biorxiv_search import BioRxivSearcher

searcher = BioRxivSearcher()
doi = "10.1101/2024.01.15.123456"
output_path = "paper.pdf"
searcher.download_pdf(doi, output_path)
print(f"Downloaded PDF to {output_path}")
```

**CLI Usage:**
```bash
python scripts/biorxiv_search.py --doi "10.1101/2024.01.15.123456" --download-pdf paper.pdf
```

## Valid Categories

Filter searches by bioRxiv subject categories:

- `animal-behavior-and-cognition`
- `biochemistry`
- `bioengineering`
- `bioinformatics`
- `biophysics`
- `cancer-biology`
- `cell-biology`
- `clinical-trials`
- `developmental-biology`
- `ecology`
- `epidemiology`
- `evolutionary-biology`
- `genetics`
- `genomics`
- `immunology`
- `microbiology`
- `molecular-biology`
- `neuroscience`
- `paleontology`
- `pathology`
- `pharmacology-and-toxicology`
- `physiology`
- `plant-biology`
- `scientific-communication-and-education`
- `synthetic-biology`
- `systems-biology`
- `zoology`

**Category Filter Usage:**
```bash
python scripts/biorxiv_search.py --keywords "neural networks" "deep learning" --days-back 180 --category neuroscience --output recent_neuroscience.json
```

## Output Format

All searches return structured JSON with the following format:

```json
{
  "query": {
    "keywords": ["CRISPR"],
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "category": "genomics"
  },
  "result_count": 42,
  "results": [
    {
      "doi": "10.1101/2024.01.15.123456",
      "title": "Paper Title Here",
      "authors": "Smith J, Doe J, Johnson A",
      "author_corresponding": "Smith J",
      "author_corresponding_institution": "University Example",
      "date": "2024-01-15",
      "version": "1",
      "type": "new results",
      "license": "cc_by",
      "category": "genomics",
      "abstract": "Full abstract text...",
      "pdf_url": "https://www.biorxiv.org/content/10.1101/2024.01.15.123456v1.full.pdf",
      "html_url": "https://www.biorxiv.org/content/10.1101/2024.01.15.123456v1",
      "jatsxml": "https://www.biorxiv.org/content/...",
      "published": ""
    }
  ]
}
```

## Common Usage Patterns

### Literature Review Workflow

1. **Broad keyword search:**
```bash
python scripts/biorxiv_search.py --keywords "organoids" "tissue engineering" --start-date 2023-01-01 --end-date 2024-12-31 --category bioengineering --output organoid_papers.json
```

2. **Extract and review results:**
```python
import json

with open('organoid_papers.json') as f:
    data = json.load(f)

print(f"Found {data['result_count']} papers")

for paper in data['results'][:5]:
    print(f"\nTitle: {paper['title']}")
    print(f"Authors: {paper['authors']}")
    print(f"Date: {paper['date']}")
    print(f"DOI: {paper['doi']}")
```

3. **Download selected papers:**
```python
from scripts.biorxiv_search import BioRxivSearcher

searcher = BioRxivSearcher()
selected_dois = ["10.1101/2024.01.15.123456", "10.1101/2024.02.20.789012"]

for doi in selected_dois:
    filename = doi.replace("/", "_").replace(".", "_") + ".pdf"
    searcher.download_pdf(doi, f"papers/{filename}")
```

### Trend Analysis

Track research trends by analyzing publication frequencies over time:

```bash
python scripts/biorxiv_search.py --keywords "machine learning" --start-date 2020-01-01 --end-date 2024-12-31 --category bioinformatics --output ml_trends.json
```

Then analyze the temporal distribution in the results.

### Author Tracking

Monitor specific researchers' preprints:

```bash
authors = ["Smith", "Johnson", "Williams"]

for author in authors:
    python scripts/biorxiv_search.py --author "{author}" --days-back 365 --output "{author}_papers.json"
```

## Advanced Features

### Result Limiting

Limit the number of results returned:

```bash
python scripts/biorxiv_search.py --keywords "COVID-19" --days-back 30 --limit 50 --output covid_top50.json
```

## Required Inputs

- A clearly specified task goal aligned with the documented scope.
- All required files, identifiers, parameters, or environment variables before execution.
- Any domain constraints, formatting requirements, and expected output destination if applicable.

## Recommended Workflow

1. Validate the request against the skill boundary and confirm all required inputs are present.
2. Select the documented execution path and prefer the simplest supported command or procedure.
3. Produce the expected output using the documented file format, schema, or narrative structure.
4. Run a final validation pass for completeness, consistency, and safety before returning the result.

## Output Contract

- Return a structured deliverable that is directly usable without reformatting.
- If a file is produced, prefer a deterministic output name such as `biorxiv_database_result.json` (or .pdf for downloads) unless the skill documentation defines a better convention.
- Include a short validation summary describing what was checked, what assumptions were made, and any remaining limitations.

## Validation and Safety Rules

- Validate required inputs before execution and stop early when mandatory fields or files are missing.
- Do not fabricate measurements, references, findings, or conclusions that are not supported by the provided source material.
- Emit a clear warning when credentials, privacy constraints, safety boundaries, or unsupported requests affect the result.
- Keep the output safe, reproducible, and within the documented scope at all times.

## Failure Handling

- If validation fails, explain the exact missing field, file, or parameter and show the minimum fix required.
- If an external dependency or script fails, surface the command path, likely cause, and the next recovery step.
- If partial output is returned, label it clearly and identify which checks could not be completed.

## Quick Validation

Run this minimal verification path before full execution when possible:

```bash
python scripts/biorxiv_search.py --help
```

Expected output:  Displays the help message for the script, confirming successful execution.

## Testing the Skill

To verify that the bioRxiv database skill is working correctly, run the comprehensive test suite.

**Prerequisites:**
```bash
pip install requests
```

**Run tests:**
```bash
python tests/test_biorxiv_search.py
```

The test suite validates:
- **Initialization**: BioRxivSearcher class instantiation
- **Date Range Search**: Retrieving papers within specific date ranges
- **Category Filtering**: Filtering papers by bioRxiv categories
- **Keyword Search**: Finding papers containing specific keywords
- **DOI Lookup**: Retrieving specific papers by DOI
- **Result Formatting**: Proper formatting of paper metadata
- **Interval Search**: Fetching recent papers by time intervals

## Reference Documentation

For detailed API specifications, endpoint documentation, and response schemas, refer to:
- `references/api_reference.md` - Complete bioRxiv API documentation

The reference file includes:
- Full API endpoint specifications
- Response format details
- Error handling patterns
- Rate limiting guidelines
- Advanced search patterns

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://api.biorxiv.org/ and
    https://www.biorxiv.org/content/about-biorxiv and to always check the
    license of the papers retrieved by the skill for any restrictions, then (2)
    create the file recording the notification text and timestamp.

## Search Strategy Guide (Read First)

**This skill browses a date-based preprint archive. It is NOT a keyword search
engine.** Choose your approach based on what you already know:

-   **A DOI** (e.g., from a citation): Use `search_by_doi.py`. Fast and
    reliable.
-   **Approximate date + category**: Use `search_by_dates.py` with a 1–4 week
    range and `--category`.
-   **Only a topic or keywords, no date**: **Do NOT use this skill for
    discovery.** Use a keyword-capable literature skill first to find relevant
    DOIs, then return here to fetch metadata.

> **CRITICAL ANTI-PATTERN — Do NOT do this:** Do NOT attempt to search broad
> date ranges (months or years) with `--keywords` hoping to find a specific
> paper. The bioRxiv API does not support server-side keyword search. The script
> must download ALL metadata for the entire date range and filter locally in
> Python. Broad ranges will result in thousands of API calls, timeouts, and your
> request being blocked for API abuse. This is the #1 reason this skill fails.

## Core Rules

-   **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
    database rather than accessing the database directly. The scripts
    automatically enforce the required rate limit gracefully.
-   **Local Filtering (CRITICAL WARNING)**: Unlike arXiv, the bioRxiv API **does
    not support server-side keyword or author searches**. Keyword and author
    filtering is performed *locally* by the scripts after downloading all
    metadata for a specified date range. You **MUST** use narrow date ranges
    (e.g., 1-4 weeks) AND the `--category` filter when searching with
    `--keywords` or `--author`.
-   **Abstracts Excluded By Default**: To save context space in the resulting
    JSON, abstracts are stripped from the output by default. If you are
    searching by `--keywords` and want to read the abstracts of the resulting
    papers to understand their context, you **MUST** pass the
    `--include_abstracts` flag.
-   **Output Redirection**: Search commands output JSON arrays to standard
    output. Always redirect output to a file (e.g., `> results.json`) and parse
    the file separately.
-   **List Sources** If this skill is used, ensure this is mentioned in the
    output AND list the URLs of all papers that were used in producing the
    output.

## Utility Scripts

All tools enforce a cross-process rate limits and retry with backoff on failure.
To ensure you respect terms-of-service, do NOT write custom `curl` queries.

**Pagination:** The bioRxiv API returns results in pages of up to 100 papers.
The `search_by_dates.py` script automatically fetches all pages and reports
pagination progress to stderr (e.g., `[Page 2] Fetched 200/543 papers...`). The
JSON output to stdout contains the **complete** filtered result set across all
pages — no manual pagination is needed.

### 1. Search by Dates (`search_by_dates.py`)

Search for preprints within an explicit date range, optionally filtering by
category, keywords, or author.

```bash
# Broad category search over a 2-week period
uv run scripts/search_by_dates.py --server biorxiv \
  --start_date 2024-01-01 --end_date 2024-01-14 \
  --category neuroscience > results.json

# Deep keyword filtering using OR logic and including abstracts
uv run scripts/search_by_dates.py --server medrxiv \
  --start_date 2023-11-01 --end_date 2023-11-30 \
  --category infectious_diseases \
  --keywords "covid" "sars-cov-2" --match_logic OR \
  --include_abstracts > covid_papers.json

# Finding papers by a specific author in a narrow window
uv run scripts/search_by_dates.py \
  --start_date 2024-05-01 --end_date 2024-05-14 \
  --author "Smith" > smith_papers.json
```

*Required Arguments:*

-   `--start_date`: YYYY-MM-DD
-   `--end_date`: YYYY-MM-DD

*Optional Arguments:*

-   `--server`: `biorxiv` (default) or `medrxiv`
-   `--category`: A valid subject category (see below). **Highly recommended** —
    dramatically reduces the data the script must download and filter.
-   `--keywords`: List of strings to search in the title/abstract.
-   `--match_logic`: `AND` (default) or `OR` for keywords.
-   `--author`: Author name (case-insensitive string match).
-   `--include_abstracts`: Flag to include full abstracts in the JSON output.

### 2. Fetch Metadata by DOI (`search_by_doi.py`)

Retrieve the detailed JSON metadata for a single paper if you already know its
DOI. **This is the most reliable entry point.**

```bash
uv run scripts/search_by_doi.py --server biorxiv \
  --doi "10.1101/2023.08.15.551388" \
  --include_abstracts > paper_info.json
```

### Downloading Full-Text PDFs

> **This skill does NOT support PDF downloads.** To download the full-text PDF
> of a bioRxiv or medRxiv preprint, use the **`literature-search-europepmc`**
> skill. First, use the paper's DOI to look up its PMCID via EuropePMC, then use
> EuropePMC's PDF retrieval to download the document.

## Valid Subject Categories

You can pass these to the `--category` flag in `search_by_dates.py`. The script
will strictly validate them.

### bioRxiv Categories:

`animal_behavior_and_cognition`, `biochemistry`, `bioengineering`,
`bioinformatics`, `biophysics`, `cancer_biology`, `cell_biology`,
`clinical_trials`, `developmental_biology`, `ecology`, `epidemiology`,
`evolutionary_biology`, `genetics`, `genomics`, `immunology`, `microbiology`,
`molecular_biology`, `neuroscience`, `paleontology`, `pathology`,
`pharmacology_and_toxicology`, `physiology`, `plant_biology`,
`scientific_communication_and_education`, `synthetic_biology`,
`systems_biology`, `zoology`

### medRxiv Categories:

`addiction_medicine`, `allergy_and_immunology`, `anesthesia`,
`cardiovascular_medicine`, `dentistry_and_oral_medicine`, `dermatology`,
`emergency_medicine`, `endocrinology`, `epidemiology`, `forensic_medicine`,
`gastroenterology`, `genetic_and_genomic_medicine`, `health_informatics`,
`health_economics_and_outcomes_research`, `health_policy`,
`health_systems_and_quality_improvement`, `hematology`, `hiv_aids`,
`infectious_diseases`, `intensive_care_and_critical_care_medicine`,
`medical_education`, `medical_ethics`, `nephrology`, `neurology`, `nursing`,
`nutrition`, `obstetrics_and_gynecology`,
`occupational_and_environmental_health`, `oncology`, `ophthalmology`,
`orthopedics`, `otolaryngology`, `pain_medicine`, `palliative_care`,
`pathology`, `pediatrics`, `pharmacology_and_therapeutics`,
`primary_care_research`, `psychiatry_and_clinical_psychology`,
`public_and_global_health`, `radiology_and_imaging`,
`rehabilitation_medicine_and_physical_therapy`, `respiratory_medicine`,
`rheumatology`, `sexual_and_reproductive_health`, `sports_medicine`, `surgery`,
`toxicology`, `transplantation`, `urology`
