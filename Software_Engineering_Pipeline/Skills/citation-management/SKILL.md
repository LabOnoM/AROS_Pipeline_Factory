---
name: citation-management
description: Comprehensive citation management for academic research; use when you need to discover papers (Google Scholar/PubMed), extract/verify metadata (DOI/PMID/arXiv/URL), and produce validated, clean BibTeX for manuscripts.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT
skill-author: AIPOCH
original-source: benchflow-ai/skillsbench
---

## Overview

Manage citations systematically throughout the research and writing process. This skill provides tools and strategies for searching academic databases (Google Scholar, PubMed), extracting accurate metadata from multiple sources (CrossRef, PubMed, arXiv), validating citation information, and generating properly formatted BibTeX entries.

Critical for maintaining citation accuracy, avoiding reference errors, and ensuring reproducible research. Integrates seamlessly with the literature-review skill for comprehensive research workflows.

## When to Use

- You need to **find relevant or highly cited papers** on a topic using Google Scholar or PubMed.
- You have identifiers (e.g., **DOI, PMID, arXiv ID, URL**) and must **convert them into correct BibTeX**.
- You want to **verify citation accuracy** (DOI resolution, required fields, consistency with CrossRef/PubMed).
- You need to **clean, deduplicate, sort, and standardize** an existing `.bib` file before submission.
- You are preparing a thesis/manuscript and need a **reproducible workflow** from search → extraction → formatting → validation.

## Key Features

- **Paper discovery**
  - Google Scholar search with year filtering, pagination, and citation-count sorting.
  - PubMed search with MeSH terms, field tags, publication-type filters, and date ranges.
- **Metadata extraction**
  - Resolve DOI/PMID/arXiv/URL to structured metadata via CrossRef, PubMed E-utilities, and arXiv APIs.
  - Batch processing from files containing mixed identifiers.
- **BibTeX generation & cleanup**
  - Generate BibTeX entries with appropriate entry types and required fields.
  - Format, sort (key/year/author), and deduplicate BibTeX libraries.
- **Citation validation**
  - DOI resolution checks and metadata cross-checking.
  - Required-field checks by entry type, syntax validation, duplicate detection, and optional auto-fix.
- **Workflow integration**
  - Produces submission-ready `.bib` files for LaTeX/Overleaf workflows and complements literature review pipelines.

## Dependencies

- Python: 3.10+ (recommended)
- Python packages:
  - `requests>=2.31.0`
  - `bibtexparser`
  - `biopython`
  - `scholarly>=1.7.11` (optional; required only for Google Scholar automation)
  - `selenium` (optional; alternative to scholarly for Google Scholar scraping)

## Example Usage

A complete, end-to-end workflow that searches, extracts metadata, formats, deduplicates, and validates a bibliography:

```bash
# 1) Search PubMed (biomedical focus)
python scripts/search_pubmed.py \
  --query '"CRISPR-Cas Systems"[MeSH] AND "Gene Editing"[MeSH]' \
  --date-start 2020-01-01 \
  --date-end 2024-12-31 \
  --limit 200 \
  --output crispr_pubmed.json

# 2) Search Google Scholar (broad coverage)
python scripts/search_google_scholar.py "CRISPR gene editing therapeutics" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --output crispr_scholar.json

# 3) Extract metadata from search outputs (or mixed identifiers)
cat crispr_pubmed.json crispr_scholar.json > combined_results.json
python scripts/extract_metadata.py \
  --input combined_results.json \
  --output combined.bib

# 4) Add known papers by DOI (append)
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2 >> combined.bib
python scripts/doi_to_bibtex.py 10.1126/science.aam9317 >> combined.bib

# 5) Format + deduplicate + sort (newest first)
python scripts/format_bibtex.py combined.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output formatted.bib

# 6) Validate + auto-fix common issues + emit report
python scripts/validate_citations.py formatted.bib \
  --auto-fix \
  --report validation.json \
  --output final_references.bib

# 7) Inspect validation results
cat validation.json
```

## Implementation Details

### 1) Search (Discovery)

