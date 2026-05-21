---
name: uniprot-database
description: Access protein metadata, function, taxonomy, and sequences across UniProtKB, UniParc, and UniRef. Use when searching for proteins, mapping identifiers, or retrieving functional annotations and publications. Don't use for sequence alignment, protein folding, or sequence similarity search (use specialized skills for those tasks).
license: MIT
skill-author: AIPOCH
metadata:
    skill-author: K-Dense Inc.
---

## Overview

UniProt is a comprehensive protein sequence and functional information resource. This skill provides direct REST API access for searching proteins, retrieving sequences, and mapping identifiers.

## When to Use This Skill

- Searching for protein entries by name, gene symbol, accession, or organism.
- Retrieving protein sequences in FASTA or other formats.
- Mapping identifiers between UniProt and external databases (Ensembl, RefSeq, PDB, etc.).
- Accessing protein annotations including GO terms, domains, and functional descriptions.
- Building automated protein annotation retrieval pipelines in JSON/TSV/FASTA formats.
- When a lightweight client that directly interacts with UniProt's REST API is needed, without additional SDKs.

## Key Features

- **Protein search:** via UniProtKB REST endpoint using Lucene query syntax.
- **Entry retrieval:** by accession with selectable output formats.
- **Identifier mapping:** between supported source/target databases using UniProt ID mapping service.
- **Format control:** (default `json`) for consistent downstream parsing.
- **Streaming:** For large queries that exceed pagination limits.
- **Field customization:** Specify exactly which fields to retrieve for efficient data transfer.
- **Reference docs:** for query syntax and available API fields:
  - `references/query_syntax.md`
  - `references/api_fields.md`

## Dependencies

- Python `>=3.8`
- `requests >=2.31.0`

## Core Capabilities

### 1. Searching for Proteins

Search UniProt using natural language queries or structured search syntax.

**Common search patterns:**

```python
# Search by protein name
query = "insulin AND organism_name:\"Homo sapiens\""

# Search by gene name
query = "gene:BRCA1 AND reviewed:true"

# Search by accession
query = "accession:P12345"

# Search by sequence length
query = "length:[100 TO 500]"

# Search by taxonomy
query = "taxonomy_id:9606"  # Human proteins

# Search by GO term
query = "go:0005515"  # Protein binding
```

Use the API search endpoint: `https://rest.uniprot.org/uniprotkb/search?query={query}&format={format}`

**Supported formats:** JSON, TSV, Excel, XML, FASTA, RDF, TXT

### 2. Retrieving Individual Protein Entries

Retrieve specific protein entries by accession number.

**Accession number formats:**
- Classic: P12345, Q1AAA9, O15530 (6 characters: letter + 5 alphanumeric)
- Extended: A0A022YWF9 (10 characters for newer entries)

**Retrieve endpoint:** `https://rest.uniprot.org/uniprotkb/{accession}.{format}`

Example: `https://rest.uniprot.org/uniprotkb/P12345.fasta`

### 3. Batch Retrieval and ID Mapping

Map protein identifiers between different
