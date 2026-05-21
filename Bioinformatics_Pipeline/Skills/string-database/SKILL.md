---
name: string-database
description: Query the STRING database for protein-protein interactions (PPIs), functional
  enrichment, and homology. Use when the user asks about interactions between specific
  proteins, interaction evidence, confidence scores, protein interaction partners,
  or pathway enrichments.
---

description: Generated skill string-database

---
name: string-database
description: Query the STRING API for protein-protein interactions (59M proteins, 20B+ interactions, 5000+ species). Perform network analysis, functional enrichment, and interaction discovery.
license: MIT
metadata:
    skill-author: K-Dense Inc. & AIPOCH
---

# STRING Database

## Overview

STRING is a comprehensive database of known and predicted protein-protein interactions, covering 59M proteins and 20B+ interactions across 5000+ organisms.  It facilitates querying interaction networks, performing functional enrichment, and discovering interaction partners via a REST API for systems biology and pathway analysis.

## When to Use This Skill

This skill should be used when:

-   Resolving gene symbols to STRING protein identifiers.
-   Retrieving protein-protein interaction (PPI) networks (functional or physical) with confidence scores.
-   Finding interaction partners for a target protein to expand candidate lists.
-   Performing functional enrichment analysis (GO, KEGG, Reactome, etc.) for a protein set.
-   Testing if proteins form significantly enriched functional modules
-   Generating network visualizations.
-   Analyzing homology and protein family relationships
-   Conducting cross-species protein interaction comparisons
-   Identifying hub proteins and network connectivity patterns

## Key Features

-   **ID Mapping**: Convert gene/protein names to STRING identifiers for a given organism.
-   **Network Retrieval**: Fetch interaction edges with confidence scores from STRING.
-   **Interaction Partners**: Expand a protein list by retrieving interaction partners.
-   **Enrichment Analysis**:
    -   Functional enrichment (e.g., GO, KEGG, Reactome)
    -   PPI enrichment statistics
    -   Functional annotations (e.g., PFAM/SMART where supported by STRING endpoints)
-   **Visualization**: Download static network images (PNG).

## Dependencies

-   Python `>=3.8`
-   `requests`
-   `pandas`

Install:

```bash
pip install requests pandas
```

## Quick Start

The skill provides:

1.  Python helper functions (`scripts/string_api.py`) for all STRING REST API operations, encapsulated in a `StringClient` class.
2.  Comprehensive reference documentation (`references/string_reference.md`) with detailed API specifications.

When users request STRING data, determine which operation is needed and use the appropriate method from the `StringClient` in `scripts/string_api.py`.

## Core Operations

### 1. Identifier Mapping (`string_map_ids`)

Convert gene names, protein names, and external IDs to STRING identifiers.

**When to use**: Starting any STRING analysis, validating protein names, finding canonical identifiers.

**Usage**:

```python
from scripts.string_api import StringClient

client = StringClient(caller_identity="my_analysis_tool")

# Map single protein
result = client.map_id(identifier='TP53', species=9606)

# Map multiple proteins
result = client.map_ids(identifiers=['TP53', 'BRCA1'], species=9606)
```