- **Google Scholar** (`scripts/search_google_scholar.py`)
  - Supports query operators such as exact phrases (`"deep learning"`), author filters (`author:LeCun`), title-only (`intitle:"neural networks"`), exclusions (`-survey`), and year ranges.
  - Typical parameters:
    - `--year-start`, `--year-end`: constrain publication years
    - `--limit`: cap results
    - `--sort-by citations`: prioritize highly cited papers (when supported by the script)

- **PubMed** (`scripts/search_pubmed.py`)
  - Uses NCBI E-utilities (e.g., ESearch/EFetch/ESummary) to retrieve PMIDs and metadata.
  - Typical parameters:
    - `--query`: supports MeSH terms, field tags, and Boolean logic
    - `--date-start`, `--date-end`: publication date filtering
    - `--publication-types`: e.g., `Clinical Trial,Review`
    - `--format`: JSON or BibTeX output

  **PubMed Best Practices**:
  - **Using MeSH Terms**:
    MeSH (Medical Subject Headings) provides controlled vocabulary for precise searching.
    1. **Find MeSH terms** at https://meshb.nlm.nih.gov/search
    2. **Use in queries**: `"Diabetes Mellitus, Type 2"[MeSH]`
    3. **Combine with keywords** for comprehensive coverage

  **Field Tags**:
  ```
  [Title]              # Search in title only
  [Title/Abstract]     # Search in title or abstract
  [Author]             # Search by author name
  [Journal]            # Search specific journal
  [Publication Date]   # Date range
  [Publication Type]   # Article type
  [MeSH]              # MeSH term
  ```

  **Building Complex Queries**:
  ```bash
  # Clinical trials on diabetes treatment published recently
  "Diabetes Mellitus, Type 2"[MeSH] AND "Drug Therapy"[MeSH]
  AND "Clinical Trial"[Publication Type] AND 2020:2024[Publication Date]

  # Reviews on CRISPR in specific journal
  "CRISPR-Cas Systems"[MeSH] AND "Nature"[Journal] AND "Review"[Publication Type]

  # Specific author's recent work
  "Smith AB"[Author] AND cancer[Title/Abstract] AND 2022:2024[Publication Date]
  ```

(See: `references/google_scholar_search.md`, `references/pubmed_search.md`)

### 2) Metadata Extraction (Normalization)

- **Identifier inputs**: DOI, PMID, arXiv ID, URL, or mixed lists/files.
- **Primary sources**:
  - CrossRef API for DOI-centric journal metadata
  - PubMed E-utilities for biomedical records (PMID/PMCID, MeSH, abstracts)
  - arXiv API for preprints and versioned records
  - DataCite API for datasets/software DOIs (if implemented/used)
- **Field mapping goals**:
  - Required: `author`, `title`, `year`
  - Articles: `journal`, `volume`, `number`, `pages`, `doi`
  - Conferences: `booktitle`, `pages`
  - Preprints: repository + identifier (e.g., `eprint`, `archivePrefix`)

(See: `references/metadata_extraction.md`)

#### Metadata Enrichment via Web Search (MANDATORY)

**Goal**: Detect and fill in any missing metadata fields using web search. This phase runs AFTER extraction and BEFORE formatting to ensure every BibTeX entry is complete.

**Why This Is Critical**: Metadata extraction from APIs (CrossRef, PubMed, arXiv) sometimes returns incomplete records — missing volume, pages, issue number, or DOI. These gaps must be filled before the bibliography is considered ready.

#### Step 1: Scan for Incomplete Entries

After extracting metadata, scan the BibTeX file for entries missing key fields:

**Fields to check per entry type:**

| Entry Type | Must Have | Should Have |
|------------|-----------|-------------|
| @article | author, title, journal, year | volume, pages, number, doi |
| @inproceedings | author, title, booktitle, year | pages, doi |
| @book | author/editor, title, publisher, year | isbn, doi |
| @misc | author, title, year | doi or url |

Any `@article` entry missing `volume`, `pages`, or `doi` is considered **incomplete** and must be enriched.

#### Step 2: Web Search for Missing Metadata

For each incomplete entry, search for the missing information:

