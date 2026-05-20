---
name: chembl-database
description: Query the ChEMBL database for bioactive molecules, drug targets, bioactivity
  data, approved drugs, and chemical structures. Use when the user asks about compounds,
  targets, IC50/Ki values, drug mechanisms, or structure searches.
license: MIT
metadata:
  skill-author: K-Dense Inc. + AIPOCH
---

---

## Overview

ChEMBL is a manually curated database of bioactive molecules maintained by the European Bioinformatics Institute (EBI), containing over 2 million compounds, 19 million bioactivity measurements, 13,000+ drug targets, and data on approved drugs and clinical candidates. Access and query this data programmatically using the ChEMBL Python client for drug discovery and medicinal chemistry research.

## When to Use This Skill

This skill should be used when you need to:

- **Compound searches**: Find molecules by name, structure, or properties. E.g., searching for “aspirin”.
- **Target information**: Retrieve data about proteins, enzymes, or biological targets and link them to ligands.
- **Bioactivity data**: Query IC50, Ki, EC50, or other activity measurements for compound-target interactions.
- **Drug information**: Look up approved drugs, mechanisms of action, or indications.
- **Structure searches**: Perform similarity or substructure searches using SMILES strings.
- **Cheminformatics**: Analyze molecular properties and drug-likeness.
- **Target-ligand relationships**: Explore compound-target interactions.
- **Drug discovery**: Identify inhibitors, agonists, or bioactive molecules.

## Key Features

- Molecule search by preferred name and other metadata fields.
- Property-based filtering (e.g., MW, LogP) using ChEMBL API filter syntax.
- Structure-aware querying via SMILES.
- Target lookup and navigation between targets, molecules, and activities.
- Bioactivity retrieval for common endpoints (IC50, Ki, EC50) and related assay context.
- Access to drug-related records, including mechanism information for approved drugs.

## Installation and Setup

### Python Client

The ChEMBL Python client is required for programmatic access:

```bash
uv pip install chembl_webresource_client
```

### Basic Usage Pattern

```python
from chembl_webresource_client.new_client import new_client

# Access different endpoints
molecule = new_client.molecule
target = new_client.target
activity = new_client.activity
drug = new_client.drug
mechanism = new_client.mechanism
```

## Core Capabilities

### 1. Molecule Queries

**Retrieve by ChEMBL ID:**
```python
molecule = new_client.molecule
aspirin = molecule.get('CHEMBL25')
```

**Search by name:**
```python
results = molecule.filter(pref_name__icontains='aspirin')
```

**Filter by properties:**
```python
# Find small molecules (MW <= 500) with favorable LogP
results = molecule.filter(
    molecule_properties__mw_freebase__lte=500,
    molecule_properties__alogp__lte=5
)
```

### 2. Target Queries

**Retrieve target information:**
```python
target = new_client.target
egfr = target.get('CHEMBL203')
```

**Search for specific target types:**
```python
# Find all kinase targets
kinases = target.filter(
    target_type='SINGLE PROTEIN',
    pref_name__icontains='kinase'
)
```

### 3. Bioactivity Data

**Query activities for a target:**
```python
activity = new_client.activity
# Find potent EGFR inhibitors
results = activity.filter(
    target_chembl_id='CHEMBL203',
    standard_type='IC50',
    standard_value__lte=100,
    standard_units='nM'
)
```

**Get all activities for a compound:**
```python
compound_activities = activity.filter(
    molecule_chembl_id='CHEMBL25',
    pchembl_value__isnull=False
)
```

### 4. Structure-Based Searches

**Similarity search:**
```python
similarity = new_client.similarity
# Find compounds similar to aspirin
similar = similarity.filter(
    smiles='CC(=O)Oc1ccccc1C(=O)O',
    similarity=85  # 85% similarity threshold
)
```

**Substructure search:**
```python
substructure = new_client.substructure
# Find compounds containing benzene ring
results = substructure.filter(smiles='c1ccccc1')
```

