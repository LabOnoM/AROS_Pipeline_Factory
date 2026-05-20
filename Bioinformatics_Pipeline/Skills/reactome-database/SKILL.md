---
name: reactome-database
description: Query the Reactome database (Analysis and Content Services). Use when
  the user asks about pathway analysis, gene list enrichment, retrieving results by
  token, finding unmapped or not-found identifiers, mapping identifiers, reaction
  participants (inputs, outputs), pathway hierarchy (including top-level pathways),
  diagram export, cross-reference mapping, or searching the knowledgebase.
license: Unknown
metadata:
  skill-author: K-Dense Inc.
---

# Reactome Database

## Overview

Reactome is a free, open-source, curated pathway database with 2,825+ human pathways. Query biological pathways, perform overrepresentation and expression analysis, map genes to pathways, explore molecular interactions via REST API and Python client for systems biology research.

## When to Use This Skill

This skill should be used when:
- Performing pathway enrichment analysis on gene or protein lists
- Analyzing gene expression data to identify relevant biological pathways
- Querying specific pathway information, reactions, or molecular interactions
- Mapping genes or proteins to biological pathways and processes
- Exploring disease-related pathways and mechanisms
- Visualizing analysis results in the Reactome Pathway Browser
- Conducting comparative pathway analysis across species

## Core Capabilities

Reactome provides two main API services and a Python client library:

### 1. Content Service - Data Retrieval

Query and retrieve biological pathway data, molecular interactions, and entity information.

**Common operations:**
- Retrieve pathway information and hierarchies
- Query specific entities (proteins, reactions, complexes)
- Get participating molecules in pathways
- Access database version and metadata
- Explore pathway compartments and locations

**API Base URL:** `https://reactome.org/ContentService`

### 2. Analysis Service - Pathway Analysis

Perform computational analysis on gene lists and expression data.

**Analysis types:**
- **Overrepresentation Analysis**: Identify statistically significant pathways from gene/protein lists
- **Expression Data Analysis**: Analyze gene expression datasets to find relevant pathways
- **Species Comparison**: Compare pathway data across different organisms

**API Base URL:** `https://reactome.org/AnalysisService`

### 3. reactome2py Python Package

Python client library that wraps Reactome API calls for easier programmatic access.

**Installation:**
```bash
uv pip install reactome2py
```

**Note:** The reactome2py package (version 3.0.0, released January 2021) is functional but not actively maintained. For the most up-to-date functionality, consider using direct REST API calls.

## Querying Pathway Data

### Using Content Service REST API

The Content Service uses REST protocol and returns data in JSON or plain text formats.

**Get database version:**
```python
import requests

response = requests.get("https://reactome.org/ContentService/data/database/version")
version = response.text
print(f"Reactome version: {version}")
```

**Query a specific entity:**
```python
import requests

entity_id = "R-HSA-69278"  # Example pathway ID
response = requests.get(f"https://reactome.org/ContentService/data/query/{entity_id}")
data = response.json()
```

**Get participating molecules in a pathway:**
```python
import requests

event_id = "R-HSA-69278"
response = requests.get(
    f"https://reactome.org/ContentService/data/event/{event_id}/participatingPhysicalEntities"
)
molecules = response.json()
```

### Using reactome2py Package

```python
import reactome2py
from reactome2py import content

# Query pathway information
pathway_info = content.query_by_id("R-HSA-69278")

# Get database version
version = content.get_database_version()
```

**For detailed API endpoints and parameters**, refer to `references/api_reference.md` in this skill.

## Performing Pathway Analysis

### Overrepresentation Analysis

Submit a list of gene/protein identifiers to find enriched pathways.

**Using REST API:**
```python
import requests

# Prepare identifier list
identifiers = ["TP53", "BRCA1", "EGFR", "MYC"]
data = "\n".join(identifiers)

# Submit analysis
response = requests.post(
    "https://reactome.org/AnalysisService/identifiers/",
    headers={"Content-Type": "text/plain"},
    data=data
)

result = response.json()
token = result["summary"]["token"]  # Save token to retrieve results later

# Access pathways
for pathway in result["pathways"]:
    print(f"{pathway['stId']}: {pathway['name']} (p-value: {pathway['entities']['pValue']})")
```

**Retrieve analysis by token:**
```python
# Token is valid for 7 days
response = requests.get(f"https://reactome.org/AnalysisService/token/{token}")
results = response.json()
```

### Expression Data Analysis

Analyze gene expression datasets with quantitative values.

