---
name: pubmed-database
description: Search PubMed for scientific literature, including published clinical
  trials. Fetch abstracts and full text. Link published research to biological databases
  (gene, protein, nucleotide, PubChem) to discover associations between papers and
  specific compounds or genes. Verify medical spelling, match raw citations, and cache
  result sets for bulk processing. Interfaces NCBI E-utilities and PMC BioC APIs.
license: Unknown
metadata:
  skill-author: K-Dense Inc.
---

# PubMed Database

## Overview

PubMed is the U.S. National Library of Medicine's comprehensive database providing free access to MEDLINE and life sciences literature. Construct advanced queries with Boolean operators, MeSH terms, and field tags, access data programmatically via E-utilities API for systematic reviews and literature analysis.

## When to Use This Skill

This skill should be used when:
- Searching for biomedical or life sciences research articles
- Constructing complex search queries with Boolean operators, field tags, or MeSH terms
- Conducting systematic literature reviews or meta-analyses
- Accessing PubMed data programmatically via the E-utilities API
- Finding articles by specific criteria (author, journal, publication date, article type)
- Retrieving citation information, abstracts, or full-text articles
- Working with PMIDs (PubMed IDs) or DOIs
- Creating automated workflows for literature monitoring or data extraction

## Core Capabilities

### 1. Advanced Search Query Construction

Construct sophisticated PubMed queries using Boolean operators, field tags, and specialized syntax.

**Basic Search Strategies**:
- Combine concepts with Boolean operators (AND, OR, NOT)
- Use field tags to limit searches to specific record parts
- Employ phrase searching with double quotes for exact matches
- Apply wildcards for term variations
- Use proximity searching for terms within specified distances

**Example Queries**:
```
# Recent systematic reviews on diabetes treatment
diabetes mellitus[mh] AND treatment[tiab] AND systematic review[pt] AND 2023:2024[dp]

# Clinical trials comparing two drugs
(metformin[nm] OR insulin[nm]) AND diabetes mellitus, type 2[mh] AND randomized controlled trial[pt]

# Author-specific research
smith ja[au] AND cancer[tiab] AND 2023[dp] AND english[la]
```

**When to consult search_syntax.md**:
- Need comprehensive list of available field tags
- Require detailed explanation of search operators
- Constructing complex proximity searches
- Understanding automatic term mapping behavior
- Need specific syntax for date ranges, wildcards, or special characters

Grep pattern for field tags: `\[au\]|\[ti\]|\[ab\]|\[mh\]|\[pt\]|\[dp\]`

### 2. MeSH Terms and Controlled Vocabulary

Use Medical Subject Headings (MeSH) for precise, consistent searching across the biomedical literature.

**MeSH Searching**:
- [mh] tag searches MeSH terms with automatic inclusion of narrower terms
- [majr] tag limits to articles where the topic is the main focus
- Combine MeSH terms with subheadings for specificity (e.g., diabetes mellitus/therapy[mh])

**Common MeSH Subheadings**:
- /diagnosis - Diagnostic methods
- /drug therapy - Pharmaceutical treatment
- /epidemiology - Disease patterns and prevalence
- /etiology - Disease causes
- /prevention & control - Preventive measures
- /therapy - Treatment approaches

**Example**:
```
# Diabetes therapy with specific focus
diabetes mellitus, type 2[mh]/drug therapy AND cardiovascular diseases[mh]/prevention & control
```

### 3. Article Type and Publication Filtering

Filter results by publication type, date, text availability, and other attributes.

**Publication Types** (use [pt] field tag):
- Clinical Trial
- Meta-Analysis
- Randomized Controlled Trial
- Review
- Systematic Review
- Case Reports
- Guideline

**Date Filtering**:
- Single year: `2024[dp]`
- Date range: `2020:2024[dp]`
- Specific date: `2024/03/15[dp]`

**Text Availability**:
- Free full text: Add `AND free full text[sb]` to query
- Has abstract: Add `AND hasabstract[text]` to query

**Example**:
```
# Recent free full-text RCTs on hypertension
hypertension[mh] AND randomized controlled trial[pt] AND 2023:2024[dp] AND free full text[sb]
```

### 4. Programmatic Access via E-utilities API

Access PubMed data programmatically using the NCBI E-utilities REST API for automation and bulk operations.

**Core API Endpoints**:
1. **ESearch** - Search database and retrieve PMIDs
2. **EFetch** - Download full records in various formats
3. **ESummary** - Get document summaries
4. **EPost** - Upload UIDs for batch processing
5. **ELink** - Find related articles and linked data

