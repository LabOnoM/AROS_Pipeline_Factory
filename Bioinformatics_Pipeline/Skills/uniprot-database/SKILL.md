---
name: uniprot-database
description: Access protein metadata, function, taxonomy, and sequences across UniProtKB,
  UniParc, and UniRef. Use when searching for proteins, mapping identifiers, or retrieving
  functional annotations and publications. Don't use for sequence alignment, protein
  folding, or sequence similarity search (use specialized skills for those tasks).
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

Map protein identifiers between different database systems and retrieve multiple entries efficiently.

**ID Mapping workflow:**
1. Submit mapping job to: `https://rest.uniprot.org/idmapping/run`
2. Check job status: `https://rest.uniprot.org/idmapping/status/{jobId}`
3. Retrieve results: `https://rest.uniprot.org/idmapping/results/{jobId}`

**Supported databases for mapping:**
- UniProtKB AC/ID
- Gene names
- Ensembl, RefSeq, EMBL
- PDB, AlphaFoldDB
- KEGG, GO terms
- And many more (see `/references/id_mapping_databases.md`)

**Limitations:**
- Maximum 100,000 IDs per job
- Results stored for 7 days

### 4. Streaming Large Result Sets

For large queries that exceed pagination limits, use the stream endpoint:

`https://rest.uniprot.org/uniprotkb/stream?query={query}&format={format}`

The stream endpoint returns all results without pagination, suitable for downloading complete datasets.

### 5. Customizing Retrieved Fields

Specify exactly which fields to retrieve for efficient data transfer.

**Common fields:**
- `accession` - UniProt accession number
- `id` - Entry name
- `gene_names` - Gene name(s)
- `organism_name` - Organism
- `protein_name` - Protein names
- `sequence` - Amino acid sequence
- `length` - Sequence length
- `go_*` - Gene Ontology annotations
- `cc_*` - Comment fields (function, interaction, etc.)
- `ft_*` - Feature annotations (domains, sites, etc.)

**Example:** `https://rest.uniprot.org/uniprotkb/search?query=insulin&fields=accession,gene_names,organism_name,length,sequence&format=tsv`

See `/references/api_fields.md` for complete field list.

## Example Usage

```python
import time
import requests

BASE = "https://rest.uniprot.org"

def search_protein(query: str, fmt: str = "json", size: int = 5):
    """
    Search UniProtKB using Lucene-style query syntax.
    """
    url = f"{BASE}/uniprotkb/search"
    params = {"query": query, "format": fmt, "size": size}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json() if fmt == "json" else r.text

def retrieve_entry(accession: str, fmt: str = "json"):
    """
    Retrieve a UniProtKB entry by accession.
    """
    url = f"{BASE}/uniprotkb/{accession}"
    params = {"format": fmt}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json() if fmt == "json" else r.text

def id_mapping(from_db: str, to_db: str, ids, poll_interval_s: float = 1.0):
    """
    Map identifiers using UniProt ID Mapping.
    ids can be a list of strings or a comma-separated string.
    """
    if isinstance(ids, (list, tuple)):
        ids = ",".join(ids)

    # 1) Submit mapping job
    submit_url = f"{BASE}/idmapping/run"
    r = requests.post(
        submit_url,
        data={"from": from_db, "to": to_db, "ids": ids},
        timeout=30,
    )
    r.raise_for_status()
    job_id = r.json()["jobId"]

    # 2) Poll job status
    status_url = f"{BASE}/idmapping/status/{job_id}"
    while True:
        s = requests.get(status_url, timeout=30)
        s.raise_for_status()
        payload = s.json()
        if payload.get("jobStatus") in (None, "FINISHED"):
            break
        if payload.get("jobStatus") == "FAILED":
            raise RuntimeError(f"ID mapping failed: {payload}")
        time.sleep(poll_interval_s)

    # 3) Fetch results (JSON)
    results_url = f"{BASE}/idmapping/results/{job_id}"
    res = requests.get(results_url, params={"format": "json"}, timeout=30)
    res.raise_for_status()
    return res.json()

if __name__ == "__main__":
    # Search example: human BRCA1
    search = search_protein("gene:BRCA1 AND organism_id:9606", size=3)
    print("Search results (first accessions):",
          [item["primaryAccession"] for item in search.get("results", [])])

    # Retrieve entry example
    entry = retrieve_entry("P38398")  # UniProt accession for human BRCA1 (example)
    print("Entry primaryAccession:", entry.get("primaryAccession"))
    print("Protein name:", entry.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value"))

    # ID mapping example: gene name -> UniProtKB
    mapping = id_mapping(from_db="Gene_Name", to_db="UniProtKB", ids=["BRCA1"])
    print("Mapping results keys:", mapping.keys())
```

## Implementation Details

