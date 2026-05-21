---
name: chembl-database
description: Query ChEMBL for bioactive molecules, targets, bioactivities, and drugs. Filter by properties, structure (SMILES), or retrieve drug mechanism information for drug discovery and medicinal chemistry.
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