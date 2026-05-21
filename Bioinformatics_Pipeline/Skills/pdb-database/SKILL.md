---
name: pdb-database
description: Access the RCSB Protein Data Bank (PDB) to search, download, and programmatically retrieve 3D macromolecular structures and metadata for structure discovery (text/sequence/3D similarity) and automated structural data ingestion in structural biology and drug discovery workflows.
license: MIT
metadata:
    skill-author: AIPOCH
---

## Overview

The RCSB PDB is the worldwide repository for 3D structural data of biological macromolecules. Use this skill to search, retrieve coordinates and metadata, and perform similarity searches.

## When to Use

Use this skill when you need to:

- Find protein/nucleic acid 3D structures by **keywords**, **organism**, **experimental method**, or **resolution**.
- Identify related structures via **sequence similarity**.
- Identify related structures via **3D structure similarity**.
- **Download coordinates** (PDB/mmCIF) for downstream analysis.
- Run **batch retrieval** of metadata/coordinates for pipelines in drug discovery, protein engineering, or structural bioinformatics.

## Key Features

- Text and attribute-based search over RCSB PDB entries.
- Sequence similarity search with configurable thresholds (e-value, identity).
- Structure similarity search using an existing entry as a query.
- Metadata retrieval via the RCSB Data API (schema-based or GraphQL).
- Coordinate downloads in **PDB** and **mmCIF** formats.
- Batch processing patterns for multiple PDB IDs.

## Dependencies

- `rcsb-api` (latest recommended; provides `rcsbapi.search` and `rcsbapi.data`)
- `requests>=2.0` (HTTP downloads)
- `biopython>=1.80` (optional; parsing/analyzing PDB coordinates)

Install (example):

```bash
uv pip install rcsb-api requests biopython
```

## Core Capabilities

### 1. Searching for Structures

Find PDB entries using various search criteria:

**Text Search:** Search by protein name, keywords, or descriptions
```python
from rcsbapi.search import TextQuery
query = TextQuery("hemoglobin")
results = list(query())
print(f"Found {len(results)} structures")
```

**Attribute Search:** Query specific properties (organism, resolution, method, etc.)
```python
from rcsbapi.search import AttributeQuery
from rcsbapi.search.attrs import rcsb_entity_source_organism, rcsb_entry_info

# Find human protein structures
query = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
results = list(query())

# Find high-resolution structures
query = AttributeQuery(
    attribute=rcsb_entry_info.resolution_combined,
    operator="less",
    value=2.0
)
results = list(query())
```

**Sequence Similarity:** Find structures similar to a given sequence
```python
from rcsbapi.search import SequenceQuery

query = SequenceQuery(
    value="MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHHYREQIKRVKDSEDVPMVLVGNKCDLPSRTVDTKQAQDLARSYGIPFIETSAKTRQGVDDAFYTLVREIRKHKEKMSKDGKKKKKKSKTKCVIM",
    evalue_cutoff=0.1,
    identity_cutoff=0.9
)
results = list(query())
```

**Structure Similarity:** Find structures with similar 3D geometry
```python
from rcsbapi.search import StructSimilarityQuery

query = StructSimilarityQuery(
    structure_search_type="entry",
    entry_id="4HHB"  # Hemoglobin
)
results = list(query())
```

**Combining Queries:** Use logical operators to build complex searches
```python
from rcsbapi.search import TextQuery, AttributeQuery
from rcsbapi.search.attrs import rcsb_entity_source_organism, rcsb_entry_info

# High-resolution human proteins
query1 = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
query2 = AttributeQuery(
    attribute=rcsb_entry_info.resolution_combined,
    operator="less",
    value=2.0
)
combined_query = query1 & query2  # AND operation
results = list(combined_query())
```

### 2. Retrieving Structure Data

Access detailed information about specific PDB entries:

**Schema-based fetch:**
```python
from rcsbapi.data import Schema, fetch

# Get entry-level data
entry_data = fetch("4HHB", schema=Schema.ENTRY)
print(entry_data["struct"]["title"])
print(entry_data["exptl"][0]["method"])
```

**Polymer Entity Information:**
```python
# Get protein/nucleic acid information
entity_data = fetch("4HHB_1", schema=Schema.POLYMER_ENTITY)
print(entity_data["entity_poly"]["pdbx_seq_one_letter_code"])
```

**Using GraphQL:**
```python
from rcsbapi.data import fetch

query = """
{
  entry(entry_id: "4HHB") {
    struct {
      title
    }
    exptl {
      method
    }
    rcsb_entry_info {
      resolution_combined
      deposited_atom_count
    }
  }
}
"""
data = fetch(query_type="graphql", query=query)
```

### 3. Downloading Structure Files

Retrieve coordinate files in various formats:

```python
import requests

pdb_id = "4HHB"

# Download PDB format
pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
response = requests.get(pdb_url)
with open(f"{pdb_id}.pdb", "w") as f:
    f.write(response.text)

# Download mmCIF format
cif_url = f"https://files.rcsb.org/download/{pdb_id}.cif"
response = requests.get(cif_url)
with open(f"{pdb_id}.cif", "w") as f:
    f.write(response.text)
```

### 4. Working with Structure Data

```python
from Bio.PDB import PDBParser

parser = PDBParser()
structure = parser.get_structure("protein", "4HHB.pdb")

# Iterate through atoms
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                print(atom.get_coord())
```

### 5. Batch Operations

Process multiple structures efficiently:

```python
from rcsbapi.data import fetch, Schema

pdb_ids = ["4HHB", "1MBN", "1GZX"]  # Hemoglobin, myoglobin, etc.

results = {}
for pdb_id in pdb_ids:
    try:
        data = fetch(pdb_id, schema=Schema.ENTRY)
        results[pdb_id] = {
            "title": data["struct"]["title"],
            "resolution": data.get("rcsb_entry_info", {}).get("resolution_combined"),
            "organism": data.get("rcsb_entity_source_organism", [{}])[0].get("scientific_name")
        }
    except Exception as e:
        print(f"Error fetching {pdb_id}: {e}")

# Display results
for pdb_id, info in results.items():
    print(f"\n{pdb_id}: {info['title']}")
    print(f"  Resolution: {info['resolution']} Å")
    print(f"  Organism: {info['organism']}")
```

## Example Usage

The following script is end-to-end runnable: it searches for a target, fetches metadata, downloads coordinates, and parses the structure.

```python
#!/usr/bin/env python3
import pathlib
import requests

from rcsbapi.search import TextQuery, AttributeQuery
from rcsbapi.search.attrs import rcsb_entry_info
from rcsbapi.data import fetch, Schema

from Bio.PDB import PDBParser


def download_text(url: str, out_path: pathlib.Path) -> None:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    out_path.write_text(r.text, encoding="utf-8")


def main():
    out_dir = pathlib.Path("pdb_out")
    out_dir.mkdir(exist_ok=True)

    # 1) Search: hemoglobin entries with resolution < 2.0 Å
    q_text = TextQuery("hemoglobin")
    q_res = AttributeQuery(
        attribute=rcsb_entry_info.resolution_combined,
        operator="less",
        value=2.0,
    )
    query = q_text & q_res

    pdb_ids = list(query())[:5]
    if not pdb_ids:
        raise SystemExit("No results found.")
    pdb_id = pdb_ids[0]
    print(f"Selected PDB ID: {pdb_id}")

    # 2) Fetch entry metadata
    entry = fetch(pdb_id, schema=Schema.ENTRY)
    title = entry.get("struct", {}).get("title")
    method = (entry.get("exptl") or [{}])[0].get("method")
    resolution = (entry.get("rcsb_entry_info") or {}).get("resolution_combined")
    deposit_date = (entry.get("rcsb_accession_info") or {}).get("deposit_date")

    print("Metadata:")
    print(f"  Title: {title}")
    print(f"  Method: {method}")
    print(f"  Resolution: {resolution}")
    print(f"  Deposit date: {deposit_date}")

    # 3) Download coordinates (PDB and mmCIF)
    pdb_path = out_dir / f"{pdb_id}.pdb"
    cif_path = out_dir / f"{pdb_id}.cif"

    download_text(f"https://files.rcsb.org/download/{pdb_id}.pdb", pdb_path)
    download_text(f"https://files.rcsb.org/download/{pdb_id}.cif", cif_path)
    print(f"Downloaded: {pdb_path} and {cif_path}")

    # 4) Parse PDB coordinates (example: count atoms)
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(pdb_id, str(pdb_path))

    atom_count = sum(1 for _ in structure.get_atoms())
    chain_ids = sorted({chain.id for chain in structure.get_chains()})
    print("Parsed structure:")
    print(f"  Chains: {chain_ids}")
    print(f"  Atom count: {atom_count}")


if __name__ == "__main__":
    main()
```

## Implementation Details

### Search Modes and Query Composition

- **Text search** uses free-text matching over entry annotations.
- **Attribute search** filters by structured fields.
- **Sequence similarity search** typically supports `evalue_cutoff` (lower is more stringent) and `identity_cutoff`.
- **Structure similarity search** uses an existing structure (e.g., an `entry_id`) as the geometric reference.
- Queries can be combined with boolean logic: `query1 & query2` (AND), `query1 | query2` (OR), and `~query` (NOT).

### Data Retrieval (Schema vs GraphQL)

- **Schema-based fetch** is convenient for common objects and stable access patterns.
- **GraphQL fetch** is best when you need a custom selection of fields in one request.

Example GraphQL pattern:

```python
from rcsbapi.data import fetch

query = """
{
  entry(entry_id: "4HHB") {
    struct { title }
    exptl { method }
    rcsb_entry_info { resolution_combined deposited_atom_count }
  }
}
"""
data = fetch(query_type="graphql", query=query)
```

### Coordinate Downloads and Formats

- **PDB**: legacy text format.
- **mmCIF (PDBx)**: modern standard; preferred for completeness and large structures.

Direct download endpoints:

- `https://files.rcsb.org/download/{PDB_ID}.pdb`
- `https://files.rcsb.org/download/{PDB_ID}.cif`

### Batch Processing

For batch metadata retrieval, iterate over IDs and call `fetch(pdb_id, schema=Schema.ENTRY)`; handle exceptions per-ID. For large batches, consider rate limiting and caching.

## Additional Information

**PDB ID:** Unique 4-character identifier (e.g., "4HHB").

**Resolution:** Measure of detail in crystallographic structures (lower values = higher detail).

## Resources

- **RCSB PDB Website:** https://www.rcsb.org
- **API Documentation:** https://www.rcsb.org/docs/programmatic-access/web-apis-overview
- **Python Package Docs:** https://rcsbapi.readthedocs.io/
- **Data API Documentation:** https://data.rcsb.org/
- **GitHub Repository:** https://github.com/rcsb/py-rcsb-api

### Reference Documentation

If present in this repository, consult `references/api_reference.md` for advanced usage, query patterns, schema details, rate limits, and troubleshooting.