**Option A — Search by title and author** (best for finding DOI):
```bash
python scripts/parallel_web.py search \
  "FIRST_AUTHOR TITLE JOURNAL_NAME volume pages DOI" \
  -o sources/search_YYYYMMDD_HHMMSS_citation_CITATIONKEY.md
```

**Option B — Extract from DOI page** (best when DOI is known but volume/pages missing):
```bash
python scripts/parallel_web.py extract \
  "https://doi.org/10.XXXX/YYYY" \
  --objective "extract complete citation metadata: volume, issue, pages, publication date" \
  -o sources/extract_YYYYMMDD_HHMMSS_doi_CITATIONKEY.md
```

**Option C — Search CrossRef API directly** (programmatic, fast):
```bash
python scripts/parallel_web.py search \
  "crossref DOI metadata FIRST_AUTHOR TITLE" \
  -o sources/search_YYYYMMDD_HHMMSS_crossref_CITATIONKEY.md
```

**Option D — Search Google Scholar** (fallback for hard-to-find papers):
```bash
python scripts/parallel_web.py search \
  "google scholar FIRST_AUTHOR TITLE YEAR complete citation" \
  -o sources/search_YYYYMMDD_HHMMSS_scholar_CITATIONKEY.md
```

#### Step 3: Update BibTeX Entries

After finding the missing metadata:

1. Open `references.bib`
2. Add the missing fields to the incomplete entry
3. Verify the found metadata is consistent with existing fields (same author, title, year)
4. Log each fix:
   ```
   [HH:MM:SS] METADATA ENRICHED: [CitationKey] - added volume={X}, pages={Y--Z}, doi={10.XXX/YYY} ✅
   ```

#### Step 4: Handle Unfindable Metadata

If metadata genuinely cannot be found after web search (very old paper, obscure conference, etc.):

1. Add a `note` field to the BibTeX entry explaining the gap:
   ```bibtex
   note = {Volume and pages not available — published online only}
   ```
2. Log the exception:
   ```
   [HH:MM:SS] METADATA INCOMPLETE: [CitationKey] - pages unavailable (online-only publication) ⚠️
   ```
3. These exceptions should be rare — most modern papers have complete metadata findable via web search.

#### Quick Reference: Common Missing Fields and Where to Find Them

| Missing Field | Best Search Strategy |
|---------------|---------------------|
| DOI | Search "AUTHOR TITLE DOI" via parallel_web.py |
| Volume | Extract from DOI page or search "JOURNAL YEAR TITLE volume" |
| Pages | Extract from DOI page or search publisher website |
| Issue/Number | Extract from DOI page or CrossRef |
| Publisher | Search "JOURNAL publisher" or check journal website |

### 3) BibTeX Formatting (Quality & Consistency)

- Entry types commonly produced: `@article`, `@inproceedings`, `@book`, `@misc`.
- Formatting rules enforced/encouraged:
  - Page ranges use `--` (e.g., `123--145`)
  - Protect capitalization in titles with braces (e.g., `{CRISPR}`)
  - Consistent author formatting (`Last, First and Last, First`)
  - Stable citation keys (project convention; often `FirstAuthorYearKeyword`)

(See: `references/bibtex_formatting.md`)

### 4) Validation (Correctness)

Validation typically checks:

- **DOI validity**: resolves via `doi.org` and matches CrossRef metadata.
- **Required fields**: present per entry type; no empty critical fields.
- **Consistency**: year format, numeric volume/issue, page-range syntax, URL accessibility.
- **Duplicates**: same DOI, near-identical titles, or same author/year/title combinations.
- **BibTeX syntax**: braces/quotes, commas, unique keys, special character handling.

Outputs may include a machine-readable report (e.g., JSON) with `errors` and `warnings`.
(See: `references/citation_validation.md`)

## Search Strategies

### Google Scholar Best Practices

**Finding Seminal and High-Impact Papers** (CRITICAL):

Always prioritize papers based on citation count, venue quality, and author reputation:

**Citation Count Thresholds:**
| Paper Age | Citations | Classification |
|-----------|-----------|----------------|
| 0-3 years | 20+ | Noteworthy |
| 0-3 years | 100+ | Highly Influential |
| 3-7 years | 100+ | Significant |
| 3-7 years | 500+ | Landmark Paper |
| 7+ years | 500+ | Seminal Work |
| 7+ years | 1000+ | Foundational |

**Venue Quality Tiers:**
- **Tier 1 (Prefer):** Nature, Science, Cell, NEJM, Lancet, JAMA, PNAS
- **Tier 2 (High Priority):** Impact Factor >10, top conferences (NeurIPS, ICML, ICLR)
- **Tier 3 (Good):** Specialized journals (IF 5-10)
- **Tier 4 (Sparingly):** Lower-impact peer-reviewed venues

**Author Reputation Indicators:**
- Senior researchers with h-index >40
- Multiple publications in Tier-1 venues
- Leadership at recognized institutions
- Awards and editorial positions

**Search Strategies for High-Impact Papers:**
- Sort by citation count (most cited first)
- Look for review articles from Tier-1 journals for overview
- Check "Cited by" for impact assessment and recent follow-up work
- Use citation alerts for tracking new citations to key papers
- Filter by top venues using `source:Nature` or `source:Science`
- Search for papers by known field leaders using `author:LastName`

**Advanced Operators** (full list in `references/google_scholar_search.md`):
```
"exact phrase"           # Exact phrase matching
author:lastname          # Search by author
intitle:keyword          # Search in title only
source:journal           # Search specific journal
-exclude                 # Exclude terms
OR                       # Alternative terms
2020..2024              # Year range
```

**Example Searches**:
```
# Find recent reviews on a topic
"CRISPR" intitle:review 2023..2024

# Find papers by specific author on topic
author:Church "synthetic biology"

# Find highly cited foundational work
"deep learning" 2012..2015 sort:citations

# Exclude surveys and focus on methods
"protein folding" -survey -review intitle:method
```

## Tools and Scripts

### search_google_scholar.py

Search Google Scholar and export results.

**Features**:
- Automated searching with rate limiting
- Pagination support
- Year range filtering
- Export to JSON or BibTeX
- Citation count information

**Usage**:
```bash
# Basic search
python scripts/search_google_scholar.py "quantum computing"

# Advanced search with filters
python scripts/search_google_scholar.py "quantum computing" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --sort-by citations \
  --output quantum_papers.json

# Export directly to BibTeX
python scripts/search_google_scholar.py "machine learning" \
  --limit 50 \
  --format bibtex \
  --output ml_papers.bib
```

### search_pubmed.py

Search PubMed using E-utilities API.

**Features**:
- Complex query support (MeSH, field tags, Boolean)
- Date range filtering
- Publication type filtering
- Batch retrieval with metadata
- Export to JSON or BibTeX

**Usage**:
```bash
# Simple keyword search
python scripts/search_pubmed.py "CRISPR gene editing"

# Complex query with filters
python scripts/search_pubmed.py \
  --query '"CRISPR-Cas Systems"[MeSH] AND "therapeutic"[Title/Abstract]' \
  --date-start 2020-01-01 \
  --date-end 2024-12-31 \
  --publication-types "Clinical Trial,Review" \
  --limit 200 \
  --output crispr_therapeutic.json

# Export to BibTeX
python scripts/search_pubmed.py "Alzheimer's disease" \
  --limit 100 \
  --format bibtex \
  --output alzheimers.bib
```

### extract_metadata.py

Extract complete metadata from paper identifiers.

**Features**:
- Supports DOI, PMID, arXiv ID, URL
- Queries CrossRef, PubMed, arXiv APIs
- Handles multiple identifier types
- Batch processing
- Multiple output formats

**Usage**:
```bash
# Single DOI
python scripts/extract_metadata.py --doi 10.1038/s41586-021-03819-2

# Single PMID
python scripts/extract_metadata.py --pmid 34265844

# Single arXiv ID
python scripts/extract_metadata.py --arxiv 2103.14030

# From URL
python scripts/extract_metadata.py \
  --url "https://www.nature.com/articles/s41586-021-03819-2"

# Batch processing (file with one identifier per line)
python scripts/extract_metadata.py \
  --input paper_ids.txt \
  --output references.bib

# Different output formats
python scripts/extract_metadata.py \
  --doi 10.1038/nature12345 \
  --format json  # or bibtex, yaml
```

