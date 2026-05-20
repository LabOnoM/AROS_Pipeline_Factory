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
result = client.map_ids(identifiers=['TP53', 'BRCA1', 'EGFR', 'MDM2'], species=9606)

# Map with multiple matches per query
result = client.map_id(identifier='p53', species=9606, limit=5)
```

**Parameters**:

-   `species`: NCBI taxon ID (9606 = human, 10090 = mouse, 7227 = fly)
-   `limit`: Number of matches per identifier (default: 1)
-   `identifier`: The identifier to map (string).
-   `identifiers`: A list of identifiers to map (list of strings).

**Best practice**: Always map identifiers first for faster subsequent queries.  Use STRING IDs when possible in subsequent calls.

### 2. Network Retrieval (`string_network`)

Get protein-protein interaction network data in tabular format.

**When to use**: Building interaction networks, analyzing connectivity, retrieving interaction evidence.

**Usage**:

```python
from scripts.string_api import StringClient
import pandas as pd

client = StringClient(caller_identity="my_analysis_tool")

# Map TP53 to STRING ID
tp53_id = client.map_id(identifier='TP53', species=9606)

# Get network for single protein
network_data = client.get_network(identifiers=[tp53_id], required_score=700)
network = pd.DataFrame(network_data)

# Get network with multiple proteins
proteins = ['9606.ENSP00000269305', '9606.ENSP00000275493']
network_data = client.get_network(identifiers=proteins, required_score=700)
network = pd.DataFrame(network_data)


# Expand network with additional interactors (example requires valid IDs)
#expanded_network = client.get_network(identifiers=[tp53_id], add_nodes=10, required_score=400) # Functionality moved to image download

# Physical interactions only (implementation detail - functional vs physical selection is handled internally by STRING, not an explicit parameter)
#physical_network = client.get_network(identifiers=[tp53_id]) # No way to pass specific network_type, requires filtering the result based on score.
```

**Parameters**:

-   `identifiers`: A list of STRING identifiers.
-   `required_score`: Confidence threshold (0-1000).
    -   150: low confidence (exploratory)
    -   400: medium confidence (default, standard analysis)
    -   700: high confidence (conservative)
    -   900: highest confidence (very stringent)
-   `add_nodes`: Number of additional nodes to add (0-10).

**Output**: A list of dictionaries, each representing an interaction. Each dictionary contains information about the interacting proteins, combined score, and individual evidence scores (neighborhood, fusion, coexpression, experimental, database, text-mining). The list can easily be converted to a Pandas DataFrame.

### 3. Network Visualization (`string_network_image`)

Generate network visualization as PNG image.

**When to use**: Creating figures, visual exploration, presentations.

**Usage**:

```python
from scripts.string_api import StringClient

client = StringClient(caller_identity="my_analysis_tool")

#Get the protein ID
protein_id = client.map_id(identifier='TP53', species=9606)

# Get network image
proteins = [protein_id]
client.get_network_image(identifiers=proteins, species=9606, required_score=700, output_file='network.png')

#Get multiple protein IDs
proteins = client.map_ids(identifiers=['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1'], species=9606)

#Evidence-colored network (evidence information encoded in line colors by default)
client.get_network_image(identifiers=proteins, species=9606, output_file='network_evidence.png')

#Expanding with 10 more partners
client.get_network_image(identifiers=proteins, species=9606, add_color_nodes=10, output_file='network_expanded.png')
```

**Parameters**:

-   `identifiers`: A list of STRING identifiers.
-   `species`: NCBI taxon ID.
-   `required_score`: Confidence threshold (0-1000).
-   `network_flavor`:  STRING uses a default evidence colored network.
-   `add_color_nodes`: Add N most connected proteins. Colors are added to the nodes.
-   `output_file`: File path to save the PNG image.

### 4. Interaction Partners (`string_interaction_partners`)

Find all proteins that interact with given protein(s).

**When to use**: Discovering novel interactions, finding hub proteins, expanding networks.

**Usage**:

```python
from scripts.string_api import StringClient

client = StringClient(caller_identity="my_analysis_tool")