### 5. Drug Information

**Retrieve drug data:**
```python
drug = new_client.drug
drug_info = drug.get('CHEMBL25')
```

**Get mechanisms of action:**
```python
mechanism = new_client.mechanism
mechanisms = mechanism.filter(molecule_chembl_id='CHEMBL25')
```

**Query drug indications:**
```python
drug_indication = new_client.drug_indication
indications = drug_indication.filter(molecule_chembl_id='CHEMBL25')
```

## Query Workflow

### Workflow 1: Finding Inhibitors for a Target

1. **Identify the target** by searching by name:
   ```python
   targets = new_client.target.filter(pref_name__icontains='EGFR')
   target_id = targets[0]['target_chembl_id']
   ```

2. **Query bioactivity data** for that target:
   ```python
   activities = new_client.activity.filter(
       target_chembl_id=target_id,
       standard_type='IC50',
       standard_value__lte=100
   )
   ```

3. **Extract compound IDs** and retrieve details:
   ```python
   compound_ids = [act['molecule_chembl_id'] for act in activities]
   compounds = [new_client.molecule.get(cid) for cid in compound_ids]
   ```

### Workflow 2: Analyzing a Known Drug

1. **Get drug information**:
   ```python
   drug_info = new_client.drug.get('CHEMBL1234')
   ```

2. **Retrieve mechanisms**:
   ```python
   mechanisms = new_client.mechanism.filter(molecule_chembl_id='CHEMBL1234')
   ```

3. **Find all bioactivities**:
   ```python
   activities = new_client.activity.filter(molecule_chembl_id='CHEMBL1234')
   ```

### Workflow 3: Structure-Activity Relationship (SAR) Study

1. **Find similar compounds**:
   ```python
   similar = new_client.similarity.filter(smiles='query_smiles', similarity=80)
   ```

2. **Get activities for each compound**:
   ```python
   for compound in similar:
       activities = new_client.activity.filter(
           molecule_chembl_id=compound['molecule_chembl_id']
       )
   ```

3. **Analyze property-activity relationships** using molecular properties from results.

## Filter Operators

ChEMBL supports Django-style query filters:

- `__exact` - Exact match
- `__iexact` - Case-insensitive exact match
- `__contains` / `__icontains` - Substring matching
- `__startswith` / `__endswith` - Prefix/suffix matching
- `__gt`, `__gte`, `__lt`, `__lte` - Numeric comparisons
- `__range` - Value in range
- `__in` - Value in list
- `__isnull` - Null/not null check

## Data Export and Analysis

Convert results to pandas DataFrame for analysis:

```python
import pandas as pd

activities = new_client.activity.filter(target_chembl_id='CHEMBL203')
df = pd.DataFrame(list(activities))

# Analyze results
print(df['standard_value'].describe())
print(df.groupby('standard_type').size())
```

## Performance Optimization

### Caching

The client automatically caches results for 24 hours. Configure caching:

```python
from chembl_webresource_client.settings import Settings

# Disable caching
Settings.Instance().CACHING = False

# Adjust cache expiration (seconds)
Settings.Instance().CACHE_EXPIRE = 86400
```

### Lazy Evaluation

Queries execute only when data is accessed. Convert to list to force execution:

```python
# Query is not executed yet
results = molecule.filter(pref_name__icontains='aspirin')

# Force execution
results_list = list(results)
```

### Pagination

Results are paginated automatically. Iterate through all results:

```python
for activity in new_client.activity.filter(target_chembl_id='CHEMBL203'):
    # Process each activity
    print(activity['molecule_chembl_id'])
```

## Example Usage (Combined)

