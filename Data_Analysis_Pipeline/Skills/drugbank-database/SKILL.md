---
name: drugbank-database
description: Access and analyze drug data from the DrugBank database, including properties, interactions, targets, pathways, and pharmacology. Use for pharmaceutical data analysis, drug discovery, and pharmacology studies.
license: MIT
metadata:
    skill-author: K-Dense Inc. & AIPOCH
---

# DrugBank Database

## Overview

DrugBank is a comprehensive bioinformatics and cheminformatics database containing detailed information on drugs and drug targets. This skill enables programmatic access to DrugBank data.

## When to Use

- Extract structured drug properties (identifiers, synonyms, ATC codes) from DrugBank XML.
- Build and analyze drug-drug interaction (DDI) networks.
- Map drugs to targets (proteins/genes) for target discovery and mechanism-of-action analysis.
- Connect drugs to pathways and pharmacology annotations.
- Generate tabular datasets (CSV/Parquet) from DrugBank.
- Drug discovery research.
- Pharmacology studies.
- Drug-drug interaction analysis.
- Target identification.
- Chemical similarity searches.
- ADMET predictions.

## Core Capabilities

### 1. Data Access and Authentication

Download and access DrugBank data using Python.

- Install and configure the `drugbank-downloader` package.
- Manage credentials securely (environment variables or config files).
- Download specific or latest database versions.
- Open and parse XML data efficiently using `lxml`.
- Work with cached data to optimize performance.

**When to use**: Setting up DrugBank access, downloading database updates, initial project configuration.

### 2. Drug Information Queries

Extract comprehensive drug information from the database.

- Search by DrugBank ID, name, CAS number, or keywords.
- Extract basic drug information (name, type, description, indication).
- Retrieve chemical properties (SMILES, InChI, molecular formula).
- Get pharmacology data (mechanism of action, pharmacodynamics, ADME).
- Access external identifiers (PubChem, ChEMBL, UniProt, KEGG).
- Build searchable drug datasets and export to DataFrames.
- Filter drugs by type (small molecule, biotech, nutraceutical).

**When to use**: Retrieving specific drug information, building drug databases, pharmacology research, literature review, drug profiling.

### 3. Drug-Drug Interactions Analysis

Analyze drug-drug interactions (DDIs).

- Extract all interactions for specific drugs.
- Build bidirectional interaction networks.
- Classify interactions by severity and mechanism.
- Check interactions between drug pairs.
- Identify drugs with most interactions.
- Analyze polypharmacy regimens for safety.
- Create interaction matrices and network graphs.
- Perform community detection in interaction networks.
- Calculate interaction risk scores.

**When to use**: Polypharmacy safety analysis, clinical decision support, drug interaction prediction, pharmacovigilance research, identifying contraindications.

### 4. Drug Targets and Pathways

Access detailed information about drug-protein interactions.

- Extract drug targets with actions (inhibitor, agonist, antagonist).
- Identify metabolic enzymes (CYP450, Phase II enzymes).
- Analyze transporters (uptake, efflux) for ADME studies.
- Map drugs to biological pathways (SMPDB).
- Find drugs targeting specific proteins.
- Identify drugs with shared targets for repurposing.
- Analyze polypharmacology and off-target effects.
- Extract Gene Ontology (GO) terms for targets.
- Cross-reference with UniProt for protein data.

**When to use**: Mechanism of action studies, drug repurposing research, target identification, pathway analysis, predicting off-target effects, understanding drug metabolism.

### 5. Chemical Properties and Similarity

Perform structure-based analysis.

- Extract chemical structures (SMILES, InChI, molecular formula).
- Calculate physicochemical properties (MW, logP, PSA, H-bonds).
- Apply Lipinski's Rule of Five and Veber's rules.
- Calculate Tanimoto similarity between molecules.
- Generate molecular fingerprints (Morgan, MACCS, topological).
- Perform substructure searches with SMARTS patterns.
- Find structurally similar drugs for repurposing.
- Create similarity matrices for drug clustering.
- Predict oral absorption and BBB permeability.
- Analyze chemical space with PCA and clustering.
- Export chemical property databases.

**When to use**: Structure-activity relationship (SAR) studies, drug similarity searches, QSAR modeling, drug-likeness assessment, ADMET prediction, chemical space exploration.

## Example Usage