### validate_citations.py

Validate BibTeX entries for accuracy and completeness.

**Features**:
- DOI verification via doi.org and CrossRef
- Required field checking
- Duplicate detection
- Format validation
- Auto-fix common issues
- Detailed reporting

**Usage**:
```bash
# Basic validation
python scripts/validate_citations.py references.bib

# With auto-fix
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --output fixed_references.bib

# Detailed validation report
python scripts/validate_citations.py references.bib \
  --report validation_report.json \
  --verbose

# Only check DOIs
python scripts/validate_citations.py references.bib \
  --check-dois-only
```

### format_bibtex.py

Format and clean BibTeX files.

**Features**:
- Standardize formatting
- Sort entries (by key, year, author)
- Remove duplicates
- Validate syntax
- Fix common errors
- Enforce citation key conventions

**Usage**:
```bash
# Basic formatting
python scripts/format_bibtex.py references.bib

# Sort by year (newest first)
python scripts/format_bibtex.py references.bib \
  --sort year \
  --descending \
  --output sorted_refs.bib

# Remove duplicates
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --output clean_refs.bib

# Complete cleanup
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --sort year \
  --validate \
  --auto-fix \
  --output final_refs.bib
```

### doi_to_bibtex.py

Quick DOI to BibTeX conversion.

**Features**:
- Fast single DOI conversion
- Batch processing
- Multiple output formats
- Clipboard support

**Usage**:
```bash
# Single DOI
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2

# Multiple DOIs
python scripts/doi_to_bibtex.py \
  10.1038/nature12345 \
  10.1126/science.abc1234 \
  10.1016/j.cell.2023.01.001

# From file (one DOI per line)
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# Copy to clipboard
python scripts/doi_to_bibtex.py 10.1038/nature12345 --clipboard
```

## Best Practices

### Search Strategy

1. **Start broad, then narrow**:
   - Begin with general terms to understand the field
   - Refine with specific keywords and filters
   - Use synonyms and related terms

2. **Use multiple sources**:
   - Google Scholar for comprehensive coverage
   - PubMed for biomedical focus
   - arXiv for preprints
   - Combine results for completeness

3. **Leverage citations**:
   - Check "Cited by" for seminal papers
   - Review references from key papers
   - Use citation networks to discover related work

4. **Document your searches**:
   - Save search queries and dates
   - Record number of results
   - Note any filters or restrictions applied

### Metadata Extraction

1. **Always use DOIs when available**:
   - Most reliable identifier
   - Permanent link to the publication
   - Best metadata source via CrossRef

2. **Verify extracted metadata**:
   - Check author names are correct
   - Verify journal/conference names
   - Confirm publication year
   - Validate page numbers and volume

3. **Handle edge cases**:
   - Preprints: Include repository and ID
   - Preprints later published: Use published version
   - Conference papers: Include conference name and location
   - Book chapters: Include book title and editors

4. **Maintain consistency**:
   - Use consistent author name format
   - Standardize journal abbreviations
   - Use same DOI format (URL preferred)

### BibTeX Quality

1. **Follow conventions**:
   - Use meaningful citation keys (FirstAuthor2024keyword)
   - Protect capitalization in titles with {}
   - Use -- for page ranges (not single dash)
   - Include DOI field for all modern publications

2. **Keep it clean**:
   - Remove unnecessary fields
   - No redundant information
   - Consistent formatting
   - Validate syntax regularly

3. **Organize systematically**:
   - Sort by year or topic
   - Group related papers
   - Use separate files for different projects
   - Merge carefully to avoid duplicates

### Validation

1. **Validate early and often**:
   - Check citations when adding them
   - Validate complete bibliography before submission
   - Re-validate after any manual edits

