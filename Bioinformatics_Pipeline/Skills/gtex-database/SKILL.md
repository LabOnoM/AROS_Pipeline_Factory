---
name: gtex-database
description: Query GTEx (Genotype-Tissue Expression) portal for tissue-specific gene
  expression, eQTLs (expression quantitative trait loci), and sQTLs. Essential for
  linking GWAS variants to gene regulation, understanding tissue-specific expression,
  and interpreting non-coding variant effects.
license: CC-BY-4.0
metadata:
  skill-author: Kuan-lin Huang
---

# GTEx Database

## Overview

The Genotype-Tissue Expression (GTEx) project provides a comprehensive resource for studying tissue-specific gene expression and genetic regulation across 54 non-diseased human tissues from nearly 1,000 individuals. GTEx v10 (the latest release) enables researchers to understand how genetic variants regulate gene expression (eQTLs) and splicing (sQTLs) in a tissue-specific manner, which is critical for interpreting GWAS loci and identifying regulatory mechanisms.

**Key resources:**
- GTEx Portal: https://gtexportal.org/
- GTEx API v2: https://gtexportal.org/api/v2/
- Data downloads: https://gtexportal.org/home/downloads/adult-gtex/
- Documentation: https://gtexportal.org/home/documentationPage

## When to Use This Skill

Use GTEx when:

- **GWAS locus interpretation**: Identifying which gene a non-coding GWAS variant regulates via eQTLs
- **Tissue-specific expression**: Comparing gene expression levels across 54 human tissues
- **eQTL colocalization**: Testing if a GWAS signal and an eQTL signal share the same causal variant
- **Multi-tissue eQTL analysis**: Finding variants that regulate expression in multiple tissues
- **Splicing QTLs (sQTLs)**: Identifying variants that affect splicing ratios
- **Tissue specificity analysis**: Determining which tissues express a gene of interest
- **Gene expression exploration**: Retrieving normalized expression levels (TPM) per tissue

## Core Capabilities

### 1. GTEx REST API v2

Base URL: `https://gtexportal.org/api/v2/`

The API returns JSON and does not require authentication. All endpoints support pagination.

```python
import requests

BASE_URL = "https://gtexportal.org/api/v2"

def gtex_get(endpoint, params=None):
    """Make a GET request to the GTEx API."""
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params, headers={"Accept": "application/json"})
    response.raise_for_status()
    return response.json()
```

### 2. Gene Expression by Tissue

```python
import requests
import pandas as pd

def get_gene_expression_by_tissue(gene_id_or_symbol, dataset_id="gtex_v10"):
    """Get median gene expression across all tissues."""
    url = "https://gtexportal.org/api/v2/expression/medianGeneExpression"
    params = {
        "gencodeId": gene_id_or_symbol,
        "datasetId": dataset_id,
        "itemsPerPage": 100
    }
    response = requests.get(url, params=params)
    data = response.json()

    records = data.get("data", [])
    df = pd.DataFrame(records)
    if not df.empty:
        df = df[["tissueSiteDetailId", "tissueSiteDetail", "median", "unit"]].sort_values(
            "median", ascending=False
        )
    return df

# Example: get expression of APOE across tissues
df = get_gene_expression_by_tissue("ENSG00000130203.10")  # APOE GENCODE ID
# Or use gene symbol (some endpoints accept both)
print(df.head(10))
# Output: tissue name, median TPM, sorted by highest expression
```

### 3. eQTL Lookup

```python
import requests
import pandas as pd

def query_eqtl(gene_id, tissue_id=None, dataset_id="gtex_v10"):
    """Query significant eQTLs for a gene, optionally filtered by tissue."""
    url = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
    params = {
        "gencodeId": gene_id,
        "datasetId": dataset_id,
        "itemsPerPage": 250
    }
    if tissue_id:
        params["tissueSiteDetailId"] = tissue_id

    all_results = []
    page = 0
    while True:
        params["page"] = page
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get("data", [])
        if not results:
            break
        all_results.extend(results)
        if len(results) < params["itemsPerPage"]:
            break
        page += 1

    df = pd.DataFrame(all_results)
    if not df.empty:
        df = df.sort_values("pval", ascending=True)
    return df

# Example: Find eQTLs for PCSK9
df = query_eqtl("ENSG00000169174.14")
print(df[["snpId", "tissueSiteDetailId", "slope", "pval", "gencodeId"]].head(20))
```