```python
"""
End-to-end example:
1) Parse a local DrugBank XML file
2) Extract a minimal drug table
3) Extract drug-drug interactions
4) Build a DDI graph

Prerequisites:
- Obtain DrugBank XML via your DrugBank account/license.
- Place the XML file at ./drugbank.xml (or update the path).
"""

from lxml import etree
import pandas as pd
import networkx as nx

DRUGBANK_XML_PATH = "./drugbank.xml"
NS = {"db": "http://www.drugbank.ca"}  # DrugBank XML namespace

# --- Parse XML ---
tree = etree.parse(DRUGBANK_XML_PATH)
root = tree.getroot()

# --- Extract drug records (minimal fields) ---
drugs = []
for drug in root.xpath("//db:drug", namespaces=NS):
    drugbank_id = drug.xpath("string(db:drugbank-id[@primary='true'])", namespaces=NS).strip()
    name = drug.xpath("string(db:name)", namespaces=NS).strip()
    drug_type = drug.get("type", "").strip()

    # Optional: first SMILES if present
    smiles = drug.xpath(
        "string(db:calculated-properties/db:property[db:kind='SMILES']/db:value)",
        namespaces=NS,
    ).strip()

    drugs.append(
        {
            "drugbank_id": drugbank_id,
            "name": name,
            "type": drug_type,
            "smiles": smiles or None,
        }
    )

drugs_df = pd.DataFrame(drugs).dropna(subset=["drugbank_id"])
print("Drugs:", len(drugs_df))
print(drugs_df.head())

# --- Extract drug-drug interactions ---
interactions = []
for drug in root.xpath("//db:drug", namespaces=NS):
    src_id = drug.xpath("string(db:drugbank-id[@primary='true'])", namespaces=NS).strip()
    src_name = drug.xpath("string(db:name)", namespaces=NS).strip()

    for ddi in drug.xpath("db:drug-interactions/db:drug-interaction", namespaces=NS):
        tgt_id = ddi.xpath("string(db:drugbank-id)", namespaces=NS).strip()
        tgt_name = ddi.xpath("string(db:name)", namespaces=NS).strip()
        description = ddi.xpath("string(db:description)", namespaces=NS).strip()

        if src_id and tgt_id:
            interactions.append(
                {
                    "source_id": src_id,
                    "source_name": src_name,
                    "target_id": tgt_id,
                    "target_name": tgt_name,
                    "description": description or None,
                }
            )

ddi_df = pd.DataFrame(interactions)
print("Interactions:", len(ddi_df))
print(ddi_df.head())

# --- Build a DDI graph ---
G = nx.from_pandas_edgelist(
    ddi_df,
    source="source_id",
    target="target_id",
    edge_attr=["description"],
    create_using=nx.Graph(),
)

print("DDI graph nodes:", G.number_of_nodes())
print("DDI graph edges:", G.number_of_edges())

# Example analysis: top 10 drugs by interaction degree
top_degree = sorted(G.degree, key=lambda x: x[1], reverse=True)[:10]
top_degree_df = pd.DataFrame(top_degree, columns=["drugbank_id", "degree"]).merge(
    drugs_df[["drugbank_id", "name"]],
    on="drugbank_id",
    how="left",
)
print(top_degree_df)
```

## Implementation Details

- **Access & Authentication**: DrugBank data access requires a free academic account or a paid license. The `drugbank-downloader` step is responsible for fetching the release artifacts; comply with DrugBank terms.
- **XML Parsing**: DrugBank is distributed as a large XML document; `lxml.etree` is used for robust XPath-based extraction.  The XML uses a namespace (commonly `http://www.drugbank.ca`); XPath queries must include the namespace mapping (e.g., `NS = {"db": "http://www.drugbank.ca"}`).
- **Core Extraction Patterns**:
    - **Primary DrugBank ID**: `db:drugbank-id[@primary='true']`
    - **Drug name**: `db:name`
    - **Calculated properties (e.g., SMILES)**: `db:calculated-properties/db:property[db:kind='SMILES']/db:value`
    - **Drug interactions**: `db:drug-interactions/db:drug-interaction` with fields `db:drugbank-id`, `db:name`, `db:description`
- **Data Modeling**: Use `pandas` DataFrames for normalized tables (drugs, targets, interactions, pathways). Use `networkx` for graph representations.
    - DDI graph: nodes are drugs, edges are interactions (store `description` as edge attribute).
    - Drug–target graph: bipartite graph with drug nodes and target nodes.
- **Performance**: For memory-sensitive environments, consider iterative parsing (`etree.iterparse`) and writing intermediate results to disk. Normalize identifiers early (e.g., always keep primary DrugBank IDs) to simplify joins across tables.
- **Reproducibility**: Always specify the DrugBank version for reproducible research.

## Dependencies

- `drugbank-downloader` (version varies by your environment)
- `lxml>=4.9`
- `pandas>=2.0`
- `networkx>=3.0`
- `rdkit>=2022.09` (optional; required only for structure/chemistry workflows)

## Installation

```bash
uv pip install drugbank-downloader
uv pip install lxml>=4.9
uv pip install pandas>=2.0
uv pip install networkx>=3.0
uv pip install rdkit>=2022.09  # Optional
```

## Best Practices

1. **Credentials**: Use environment variables or config files, never hardcode.
2. **Versioning**: Specify exact database version for reproducibility.
3. **Caching**: Cache parsed data to avoid re-downloading and re-parsing.
4. **Namespaces**: Handle XML namespaces properly when parsing.
5. **Validation**: Validate chemical structures with RDKit before use.
6. **Cross-referencing**: Use external identifiers (UniProt, PubChem) for integration.
7. **Clinical Context**: Always consider clinical context when interpreting interaction data.
8. **License Compliance**: Ensure proper licensing for your use case.

## Reference Documentation

- **references/data-access.md**: Authentication, download, parsing, API access, caching
- **references/drug-queries.md**: XML navigation, query methods, data extraction, indexing
- **references/interactions.md**: DDI extraction, classification, network analysis, safety scoring
- **references/targets-pathways.md**: Target/enzyme/transporter extraction, pathway mapping, repurposing
- **references/chemical-analysis.md**: Structure extraction, similarity, fingerprints, ADMET prediction