**Input format (TSV with header starting with #):**
```
#Gene	Sample1	Sample2	Sample3
TP53	2.5	3.1	2.8
BRCA1	1.2	1.5	1.3
EGFR	4.5	4.2	4.8
```

**Submit expression data:**
```python
import requests

# Read TSV file
with open("expression_data.tsv", "r") as f:
    data = f.read()

response = requests.post(
    "https://reactome.org/AnalysisService/identifiers/",
    headers={"Content-Type": "text/plain"},
    data=data
)

result = response.json()
```

### Species Projection

Map identifiers to human pathways exclusively using the `/projection/` endpoint:

```python
response = requests.post(
    "https://reactome.org/AnalysisService/identifiers/projection/",
    headers={"Content-Type": "text/plain"},
    data=data
)
```

## Visualizing Results

Analysis results can be visualized in the Reactome Pathway Browser by constructing URLs with the analysis token:

```python
token = result["summary"]["token"]
pathway_id = "R-HSA-69278"
url = f"https://reactome.org/PathwayBrowser/#{pathway_id}&DTAB=AN&ANALYSIS={token}"
print(f"View results: {url}")
```

## Working with Analysis Tokens

- Analysis tokens are valid for **7 days**
- Tokens allow retrieval of previously computed results without re-submission
- Store tokens to access results across sessions
- Use `GET /token/{TOKEN}` endpoint to retrieve results

## Data Formats and Identifiers

### Supported Identifier Types

Reactome accepts various identifier formats:
- UniProt accessions (e.g., P04637)
- Gene symbols (e.g., TP53)
- Ensembl IDs (e.g., ENSG00000141510)
- EntrezGene IDs (e.g., 7157)
- ChEBI IDs for small molecules

The system automatically detects identifier types.

### Input Format Requirements

**For overrepresentation analysis:**
- Plain text list of identifiers (one per line)
- OR single column in TSV format

**For expression analysis:**
- TSV format with mandatory header row starting with "#"
- Column 1: identifiers
- Columns 2+: numeric expression values
- Use period (.) as decimal separator

### Output Format

All API responses return JSON containing:
- `pathways`: Array of enriched pathways with statistical metrics
- `summary`: Analysis metadata and token
- `entities`: Matched and unmapped identifiers
- Statistical values: pValue, FDR (false discovery rate)

## Helper Scripts

This skill includes `scripts/reactome_query.py`, a helper script for common Reactome operations:

```bash
# Query pathway information
python scripts/reactome_query.py query R-HSA-69278

# Perform overrepresentation analysis
python scripts/reactome_query.py analyze gene_list.txt

# Get database version
python scripts/reactome_query.py version
```

## Additional Resources

- **API Documentation**: https://reactome.org/dev
- **User Guide**: https://reactome.org/userguide
- **Documentation Portal**: https://reactome.org/documentation
- **Data Downloads**: https://reactome.org/download-data
- **reactome2py Docs**: https://reactome.github.io/reactome2py/

For comprehensive API endpoint documentation, see `references/api_reference.md` in this skill.

## Current Database Statistics (Version 94, September 2025)

- 2,825 human pathways
- 16,002 reactions
- 11,630 proteins
- 2,176 small molecules
- 1,070 drugs
- 41,373 literature references

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://reactome.org/license and https://reactome.org/cite, then (2)
    create the file recording the notification text and timestamp.

## Overview

Reactome is a free, open-source, curated pathway database. This skill wraps both
the **Analysis Service** (`https://reactome.org/AnalysisService/`) and the
**Content Service** (`https://reactome.org/ContentService/`) providing pathway
enrichment analysis, identifier mapping, reaction details, pathway hierarchy
navigation, diagram export, cross-reference mapping, and search.

## When to Use This Skill

-   Performing pathway enrichment (overrepresentation) analysis on gene/protein
    lists
-   Retrieving analysis results using a token from previous enrichment
-   Identifying which genes or proteins were not found in a pathway analysis
-   Analyzing gene expression data against pathway annotations
-   Mapping identifiers to Reactome entities across species
-   Retrieving reaction participants (inputs, outputs, catalysts, regulators)
-   Navigating pathway hierarchy and listing top-level pathways
-   Finding which complexes or sets contain a protein
-   Exporting pathway/reaction diagrams (PNG/SVG) with gene highlighting
-   Cross-referencing identifiers across databases (UniProt, Ensembl, etc.)
-   Searching the Reactome knowledgebase
-   Downloading analysis reports (PDF, CSV, JSON)
-   Comparing pathways across species

## Common Species IDs

Reference list for common research organisms:

-   Homo sapiens
    -   ID: 9606
-   Mus musculus (Mouse)
    -   ID: 48892
-   Rattus norvegicus (Rat)
    -   ID: 48895

## Common Pathway IDs

Reference list for commonly used Reactome pathway stable IDs:

-   Cell Cycle
    -   Stable ID: R-HSA-1640170
    -   Notes: Top-level pathway (broad)
-   Cell Cycle, Mitotic
    -   Stable ID: R-HSA-69278
    -   Notes: Specific sub-pathway — use this for diagrams and drill-downs
-   Immune System
    -   Stable ID: R-HSA-168256
    -   Notes: Top-level pathway
-   Signal Transduction
    -   Stable ID: R-HSA-162582
    -   Notes: Top-level pathway
-   Gene Expression
    -   Stable ID: R-HSA-74160
    -   Notes: Top-level pathway
-   Programmed Cell Death
    -   Stable ID: R-HSA-5357801
    -   Notes: Top-level pathway

> **Important**: When the user asks for a "Cell Cycle" diagram or analysis,
> prefer the specific **Cell Cycle, Mitotic** pathway (`R-HSA-69278`) unless the
> user explicitly requests the top-level overview. The examples throughout this
> document use `R-HSA-69278`.

## Core Rules

1.  **Always use `--output`**: Every subcommand requires `--output <file>` to
    write results to a file. Never rely on stdout for large results.
2.  **Default species is Homo sapiens**: Use `--species` to override.
3.  **Tokens expire after 7 days**: Store tokens from analysis results to
    retrieve them later without re-submitting data.
4.  **Use `--fdr` and `--pvalue` to filter**: Enrichment results can be
    overwhelming. Filter with `--fdr 0.05` or `--pvalue 0.01` to focus on
    statistically significant pathways.
5.  **Identifier formats**: Reactome auto-detects identifiers including gene
    symbols (TP53), UniProt (P04637), Ensembl (ENSG00000141510), ChEBI, OMIM,
    EntrezGene, and many more.
6.  **Handle large outputs**: For commands that return large data (like
    `species-comparison`), use the `--summary` flag to truncate lists and avoid
    exceeding workspace file size limits (1MB).
7.  **Notification**: If this skill is used, ensure this is mentioned in the
    output.

## Tool Execution

The CLI tool is at `scripts/reactome_analysis.py`. Run with `uv`:

```bash
uv run scripts/reactome_analysis.py <command> [options] --output /tmp/out.json
```

**To list all available subcommands and flags**, run:

```bash
uv run scripts/reactome_analysis.py --help
```

Use `--help` to verify available subcommands or flags before executing an
unfamiliar command.

## Feature Domains

### 1. Database Info

```bash
uv run scripts/reactome_analysis.py db-version --output /tmp/version.json
uv run scripts/reactome_analysis.py db-name --output /tmp/name.json
```

### 2. Single Identifier Analysis

```bash
uv run scripts/reactome_analysis.py identifier --id TP53 --output /tmp/tp53.json
uv run scripts/reactome_analysis.py identifier-projection --id TP53 --output /tmp/tp53_proj.json
```

### 3. Batch Analysis (Enrichment)

Submit a list of identifiers for overrepresentation or expression analysis:

```bash
uv run scripts/reactome_analysis.py analyze --data "TP53,BRCA1,EGFR" --output /tmp/enrich.json
uv run scripts/reactome_analysis.py analyze --file genes.txt --output /tmp/enrich.json
uv run scripts/reactome_analysis.py analyze-projection --data "TP53,BRCA1" --output /tmp/proj.json
uv run scripts/reactome_analysis.py analyze --data "TP53,BRCA1" --fdr 0.05 --output /tmp/sig.json
```

Common options: `--page-size` (alias `--limit`), `--page` (alias `--offset`),
`--sort-by`, `--order`, `--resource`, `--species`, `--fdr`, `--pvalue`.

### 4. Token-Based Result Retrieval

```bash
uv run scripts/reactome_analysis.py token-result --token TOKEN --output /tmp/result.json
uv run scripts/reactome_analysis.py token-not-found --token TOKEN --output /tmp/notfound.json
uv run scripts/reactome_analysis.py token-resources --token TOKEN --output /tmp/resources.json
uv run scripts/reactome_analysis.py token-found-entities --token TOKEN --pathway R-HSA-69278 --output /tmp/found.json
uv run scripts/reactome_analysis.py token-filter-species --token TOKEN --species-filter 9606 --output /tmp/filtered.json
uv run scripts/reactome_analysis.py token-reactions-pathway --token TOKEN --pathway R-HSA-69278 --output /tmp/rxns.json
```

### 5. Download Results

```bash
uv run scripts/reactome_analysis.py download-result --token TOKEN --output /tmp/full.json
uv run scripts/reactome_analysis.py download-pathways --token TOKEN --output /tmp/pathways.csv
uv run scripts/reactome_analysis.py download-found --token TOKEN --output /tmp/found.csv
uv run scripts/reactome_analysis.py download-not-found --token TOKEN --output /tmp/notfound.csv
```

### 6. Identifier Mapping

```bash
uv run scripts/reactome_analysis.py mapping --data "TP53,BRCA1" --output /tmp/mapped.json
uv run scripts/reactome_analysis.py mapping-projection --data "TP53" --output /tmp/mapped_proj.json
```

### 7. Reaction Participants & Mechanism of Action

Retrieve the molecular participants of a reaction (inputs, outputs, catalysts):

```bash
uv run scripts/reactome_analysis.py participants --id R-HSA-6804194 --output /tmp/participants.json
uv run scripts/reactome_analysis.py participating-entities --id R-HSA-6804194 --output /tmp/entities.json
```

### 8. Complex & Set Membership

Find which complexes or sets contain a given entity:

```bash
uv run scripts/reactome_analysis.py component-of --id R-HSA-69488 --output /tmp/complexes.json
```

### 9. Pathway Hierarchy Navigation

Move up (ancestors) or down (contained events) the pathway hierarchy:

```bash
uv run scripts/reactome_analysis.py event-ancestors --id R-HSA-69278 --output /tmp/ancestors.json
uv run scripts/reactome_analysis.py contained-events --id R-HSA-69278 --output /tmp/steps.json
uv run scripts/reactome_analysis.py top-pathways --output /tmp/top.json
uv run scripts/reactome_analysis.py low-pathways --id R-HSA-69488 --output /tmp/low.json
```

### 10. Diagram Export

Export pathway or reaction diagrams as PNG/SVG, with optional gene highlighting:

```bash
uv run scripts/reactome_analysis.py diagram --id R-HSA-69278 --output /tmp/diagram.png
uv run scripts/reactome_analysis.py diagram --id R-HSA-69278 --highlight TP53 --output /tmp/highlighted.png
uv run scripts/reactome_analysis.py diagram --id R-HSA-69278 --format svg --output /tmp/diagram.svg
uv run scripts/reactome_analysis.py reaction-diagram --id R-HSA-6804194 --output /tmp/rxn.png
```

### 11. Cross-Reference Mapping

Resolve identifiers to Reactome internal IDs and cross-references:

```bash
uv run scripts/reactome_analysis.py xref-mapping --id TP53 --output /tmp/xref.json
uv run scripts/reactome_analysis.py xref-mapping-batch --data "TP53,BRCA1" --output /tmp/xrefs.json
```

### 12. Search

```bash
uv run scripts/reactome_analysis.py search --query "TP53 apoptosis" --output /tmp/results.json
```

### 13. Query Entry by ID

```bash
uv run scripts/reactome_analysis.py query --id R-HSA-69278 --output /tmp/entry.json
```

### 14. Report & Species Comparison

```bash
uv run scripts/reactome_analysis.py report --token TOKEN --output /tmp/report.pdf
uv run scripts/reactome_analysis.py species-comparison --species-id 48892 --output /tmp/species.json
# Use --summary to truncate large output and avoid workspace file size limits
uv run scripts/reactome_analysis.py species-comparison --species-id 48892 --summary --output /tmp/species.json
```

## Recipe: Interpreting Gene Set Enrichment

A step-by-step workflow for interpreting gene set enrichment results:

1.  **Submit gene list** with projection to human pathways: `bash uv run
    scripts/reactome_analysis.py analyze-projection \ --data
    "TP53,BRCA1,EGFR,MYC,PTEN" --fdr 0.05 --output /tmp/enrichment.json`

2.  **Inspect top pathways** — examine `pathwaysFound`, top pathway names,
    p-values, and FDR values in the output.

3.  **Drill into a pathway** — get its sub-events and reaction details: `bash uv
    run scripts/reactome_analysis.py contained-events --id R-HSA-69278 --output
    /tmp/steps.json uv run scripts/reactome_analysis.py participants --id
    <reaction_id> --output /tmp/parts.json`

4.  **Visualise** — export a diagram with your genes highlighted: `bash uv run
    scripts/reactome_analysis.py diagram --id R-HSA-69278 \ --highlight
    "TP53,BRCA1" --output /tmp/diagram.png`

5.  **Check hierarchy** — navigate up to see broader biological context: `bash
    uv run scripts/reactome_analysis.py event-ancestors --id R-HSA-69278
    --output /tmp/ancestors.json`

6.  **Cross-reference** — map identifiers to other databases: `bash uv run
    scripts/reactome_analysis.py xref-mapping --id TP53 --output
    /tmp/xrefs.json`

## Reference

For detailed API endpoint documentation, see
[references/api_reference.md](references/api_reference.md).