### 4. Single-Tissue eQTL by Variant

```python
import requests

def query_variant_eqtl(variant_id, tissue_id=None, dataset_id="gtex_v10"):
    """Get all eQTL associations for a specific variant."""
    url = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
    params = {
        "variantId": variant_id,  # e.g., "chr1_55516888_G_GA_b38"
        "datasetId": dataset_id,
        "itemsPerPage": 250
    }
    if tissue_id:
        params["tissueSiteDetailId"] = tissue_id

    response = requests.get(url, params=params)
    return response.json()

# GTEx variant ID format: chr{chrom}_{pos}_{ref}_{alt}_b38
# Example: "chr17_43094692_G_A_b38"
```

### 5. Multi-Tissue eQTL (eGenes)

```python
import requests

def get_egenes(tissue_id, dataset_id="gtex_v10"):
    """Get all eGenes (genes with at least one significant eQTL) in a tissue."""
    url = "https://gtexportal.org/api/v2/association/egene"
    params = {
        "tissueSiteDetailId": tissue_id,
        "datasetId": dataset_id,
        "itemsPerPage": 500
    }

    all_egenes = []
    page = 0
    while True:
        params["page"] = page
        response = requests.get(url, params=params)
        data = response.json()
        batch = data.get("data", [])
        if not batch:
            break
        all_egenes.extend(batch)
        if len(batch) < params["itemsPerPage"]:
            break
        page += 1
    return all_egenes

# Example: all eGenes in whole blood
egenes = get_egenes("Whole_Blood")
print(f"Found {len(egenes)} eGenes in Whole Blood")
```

### 6. Tissue List

```python
import requests

def get_tissues(dataset_id="gtex_v10"):
    """Get all available tissues with metadata."""
    url = "https://gtexportal.org/api/v2/dataset/tissueSiteDetail"
    params = {"datasetId": dataset_id, "itemsPerPage": 100}
    response = requests.get(url, params=params)
    return response.json()["data"]

tissues = get_tissues()
# Key fields: tissueSiteDetailId, tissueSiteDetail, colorHex, samplingSite
# Common tissue IDs:
# Whole_Blood, Brain_Cortex, Liver, Kidney_Cortex, Heart_Left_Ventricle,
# Lung, Muscle_Skeletal, Adipose_Subcutaneous, Colon_Transverse, ...
```

### 7. sQTL (Splicing QTLs)

```python
import requests

def query_sqtl(gene_id, tissue_id=None, dataset_id="gtex_v10"):
    """Query significant sQTLs for a gene."""
    url = "https://gtexportal.org/api/v2/association/singleTissueSqtl"
    params = {
        "gencodeId": gene_id,
        "datasetId": dataset_id,
        "itemsPerPage": 250
    }
    if tissue_id:
        params["tissueSiteDetailId"] = tissue_id

    response = requests.get(url, params=params)
    return response.json()
```

## Query Workflows

### Workflow 1: Interpreting a GWAS Variant via eQTLs

1. **Identify the GWAS variant** (rs ID or chromosome position)
2. **Convert to GTEx variant ID format** (`chr{chrom}_{pos}_{ref}_{alt}_b38`)
3. **Query all eQTL associations** for that variant across tissues
4. **Check effect direction**: is the GWAS risk allele the same as the eQTL effect allele?
5. **Prioritize tissues**: select tissues biologically relevant to the disease
6. **Consider colocalization** using `coloc` (R package) with full summary statistics

```python
import requests, pandas as pd

def interpret_gwas_variant(variant_id, dataset_id="gtex_v10"):
    """Find all genes regulated by a GWAS variant."""
    url = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
    params = {"variantId": variant_id, "datasetId": dataset_id, "itemsPerPage": 500}
    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data.get("data", []))
    if df.empty:
        return df
    return df[["geneSymbol", "tissueSiteDetailId", "slope", "pval", "maf"]].sort_values("pval")

# Example
results = interpret_gwas_variant("chr1_154453788_A_T_b38")
print(results.groupby("geneSymbol")["tissueSiteDetailId"].count().sort_values(ascending=False))
```

### Workflow 2: Gene Expression Atlas