```python
from chembl_webresource_client.new_client import new_client

def main():
    molecule = new_client.molecule
    target = new_client.target
    activity = new_client.activity
    mechanism = new_client.mechanism

    # 1) Search for molecules by name (case-insensitive substring match)
    mols = list(molecule.filter(pref_name__icontains="aspirin")[:5])
    if not mols:
        raise SystemExit("No molecules found for query.")

    first = mols[0]
    chembl_id = first.get("molecule_chembl_id")
    print("Top molecule hit:", chembl_id, "-", first.get("pref_name"))

    # 2) Filter molecules by a simple property constraint (example: MW <= 500)
    # Note: exact field names and operators depend on ChEMBL API schema.
    druglike = list(molecule.filter(molecule_properties__mw_freebase__lte=500)[:5])
    print("Example drug-like hits (MW<=500):", [m.get("molecule_chembl_id") for m in druglike])

    # 3) Get target information (example: targets containing "COX")
    targets = list(target.filter(pref_name__icontains="cyclooxygenase")[:5])
    print("Example targets:", [(t.get("target_chembl_id"), t.get("pref_name")) for t in targets])

    # 4) Query bioactivity for a molecule (IC50/Ki/EC50 etc. depend on available records)
    # Here we fetch a few activity records linked to the molecule.
    acts = list(activity.filter(molecule_chembl_id=chembl_id)[:5])
    for a in acts:
        print(
            "Activity:",
            a.get("activity_id"),
            "type=", a.get("standard_type"),
            "value=", a.get("standard_value"),
            "units=", a.get("standard_units"),
            "target=", a.get("target_chembl_id"),
        )

    # 5) Retrieve mechanism-of-action records (often used for approved drugs)
    mechs = list(mechanism.filter(molecule_chembl_id=chembl_id)[:5])
    for m in mechs:
        print(
            "Mechanism:",
            "target=", m.get("target_chembl_id"),
            "action=", m.get("action_type"),
            "mechanism=", m.get("mechanism_of_action"),
        )

if __name__ == "__main__":
    main()
```

## Implementation Details

- **Client/Resources**: Uses `chembl_webresource_client.new_client.new_client` to access resource endpoints such as `molecule`, `target`, `activity`, `drug`, and `mechanism`.
- **Filtering Model**: Queries are built via `.filter(...)` with field lookups and operators (e.g., `__icontains`, `__lte`). The exact available fields and supported operators are defined by the ChEMBL API schema.
- **Pagination/Slicing**: Results are iterable and can be sliced (e.g., `[:5]`) to limit network calls and output size.
- **Bioactivity Fields**: Common normalized fields include `standard_type`, `standard_value`, and `standard_units`. Not all records contain all fields; code should handle missing keys.
- **Mechanism Retrieval**: Mechanism-of-action data is accessed via the `mechanism` resource and is typically most complete for approved/annotated drugs.
- **Structure Queries (SMILES)**: Structure-based search support depends on the API endpoint and client capabilities; when enabled, it is typically performed by passing a SMILES string to the appropriate structure/compound endpoint or filter.

## Resources

### scripts/example_queries.py

Ready-to-use Python functions demonstrating common ChEMBL query patterns:

- `get_molecule_info()` - Retrieve molecule details by ID
- `search_molecules_by_name()` - Name-based molecule search
- `find_molecules_by_properties()` - Property-based filtering
- `get_bioactivity_data()` - Query bioactivities for targets
- `find_similar_compounds()` - Similarity searching
- `substructure_search()` - Substructure matching
- `get_drug_info()` - Retrieve drug information
- `find_kinase_inhibitors()` - Specialized kinase inhibitor search
- `export_to_dataframe()` - Convert results to pandas DataFrame

Consult this script for implementation details and usage examples.

### references/api_reference.md

Comprehensive API documentation including:

- Complete endpoint listing (molecule, target, activity, assay, drug, etc.)
- All filter operators and query patterns
- Molecular properties and bioactivity fields
- Advanced query examples
- Configuration and performance tuning
- Error handling and rate limiting

Refer to this document when detailed API information is needed or when troubleshooting queries.

## Important Notes

### Data Reliability

- ChEMBL data is manually curated but may contain inconsistencies
- Always check `data_validity_comment` field in activity records
- Be aware of `potential_duplicate` flags