- **Search Protein**
  - Uses `GET /uniprotkb/search`
  - Key parameters:
    - `query`: Lucene-style query string (see `references/query_syntax.md`)
    - `format`: output format (default `json`)
    - Optional common parameters: `size`, `fields`, `sort`
  - Returns parsed JSON when `format=json`, otherwise raw text.

- **Retrieve Entry**
  - Uses `GET /uniprotkb/{accession}`
  - Key parameters:
    - `accession`: UniProt accession (e.g., `P12345`)
    - `format`: output format (default `json`)
  - Suitable for fetching full record details for a known accession.

- **ID Mapping**
  - Uses UniProt asynchronous mapping workflow:
    1. `POST /idmapping/run` with `from`, `to`, `ids`
    2. Poll `GET /idmapping/status/{jobId}` until finished
    3. Fetch `GET /idmapping/results/{jobId}?format=json`
  - `ids` accepts either a list or a comma-separated string.
  - Recommended parameters:
    - `poll_interval_s`: controls polling frequency to avoid excessive requests.
  - `from_db` / `to_db` must match UniProt-supported database identifiers (consult UniProt mapping documentation as needed).

## Query Syntax Examples

```
kinase AND organism_name:human
(diabetes OR insulin) AND reviewed:true
cancer NOT lung
```

```
gene:BRCA1
accession:P12345
organism_id:9606
taxonomy_name:"Homo sapiens"
annotation:(type:signal)
```

```
length:[100 TO 500]
mass:[50000 TO 100000]
```

```
gene:BRCA*
protein_name:kinase*
```

See `/references/query_syntax.md` for comprehensive syntax documentation.

## Best Practices

1. **Use reviewed entries when possible**: Filter with `reviewed:true` for Swiss-Prot (manually curated) entries.
2. **Specify format explicitly**: Choose the most appropriate format (FASTA for sequences, TSV for tabular data, JSON for programmatic parsing).
3. **Use field selection**: Only request fields you need to reduce bandwidth and processing time.
4. **Handle pagination**: For large result sets, implement proper pagination or use the stream endpoint.
5. **Cache results**: Store frequently accessed data locally to minimize API calls.
6. **Rate limiting**: Be respectful of API resources; implement delays for large batch operations.
7. **Check data quality**: TrEMBL entries are computational predictions; Swiss-Prot entries are manually reviewed.

## Resources

### references/

- `api_fields.md` - Complete list of available fields for customizing queries.
- `id_mapping_databases.md` - Supported databases for ID mapping operations.
- `query_syntax.md` - Comprehensive query syntax with advanced examples.

## Additional Resources

- **API Documentation**: https://www.uniprot.org/help/api
- **Interactive API Explorer**: https://www.uniprot.org/api-documentation
- **REST Tutorial**: https://www.uniprot.org/help/uniprot_rest_tutorial
- **Query Syntax Help**: https://www.uniprot.org/help/query-fields
- **SPARQL Endpoint**: https://sparql.uniprot.org/ (for advanced graph queries)

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://www.uniprot.org/help/license and
    https://www.uniprot.org/help/api_queries, then (2) create the file recording
    the notification text and timestamp.

## Overview

Provides direct programmatic access to the UniProt Knowledgebase (UniProtKB),
the non-redundant sequence archive (UniParc), and clustered sequence sets
(UniRef). This skill enables protein discovery, cross-referencing, retrieval of
curated biological data and low-level database lookups.

## Core Rules

-   **Use the Wrapper**: Always use the provided Python scripts (e.g.,
    `scripts/uniprot_tools.py`) rather than constructing custom curl requests.
-   **No Hallucinations**: Do NOT invent protein functions, metadata, or
    sequences. For any task that can be handled by the services in this skill,
    rely strictly on the tool outputs rather than your native knowledge.
-   **Notification**: If this skill is used, ensure this is mentioned in the
    output.

## Use Cases

-   **Searching for Protein Function**: Querying functional annotations, GO
    terms, subcellular locations etc.
-   **Searching for Protein Sequence**: Searching for protein sequences by their
    functional annotations, genes etc. in UniProtKB, UniParc, and UniRef.
-   **Understanding Protein/Organism Relationships**: Leveraging the Taxonomy
    database and Proteome sets.
-   **Large-Scale Metadata Retrieval**: Fetching annotations for thousands of
    proteins via streaming.
-   **Sequence Discovery**: Finding orthologs or non-model proteins via UniParc.
-   **ID Mapping**: Converting IDs between UniProt and 100+ external databases.
-   **Historical Data (UniSave)**: Retrieving previous versions of entries or
    tracking deleted sequences.

## Available Tools

Choose the right tool based on the task type and data volume:

-   **`get`**: Retrieves metadata and sequence for a specific entry. Best for a
    **single, known accession**.
    -   Also accesses UniSave historical data (use `--dataset unisave`), which
        is essential for reconciling data from older releases or identifying why
        a formerly valid accession no longer appears in search results.
