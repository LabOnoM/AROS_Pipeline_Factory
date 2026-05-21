---
name: clinvar-database
description: Query NCBI ClinVar for variant clinical significance, pathogenicity classifications (e.g., Pathogenic, Benign, VUS), and phenotype relationships. Use to search by gene/condition/significance, interpret classifications, annotate VCFs, access via API or FTP, and find clinical evidence rationales or "hard positive" benchmark controls for human genomic variants.
license: MIT
metadata:
    skill-author: K-Dense Inc. and AIPOCH
---

## Overview

ClinVar is NCBI's freely accessible archive of reports on relationships between human genetic variants and phenotypes, with supporting evidence. The database aggregates information about genomic variation and its relationship to human health, providing standardized variant classifications used in clinical genetics and research.

## When to Use This Skill

This skill should be used when:

- Searching for variants by gene, condition, or clinical significance.
- Interpreting clinical significance classifications (pathogenic, benign, VUS).
- Accessing ClinVar data programmatically via E-utilities API.
- Downloading and processing bulk data from FTP.
- Understanding review status and star ratings.
- Resolving conflicting variant interpretations.
- Annotating variant call sets with clinical significance.
- Performing bulk retrieval of ClinVar datasets for offline analysis or periodic database refresh.

## Core Capabilities

### 1. Search and Query ClinVar

#### Web Interface Queries

Search ClinVar using the web interface at https://www.ncbi.nlm.nih.gov/clinvar/

**Common search patterns:**
- By gene: `BRCA1[gene]`
- By clinical significance: `pathogenic[CLNSIG]`
- By condition: `breast cancer[disorder]`
- By variant: `NM_000059.3:c.1310_1313del[variant name]`
- By chromosome: `13[chr]`
- Combined: `BRCA1[gene] AND pathogenic[CLNSIG]`

#### Programmatic Access via E-utilities

Access ClinVar programmatically using NCBI's E-utilities API. Refer to `references/api_reference.md` for comprehensive API documentation including:
- **esearch** - Search for variants matching criteria
- **esummary** - Retrieve variant summaries
- **efetch** - Download full XML records
- **elink** - Find related records in other NCBI databases

**Quick example using curl:**
```bash
# Search for pathogenic BRCA1 variants
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BRCA1[gene]+AND+pathogenic[CLNSIG]&retmode=json"
```

**Best practices:**
- Test queries on the web interface before automating.
- Use API keys to increase rate limits from 3 to 10 requests/second.
- Implement exponential backoff for rate limit errors.
- Set `Entrez.email` when using Biopython.

### 2. Interpret Clinical Significance

#### Understanding Classifications

ClinVar uses standardized terminology for variant classifications. Refer to `references/clinical_significance.md` for detailed interpretation guidelines.

**Key germline classification terms (ACMG/AMP):**
- **Pathogenic (P)** - Variant causes disease (~99% probability)
- **Likely Pathogenic (LP)** - Variant likely causes disease (~90% probability)
- **Uncertain Significance (VUS)** - Insuffici