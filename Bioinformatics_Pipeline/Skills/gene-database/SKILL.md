---
name: gene-database
description: Query the NCBI Gene database via E-utilities and Datasets API; search genes by symbol/ID, retrieve annotations (RefSeq, GO, location, phenotype) for single or batch gene lists, and analyze gene functions and pathways.
license: MIT
metadata:
    skill-author: K-Dense Inc. + AIPOCH
---

## Overview

NCBI Gene is a comprehensive database integrating gene information from diverse species, providing nomenclature, reference sequences (RefSeqs), chromosomal maps, biological pathways, genetic variations, phenotypes, and cross-references to global genomic resources.

## When to Use

- You have a gene symbol (e.g., **BRCA1**) and need the correct **NCBI Gene ID** for a specific organism.
- You have an NCBI **Gene ID** and need consolidated metadata (aliases, RefSeq accessions, genomic location, GO, literature links).
- You need to **annotate a gene panel** (dozens to thousands of genes) with consistent identifiers and core annotations.
- You want to search genes by **biological context** (GO terms, phenotype/disease keywords, pathway terms) and then retrieve details for the hits.
- You are building a pipeline that must respect **NCBI rate limits** and handle retries for transient API failures.

## Key Features

- Symbol/name search with organism scoping using **E-utilities (ESearch)**.
- Gene record retrieval by ID using **E-utilities (EFetch/ESummary)** in JSON/XML/text-oriented outputs.
- Streamlined, gene-focused retrieval using the **NCBI Datasets API** (metadata + sequences/links in a single workflow).
- Batch lookup utilities with rate-limit awareness and output aggregation.
- Supports common annotation fields: nomenclature/aliases, RefSeq transcripts/proteins, genomic location, GO annotations, phenotype/disease keywords, and related literature references.

## Dependencies

- Python **3.9+**
- `requests` **>= 2.28**
- NCBI E-utilities (Entrez) HTTP API (public service)
- NCBI Datasets HTTP API (public service)
- Optional: NCBI API key (recommended for higher throughput)

## API Selection Guidance

- Use **E-utilities** when you need:
  - Complex Entrez query syntax (fielded queries, boolean logic).
  - Cross-database patterns.
  - Fine control over search and retrieval steps (ESearch → ESummary/EFetch).
- Use **NCBI Datasets API** when you need:
  - A streamlined gene-centric retrieval path.
  - Consolidated metadata (and often sequence-related links) with fewer round trips.

## Example Usage

> The following examples assume the repository provides these scripts:
> - `scripts/query_gene.py`
> - `scripts/fetch_gene_data.py`
> - `scripts/batch_gene_lookup.py`

### 1) Search by symbol/name (E-utilities / ESearch)

```bash
python scripts/query_gene.py --search "BRCA1" --organism "human"
```

Example advanced query strings:

```bash
python scripts/query_gene.py --search "insulin[gene name] AND human[organism]"
python scripts/query_gene.py --search "dystrophin[gene name] AND muscular dystrophy[disease]"
python scripts/query_gene.py --search "human[organism] AND 17q21[chromosome]"
```

### 2) Retrieve gene information by Gene ID

Using E-utilities (format-oriented retrieval):

```bash
python scripts/query_gene.py --id 672 --format json
```

Using NCBI Datasets API (consolidated gene payload):

```bash
python scripts/fetch_gene_data.py --gene-id 672
```

Or by symbol + taxon:

```bash
python scripts/fetch_gene_data.py --symbol BRCA1 --taxon human
python scripts/fetch_gene_data.py --symbol TP53 --taxon "Homo sapiens" --output json
```

### 3) Batch lookup for gene list annotation

From a file of symbols (organism required for symbol disambiguation):

```bash
python scripts/batch_gene_lookup.py --file gene_list.txt --organism human
```

From a comma-separated list of Gene IDs:

```bash
python scripts/batch_gene_lookup.py --ids 672,7157,5594 --output results.json
```

## Query Patterns (E-utilities)

Typical fielded query components include:

- `"<SYMBOL>"` plus organism scoping: `BRCA1[gene name] AND human[organism]`
- GO term searches (example): `GO:0006915[biological process]`
- Phenotype/disease keywords (example): `diabetes[phenotype] AND mouse[organism]`
- Pathway keywords (example): `insulin signaling pathway[pathway]`

## Rate Limits and API Keys

- Without an API key (typical defaults):
  - E-utilities: ~**3 requests/sec**
  - Datasets API: ~**5 requests/sec**
- With an NCBI API key:
  - both can be used up to ~**10 requests/sec** (service-dependent)

Obtain an API key from: https://www.ncbi.nlm.nih.gov/account/

## Error Handling Recommendations

- Handle standard HTTP errors:
  - **400**: invalid/malformed query or parameters
  - **404**: Gene ID not found
  - **429**: rate limit exceeded
- Use **exponential backoff** with jitter for retries on 429/5xx.
- Cache results for repeated lookups (especially in batch annotation workflows).

## Output/Data Formats

Depending on endpoint/script options, gene data may be returned as:

- **JSON** (recommended for pipelines)
- **XML** (legacy/verbose metadata)
- **Text summaries**
- Sequence-oriented formats such as **FASTA** or **GenBank** (when supported by the chosen endpoint/workflow)

## Best Practices

1. **Always specify organism** when searching by gene symbol to avoid ambiguity.
2. **Use Gene IDs** for precise lookups when available.
3. **Batch requests** when working with multiple genes to minimize API calls.
4. **Cache results** locally to reduce redundant queries.
5. **Include API key** in scripts for higher rate limits.
6. **Handle errors gracefully** with retry logic for transient failures.
7. **Validate gene symbols** before batch processing to catch typos.

## Resources

This skill includes:

### scripts/

- `query_gene.py` - Query genes using E-utilities (ESearch, ESummary, EFetch)
- `fetch_gene_data.py` - Fetch gene data using NCBI Datasets API
- `batch_gene_lookup.py` - Handle multiple gene queries efficiently

### references/

If present in the repository, consult:

- `api_reference.md` for endpoint/parameter details and response structures
- `common_workflows.md` for additional query patterns and end-to-end examples