**Basic Workflow**:
```python
import requests

# Step 1: Search for articles
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
search_url = f"{base_url}esearch.fcgi"
params = {
    "db": "pubmed",
    "term": "diabetes[tiab] AND 2024[dp]",
    "retmax": 100,
    "retmode": "json",
    "api_key": "YOUR_API_KEY"  # Optional but recommended
}
response = requests.get(search_url, params=params)
pmids = response.json()["esearchresult"]["idlist"]

# Step 2: Fetch article details
fetch_url = f"{base_url}efetch.fcgi"
params = {
    "db": "pubmed",
    "id": ",".join(pmids),
    "rettype": "abstract",
    "retmode": "text",
    "api_key": "YOUR_API_KEY"
}
response = requests.get(fetch_url, params=params)
abstracts = response.text
```

**Rate Limits**:
- Without API key: 3 requests/second
- With API key: 10 requests/second
- Always include User-Agent header

**Best Practices**:
- Use history server (usehistory=y) for large result sets
- Implement batch operations via EPost for multiple UIDs
- Cache results locally to minimize redundant calls
- Respect rate limits to avoid service disruption

**When to consult api_reference.md**:
- Need detailed endpoint documentation
- Require parameter specifications for each E-utility
- Constructing batch operations or history server workflows
- Understanding response formats (XML, JSON, text)
- Troubleshooting API errors or rate limit issues

Grep pattern for API endpoints: `esearch|efetch|esummary|epost|elink|einfo`

### 5. Citation Matching and Article Retrieval

Find articles using partial citation information or specific identifiers.

**By Identifier**:
```
# By PMID
12345678[pmid]

# By DOI
10.1056/NEJMoa123456[doi]

# By PMC ID
PMC123456[pmc]
```

**Citation Matching** (via ECitMatch API):
Use journal name, year, volume, page, and author to find PMIDs:
```
Format: journal|year|volume|page|author|key|
Example: Science|2008|320|5880|1185|key1|
```

**By Author and Metadata**:
```
# First author with year and topic
smith ja[1au] AND 2023[dp] AND cancer[tiab]

# Journal, volume, and page
nature[ta] AND 2024[dp] AND 456[vi] AND 123-130[pg]
```

### 6. Systematic Literature Reviews

Conduct comprehensive literature searches for systematic reviews and meta-analyses.

**PICO Framework** (Population, Intervention, Comparison, Outcome):
Structure clinical research questions systematically:
```
# Example: Diabetes treatment effectiveness
# P: diabetes mellitus, type 2[mh]
# I: metformin[nm]
# C: lifestyle modification[tiab]
# O: glycemic control[tiab]

diabetes mellitus, type 2[mh] AND
(metformin[nm] OR lifestyle modification[tiab]) AND
glycemic control[tiab] AND
randomized controlled trial[pt]
```

**Comprehensive Search Strategy**:
```
# Include multiple synonyms and MeSH terms
(disease name[tiab] OR disease name[mh] OR synonym[tiab]) AND
(treatment[tiab] OR therapy[tiab] OR intervention[tiab]) AND
(systematic review[pt] OR meta-analysis[pt] OR randomized controlled trial[pt]) AND
2020:2024[dp] AND
english[la]
```

**Search Refinement**:
1. Start broad, review results
2. Add specificity with field tags
3. Apply date and publication type filters
4. Use Advanced Search to view query translation
5. Combine search history for complex queries

**When to consult common_queries.md**:
- Need example queries for specific disease types or research areas
- Require templates for different study designs
- Looking for population-specific query patterns (pediatric, geriatric, etc.)
- Constructing methodology-specific searches
- Need quality filters or best practice patterns

Grep pattern for query examples: `diabetes|cancer|cardiovascular|clinical trial|systematic review`

### 7. Search History and Saved Searches

Use PubMed's search history and My NCBI features for efficient research workflows.

**Search History** (via Advanced Search):
- Maintains up to 100 searches
- Expires after 8 hours of inactivity
- Combine previous searches using # references
- Preview result counts before executing

**Example**:
```
#1: diabetes mellitus[mh]
#2: cardiovascular diseases[mh]
#3: #1 AND #2 AND risk factors[tiab]
```

**My NCBI Features**:
- Save searches indefinitely
- Set up email alerts for new matching articles
- Create collections of saved articles
- Organize research by project or topic

**RSS Feeds**:
Create RSS feeds for any search to monitor new publications in your area of interest.