1. Get median expression for a gene across all tissues
2. Identify the primary expression site(s)
3. Compare with disease-relevant tissues
4. Download raw data for statistical comparisons

### Workflow 3: Tissue-Specific eQTL Analysis

1. Select tissues relevant to your disease
2. Query all eGenes in that tissue
3. Cross-reference with GWAS-significant loci
4. Identify co-localized signals

## Key API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/expression/medianGeneExpression` | Median TPM by tissue for a gene |
| `/expression/geneExpression` | Full distribution of expression per tissue |
| `/association/singleTissueEqtl` | Significant eQTL associations |
| `/association/singleTissueSqtl` | Significant sQTL associations |
| `/association/egene` | eGenes in a tissue |
| `/dataset/tissueSiteDetail` | Available tissues with metadata |
| `/reference/gene` | Gene metadata (GENCODE IDs, coordinates) |
| `/variant/variantPage` | Variant lookup by rsID or position |

## Datasets Available

| ID | Description |
|----|-------------|
| `gtex_v10` | GTEx v10 (current; ~960 donors, 54 tissues) |
| `gtex_v8` | GTEx v8 (838 donors, 49 tissues) — older but widely cited |

## Best Practices

- **Use GENCODE IDs** (e.g., `ENSG00000130203.10`) for gene queries; the `.version` suffix matters for some endpoints
- **GTEx variant IDs** use the format `chr{chrom}_{pos}_{ref}_{alt}_b38` (GRCh38) — different from rs IDs
- **Handle pagination**: Large queries (e.g., all eGenes) require iterating through pages
- **Tissue nomenclature**: Use `tissueSiteDetailId` (e.g., `Whole_Blood`) not display names for API calls
- **FDR correction**: GTEx uses FDR < 0.05 (q-value) as the significance threshold for eQTLs
- **Effect alleles**: The `slope` field is the effect of the alternative allele; positive = higher expression with alt allele

## Data Downloads (for large-scale analysis)

For genome-wide analyses, download full summary statistics rather than using the API:

```bash
# All significant eQTLs (v10)
wget https://storage.googleapis.com/adult-gtex/bulk-qtl/v10/single-tissue-cis-qtl/GTEx_Analysis_v10_eQTL.tar

# Normalized expression matrices
wget https://storage.googleapis.com/adult-gtex/bulk-gex/v10/rna-seq/GTEx_Analysis_v10_RNASeQCv2.4.2_gene_reads.gct.gz
```

## Additional Resources

- **GTEx Portal**: https://gtexportal.org/
- **API documentation**: https://gtexportal.org/api/v2/
- **Data downloads**: https://gtexportal.org/home/downloads/adult-gtex/
- **GitHub**: https://github.com/broadinstitute/gtex-pipeline
- **Citation**: GTEx Consortium (2020) Science. PMID: 32913098

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


This skill retrieves transcriptomics data (RNA expression baselines) and
expression Quantitative Trait Loci (eQTLs) from the GTEx Portal API V2. It
provides access to median TPM (Transcripts Per Million) values for genes and
significant eQTLs for variants across 54 human tissue sites.

## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://gtexportal.org/home/license and
    https://gtexportal.org/home/documentationPage#gtexApi, then (2) create the
    file recording the notification text and timestamp.

## When to Use

**Use this skill when you need to:**

-   Map a gene symbol to its Versioned GENCODE ID.
-   Retrieve the baseline median expression level (in TPM) of a gene across
    various tissues.
-   Find the top tissues where a particular gene is most highly expressed.
-   Fetch significant single-tissue eQTLs for a variant or within a chromosomal
    window.
-   Get all significant eQTLs associated with a specific gene.
-   Contextualise a variant within GWAS loci using eQTL data.

**Do NOT use when you need to:**

-   Query for protein-level expression or post-translational modifications
    (PTMs). GTEx only measures mRNA abundance.
-   Query gene expression in diseased tissues (e.g., tumor samples, cirrhosis).
    GTEx is a baseline atlas of normal, non-diseased tissues.
-   Query embryonic or fetal gene expression. GTEx donors are adults only.

## Core Rules

**CRITICAL**: You MUST respect GTEx Portal API Terms of Use.

-   **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
    database rather than accessing the database directly. The scripts
    automatically enforce the required rate limit gracefully.