2. **Fix issues promptly**:
   - Broken DOIs: Find correct identifier
   - Missing fields: Extract from original source
   - Duplicates: Choose best version, remove others
   - Format errors: Use auto-fix when safe

3. **Manual review for critical citations**:
   - Verify key papers cited correctly
   - Check author names match publication
   - Confirm page numbers and volume
   - Ensure URLs are current

## Common Pitfalls to Avoid

1. **Single source bias**: Only using Google Scholar or PubMed
   - **Solution**: Search multiple databases for comprehensive coverage

2. **Accepting metadata blindly**: Not verifying extracted information
   - **Solution**: Spot-check extracted metadata against original sources

3. **Ignoring DOI errors**: Broken or incorrect DOIs in bibliography
   - **Solution**: Run validation before final submission

4. **Inconsistent formatting**: Mixed citation key styles, formatting
   - **Solution**: Use format_bibtex.py to standardize

5. **Duplicate entries**: Same paper cited multiple times with different keys
   - **Solution**: Use duplicate detection in validation

6. **Missing required fields**: Incomplete BibTeX entries (volume, pages, DOI missing)
   - **Solution**: Run Phase 2.5 metadata enrichment — web search for every missing field before proceeding. NEVER leave an @article entry without volume, pages, and DOI.

7. **Outdated preprints**: Citing preprint when published version exists
   - **Solution**: Check if preprints have been published, update to journal version

8. **Special character issues**: Broken LaTeX compilation due to characters
   - **Solution**: Use proper escaping or Unicode in BibTeX

9. **No validation before submission**: Submitting with citation errors
   - **Solution**: Always run validation as final check

10. **Manual BibTeX entry**: Typing entries by hand
    - **Solution**: Always extract from metadata sources using scripts

## Example Workflows

### Example 1: Building a Bibliography for a Paper

```bash
# Step 1: Find key papers on your topic
python scripts/search_google_scholar.py "transformer neural networks" \
  --year-start 2017 \
  --limit 50 \
  --output transformers_gs.json

python scripts/search_pubmed.py "deep learning medical imaging" \
  --date-start 2020 \
  --limit 50 \
  --output medical_dl_pm.json

# Step 2: Extract metadata from search results
python scripts/extract_metadata.py \
  --input transformers_gs.json \
  --output transformers.bib

python scripts/extract_metadata.py \
  --input medical_dl_pm.json \
  --output medical.bib

# Step 3: Add specific papers you already know
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2 >> specific.bib
python scripts/doi_to_bibtex.py 10.1126/science.aam9317 >> specific.bib

# Step 4: Combine all BibTeX files
cat transformers.bib medical.bib specific.bib > combined.bib

# Step 5: Format and deduplicate
python scripts/format_bibtex.py combined.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output formatted.bib

# Step 6: Validate
python scripts/validate_citations.py formatted.bib \
  --auto-fix \
  --report validation.json \
  --output final_references.bib

# Step 7: Review any issues
cat validation.json | grep -A 3 '"errors"'

# Step 8: Use in LaTeX
# \bibliography{final_references}
```

### Example 2: Converting a List of DOIs

```bash
# You have a text file with DOIs (one per line)
# dois.txt contains:
# 10.1038/s41586-021-03819-2
# 10.1126/science.aam9317
# 10.1016/j.cell.2023.01.001

# Convert all to BibTeX
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# Validate the result
python scripts/validate_citations.py references.bib --verbose
```

### Example 3: Cleaning an Existing BibTeX File

```bash
# You have a messy BibTeX file from various sources
# Clean it up systematically

# Step 1: Format and standardize
python scripts/format_bibtex.py messy_references.bib \
  --output step1_formatted.bib

# Step 2: Remove duplicates
python scripts/format_bibtex.py step1_formatted.bib \
  --deduplicate \
  --output step2_deduplicated.bib

# Step 3: Validate and auto-fix
python scripts/validate_citations.py step2_deduplicated.bib \
  --auto-fix \
  --output step3_validated.bib

# Step 4: Sort by year
python scripts/format_bibtex.py step3_validated.bib \
  --sort year \
  --descending \
  --output clean_references.bib

# Step 5: Final validation report
python scripts/validate_citations.py clean_references.bib \
  --report final_validation.json \
  --verbose

# Review report
cat final_validation.json
```