# Get top 10 interactors of TP53
partners = client.get_interaction_partners(identifier='TP53', species=9606, limit=10)

# Get high-confidence interactors
partners = client.get_interaction_partners(identifier='TP53', species=9606, limit=20, required_score=700)

# Find interactors for multiple proteins
partners = client.get_interaction_partners(identifier=['TP53', 'MDM2'], species=9606, limit=15)
```

**Parameters**:

-   `identifier`: The protein identifier to search for interaction partners.
-   `identifiers`: A list of identifiers to search for interaction partners.
-   `species`: NCBI taxon ID.
-   `limit`: Maximum number of partners to return (default: 10).
-   `required_score`: Confidence threshold (0-1000).

**Use cases**:

-   Hub protein identification
-   Network expansion from seed proteins
-   Discovering indirect connections

### 5. Functional Enrichment (`string_enrichment`)

Perform enrichment analysis across Gene Ontology, KEGG pathways, Reactome and more.

**When to use**: Interpreting protein lists, pathway analysis, functional characterization, understanding biological processes.

**Usage**:

```python
from scripts.string_api import StringClient
import pandas as pd
import io

client = StringClient(caller_identity="my_analysis_tool")

# Enrichment for a protein list
proteins = ['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1', 'ATR', 'TP73']
enrichment_data = client.get_enrichment(identifiers=proteins, species=9606)

# Convert to TSV format for easier parsing
enrichment_tsv = client.convert_enrichment_to_tsv(enrichment_data)

# Parse results to find significant terms
df = pd.read_csv(io.StringIO(enrichment_tsv), sep='\t')
significant = df[df['fdr'] < 0.05]
```

**Enrichment categories**:

-   **Gene Ontology**: Biological Process, Molecular Function, Cellular Component
-   **KEGG Pathways**: Metabolic and signaling pathways
-   **Reactome Pathways**: Biological pathways
-   **Pfam**: Protein domains
-   **InterPro**: Protein families and domains
-   **SMART**: Domain architecture
-   **UniProt Keywords**: Curated functional keywords

**Output**: A TSV formatted string containing:

-   `category`: Annotation database (e.g., "KEGG Pathways", "GO Biological Process")
-   `term`: Term identifier
-   `description`: Human-readable term description
-   `number_of_genes`: Input proteins with this annotation
-   `p_value`: Uncorrected enrichment p-value
-   `fdr`: False discovery rate (corrected p-value)

**Statistical method**: Fisher's exact test with Benjamini-Hochberg FDR correction.

**Interpretation**: FDR < 0.05 indicates statistically significant enrichment.

### 6. PPI Enrichment (`string_ppi_enrichment`)

Test if a protein network has significantly more interactions than expected by chance.

**When to use**: Validating if proteins form functional module, testing network connectivity.

**Usage**:

```python
from scripts.string_api import StringClient

client = StringClient(caller_identity="my_analysis_tool")

# Test network connectivity
proteins = ['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1']
result = client.get_ppi_enrichment(identifiers=proteins, species=9606, required_score=400)

print(f"Observed edges: {result['number_of_edges']}")
print(f"Expected edges: {result['expected_number_of_edges']}")
print(f"P-value: {result['p_value']}")
```

**Parameters**:

-   `identifiers`: List of STRING identifiers.
-   `species`: NCBI taxon ID.
-   `required_score`: Confidence score.

**Output**: A dictionary containing:

-   `number_of_nodes`: Proteins in network
-   `number_of_edges`: Observed interactions
-   `expected_number_of_edges`: Expected in random network
-   `p_value`: Statistical significance

**Interpretation**:

-   p-value < 0.05: Network is significantly enriched (proteins likely form functional module)
-   p-value ≥ 0.05: No significant enrichment (proteins may be unrelated)

### 7. Homology Scores (`string_homology`)

Retrieve protein similarity and homology information.

**When to use**: Identifying protein families, paralog analysis, cross-species comparisons.

**Usage**:

```python
from scripts.string_api import StringClient

client = StringClient(caller_identity="my_analysis_tool")