### Units and Standards

- Bioactivity values use standard units (nM, uM, etc.)
- `pchembl_value` provides normalized activity (-log scale)
- Check `standard_type` to understand measurement type (IC50, Ki, EC50, etc.)

### Rate Limiting

- Respect ChEMBL's fair usage policies
- Use caching to minimize repeated requests
- Consider bulk downloads for large datasets
- Avoid hammering the API with rapid consecutive requests

### Chemical Structure Formats

- SMILES strings are the primary structure format
- InChI keys available for compounds
- SVG images can be generated via the image endpoint

## Additional Resources

- ChEMBL website: https://www.ebi.ac.uk/chembl/
- API documentation: https://www.ebi.ac.uk/chembl/api/data/docs
- Python client GitHub: https://github.com/chembl/chembl_webresource_client
- Interface documentation: https://chembl.gitbook.io/chembl-interface-documentation/
- Example notebooks: https://github.com/chembl/notebooks

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://chembl.gitbook.io/chembl-interface-documentation/about, then (2)
    create the file recording the notification text and timestamp.

## Core Rules

-   [!IMPORTANT] **Use the Utility Scripts**: You MUST ALWAYS use the provided
    utility script `scripts/chembl_api.py` for all ChEMBL API interactions,
    including checking status. NEVER use `curl` or custom Python requests to
    query the ChEMBL API directly. This ensures rate limit is enfoced and also
    retries on network errors.

-   **Output to File (Required)**: The `--output` flag is **required** for every
    subcommand. All JSON results are written to the specified file. After
    running the command, read the output file with jq or your own code to
    extract the data. List results are typically wrapped in a JSON array keyed
    by the endpoint name (e.g., `molecules`, `activities`).

-   **Notification**: If this skill is used, ensure this is mentioned in the
    output.

## Utility Script

All ChEMBL API queries use one script with subcommands:

```bash
uv run scripts/chembl_api.py <subcommand> --output <file> [options]
```

--------------------------------------------------------------------------------

### 1. Check API Status

```bash
uv run scripts/chembl_api.py status --output /tmp/status.json
```

--------------------------------------------------------------------------------

### 2. Molecule Queries

**Fetch by ChEMBL ID:** `bash uv run scripts/chembl_api.py molecule --id
CHEMBL25 --output /tmp/mol.json`

**Search by name:** `bash uv run scripts/chembl_api.py molecule --search
"aspirin" --limit 3 --output /tmp/mol_search.json`

**Batch fetch:** `bash uv run scripts/chembl_api.py molecule --ids
"CHEMBL25;CHEMBL1642" --limit 10 --output /tmp/mol_batch.json`

**Filter by properties:** `bash uv run scripts/chembl_api.py molecule --filter
molecule_properties__mw_freebase__lte=500 --limit 5 --output
/tmp/mol_filter.json`

**Filter by range:** `bash uv run scripts/chembl_api.py molecule --filter
molecule_properties__mw_freebase__range=150,200 --limit 5 --output
/tmp/mol_range.json`

**Download SDF structure file:** `bash uv run scripts/chembl_api.py molecule
--id CHEMBL25 --dl_format sdf --output /tmp/aspirin.sdf`

> **Tip**: SDF/MOL files can be passed directly to tools like PyMOL or RDKit for
> 3D visualization and analysis.

--------------------------------------------------------------------------------

### 3. Target Queries

**Search for targets:** `bash uv run scripts/chembl_api.py target --search
"EGFR" --limit 5 --output /tmp/targets.json`

**Fetch by ID:** `bash uv run scripts/chembl_api.py target --id CHEMBL203
--output /tmp/egfr.json`

--------------------------------------------------------------------------------

### 4. Bioactivity Data

**Fetch activity by ID:** `bash uv run scripts/chembl_api.py activity --id 31863
--output /tmp/act.json`

**Search activities:** `bash uv run scripts/chembl_api.py activity --search
"EGFR" --limit 5 --output /tmp/act_search.json`