### Example 4: Finding and Citing Seminal Papers

```bash
# Find highly cited papers on a topic
python scripts/search_google_scholar.py "AlphaFold protein structure" \
  --year-start 2020 \
  --year-end 2024 \
  --sort-by citations \
  --limit 20 \
  --output alphafold_seminal.json

# Extract the top 10 by citation count
# (script will have included citation counts in JSON)

# Convert to BibTeX
python scripts/extract_metadata.py \
  --input alphafold_seminal.json \
  --output alphafold_refs.bib

# The BibTeX file now contains the most influential papers
```

## Integration with Other Skills

### Literature Review Skill

**Citation Management** provides the technical infrastructure for **Literature Review**:

- **Literature Review**: Multi-database systematic search and synthesis
- **Citation Management**: Metadata extraction and validation

**Combined workflow**:
1. Use literature-review for systematic search methodology
2. Use citation-management to extract and validate citations
3. Use literature-review to synthesize findings
4. Use citation-management to ensure bibliography accuracy

### Scientific Writing Skill

**Citation Management** ensures accurate references for **Scientific Writing**:

- Export validated BibTeX for use in LaTeX manuscripts
- Verify citations match publication standards
- Format references according to journal requirements

### Venue Templates Skill

**Citation Management** works with **Venue Templates** for submission-ready manuscripts:

- Different venues require different citation styles
- Generate properly formatted references
- Validate citations meet venue requirements

## Resources

### Bundled Resources

**References** (in `references/`):
- `google_scholar_search.md`: Complete Google Scholar search guide
- `pubmed_search.md`: PubMed and E-utilities API documentation
- `metadata_extraction.md`: Metadata sources and field requirements
- `citation_validation.md`: Validation criteria and quality checks
- `bibtex_formatting.md`: BibTeX entry types and formatting rules

**Scripts** (in `scripts/`):
- `search_google_scholar.py`: Google Scholar search automation
- `search_pubmed.py`: PubMed E-utilities API client
- `extract_metadata.py`: Universal metadata extractor
- `validate_citations.py`: Citation validation and verification
- `format_bibtex.py`: BibTeX formatter and cleaner
- `doi_to_bibtex.py`: Quick DOI to BibTeX converter

**Assets** (in `assets/`):
- `bibtex_template.bib`: Example BibTeX entries for all types
- `citation_checklist.md`: Quality assurance checklist

### External Resources

**Search Engines**:
- Google Scholar: https://scholar.google.com/
- PubMed: https://pubmed.ncbi.nlm.nih.gov/
- PubMed Advanced Search: https://pubmed.ncbi.nlm.nih.gov/advanced/

**Metadata APIs**:
- CrossRef API: https://api.crossref.org/
- PubMed E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- arXiv API: https://arxiv.org/help/api/
- DataCite API: https://api.datacite.org/

**Tools and Validators**:
- MeSH Browser: https://meshb.nlm.nih.gov/search
- DOI Resolver: https://doi.org/
- BibTeX Format: http://www.bibtex.org/Format/

**Citation Styles**:
- BibTeX documentation: http://www.bibtex.org/
- LaTeX bibliography management: https://www.overleaf.com/learn/latex/Bibliography_management

## Summary

The citation-management skill provides:

1. **Comprehensive search capabilities** for Google Scholar and PubMed
2. **Automated metadata extraction** from DOI, PMID, arXiv ID, URLs
3. **Citation validation** with DOI verification and completeness checking
4. **BibTeX formatting** with standardization and cleaning tools
5. **Quality assurance** through validation and reporting
6. **Integration** with scientific writing workflow
7. **Reproducibility** through documented search and extraction methods

Use this skill to maintain accurate, complete citations throughout your research and ensure publication-ready bibliographies.

## Automated DOI/BibTeX Pipeline (Merged from Benchflow)
- Use programmatic validation scripts for DOI-to-BibTeX conversion to ensure 100% accurate metadata extraction before citing.