# Get homology between proteins
proteins = ['TP53', 'TP63', 'TP73']  # p53 family
homology = client.get_homology(identifiers=proteins, species=9606)
```

**Parameters**:

-   `identifiers`: List of protein identifiers.
-   `species`: NCBI Taxon ID.

**Use cases**:

-   Protein family identification
-   Paralog discovery
-   Evolutionary analysis

### 8. Version Information (`string_version`)

Get current STRING database version.

**When to use**: Ensuring reproducibility, documenting methods.

**Usage**:

```python
from scripts.string_api import StringClient

client = StringClient(caller_identity="my_analysis_tool")
version = client.get_string_version()
print(f"STRING version: {version}")
```

## Common Analysis Workflows

### Workflow 1: Protein List Analysis (Standard Workflow)

**Use case**: Analyze a list of proteins from experiment (e.g., differential expression, proteomics).

```python
from scripts.string_api import StringClient
import pandas as pd
import io

client = StringClient(caller_identity="my_analysis_tool")

# Step 1: Map gene names to STRING IDs
gene_list = ['TP53', 'BRCA1', 'ATM', 'CHEK2', 'MDM2', 'ATR', 'BRCA2']
mapping = client.map_ids(identifiers=gene_list, species=9606)

# Step 2: Get interaction network
network = client.get_network(identifiers=gene_list, species=9606, required_score=400)

# Step 3: Test if network is enriched
ppi_result = client.get_ppi_enrichment(identifiers=gene_list, species=9606, required_score=400)

# Step 4: Perform functional enrichment
enrichment_data = client.get_enrichment(identifiers=gene_list, species=9606)
enrichment = client.convert_enrichment_to_tsv(enrichment_data)

# Step 5: Generate network visualization
client.get_network_image(identifiers=gene_list, species=9606, required_score=400, output_file='protein_network.png')

# Step 6: Parse and interpret results
```

### Workflow 2: Single Protein Investigation

**Use case**: Deep dive into one protein's interactions and partners.

```python
from scripts.string_api import StringClient

client = StringClient(caller_identity="my_analysis_tool")

# Step 1: Map protein name
protein = 'TP53'
mapping = client.map_id(identifier=protein, species=9606)

# Step 2: Get all interaction partners
partners = client.get_interaction_partners(identifier=protein, species=9606, limit=20, required_score=700)

# Step 3: Visualize expanded network
client.get_network_image(identifiers=[protein], species=9606, add_color_nodes=15, required_score=700, output_file='tp53_network.png')
```

### Workflow 3: Pathway-Centric Analysis

**Use case**: Identify and visualize proteins in a specific biological pathway.

```python
from scripts.string_api import StringClient
import pandas as pd
import io

client = StringClient(caller_identity="my_analysis_tool")

# Step 1: Start with known pathway proteins
dna_repair_proteins = ['TP53', 'ATM', 'ATR', 'CHEK1', 'CHEK2', 'BRCA1', 'BRCA2', 'RAD51', 'XRCC1']

# Step 2: Get network
network = client.get_network(identifiers=dna_repair_proteins, species=9606, required_score=700)

# Step 3: Enrichment to confirm pathway annotation
enrichment_data = client.get_enrichment(identifiers=dna_repair_proteins, species=9606)
enrichment = client.convert_enrichment_to_tsv(enrichment_data)

# Step 4: Parse enrichment for DNA repair pathways
df = pd.read_csv(io.StringIO(enrichment), sep='\t')
dna_repair = df[df['description'].str.contains('DNA repair', case=False)]
```

### Workflow 4: Cross-Species Analysis

**Use case**: Compare protein interactions across different organisms.

```python
from scripts.string_api import StringClient

client = StringClient(caller_identity="my_analysis_tool")

# Human network
human_network = client.get_network(identifiers=['TP53'], species=9606, required_score=700)

# Mouse network (requires mapping Trp53 to mouse STRING ID)
mouse_network = client.get_network(identifiers=['10090.ENSMUSP00000000592'], species=10090, required_score=700) #Requires string id

