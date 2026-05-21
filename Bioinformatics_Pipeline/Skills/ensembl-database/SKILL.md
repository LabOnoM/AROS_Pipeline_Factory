---
name: ensembl-database
description: Query the Ensembl database to resolve gene, transcript, and protein IDs,
  fetch genomic or protein sequences, retrieve gene structures (exons), and get variant
  consequence and effect predictions (VEP). Use this skill as a primary ID translator,
  genomic sequence database and variant effect prediction tool.
license: MIT
metadata:
  skill-author: AIPOCH + K-Dense Inc.
---
# Ensembl Database Skill

## Overview

Access and query the Ensembl genome database, a comprehensive resource for vertebrate genomic data maintained by EMBL-EBI. The database provides gene annotations, sequences, variants, regulatory information, and comparative genomics data for over 250 species. Current release is 115 (September 2025).

## When to Use This Skill

- Use this skill when you need access to the Ensembl REST API for vertebrate genomic data for gene/ID lookups, sequence retrieval, variant effect prediction (VEP), or homology/assembly coordinate mapping in a reproducible workflow.
- Use this skill when an evidence insight task needs a packaged method instead of ad-hoc freeform output.
- Use this skill when the user expects a concrete deliverable or file-based result.
- Use this skill when `scripts/query_ensembl.py` is the most direct path to complete the request.
- Use this skill when you need the `ensembl-database` package behavior rather than a generic answer.
- **Gene-centric queries**: When you need to resolve a gene symbol or region to Ensembl identifiers and basic annotations (e.g., `BRCA2` in human).
- **Sequence extraction**: When you need DNA/cDNA/protein sequences for a known Ensembl gene/transcript/protein ID in FASTA or JSON.
- **Variant interpretation**: When you need to predict functional consequences of variants using **VEP** from HGVS notation.
- **Comparative genomics**: When you need ortholog/paralog relationships across vertebrate species.
- **Assembly/coordinate mapping**: When you need to map coordinates between assemblies (e.g., GRCh37 ↔ GRCh38).

## Key Features

- Scope-focused workflow aligned to: Access Ensembl REST API for vertebrate genomic data; use when you need gene/ID lookups, sequence retrieval, variant effect prediction (VEP), or homology/assembly coordinate mapping.
- Packaged executable path(s): `scripts/query_ensembl.py`.
- Reference material available in `references/` for task-specific guidance.
- Structured execution path designed to keep outputs consistent and reviewable.
- Query Ensembl REST endpoints for:
    - **Gene lookup** by symbol, Ensembl ID, or genomic region
    - **Sequence retrieval** (DNA, cDNA, protein) in FASTA/JSON
    - **Variant Effect Predictor (VEP)** analysis from HGVS inputs
    - **Homology** retrieval (orthologs/paralogs)
    - **Assembly/coordinate mapping** between common human assemblies
- CLI helper script for repeatable queries:
    - `scripts/query_ensembl.py` (wrapper around an `ensembl_rest` client)
- Reference documentation for endpoints:
    - `references/api_endpoints.md`
    - Ensembl REST base URL: https://rest.ensembl.org

## Dependencies

- `Python`: `3.8+`. Repository baseline
