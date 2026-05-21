---
name: opentargets-database
description: Query Open Targets Platform for target-disease associations, drug target discovery, tractability/safety data, genetics/omics evidence, known drugs, for therapeutic target identification.
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Open Targets Database

## Overview

The Open Targets Platform is a comprehensive resource for systematic identification and prioritization of potential therapeutic drug targets. It integrates publicly available datasets including human genetics, omics, literature, and chemical data to build and score target-disease associations.

**Key capabilities:**
- Query target (gene) annotations including tractability, safety, expression
- Search for disease-target associations with evidence scores
- Retrieve evidence from multiple data types (genetics, pathways, literature, etc.)
- Find known drugs for diseases and their mechanisms
- Access drug information including clinical trial phases and adverse events
- Evaluate target druggability and therapeutic potential

**Data access:** The platform provides a GraphQL API, web interface, data downloads, and Google BigQuery access. This skill focuses on the GraphQL API for programmatic access.

## When to Use This Skill

This skill should be used when:

- **Target discovery:** Finding potential therapeutic targets for a disease
- **Target assessment:** Evaluating tractability, safety, and druggability of genes
- **Evidence gathering:** Retrieving supporting evidence for target-disease associations
- **Drug repurposing:** Identifying existing drugs that could be repurposed for new indications
- **Competitive intelligence:** Understanding clinical precedence and drug development landscape
- **Target prioritization:** Ranking targets based on genetic evidence and other data types
- **Mechanism research:** Investigating biological pathways and gene functions
- **Biomarker discovery:** Finding genes differentially expressed in disease
- **Safety assessment:** Identifying potential toxicity concerns for drug targets

## Core Workflow

### 1. Search for Entities

Start by finding the identifiers for targets, diseases, or drugs of interest.

**For targets (genes):**
```python
from scripts.query_opentargets import search_entities

# Search by gene symbol or name
results = search_entities("BRCA1", entity_types=["target"])
# Returns: [{"id": "ENSG00000012048", "name": "BRCA1", ...}]
```

**For diseases:**
```python
# Search by disease name
results = search_entities("alzheimer", entity_types=["disease"])
# Returns: [{"id": "EFO_0000249", "name": "Alzheimer disease", ...}]
```

**For drugs:**
```python
# Search by drug name
results = search_entities("aspirin", entity_types=["drug"])
# Returns: [{"id": "CHEMBL25", "name": "ASPIRIN", ...}]
```

**Identifiers used:**
- Targets: Ensembl gene IDs (e.g., `ENSG00000157764`)
- Diseases: EFO (Experimental Factor Ontology) IDs (e.g., `EFO_0000249`)
- Drugs: ChEMBL IDs (e.g., `CHEMBL25`)

### 2.