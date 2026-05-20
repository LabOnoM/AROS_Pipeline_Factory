---
name: hmdb-database
description: Access the Human Metabolome Database (HMDB) to search metabolites by name/structure/ID and extract chemical/biological/clinical fields for metabolomics research and automated HMDB XML mining.
license: MIT
metadata:
    skill-author: AIPOCH & K-Dense Inc.
---
---

## Overview

The Human Metabolome Database (HMDB) is a comprehensive, freely available resource containing detailed information about small molecule metabolites found in the human body. This skill provides access to HMDB data, enabling metabolite searches, data extraction, and integration into analysis pipelines.

## When to Use This Skill

- You need to look up a metabolite by **common name** (e.g., “Caffeine”) and retrieve its HMDB entry data.
- You have an **HMDB ID** (e.g., `HMDB0000001`) and want to extract standardized chemical/biological/clinical fields for downstream analysis.
- You want to build a **local, scriptable pipeline** to mine the HMDB XML dump instead of manually browsing the website.
- You need to **map HMDB identifiers** to external resources (e.g., KEGG, PubChem, ChEBI) for integration tasks.
- You are preparing metabolomics datasets and need **pathway/enzyme/transporter** annotations from HMDB entries.
- You are performing metabolomics research, clinical chemistry, biomarker discovery, or metabolite identification tasks.

## Key Features

- Search metabolites by:
  - Text name (common name, synonym)
  - HMDB identifier (e.g., `HMDB0000001`)
  - Structure-related query (SMILES/InChI, if supported by the parser implementation)
- Parse the HMDB XML dataset and extract:
  - **Chemical data:** formula, molecular weight, InChI/SMILES
  - **Biological data:** pathways, enzymes, transporters, subcellular locations
  - **Clinical data:** disease associations, biofluid concentrations, biomarker associations
- Supports integration workflows by exposing identifiers suitable for cross-database mapping (KEGG, PubChem, ChEBI).

## Database Contents

HMDB version 5.0 (current as of 2025) typically contains:

- **220,000+ metabolite entries** covering both water-soluble and lipid-soluble compounds
- **8,000+ protein sequences** for enzymes and transporters involved in metabolism
- **130+ data fields per metabolite** including:
  - Chemical properties (structure, formula, molecular weight, InChI, SMILES)
  - Clinical data (biomarker associations, diseases, normal/abnormal concentrations)
  - Biological information (pathways, reactions, locations)
  - Spectroscopic data (NMR, MS, MS-MS spectra - availability may vary)
  - External database links (KEGG, PubChem, MetaCyc, ChEBI, PDB, UniProt, GenBank)

## Example Usage

### 1) Download HMDB XML

Download the HMDB metabolite XML dataset from:
- https://hmdb.ca/downloads

Assume you saved it as:

```text
data/hmdb_metabolites.xml
```

### 2) Search and Extract Fields (Runnable Example)

```python
from scripts.hmdb_parser import HMDBParser

def main():
    # Path to the HMDB XML dump downloaded from hmdb.ca/downloads
    xml_path = "data/hmdb_metabolites.xml"

    parser = HMDBParser(xml_path)

    # Search by metabolite name (text query)
    results = parser.search("Caffeine")

    # Print basic information from the first match (structure depends on implementation)
    if not results:
        print("No results found.")
        return

    first = results[0]
    print("Top match:")
    print(first)

if __name__ == "__main__":
    main()
```

## Implementation Details

- **Data Acquisition:**
  - Primary workflow utilizes the official HMDB downloadable XML dataset (recommended for bulk parsing).
  - Single-entry lookups can be done via the HMDB website, but this skill is designed around XML parsing.

- **Parsing Approach:**
  - The parser reads the HMDB XML and traverses metabolite entries using `xml.etree.ElementTree` (or a similar XML parsing library).
  - Extracted fields should follow the definitions documented in `references/hmdb_data_fields.md`.

- **Search Behavior:**
  - Name/ID search typically matches against key textual identifiers (e.g., common name, synonyms, HMDB accession).
  - Structure-based search is dependent on what structural fields are indexed/exposed by `HMDBParser` (e.g., SMILES/InChI).

- **Integration / Cross-references:**
  - HMDB entries often include cross-references to external databases (e.g., KEGG, PubChem, ChEBI).
  - A common workflow is to extract these identifiers and build mapping tables for downstream joins.

- **Spectral Analysis (Conceptual):**
  - HMDB contains NMR/MS references for some metabolites; this skill can be extended to link parsed entries to spectral metadata.
  - Actual spectral matching/identification is not guaranteed unless implemented in the codebase.

## Dependencies

- Python `>=3.9`
- Standard library:
  - `xml.etree.ElementTree` (built-in)
- Optional:
  - `pandas >= 1.5` (for tabular data handling)

## Best Practices

- **Data Quality:** Verify metabolite identifications with multiple evidence types (spectra, structure, properties).
- **Version Tracking:** Note HMDB version used in research (current: v5.0). Databases are updated periodically; re-query for updates when publishing.
- **Citation:** Always cite HMDB in publications using the database. Reference specific HMDB IDs when discussing metabolites.
- **Performance:** For large-scale analysis, download complete datasets rather than repeated web queries.

## Reference Documentation

See `references/hmdb_data_fields.md` for a curated list of extractable fields, their mappings to HMDB XML elements, and their meanings.