### 8. Related Articles and Citation Discovery

Find related research and explore citation networks.

**Similar Articles Feature**:
Every PubMed article includes pre-calculated related articles based on:
- Title and abstract similarity
- MeSH term overlap
- Weighted algorithmic matching

**ELink for Related Data**:
```
# Find related articles programmatically
elink.fcgi?dbfrom=pubmed&db=pubmed&id=PMID&cmd=neighbor
```

**Citation Links**:
- LinkOut to full text from publishers
- Links to PubMed Central free articles
- Connections to related NCBI databases (GenBank, ClinicalTrials.gov, etc.)

### 9. Export and Citation Management

Export search results in various formats for citation management and further analysis.

**Export Formats**:
- .nbib files for reference managers (Zotero, Mendeley, EndNote)
- AMA, MLA, APA, NLM citation styles
- CSV for data analysis
- XML for programmatic processing

**Clipboard and Collections**:
- Clipboard: Temporary storage for up to 500 items (8-hour expiration)
- Collections: Permanent storage via My NCBI account

**Batch Export via API**:
```python
# Export citations in MEDLINE format
efetch.fcgi?db=pubmed&id=PMID1,PMID2&rettype=medline&retmode=text
```

## Working with Reference Files

This skill includes three comprehensive reference files in the `references/` directory:

### references/api_reference.md
Complete E-utilities API documentation including all nine endpoints, parameters, response formats, and best practices. Consult when:
- Implementing programmatic PubMed access
- Constructing API requests
- Understanding rate limits and authentication
- Working with large datasets via history server
- Troubleshooting API errors

### references/search_syntax.md
Detailed guide to PubMed search syntax including field tags, Boolean operators, wildcards, and special characters. Consult when:
- Constructing complex search queries
- Understanding automatic term mapping
- Using advanced search features (proximity, wildcards)
- Applying filters and limits
- Troubleshooting unexpected search results

### references/common_queries.md
Extensive collection of example queries for various research scenarios, disease types, and methodologies. Consult when:
- Starting a new literature search
- Need templates for specific research areas
- Looking for best practice query patterns
- Conducting systematic reviews
- Searching for specific study designs or populations

**Reference Loading Strategy**:
Load reference files into context as needed based on the specific task. For brief queries or basic searches, the information in this SKILL.md may be sufficient. For complex operations, consult the appropriate reference file.

## Common Workflows

### Workflow 1: Basic Literature Search

1. Identify key concepts and synonyms
2. Construct query with Boolean operators and field tags
3. Review initial results and refine query
4. Apply filters (date, article type, language)
5. Export results for analysis

### Workflow 2: Systematic Review Search

1. Define research question using PICO framework
2. Identify all relevant MeSH terms and synonyms
3. Construct comprehensive search strategy
4. Search multiple databases (include PubMed)
5. Document search strategy and date
6. Export results for screening and review

### Workflow 3: Programmatic Data Extraction

1. Design search query and test in web interface
2. Implement search using ESearch API
3. Use history server for large result sets
4. Retrieve detailed records with EFetch
5. Parse XML/JSON responses
6. Store data locally with caching
7. Implement rate limiting and error handling

### Workflow 4: Citation Discovery

1. Start with known relevant article
2. Use Similar Articles to find related work
3. Check citing articles (when available)
4. Explore MeSH terms from relevant articles
5. Construct new searches based on discoveries
6. Use ELink to find related database entries

### Workflow 5: Ongoing Literature Monitoring

1. Construct comprehensive search query
2. Test and refine query for precision
3. Save search to My NCBI account
4. Set up email alerts for new matches
5. Create RSS feed for feed reader monitoring
6. Review new articles regularly

## Tips and Best Practices

### Search Strategy
- Start broad, then narrow with field tags and filters
- Include synonyms and MeSH terms for comprehensive coverage
- Use quotation marks for exact phrases
- Check Search Details in Advanced Search to verify query translation
- Combine multiple searches using search history

### API Usage
- Obtain API key for higher rate limits (10 req/sec vs 3 req/sec)
- Use history server for result sets > 500 articles
- Implement exponential backoff for rate limit handling
- Cache results locally to minimize redundant requests
- Always include descriptive User-Agent header

### Quality Filtering
- Prefer systematic reviews and meta-analyses for synthesized evidence
- Use publication type filters to find specific study designs
- Filter by date for most recent research
- Apply language filters as appropriate
- Use free full text filter for immediate access