**Filter activities for a target:** `bash uv run scripts/chembl_api.py activity
--filter target_chembl_id=CHEMBL203 standard_type=IC50 --limit 10 --output
/tmp/egfr_ic50.json`

**Normalize bioactivity units to nM:** `bash uv run scripts/chembl_api.py
activity --filter target_chembl_id=CHEMBL203 standard_type=IC50 --limit 5
--normalize --output /tmp/egfr_normalized.json`

> **Important**: Bioactivity values come in various units (nM, µM, pM). Use
> `--normalize` to convert all values to nM for consistent comparison. Each
> record will include `normalized_value_nM` and `normalization_note`.

--------------------------------------------------------------------------------

### 5. Drug Information

**Fetch drug details:** `bash uv run scripts/chembl_api.py drug --id CHEMBL25
--output /tmp/drug.json`

**Drug indications:** `bash uv run scripts/chembl_api.py drug_indication
--filter molecule_chembl_id=CHEMBL25 --limit 10 --output /tmp/indications.json`

**Filter indications by phase:** `bash uv run scripts/chembl_api.py
drug_indication --filter molecule_chembl_id=CHEMBL25 max_phase_for_ind=4.0
--limit 10 --output /tmp/approved_indications.json`

**Drug warnings:** `bash uv run scripts/chembl_api.py drug_warning --limit 5
--output /tmp/warnings.json`

**Mechanisms of action:** `bash uv run scripts/chembl_api.py mechanism --filter
molecule_chembl_id=CHEMBL25 --limit 5 --output /tmp/mech.json`

--------------------------------------------------------------------------------

### 6. Structure-Based Searches

> **Note**: Both similarity and substructure searches are performed
> **server-side** on ChEMBL's pre-indexed database. They do not require a local
> RDKit installation.

**Similarity search (SMILES + threshold):** `bash uv run scripts/chembl_api.py
similarity --smiles "CC(=O)Oc1ccccc1C(=O)O" --similarity 85 --limit 5 --output
/tmp/similar.json`

**Substructure search (SMILES):** `bash uv run scripts/chembl_api.py
substructure --smiles "c1ccccc1" --limit 5 --output /tmp/substruct.json`

--------------------------------------------------------------------------------

### 7. Compound Image

Download a 2D structure image (SVG by default, scalable for publication):

```bash
uv run scripts/chembl_api.py image --id CHEMBL25 --output /tmp/chembl25.svg
```

*Options:*

-   `--dimensions`: Image size in pixels (max 500, default 500).
-   `--engine`: Rendering engine (default: rdkit).
-   `--img_format`: Output format — `svg` (default, vector) or `png` (raster).

--------------------------------------------------------------------------------

### 8. Cross-Referencing with Other Databases

ChEMBL integrates with UniProt, Ensembl, PubChem, and other databases. Common
cross-referencing patterns:

**Find a ChEMBL target from a UniProt accession:** `bash uv run
scripts/chembl_api.py target --filter target_components__accession=P00533
--limit 5 --output /tmp/uniprot_target.json`

**Resolve any ChEMBL ID to its entity type:** `bash uv run scripts/chembl_api.py
chembl_id_lookup --id CHEMBL203 --output /tmp/lookup.json`

**Look up cross-reference sources:** `bash uv run scripts/chembl_api.py
xref_source --limit 10 --output /tmp/xrefs.json`

> **Tip**: Use the `target_component` endpoint to find UniProt accessions, gene
> names, and protein sequences for any ChEMBL target.

--------------------------------------------------------------------------------

### 9. Pagination

All list endpoints support `--limit` and `--offset` for pagination:

```bash
# First page: 2 results starting at offset 0
uv run scripts/chembl_api.py molecule --limit 2 --offset 0 --output /tmp/page1.json

# Second page: next 2 results starting at offset 2
uv run scripts/chembl_api.py molecule --limit 2 --offset 2 --output /tmp/page2.json
```

