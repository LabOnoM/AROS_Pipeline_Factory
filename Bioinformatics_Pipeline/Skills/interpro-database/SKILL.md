---
name: interpro-database
description: Identify domains, families, and sites in proteins; find all proteins
  in a family or sharing a domain; explore species distribution for a domain; annotate
  genomes with protein families and GO terms. InterPro combines 14 databases (e.g.,
  Pfam, CDD) into one searchable resource. InterPro-N significantly expands annotation
  and sequence coverage with deep learning. Includes domain architecture (IDA) search.
license: CC0-1.0
metadata:
  skill-author: Kuan-lin Huang
---

# InterPro Database

## Overview

InterPro (https://www.ebi.ac.uk/interpro/) is a comprehensive resource for protein family and domain classification maintained by EMBL-EBI. It integrates signatures from 13 member databases including Pfam, PANTHER, PRINTS, ProSite, SMART, TIGRFAM, SUPERFAMILY, CDD, and others, providing a unified view of protein functional annotations for over 100 million protein sequences.

InterPro classifies proteins into:
- **Families**: Groups of proteins sharing common ancestry and function
- **Domains**: Independently folding structural/functional units
- **Homologous superfamilies**: Structurally similar protein regions
- **Repeats**: Short tandem sequences
- **Sites**: Functional sites (active, binding, PTM)

**Key resources:**
- InterPro website: https://www.ebi.ac.uk/interpro/
- REST API: https://www.ebi.ac.uk/interpro/api/
- API documentation: https://github.com/ProteinsWebTeam/interpro7-api/blob/master/docs/
- Python client: via `requests`

## When to Use This Skill

Use InterPro when:

- **Protein function prediction**: What function(s) does an uncharacterized protein likely have?
- **Domain architecture**: What domains make up a protein, and in what order?
- **Protein family classification**: Which family/superfamily does a protein belong to?
- **GO term annotation**: Map protein sequences to Gene Ontology terms via InterPro
- **Evolutionary analysis**: Are two proteins in the same homologous superfamily?
- **Structure prediction context**: What domains should a new protein structure be compared against?
- **Pipeline annotation**: Batch-annotate proteomes or novel sequences

## Core Capabilities

### 1. InterPro REST API

Base URL: `https://www.ebi.ac.uk/interpro/api/`

```python
import requests

BASE_URL = "https://www.ebi.ac.uk/interpro/api"

def interpro_get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()
```

### 2. Look Up a Protein

```python
def get_protein_entries(uniprot_id):
    """Get all InterPro entries that match a UniProt protein."""
    data = interpro_get(f"protein/UniProt/{uniprot_id}/entry/InterPro/")
    return data

# Example: Human p53 (TP53)
result = get_protein_entries("P04637")
entries = result.get("results", [])

for entry in entries:
    meta = entry["metadata"]
    print(f"  {meta['accession']} ({meta['type']}): {meta['name']}")
    # e.g., IPR011615 (domain): p53, tetramerisation domain
    #       IPR010991 (domain): p53, DNA-binding domain
    #       IPR013872 (family): p53 family
```

### 3. Get Specific InterPro Entry

```python
def get_entry(interpro_id):
    """Fetch details for an InterPro entry."""
    return interpro_get(f"entry/InterPro/{interpro_id}/")

# Example: Get Pfam domain PF00397 (WW domain)
ww_entry = get_entry("IPR001202")
print(f"Name: {ww_entry['metadata']['name']}")
print(f"Type: {ww_entry['metadata']['type']}")

# Also supports member database IDs:
def get_pfam_entry(pfam_id):
    return interpro_get(f"entry/Pfam/{pfam_id}/")

pfam = get_pfam_entry("PF00397")
```

### 4. Search Proteins by InterPro Entry

```python
def get_proteins_for_entry(interpro_id, database="UniProt", page_size=25):
    """Get all proteins annotated with an InterPro entry."""
    params = {"page_size": page_size}
    data = interpro_get(f"entry/InterPro/{interpro_id}/protein/{database}/", params)
    return data

# Example: Find all human kinase-domain proteins
kinase_proteins = get_proteins_for_entry("IPR000719")  # Protein kinase domain
print(f"Total proteins: {kinase_proteins['count']}")
```

### 5. Domain Architecture

```python
def get_domain_architecture(uniprot_id):
    """Get the complete domain architecture of a protein."""
    data = interpro_get(f"protein/UniProt/{uniprot_id}/")
    return data

# Example: Get full domain architecture for EGFR
egfr = get_domain_architecture("P00533")

# The response includes locations of all matching entries on the sequence
for entry in egfr.get("entries", []):
    for fragment in entry.get("entry_protein_locations", []):
        for loc in fragment.get("fragments", []):
            print(f"  {entry['accession']}: {loc['start']}-{loc['end']}")
```

### 6. GO Term Mapping

```python
def get_go_terms_for_protein(uniprot_id):
    """Get GO terms associated with a protein via InterPro."""
    data = interpro_get(f"protein/UniProt/{uniprot_id}/")

    # GO terms are embedded in the entry metadata
    go_terms = []
    for entry in data.get("entries", []):
        go = entry.get("metadata", {}).get("go_terms", [])
        go_terms.extend(go)

    # Deduplicate
    seen = set()
    unique_go = []
    for term in go_terms:
        if term["identifier"] not in seen:
            seen.add(term["identifier"])
            unique_go.append(term)

    return unique_go

# GO terms include:
# {"identifier": "GO:0004672", "name": "protein kinase activity", "category": {"code": "F", "name": "Molecular Function"}}
```

### 7. Batch Protein Lookup

```python
def batch_lookup_proteins(uniprot_ids, database="UniProt"):
    """Look up multiple proteins and collect their InterPro entries."""
    import time
    results = {}
    for uid in uniprot_ids:
        try:
            data = interpro_get(f"protein/{database}/{uid}/entry/InterPro/")
            entries = data.get("results", [])
            results[uid] = [
                {
                    "accession": e["metadata"]["accession"],
                    "name": e["metadata"]["name"],
                    "type": e["metadata"]["type"]
                }
                for e in entries
            ]
        except Exception as e:
            results[uid] = {"error": str(e)}
        time.sleep(0.3)  # Rate limiting
    return results

# Example
proteins = ["P04637", "P00533", "P38398", "Q9Y6I9"]
domain_info = batch_lookup_proteins(proteins)
for uid, entries in domain_info.items():
    print(f"\n{uid}:")
    for e in entries[:3]:
        print(f"  - {e['accession']} ({e['type']}): {e['name']}")
```

### 8. Search by Text or Taxonomy

```python
def search_entries(query, entry_type=None, taxonomy_id=None):
    """Search InterPro entries by text."""
    params = {"search": query, "page_size": 20}
    if entry_type:
        params["type"] = entry_type  # family, domain, homologous_superfamily, etc.

    endpoint = "entry/InterPro/"
    if taxonomy_id:
        endpoint = f"entry/InterPro/taxonomy/UniProt/{taxonomy_id}/"

    return interpro_get(endpoint, params)

# Search for kinase-related entries
kinase_entries = search_entries("kinase", entry_type="domain")
```

## Query Workflows

### Workflow 1: Characterize an Unknown Protein

1. **Run InterProScan** locally or via the web (https://www.ebi.ac.uk/interpro/search/sequence/) to scan a protein sequence
2. **Parse results** to identify domain architecture
3. **Look up each InterPro entry** for biological context
4. **Get GO terms** from associated InterPro entries for functional inference

```python
# After running InterProScan and getting a UniProt ID:
def characterize_protein(uniprot_id):
    """Complete characterization workflow."""

    # 1. Get all annotations
    entries = get_protein_entries(uniprot_id)

    # 2. Group by type
    by_type = {}
    for e in entries.get("results", []):
        t = e["metadata"]["type"]
        by_type.setdefault(t, []).append({
            "accession": e["metadata"]["accession"],
            "name": e["metadata"]["name"]
        })

    # 3. Get GO terms
    go_terms = get_go_terms_for_protein(uniprot_id)

    return {
        "families": by_type.get("family", []),
        "domains": by_type.get("domain", []),
        "superfamilies": by_type.get("homologous_superfamily", []),
        "go_terms": go_terms
    }
```

### Workflow 2: Find All Members of a Protein Family

1. Identify the InterPro family entry ID (e.g., IPR000719 for protein kinases)
2. Query all UniProt proteins annotated with that entry
3. Filter by organism/taxonomy if needed
4. Download FASTA sequences for phylogenetic analysis

### Workflow 3: Comparative Domain Analysis

1. Collect proteins of interest (e.g., all paralogs)
2. Get domain architecture for each protein
3. Compare domain compositions and orders
4. Identify domain gain/loss events

## API Endpoint Summary

| Endpoint | Description |
|----------|-------------|
| `/protein/UniProt/{id}/` | Full annotation for a protein |
| `/protein/UniProt/{id}/entry/InterPro/` | InterPro entries for a protein |
| `/entry/InterPro/{id}/` | Details of an InterPro entry |
| `/entry/Pfam/{id}/` | Pfam entry details |
| `/entry/InterPro/{id}/protein/UniProt/` | Proteins with an entry |
| `/entry/InterPro/` | Search/list InterPro entries |
| `/taxonomy/UniProt/{tax_id}/` | Proteins from a taxon |
| `/structure/PDB/{pdb_id}/` | Structures mapped to InterPro |

## Member Databases

| Database | Focus |
|----------|-------|
| Pfam | Protein domains (HMM profiles) |
| PANTHER | Protein families and subfamilies |
| PRINTS | Protein fingerprints |
| ProSitePatterns | Amino acid patterns |
| ProSiteProfiles | Protein profile patterns |
| SMART | Protein domain analysis |
| TIGRFAM | JCVI curated protein families |
| SUPERFAMILY | Structural classification |
| CDD | Conserved Domain Database (NCBI) |
| HAMAP | Microbial protein families |
| NCBIfam | NCBI curated TIGRFAMs |
| Gene3D | CATH structural classification |
| PIRSR | PIR site rules |

## Best Practices

- **Use UniProt accession numbers** (not gene names) for the most reliable lookups
- **Distinguish types**: `family` gives broad classification; `domain` gives specific structural/functional units
- **InterProScan is faster for novel sequences**: For sequences not in UniProt, submit to the web service
- **Handle pagination**: Large result sets require iterating through pages
- **Combine with UniProt data**: InterPro entries often include links to UniProt, PDB, and GO

## Additional Resources

- **InterPro website**: https://www.ebi.ac.uk/interpro/
- **InterProScan** (run locally): https://github.com/ebi-pf-team/interproscan
- **API documentation**: https://github.com/ProteinsWebTeam/interpro7-api/blob/master/docs/
- **Pfam**: https://www.ebi.ac.uk/interpro/entry/pfam/
- **Citation**: Paysan-Lafosse T et al. (2023) Nucleic Acids Research. PMID: 36350672

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://www.ebi.ac.uk/interpro/ and
    https://www.ebi.ac.uk/about/terms-of-use/, then (2) create the file
    recording the notification text and timestamp.

## Overview

InterPro combines signatures from multiple, diverse databases into a single
searchable resource, reducing redundancy and helping users interpret their
sequence analysis results. By uniting these member databases (e.g., Pfam, CDD,
SMART), InterPro capitalises on their individual strengths to produce a powerful
diagnostic tool and integrated resource.

Use `interpro-database` to:

-   Identify what domains, families, and sites are found in a particular
    protein.
-   Identify all proteins that belong to a protein family or contain a
    particular domain, even when the names and activities of the proteins are
    highly variable.
-   Examine the species in which a particular protein family or domain is found.
-   Annotate genomes with protein family information and Gene Ontology (GO)
    terms.

This skill provides a robust utility, `interpro_client.py`, to interact with the
InterPro API seamlessly. It natively handles rate limiting (HTTP 429),
background query sleep tracking (HTTP 408), terminal errors (HTTP 404/410), and
lazy pagination.

## Core Rules

-   **Use the Wrapper**: ALWAYS execute the `scripts/interpro_client.py` helper
    script to query the database rather than accessing the database directly.
    The scripts automatically enforce fair use and implement retry logic.
-   **For exploratory queries**: ALWAYS use the CLI with a strict `--limit`.
    This allows you to rapidly understand the data schema without polluting your
    context window or fetching millions of results.
-   **Output to file**: Use the CLI with --output to output to a file rather
    than attempting to print it all to the console. Process the output using jq
    or code.
-   **For more complex pipelines** import the module natively into your Python
    scripts to consume the generator directly, preventing the need to
    deserialize CLI strings in large workflows.
-   **Notification**: If this skill is used, ensure this is mentioned in the
    output.

Examples:

```bash
uv run ./scripts/interpro_client.py fetch protein --source_db reviewed --limit 2 --query_params tax_id=9606 --output exploratory_results.jsonl
```

```python
import sys
sys.path.append('scripts')
from interpro_client import fetch_interpro_data
import itertools

# fetch_interpro_data lazily yields results page-by-page
results = fetch_interpro_data(
    endpoint="entry",
    source_db="pfam",
    query_params={"page_size": 10}
)
for match in itertools.islice(results, 10):
    print(match["metadata"]["accession"])
```

### 4 Ways to Construct Endpoints:

The arguments strictly map to the four common API path constructions. **Do not
format your own `/` separated strings:**

1.  **`/{endpoint}`** (e.g. `/entry`) `uv run ./scripts/interpro_client.py fetch
    entry --limit 10 --output entries.jsonl`
2.  **`/{endpoint}/{sourceDB}`** (e.g. `/entry/pfam`) `uv run
    ./scripts/interpro_client.py fetch entry --source_db pfam --limit 10
    --output pfam_entries.jsonl`
3.  **`/{endpoint}/{sourceDB}/{accession}`** (e.g. `/entry/pfam/PF00001`) `uv
    run ./scripts/interpro_client.py fetch entry --source_db pfam --accession
    PF00001 --limit 10 --output pf00001_entry.jsonl`
4.  **`/{endpoint}/{sourceDB}/{linked_endpoint}/{sourceDB}/{accession}`** (e.g.
    `/entry/interpro/protein/uniprot/P04637`) `uv run
    ./scripts/interpro_client.py fetch entry \ --source_db interpro \
    --linked_endpoint protein \ --linked_source_db uniprot \ --linked_accession
    P04637 \ --limit 10 --output p04637_entries.jsonl`

## Valid Source Databases (`--source_db`)

Each endpoint only accepts specific `source_db` values. Using an invalid value
returns a 404 error.

*   **`/entry`** (16 values): `interpro`, `pfam`, `cathgene3d`, `ssf`,
    `panther`, `cdd`, `profile`, `smart`, `ncbifam`, `prosite`, `prints`,
    `hamap`, `pirsf`, `sfld`, `antifam`.
*   **`/protein`** (3 values): `uniprot` (all), `reviewed` (SwissProt),
    `unreviewed` (TrEMBL).
*   **`/structure`** (1 value): `pdb`.
*   **`/taxonomy`** (1 value): `uniprot`.
*   **`/proteome`** (1 value): `uniprot`.
*   **`/set`** (2 values): `pfam`, `cdd`.

## Quick Reference / Core Endpoints & Parameters

**For a complete, exhaustive list of all query parameters, see the
[Full API Reference](references/api_reference.md).**

The API is fully open and supports 6 core endpoints. You can combine them using
the linked parameters described above. Below is a nested list of the specific
query parameters available for each endpoint:

*   **`/entry`** (Domain, family, active site, repeat, or homologous superfamily
    entries)

    *   `integrated`: Filter by integrated status (e.g., `pfam`).
    *   `type`: Filter by type (e.g., `family`, `domain`,
        `homologous_superfamily`).
    *   `go_term` / `go_category`: Filter by Gene Ontology.
    *   `ida_search` / `ida_ignore` / `exact` / `ordered`: Filter by domain
        architecture (see IDA Search section).
    *   `extra_fields`: Request additional data (e.g., `counters` for match
        coordinates).
    *   `group_by` / `sort_by`: Aggregate or sort results *(valid values depend
        on context, see [Full API Reference](references/api_reference.md))*.
    *   *Example*: `uv run ./scripts/interpro_client.py count entry --source_db
        pfam --query_params type=domain --output count.jsonl`

*   **`/protein`** (Protein records matching entries or domains)

    *   `tax_id`: Filter by taxonomy ID (does not search lineage).
    *   `match_presence`: Filter by proteins having InterPro matches
        (`true`/`false`).
    *   `is_fragment`: Filter complete vs. fragment sequences.
    *   `group_by`: Aggregate results (e.g., `taxonomy`).
    *   `extra_fields`: Request sequence or match details.
    *   `isoforms` / `residues` / `structureinfo`: Include specific
        sub-features.
    *   `conservation` / `extra_features`: Append residue conservation flags or
        Mobidb/coil features *(only valid for
        `/protein/{source_db}/{accession}`)*.
    *   *Example*: `uv run ./scripts/interpro_client.py fetch protein
        --source_db uniprot --limit 20 --query_params tax_id=9606 --output
        human_proteins.jsonl`

*   **`/structure`** (PDB structures linked to InterPro entries)

    *   `experiment_type`: Filter by experimental method (e.g., `X-RAY
        DIFFRACTION`).
    *   `resolution`: Filter by resolution limit.
    *   `extra_fields`: Include additional structural metadata.
    *   `group_by`: Aggregate results.
    *   *Example*: `./scripts/interpro_client.py fetch structure --source_db pdb
        --accession 1ATP --limit 10 --output 1atp_structures.jsonl`

*   **`/taxonomy`** (Taxonomy distribution nodes)

    *   `key_species`: Filter to limit to key species.
    *   `with_names`: Include scientific names.
    *   `filter_by_entry` / `filter_by_entry_db`: Filter intersection with
        specific entries.
    *   `extra_fields`: Additional taxonomic metadata.
    *   *Example*: `./scripts/interpro_client.py fetch taxonomy --source_db
        uniprot --accession 9606 --limit 10 --output human_taxonomy.jsonl`

*   **`/proteome`** (Complete proteomes linked to InterPro)

    *   `extra_fields`: General query expansion.
    *   *Example*: `uv run ./scripts/interpro_client.py fetch proteome
        --source_db uniprot --accession UP000005640 --limit 10 --output
        proteome.jsonl`

*   **`/set`** (Curated sets of related entries, e.g., Pfam clans)

    *   `extra_fields`: Additional metadata *(only valid for
        `/set/{sourceDB}`)*.
    *   *Example*: `uv run ./scripts/interpro_client.py fetch set --source_db
        pfam --accession CL0001 --limit 10 --output pfam_clan.jsonl`

## InterPro Domain Architecture (IDA) Search

InterPro provides powerful tools for searching proteins by their domain
architecture (the exact combination and order of domains). Because the API does
not allow querying proteins directly by multiple domains at once (e.g., "give me
proteins with PF00069 AND PF00017"), finding proteins with specific domain
combinations requires a two-step process.

### Step 1: Find matching architectures (`ida_search`)

The `ida_search` parameter is used on the root `/entry` endpoint to find all
Domain Architectures (IDAs) containing the domains you specify.

-   **Constraints**:
    -   Valid ONLY on the root `/entry` endpoint.
    -   Cannot be combined with non-IDA parameters.
-   **Modifiers** (Only valid with `ida_search`):
    -   `ida_ignore`: Ignores the given domains in the search (query param).
    -   `ordered`: Ensures domains appear in the exact specified order (flag).
    -   `exact`: Ensures the architecture matches exactly (no additional
        domains) (flag). **Requires `ordered` flag to be present.**

**Example**: Find architectures containing both a kinase domain (PF00069) and an
SH2 domain (PF00017), in that exact order:

```bash
uv run scripts/interpro_client.py fetch entry
  --query_params ida_search=PF00069,PF00017
  --flags ordered exact
  --output architectures.jsonl
```

*Note: This returns the architectures and their unique `ida_id`s, not all
individual proteins.*

### Step 2: Fetch proteins for those architectures (`ida`)

Once you have the `ida_id`s (e.g., `619edbb...`) from Step 1, you can fetch all
the actual proteins that share that precise layout by filtering the `/protein`
endpoint.

**Constraints**:

-   Valid on `/protein` and `/entry/{sourceDB}/{accession}` endpoints.

**Example**: Fetch proteins matching one of the architecture IDs from Step 1:

```bash
uv run scripts/interpro_client.py fetch protein
  --source_db uniprot
  --query_params ida=619edbb2b445bfa3ad51bd894e3c115b025a5f25
  --output matching_proteins.jsonl
```

*(When building pipelines or querying comprehensively, you would loop through
all the `ida_id`s from Step 1 and run Step 2 for each one).*

## InterPro Entry Types

Each InterPro entry is assigned a type indicating what you can infer when a
protein matches the entry:

-   **Domain**: Distinct functional, structural or sequence units that may exist
    in a variety of biological contexts. Example: *PH domain* or *classical C2H2
    zinc finger*.
-   **Family**: A group of proteins sharing a common evolutionary origin
    reflected by related functions, sequence similarities, or
    primary/secondary/tertiary structures.
-   **Homologous Superfamily**: Proteins sharing an evolutionary origin
    reflected by structural similarity but often displaying very low sequence
    similarity. Usually comprises signatures from the SUPERFAMILY and
    CATH-Gene3D databases.
-   **Repeat**: A short sequence that is typically repeated within a protein,
    often <50 amino acids long. Example: *Leucine Rich Repeats* or *WD40
    repeats*.
-   **Site**: Includes `Active site` (sequence containing conserved residues for
    catalytic activity) and `Binding site` (sequence containing conserved
    residues forming a protein interaction site).

## InterPro-N Predictions

InterPro-N is a deep-learning-based extension of the standard InterPro database.
It utilizes an AI architecture inspired by computer vision to treat protein
sequence annotation as a "panoptic segmentation" task, labeling residues and
distinguishing between domains.

### When to use InterPro-N

Standard InterPro signatures are the "gold standard" and should not be discarded
in favor of InterPro-N predictions. Use InterPro-N primarily to fill in gaps or
refine results.

**In addition to standard InterPro:**

-   **Analyzing "Dark Matter" (Uncharacterised Proteins)**: Use when a protein
    returns no hits in standard InterPro. InterPro-N excels at identifying
    remote homologs.
-   **Resolving Complex Repeats**: Use for proteins with multiple tandem repeats
    (e.g., TPR or WD40) where standard HMMs might merge or miss them.
-   **Predicting Discontinuous Domains**: Use when a domain sequence is
    interrupted by a completely different inserted sequence.

**Instead of standard InterPro (specific scenarios):**

-   **Precise Boundary Delineation**: When you need more accurate start-and-stop
    coordinates for a domain than fuzzy standard hits provide.
-   **Large-Scale Metagenomic Screening**: For initial high-recovery screening
    of fragmented or highly divergent sequences.

### Fallback Strategy: Checking InterPro-N

When you are asked to find annotations for a protein and standard InterPro
queries return no results or no annotations, you **MUST** check InterPro-N as a
fallback.

**Example Scenario:** If a user asks to "List the SSF annotations for protein X"
and the standard query returns no hits, you should retry the query with the
`interpro_n` flag.

This fallback is crucial because InterPro-N can identify remote homologs and
domains in "dark matter" proteins that standard methods miss.

If found, **ALWAYS** report to the user that these annotations are deep learning
predictions from InterPro-N.

### How to Use

InterPro-N predictions are accessed by passing the `interpro_n` flag to the
`protein` endpoint with `uniprot` as the source database.

**Via CLI:**

```bash
uv run ./scripts/interpro_client.py fetch protein
    --source_db uniprot
    --accession A0A096LNN2
    --flags interpro_n
    --output A0A096LNN2_interpro_n.jsonl
```

**Via Python Pipeline:**

```python
results = fetch_interpro_data(
    endpoint="protein",
    source_db="uniprot",
    accession="A0A096LNN2",
    flags=["interpro_n"])
```

## Strict Lookup Rules

1.  **Always Use UniProt Accessions, NEVER Gene Names:** When looking up
    proteins in InterPro, you MUST use their UniProt Accessions (e.g. `P04637`).
    InterPro does not natively support or reliably map gene names (e.g. `TP53`).
    If the user provides a gene name, you must use a database like Ensembl or
    UniProt first to resolve it to an accession.

2.  **NEVER Iterate to Count:** When asked for an aggregate count (e.g., "How
    many domains are there?"), you MUST read the `count` field from the initial
    API JSON response using the `get_interpro_count()` helper. NEVER iterate
    over the `fetch_interpro_data` generator to tally elements. Iterating over
    an endpoint with 50,000+ entries just to count them silently hangs the agent
    and abuses the API. Every time. No exceptions.

    ✅ **Correct**:

    **Via CLI:**

    ```bash
    uv run ./scripts/interpro_client.py count entry
        --source_db interpro
        --query_params type=domain
        --output count.json
    ```

    **Via Python Pipeline:**

    ```python
    from interpro_client import get_interpro_count
    cnt = get_interpro_count(
        endpoint="entry",
        source_db="interpro",
        query_params={"type": "domain"},
    )
    ```

    ❌ **Wrong** (Iterating over fetch):

    ```bash
    # NEVER DO THIS:
    uv run ./scripts/interpro_client.py fetch entry
        --source_db interpro
        --query_params type=domain
        --output output.jsonl
        && wc -l output.jsonl
    ```

## Quick examples

**For detailed examples of the invocations and JSON output schemas returned by
various endpoints, see the
[Example Responses Reference](references/example_responses.tsv).** This TSV
contains command-line calls, Python equivalents, and the corresponding JSON
payload structures.

### 1. Determining all protein domains

```bash
# Fetches InterPro Entries within UniProt protein P04637
# URL equivalent: /entry/interpro/protein/uniprot/P04637
uv run ./scripts/interpro_client.py fetch entry
    --source_db interpro
    --linked_endpoint protein
    --linked_source_db uniprot
    --linked_accession P04637
    --output p04637_domains.jsonl
```

### 2. Fetching all PDB structures for an Entry

```bash
# URL equivalent: /structure/pdb/entry/interpro/IPR011615
# Only fetch the first 5 structures
uv run ./scripts/interpro_client.py fetch structure
    --source_db pdb
    --linked_endpoint entry
    --linked_source_db interpro
    --linked_accession IPR011615
    --output ipr011615_structures.jsonl
```