# Yeast network (if ortholog exists) #Requires string id
#yeast_network = client.get_network(identifiers=['gene_name'], species=4932, required_score=700)
```

### Workflow 5: Network Expansion and Discovery

**Use case**: Start with seed proteins and discover connected functional modules.

```python
from scripts.string_api import StringClient
import pandas as pd
import io

client = StringClient(caller_identity="my_analysis_tool")

# Step 1: Start with seed protein(s)
seed_proteins = ['TP53']

# Step 2: Get first-degree interactors
partners_data = client.get_interaction_partners(identifiers=seed_proteins, species=9606, limit=30, required_score=700)

#Covert the data to dataframe format
partners_tsv = client.convert_interaction_partners_to_tsv(partners_data)

# Step 3: Parse partners to get protein list
df = pd.read_csv(io.StringIO(partners_tsv), sep='\t')

all_proteins = list(set(df['preferredName_A'].tolist() + df['preferredName_B'].tolist()))

# Step 4: Perform enrichment on expanded network
enrichment_data = client.get_enrichment(identifiers=all_proteins[:50], species=9606)
enrichment = client.convert_enrichment_to_tsv(enrichment_data)

# Step 5: Filter for interesting functional modules
enrichment_df = pd.read_csv(io.StringIO(enrichment), sep='\t')
modules = enrichment_df[enrichment_df['fdr'] < 0.001]
```

## Common Species

When specifying species, use NCBI taxon IDs:

| Organism              | Common Name | Taxon ID |
| --------------------- | ----------- | -------- |
| *Homo sapiens*        | Human       | 9606     |
| *Mus musculus*        | Mouse       | 10090    |
| *Rattus norvegicus*   | Rat         | 10116    |
| *Drosophila melanogaster* | Fruit fly | 7227     |
| *Caenorhabditis elegans* | *C. elegans* | 6239   |
| *Saccharomyces cerevisiae* | Yeast     | 4932     |
| *Arabidopsis thaliana* | Thale cress | 3702     |
| *Escherichia coli*    | *E. coli*   | 511145   |
| *Danio rerio*         | Zebrafish   | 7955     |

Full list available at: <https://string-db.org/cgi/input?input_page_active_form=organisms>

## Understanding Confidence Scores

STRING provides combined confidence scores (0-1000) integrating multiple evidence types:

### Evidence Channels

1.  **Neighborhood (nscore)**: Conserved genomic neighborhood across species
2.  **Fusion (fscore)**: Gene fusion events
3.  **Phylogenetic Profile (pscore)**: Co-occurrence patterns across species
4.  **Coexpression (ascore)**: Correlated RNA expression
5.  **Experimental (escore)**: Biochemical and genetic experiments
6.  **Database (dscore)**: Curated pathway and complex databases
7.  **Text-mining (tscore)**: Literature co-occurrence and NLP extraction

### Recommended Thresholds

Choose threshold based on analysis goals:

-   **150 (low confidence)**: Exploratory analysis, hypothesis generation
-   **400 (medium confidence)**: Standard analysis, balanced sensitivity/specificity
-   **700 (high confidence)**: Conservative analysis, high-confidence interactions
-   **900 (highest confidence)**: Very stringent, experimental evidence preferred

**Trade-offs**:

-   Lower thresholds: More interactions (higher recall, more false positives)
-   Higher thresholds: Fewer interactions (higher precision, more false negatives)

## Network Types

### Functional Networks (Default)

Includes all evidence types (experimental, computational, text-mining). Represents proteins that are functionally associated, even without direct physical binding.

**When to use**:

-   Pathway analysis
-   Functional enrichment studies
-   Systems biology
-   Most general analyses

### Physical Networks

Only includes evidence for direct physical binding (experimental data and database annotations for physical interactions).

**When to use**:

-   Structural biology studies
-   Protein complex analysis
-   Direct binding validation
-   When physical contact is required

## API Best Practices

1.  **Always map identifiers first**: Use `string_map_ids()` before other operations for faster queries
2.  **Use STRING IDs when possible**: Use format `9606.ENSP00000269305` instead of gene names
3.  **Specify species for networks >10 proteins**: Required for accurate results
4.  **Respect rate limits**: Wait 1 second between API calls
5.  **Use versioned URLs for reproducibility**: Available in reference documentation
6.  **Handle errors gracefully**: Check for "Error:" prefix in returned strings
7.  **Choose appropriate confidence thresholds**: Match threshold to analysis goals
8.  **Provide Caller Identity**: Provide a caller identity to the `StringClient` to support load management.

## Detailed Reference

For comprehensive API documentation, complete parameter lists, output formats, and advanced usage, refer to `references/string_reference.md`. This includes:

-   Complete API endpoint specifications
-   All supported output formats (TSV, JSON, XML, PSI-MI)
-   Advanced features (bulk upload, values/ranks enrichment)
-   Error handling and troubleshooting
-   Integration with other tools (Cytoscape, R, Python libraries)
-   Data license and citation information

## Troubleshooting

**No proteins found**:

-   Verify species parameter matches identifiers
-   Try mapping identifiers first with `string_map_ids()`
-   Check for typos in protein names

**Empty network results**:

-   Lower confidence threshold (`required_score`)
-   Check if proteins actually interact
-   Verify species is correct

**Timeout or slow queries**:

-   Reduce number of input proteins
-   Use STRING IDs instead of gene names
-   Split large queries into batches

**"Species required" error**:

-   Add `species` parameter for networks with >10 proteins
-   Always include species for consistency

**Results look unexpected**:

-   Check STRING version with `string_version()`
-   Review confidence threshold selection

## Additional Resources

For proteome-scale analysis or complete species network upload:

-   Visit <https://string-db.org>
-   Use "Upload proteome" feature
-   STRING will generate complete interaction network and predict functions

For bulk downloads of complete datasets:

-   Download page: <https://string-db.org/cgi/download>
-   Includes complete interaction files, protein annotations, and pathway mappings

## Data License

STRING data is freely available under **Creative Commons BY 4.0** license:

-   Free for academic and commercial use
-   Attribution required when publishing
-   Cite latest STRING publication

## Citation

When using STRING in publications, cite the most recent publication from: <https://string-db.org/cgi/about>

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


This skill allows you to query the STRING database programmatically using a
bundled Python CLI wrapper.

## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://string-db.org/cgi/access, then (2) create the file recording the
    notification text and timestamp.

## Core Rules

1.  **MANDATORY: Ask for Species First:** The STRING API requires NCBI Taxon
    IDs. **You MUST NOT guess or assume a species.** If the user does not
    explicitly state a species or Taxon ID, you MUST stop and ask: "Which
    species are you interested in? I need the NCBI Taxon ID to proceed." Even
    for well-known proteins like TP53, BRCA1, or MDM2 that are commonly
    associated with human studies, you MUST still ask — do not default to Human.
2.  **Never print output to stdout:** The `--output <file.tsv>` is required.
    Never read large outputs into context. Instead use jq, python or file
    operations (`grep`, `head`) to process large output.
3.  **Map Identifiers first:** If you only have common gene names (e.g.,
    'TP53'), map them to STRING IDs first as this guarantees much faster server
    responses. Use the `map` command for this.
4.  **Notification**: If this skill is used, ensure this is mentioned in the
    output.

## Tool Execution

The CLI is at `scripts/string_cli.py` and should be run using `uv run`:

```bash
uv run scripts/string_cli.py <command> [options] --output /tmp/out.tsv
```

## Feature Domains (Progressive Disclosure)

Read the following reference files based on the user's request:

*   **[Mapping Identifiers](references/mapping.md)** - Map common protein names
    to STRING IDs.
*   **[Interactions & Network](references/interactions.md)** - Find interacting
    proteins, network topologies, mediators, homology, and visual network
    images.
*   **[Enrichment & Functional Annotations](references/enrichment.md)** -
    Analyze pathway enrichment (GO, KEGG, Pfam), PPI significance, or find all
    proteins associated with a specific term (e.g. Melanoma).
*   **[Values/Ranks Enrichment](references/valuesranks.md)** - Submit full
    experimental datasets (e.g., logFC, p-values) for rank-based enrichment
    analysis using the async background API.

To begin, read the reference file most appropriate to the current task to
discover the correct CLI command.