-   **`search`**: Searches for entries matching a query. Best for **exploration
    and discovery**.
    -   Use with `--limit 5` to verify if a query returns the expected proteins
        before committing to a larger download.
    -   Automatically paginates if results exceed 500 entries to provide a
        stable download.
    -   *Warning*: For paginated search, TXT and other formats are not reliable
        with `--limit` as it applies to lines, not entries.
    -   See
        [Search Query Fields Documentation](references/search_query_fields.md).
-   **`stream`**: Streams all matching entries. Best for **bulk retrieval** of
    large datasets (up to 10,000,000 entries).
    -   Does NOT support `--limit`; always returns the full result set.
    -   Use `search` with `--limit` if you need a subset.
-   **`count`**: Counts entries matching a query. Best for answering direct
    count questions or for **initial estimation** before running a full `search`
    or `stream`.
-   **`sparql`**: Executes graph queries for complex discovery. Best for
    counting, exact sequence matches, and multi-database queries.
    -   See [SPARQL Examples](references/sparql_examples.md).
-   **`map`**: Converts IDs between UniProt and 100+ databases. Best for ID
    mapping tasks.
    -   See [ID Mapping Documentation](references/id_mapping_documentation.md).
    -   **`search` vs. `map`**: Try `search` first before resorting to `map` if
        not explicitly requested by the user. E.g., an external ID might be
        searchable in UniParc but fail to map to UniProtKB.

## Workflows

### Typical Protein Research Workflow

Copy this checklist and track progress:

-   [ ] Step 1: Identify target protein(s) and organism(s).
-   [ ] Step 2: Search UniProtKB for reviewed entries (`reviewed:true`).
-   [ ] Step 3: If no reviewed entries, search unreviewed or use UniParc for
    sequence discovery.
-   [ ] Step 4: Map external IDs (e.g., Ensembl, PDB) to UniProt Accessions if
    necessary.
-   [ ] Step 5: Retrieve functional metadata or sequence in desired format
    (JSON, FASTA).

### Handling Search Misses (e.g. Gene Search in Non-Model Organisms)

If a direct query (e.g., `gene:SYMBOL`) fails:

1.  **Pivot to Protein Name**: Search for the common protein name (e.g.,
    `protein_name:Alpha-crystallin A`).
2.  **Use UniParc**: Search the UniParc dataset, which integrates sequences from
    across all of life, even if they aren't fully annotated in UniProtKB.
3.  **Check Orthologs/Canonical**: Resolve the Human/Mouse ortholog first to
    find the correct naming/mnemonic.

### Bulk Retrieval Priorities

> [!IMPORTANT] Always prefer **`stream`** or **`sparql`** for bulk data.
> `search` is suitable for exploration; if results exceed 500 entries, it
> automatically paginates to provide a stable download.

-   **Priority 0: `count`**: ALWAYS check the result count before running a
    `search` or `stream`.
-   **Priority 1: `stream`**: The primary method for bulk data retrieval (up to
    10M entries). Does NOT support `--limit`; always returns all results.
-   **Priority 2: `sparql`**: Best for complex filtering and exact matching
    during retrieval.

### Sequence-Based Search (Exact Match)

> [!IMPORTANT] Use **SPARQL** when searching for a protein by its full amino
> acid sequence. The REST API `/search` endpoint does not support direct
> sequence-string lookups. For any non-exact match use specialized sequence
> similarity search skills. Use UniParc if you cannot find query in UniProt.

**SPARQL Query Pattern (UniProt):**

```text
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?protein ?name WHERE {
  ?protein a up:Protein ;
           up:sequence/rdf:value "SEQUENCE_HERE" .
  OPTIONAL {
    ?protein up:recommendedName/up:fullName ?name .
  }
}
```

**SPARQL Query Pattern (UniParc):**

```text
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?uniparc ?val WHERE {
  GRAPH <http://sparql.uniprot.org/uniparc> {
    ?uniparc a up:Sequence ;
             rdf:value ?val .
    FILTER (?val = "SEQUENCE_HERE")
  }
}
```

### Counting Entries Efficiently