The response includes `page_meta` with `total_count`, `limit`, `offset`, `next`,
and `previous` links. Use successive `--offset` values to page through large
result sets.

--------------------------------------------------------------------------------

### 10. Other Endpoints

All remaining endpoints follow the same pattern:

```bash
uv run scripts/chembl_api.py <subcommand> --output <file> [--id ID | --ids ID1;ID2 | --search QUERY] [--limit N] [--offset N] [--filter KEY=VAL ...]
```

**Key subcommands at a glance:**

-   `molecule` (searchable: true): Molecules/compounds — the primary entry point
-   `target` (searchable: true): Drug targets (proteins, organisms, etc.)
-   `activity` (searchable: true): Bioactivity data (IC50, Ki, EC50, etc.)
-   `drug` (searchable: false): Approved drugs
-   `mechanism` (searchable: false): Mechanisms of action
-   `assay` (searchable: true): Assay descriptions
-   `similarity` (searchable: false): Similarity search (special)
-   `substructure` (searchable: false): Substructure search (special)
-   `image` (searchable: false): Compound image download (special)

**Full subcommand list:**

-   `activity_supp` (searchable: false): Supplementary activity data
-   `assay_class` (searchable: false): Assay classifications
-   `atc_class` (searchable: false): ATC drug classifications
-   `binding_site` (searchable: false): Binding site information
-   `biotherapeutic` (searchable: false): Biotherapeutic molecules
-   `cell_line` (searchable: false): Cell line details
-   `chembl_id_lookup` (searchable: true): ChEMBL ID resolution
-   `chembl_release` (searchable: false): Database release info
-   `compound_record` (searchable: false): Compound records
-   `compound_structural_alert` (searchable: false): Structural alerts
-   `document` (searchable: true): Literature documents
-   `document_similarity` (searchable: false): Document similarity
-   `drug_indication` (searchable: false): Drug indications
-   `drug_warning` (searchable: false): Drug safety warnings
-   `go_slim` (searchable: false): GO slim terms
-   `metabolism` (searchable: false): Metabolism data
-   `molecule_form` (searchable: false): Molecule forms (salts/parents)
-   `organism` (searchable: false): Organisms
-   `protein_classification` (searchable: true): Protein classifications
-   `source` (searchable: false): Data sources
-   `target_component` (searchable: false): Target protein components
-   `target_relation` (searchable: false): Target relationships
-   `tissue` (searchable: false): Tissue types
-   `xref_source` (searchable: false): Cross-reference sources
-   `status` (searchable: false): API status check (special)

## Common Options

-   `--output FILE`: **Required.** Output file path for JSON results.
-   `--id ID`: Fetch a single record by ID.
-   `--ids ID1;ID2;...`: Batch fetch multiple records.
-   `--search QUERY`: Free-text search (only for searchable endpoints, marked
    ✓).
-   `--limit N`: Max results to return (default: 5).
-   `--offset N`: Pagination offset.
-   `--filter KEY=VAL`: Filter parameters (can specify multiple).
-   `--normalize`: (activity only) Normalize values to nM.
-   `--dl_format sdf|mol`: (molecule only) Download structure file.

## Reference

-   **API Endpoints Reference**: See
    [references/api_endpoints.md](references/api_endpoints.md) for the full list
    of endpoints and filter operators.

## Workflow

1.  Use `status --output /tmp/status.json` to verify the API is available.
2.  Search for targets, molecules, or drugs using the relevant subcommand.
3.  Read the output JSON file to extract IDs and data.
4.  Use IDs from search results to fetch detailed records.
5.  Query `activity` with filters to get bioactivity data for targets/molecules.
    Use `--normalize` when comparing values across studies.
6.  Use `similarity` or `substructure` for server-side structure-based queries.
7.  Download compound images with `image` or structure files with `molecule
    --dl_format sdf`.
8.  Use `target --filter target_components__accession=<UniProt>` to cross-
    reference with UniProt.