### Citation Management
- Export early and often to avoid losing search results
- Use .nbib format for compatibility with most reference managers
- Create My NCBI account for permanent collections
- Document search strategies for reproducibility
- Use Collections to organize research by project

## Limitations and Considerations

### Database Coverage
- Primarily biomedical and life sciences literature
- Pre-1975 articles often lack abstracts
- Full author names available from 2002 forward
- Non-English abstracts available but may default to English display

### Search Limitations
- Display limited to 10,000 results maximum
- Search history expires after 8 hours of inactivity
- Clipboard holds max 500 items with 8-hour expiration
- Automatic term mapping may produce unexpected results

### API Considerations
- Rate limits apply (3-10 requests/second)
- Large queries may time out (use history server)
- XML parsing required for detailed data extraction
- API key recommended for production use

### Access Limitations
- PubMed provides citations and abstracts (not always full text)
- Full text access depends on publisher, institutional access, or open access status
- LinkOut availability varies by journal and institution
- Some content requires subscription or payment

## Support Resources

- **PubMed Help**: https://pubmed.ncbi.nlm.nih.gov/help/
- **E-utilities Documentation**: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **NLM Help Desk**: 1-888-FIND-NLM (1-888-346-3656)
- **Technical Support**: vog.hin.mln.ibcn@seitilitue
- **Mailing List**: utilities-announce@ncbi.nlm.nih.gov

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://pubmed.ncbi.nlm.nih.gov/disclaimer/ and
    https://www.ncbi.nlm.nih.gov/home/about/policies/ and to always check the
    license of the papers retrieved by the skill for any restrictions, then (2)
    create the file recording the notification text and timestamp.
3.  **`.env` file**: Make sure the `.env` file exists in your home directory.
    Create one if it does not exist.
4.  **`NCBI_API_KEY`** (optional): Raises the NCBI E-utilities rate limit from 3
    to 10 requests/second. The skill works without it, but a key is recommended
    if the user plans many queries or encounters a 429 error. The user can
    obtain one for free by registering at
    https://www.ncbi.nlm.nih.gov/account/settings/
5.  **`USER_EMAIL`** (optional but recommended): Identifies the caller to NCBI
    (recommended by their Terms of Use).