-   Limit requests to maximum 250 items per page where applicable.
-   **Notification**: If this skill is used, ensure this is mentioned in the
    output.

## Command Selection Guide

**Pick the right command on the first try.** Match the user's input to the
correct subcommand below.

-   Map a gene symbol to GENCODE ID: `resolve-gencode-id`
-   Get median expression (TPM) for a gene: `get-median-expression`
-   Find tissues with highest expression for a gene: `get-top-expressed-tissues`
-   Get all eQTLs for a specific gene: `get-gene-eqtls`
-   Find eQTLs within a chromosomal region: `get-eqtls-in-region`

## Quick Start

```bash
# Map the TNF gene symbol to its GENCODE ID
uv run scripts/gtex_cli.py resolve-gencode-id TNF --output /tmp/tnf_id.json

# Get median expression of a gene by GENCODE ID
uv run scripts/gtex_cli.py get-median-expression ENSG00000232810.2 --output /tmp/tnf_expr.json
```

All subcommands write JSON to disk. Always save output in the `/tmp/` directory.
The default output file is `/tmp/gtex_output.json` if `--output` is not
specified.

## Commands

### 1. `resolve-gencode-id` — Gene Symbol → GENCODE ID

Maps a standard gene symbol (e.g., "JUN", "TNF") to its Versioned GENCODE ID.
This ID is required for all other expression and eQTL calls.

```bash
uv run scripts/gtex_cli.py resolve-gencode-id TNF --output /tmp/tnf_id.json
```

*Arguments:*

-   `gene_symbol` (positional): The standard gene symbol (e.g., "TNF").
-   `--output`: Output file path (default: `/tmp/gtex_output.json`).

### 2. `get-median-expression` — Get Median Expression (TPM)

Retrieves the median TPM for a gene across all 54 GTEx tissue sites or specified
tissues.

```bash
uv run scripts/gtex_cli.py get-median-expression ENSG00000232810.2 \
  --tissues "Whole Blood,Spleen" --output /tmp/expr.json
```

*Arguments:*

-   `gencode_id` (positional): The Versioned GENCODE ID.
-   `--tissues`: Comma-separated list of tissue IDs (optional, defaults to all
    54 tissues).
-   `--output`: Output file path (default: `/tmp/gtex_output.json`).

### 3. `get-top-expressed-tissues` — Get Top Expressed Tissues

Returns the `n` tissues with the highest median expression for the target gene.

```bash
uv run scripts/gtex_cli.py get-top-expressed-tissues ENSG00000232810.2 \
  --n 5 --output /tmp/top_tissues.json
```

*Arguments:*

-   `gencode_id` (positional): The Versioned GENCODE ID.
-   `--n`: Number of top tissues to return (default: 5).
-   `--output`: Output file path.

### 4. `get-gene-eqtls` — Get All eQTLs for a Gene

Returns every significant eQTL associated with the gene across specified
tissues.

```bash
uv run scripts/gtex_cli.py get-gene-eqtls ENSG00000232810.2 \
  --tissues "Whole Blood" --output /tmp/eqtls.json
```

*Arguments:*

-   `gencode_id` (positional): The Versioned GENCODE ID.
-   `--tissues`: Comma-separated list of tissue IDs (optional, defaults to all).
-   `--output`: Output file path.

### 5. `get-eqtls-in-region` — Get eQTLs in Chromosomal Region

Returns all significant single-tissue eQTLs within a chromosomal window (up to
8Mb).

```bash
uv run scripts/gtex_cli.py get-eqtls-in-region chr17 7000000 7100000 "Esophagus - Muscularis" \
  --output /tmp/region_eqtls.json
```

*Arguments:*

-   `chromosome` (positional): Chromosome name (e.g., `chr17`).
-   `start` (positional): Start position.
-   `end` (positional): End position (max 8Mb from start).
-   `tissue_id` (positional): The target tissue ID.
-   `--output`: Output file path.

## Typical Workflows

### Identify highest expressing tissues for a gene

```bash
# Step 1: Map symbol to GENCODE ID
uv run scripts/gtex_cli.py resolve-gencode-id GATA4 --output /tmp/gata4_id.json

# Step 2: Query for top tissues using the resolved ID
uv run scripts/gtex_cli.py get-top-expressed-tissues <gencode_id> --n 5 \
  --output /tmp/gata4_top.json
```