> [!IMPORTANT] Use **`count`** or **`SPARQL`** for counting entries (e.g., "How
> many proteins in Human?").

**Counting Pattern (Proteins per Organism):**

```text
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX taxon: <http://purl.uniprot.org/taxonomy/>
SELECT (COUNT(?protein) AS ?count) WHERE {
  ?protein a up:Protein ;
           up:reviewed true ;
           up:organism taxon:9606 .
}
```

### REST Search Syntax

-   **No Commas in Lists**: Commas are treated as literals. Use capitalized `OR`
    to separate items.
    *   Grouped: `accession:(P12345 OR P67890)`
    *   Repeated: `accession:P12345 OR accession:P67890`
-   **Space = AND**: E.g., `gene:p53 human` searches for both.

## Example Commands

Below are example commands for each mode of `uniprot_tools.py`.

Count total number of entries for a given query.

```bash
uv run scripts/uniprot_tools.py count "taxonomy_id:9606"
```

Search for entries.

```bash
uv run scripts/uniprot_tools.py search "gene:p53 AND reviewed:true" --limit 5
```

Retrieve a single entry by accession.

```bash
uv run scripts/uniprot_tools.py get P04637
```

Retrieve Historical/Deleted Entry (UniSave).

```bash
uv run scripts/uniprot_tools.py get P04637 --dataset unisave
```

Stream large result sets for bulk retrieval (returns ALL matched entries, no
`--limit` support).

```bash
uv run scripts/uniprot_tools.py stream "taxonomy_id:9606 AND reviewed:true" --format tsv --fields accession,gene_names > human_reviewed.tsv
```

Map IDs from one database to another.

```bash
uv run scripts/uniprot_tools.py map "P04637" --from_db UniProtKB_AC-ID --to_db Gene_Name
```

Execute graph queries with SPARQL.

```bash
uv run scripts/uniprot_tools.py sparql 'PREFIX up: <http://purl.uniprot.org/core/> SELECT ?protein WHERE { ?protein a up:Protein ; up:reviewed true . } LIMIT 5'
```

## Common Mistakes

-   **Using `name:` instead of `protein_name:`**: `name:` is not a supported
    query term, use `protein_name:` instead.
-   **Ignoring UniParc**: Non-model organisms might only exist in UniParc.
-   **Confusing Accession with UPI**: UniProtKB Accessions (e.g., `P04637`) are
    linked to functional metadata; UniParc IDs (`UPI...`) are for sequences
    only. You can find cross-references from UniParc IDs to UniProtKB Accessions
    using the ID Mapping tool.
-   **Using UniProtKB-AC as Target in ID Mapping**: Use `UniProtKB` instead.
-   **Giving up on Complex Queries**: If a complex search query fails, try to
    use SPARQL instead of giving up.
-   **Using IDs Without Verifying Meaning**: NEVER assume you know the meaning
    of an ID (e.g. keyword, GO term, Pfam ID etc.). ALWAYS look up the natural
    language description/meaning of an ID in UniProt before using it for search
    to ensure it matches your intended search term.
-   **Ignoring Citation Noise in Broad Searches**: Broad text searches (`search
    "term"`) frequently return false positives (e.g., common maintenance
    proteins) because UniProt searches full metadata, including publication
    titles. ALWAYS prefer field-specific filters like `cc_function:` or
    `protein_name:` for functional discovery.
-   **Forgetting to Quote Short Search Terms**: Short, unquoted terms (e.g.,
    `lanM`) can match substrings in organism names (e.g., *Lan*cefieldella) or
    other fields. Use quotes and field prefixes (e.g., `gene:lanM`) to isolate
    true hits.
-   **Manipulating Protein Sequences Directly**: Always use code and tools for
    sequence-based operations. Do not attempt to edit, truncate, or modify
    protein sequences manually.
-   **Over-using Search for Bulk Data**: DO NOT use `search` for retrieving
    millions of entries if `stream` or `sparql` can do the job. Streaming is
    more efficient for very large datasets. Note that `stream` has a hard limit
    of 10,000,000 outputs and does NOT support `--limit`.
-   **Forgetting to Check Data Volume**: ALWAYS perform a `count` before running
    a `search` without `--limit` or before using `stream`. Unlimited queries can
    take a long time and consume significant resources if millions of entries
    are returned.
-   **Using `--limit` with `stream`**: The `stream` command does NOT support
    `--limit`. If you need a limited number of results, use `search` with
    `--limit` instead.
-   **Forgetting the License Notice**: Do not neglect to state that the UniProt
    Database was used and to advise the user to review the licensing terms when
    presenting results for the **first time**. Even if the task is concise, this
    attribution is required in the first response containing UniProt data.

## Reference Materials

-   [SPARQL Examples](references/sparql_examples.md)
-   [Search Query Fields Documentation](references/search_query_fields.md)
-   [ID Mapping Documentation](references/id_mapping_documentation.md)
-   [UniProt Evidence Docs](https://www.uniprot.org/help/evidences)
-   **Underlying API Endpoints** (Used by `scripts/uniprot_tools.py`):
    -   `get`, `search`, `stream`, `count` -> `rest.uniprot.org/{dataset}/`
    -   `map` -> `rest.uniprot.org/idmapping/`
    -   `sparql` -> `sparql.uniprot.org/sparql`
    -   `get --dataset unisave` -> `rest.uniprot.org/unisave/`