If the variables are missing from `.env`, do NOT ask the user to paste them into
the chat (this would leak keys into the agent's context). Instead, give the user
these commands — **substituting `ENV_FILE` with the resolved literal path to the
`.env` file**:

```bash
printf "Enter NCBI API key (typing hidden): " && read -s key && echo && echo "NCBI_API_KEY=$key" >> "ENV_FILE" && echo "Saved."
```

```bash
printf "Enter contact email: " && read email && echo "USER_EMAIL=$email" >> "ENV_FILE" && echo "Saved."
```

The scripts load credentials automatically via `dotenv`. **NEVER** read,
print, or inspect the `.env` file or its variables (e.g. no `cat`, `grep`,
`echo`, `printenv`, or `os.environ.get` on keys). Credentials must stay
out of the agent's context.

This skill provides CLI access to the NCBI PubMed and PubMed Central APIs via
`scripts/pubmed_api.py` — a single CLI with 10 functions covering search, fetch,
linking, full text, spelling, discovery, citation matching, and caching.

## Core Rules

-   **API Use**: Always use the provided wrapper `scripts/pubmed_api.py` which
    manages rate limits automatically and prevents API abuse. Setting the
    `NCBI_API_KEY` environment variable raises the rate limit from 3 to 10
    requests/second. Querying the API any other way (e.g. via curl, wget, or
    hand-written code) is strictly forbidden.
-   **JSON Processing**: Use `jq` to filter and transform JSON output (or python
    equivalents if `jq` is not available) to prevent hallucinations and context
    overflow.
-   **Temporary Files**: To avoid polluting the working directory with JSON
    files, use a temporary directory inside the current directory. When running
    multiple agents or tasks in parallel, ensure each uses a unique subdirectory
    name (e.g., `tmp_$TASK_ID/`) to avoid file collisions.
-   **Notification**: If this skill is used, ensure this is mentioned in the
    output AND list the URLs of all papers that were used in producing the
    output.

## Structure of the skill folder

-   `SKILL.md` - This file
-   `scripts/pubmed_api.py` - The skill CLI
-   `references/` - Directory with detailed function specifications
    -   `advanced-linking.md`
    -   `advanced-search.md`
    -   `bulk-workflows.md`
    -   `citation-matching.md`
    -   `cross-database-linking.md`
    -   `fetch-and-resolve.md`
    -   `search-and-discovery.md`
    -   `utilities.md`

## CLI Usage

```bash
uv run scripts/pubmed_api.py <output_file> <function_name> <required_args> [--flag value ...]
```

-   **Positional Arguments**: Arguments are positional; list arguments are
    passed as comma-separated strings without spaces (e.g.
    `"35113657,31234568"`).
-   **Flag Options**: Optional arguments can be passed as `--flag value` instead
    of positional args.
-   **Output Handling**: On success, JSON is written to `output_file`. On error,
    the process exits with a non-zero code and no output file is written.

### Example Usage

```bash
uv run scripts/pubmed_api.py ./search_results.json search_pubmed "BRCA1" --max_results 5
cat ./search_results.json | jq '.[]' -r
uv run scripts/pubmed_api.py ./abstracts.json fetch_article_abstracts "35113657"
cat ./abstracts.json | jq '.[0].title' -r
```

## Essential Recipes

**Join PMIDs for the next call (most common chaining pattern):**

```bash
cat ./search_results.json | jq -r 'join(",")'
```

**Slim abstracts to essential fields and truncate long abstracts:**

```bash
cat ./abstracts.json | jq '[.[] | {pmid, title, snippet: (.abstract // "")[:500]}]'
```

**Filter by keyword (null-safe):**

```bash
cat ./abstracts.json | jq '[.[] | select((.title // "") | contains("Review"))]'
```

### Context Management & Accuracy

When processing larger result sets (>10 abstracts):

1.  **Filter Early**: Use `jq` to verify keywords in abstracts *before* reading
    the full JSON into context.
2.  **Slimming**: Extract only `title` and `abstract` fields unless explicitly
    instructed otherwise. Author lists and metadata contribute to noise.
3.  **Bulk Operations (N > 10)**: Avoid fetching or processing IDs one-by-one.
    The API and History Server are designed for bulk retrieval. Fetch all data
    in a **single turn** and use shell pipelines to slim the results before
    reading into context. This prevents turn exhaustion and context overflow.
4.  **Grounding**: Never use internal knowledge to provide specific identifiers
    (PMIDs, CIDs, Gene IDs) if no results are found. Report the tool's output
    accurately to ensure results are grounded in the current database state.
5.  **Search Termination**: When asked to find papers that may not exist, limit
    exploration to 3–5 high-quality, varied search queries. If no results match
    after these attempts, conclude that no papers meet the criteria rather than
    continuing to iterate — unless explicitly instructed to be thorough.

## Functions

> **⚠️ MANDATORY**: You **MUST** read the linked reference file for a function
> group **before calling any function** in that group. The tables below only
> describe *what* each function does — not *how* to call it. Argument names,
> argument order, flags, and output schemas are **only** documented in the
> reference files. **Do NOT guess or infer arguments from function names.** If
> you call a function without first reading its reference, you **will** produce
> incorrect invocations.

### [Search](references/search-and-discovery.md)

-   `search_pubmed`: Find PMIDs matching a free-text or structured NCBI query.
-   `global_database_discovery`: Count how many records match a query across
    every NCBI database.

### [Fetch & Resolve](references/fetch-and-resolve.md)

-   `fetch_article_abstracts`: Retrieve metadata and abstracts for a batch of
    PMIDs.
-   `get_full_text_pmc`: Retrieve open-access full text from PMC.
-   `fetch_database_summary`: Resolve opaque UIDs from any NCBI database into
    human-readable metadata.

### [Cross-Database Linking](references/cross-database-linking.md)

-   `find_linked_biological_data`: Find records in other NCBI databases linked
    to a source record.
-   `discover_available_links`: List all available ELink linknames for a given
    record.

### [Bulk Workflows](references/bulk-workflows.md)

When working with **more than ~10 PMIDs**, avoid processing IDs one-by-one.
Upload them to the NCBI History Server via `cache_results_history` to get a
session handle (`webenv` + `query_key`), then pass that handle to
`fetch_article_abstracts` or `find_linked_biological_data` for a single bulk
call. Chain with `jq` shell pipelines to slim results before reading into
context. This prevents turn exhaustion and context overflow. See the reference
for complete workflow recipes (search→fetch, cross-db exploration, citation
resolution, and bulk retrieval with data slimming).

-   `cache_results_history`: Upload PMIDs to the NCBI History Server for bulk
    retrieval.

### [Utilities](references/utilities.md)

-   `verify_medical_spelling`: Spell-check biomedical terms before searching.
-   `match_raw_citations`: Resolve incomplete bibliographic citations to PMIDs.
