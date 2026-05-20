---
name: cellphonedb
description: Guide for using CellphoneDB v5 to infer cell-cell communication from single-cell transcriptomics data. Covers installation, running all three analysis methods (basic means, statistical permutation, DEG-based), preparing inputs (counts, metadata, DEGs, microenvironments, active TFs), interpreting outputs (means, p-values, significant_means, deconvoluted, interaction_scores), querying results, CellSign module, scoring module, custom database creation, and visualization with ktplotspy. Use this skill whenever the user mentions CellphoneDB, cell-cell interactions, ligand-receptor analysis, receptor-ligand inference, cell communication analysis, cell signaling from scRNA-seq, or wants to identify interacting cell type pairs and their molecular mediators. Also trigger when users want to plot or visualize CellphoneDB results, create dot plots or heatmaps of interactions, or query specific interactions between cell types.
---

# CellphoneDB v5 — Cell-Cell Communication Analysis

CellphoneDB is a publicly available repository of **HUMAN** curated receptors, ligands and their interactions, paired with a computational tool to interrogate single-cell transcriptomics data. It accurately represents heteromeric complexes (multi-subunit receptors/ligands) and includes non-peptidic molecule interactions via biosynthetic pathway proxies.

> **Important**: CellphoneDB works with **HUMAN** gene identifiers only. For other species (e.g., mouse), convert gene IDs to human orthologues first.

## Installation

```bash
# Create isolated environment
conda create -n cpdb python=3.8
conda activate cpdb

# Install
pip install cellphonedb

# For Jupyter support
pip install -U ipykernel
python -m ipykernel install --user --name 'cpdb'
```

Also install visualization tools:
```bash
pip install ktplotspy  # Python plotting for CellphoneDB results
```

## Database Setup

Download the CellphoneDB database before running analyses:

```python
from cellphonedb.utils import db_utils

# Download latest database
db_utils.download_database(cpdb_target_dir="./cpdb_data")

# List available versions
from cellphonedb.utils import db_releases_utils
from IPython.display import HTML, display
display(HTML(db_releases_utils.get_remote_database_versions_html()['db_releases_html_table']))

# Download specific version
db_utils.download_database(cpdb_target_dir="./cpdb_data", cpdb_version="v5.0.0")
```

The database downloads as a `.zip` file. CellphoneDB v5 requires database version ≥4.1.0.

## Preparing Inputs

### Counts File (mandatory)
Formats accepted: `.h5ad` (recommended), `.h5`, 10x mtx/barcode/features folder, or `.txt`.

- Gene IDs must be HUMAN
- Default assumption is Ensembl IDs; if using gene symbols add `counts_data='hgnc_symbol'`

### Meta File (mandatory)
Two-column file mapping cells to cell types:
- Column 1: `Cell` (barcode/cell name)
- Column 2: `cell_type` (cluster annotation)
- Formats: `.csv`, `.txt`, `.tsv`, `.tab`, `.pickle`

### DEGs File (optional — required for Method 3)
Two-column file: cell type name + significant gene ID. The user designs the DEG analysis appropriate to their research question.

### Microenvironments File (optional)
Two-column file: cell type + microenvironment name. Restricts cell-type pairs to those co-existing in a microenvironment.

### Active TFs File (optional — for CellSign)
Two-column file: cell type + active transcription factor name.

> **Data format warnings**:
> - Do NOT use numeric cell type names
> - Do NOT use dashes (`-`) in cell names

## Three Analysis Methods

### Method 1: Basic Means (`cpdb_analysis_method`)
No significance testing. Returns mean expression for each interaction in each cell-type pair.

```python
from cellphonedb.src.core.methods import cpdb_analysis_method

cpdb_results = cpdb_analysis_method.call(
    cpdb_file_path = "cellphonedb.zip",
    meta_file_path = "meta.txt",
    counts_file_path = "counts.h5ad",
    counts_data = 'hgnc_symbol',
    score_interactions = True,
    output_path = "out"
)
```

**Output**: `means.csv`, `deconvoluted.csv`

### Method 2: Statistical Analysis (`cpdb_statistical_analysis_method`)
Permutation-based test for enrichment of receptor-ligand interactions between cell types. Randomly permutes cluster labels (default 1000 iterations) to build null distributions.

```python
from cellphonedb.src.core.methods import cpdb_statistical_analysis_method

cpdb_results = cpdb_statistical_analysis_method.call(
    cpdb_file_path = "cellphonedb.zip",
    meta_file_path = "meta.txt",
    counts_file_path = "counts.h5ad",
    counts_data = 'hgnc_symbol',
    score_interactions = True,
    active_tfs_file_path = "active_tf.txt",       # optional
    microenvs_file_path = "microenvs.txt",          # optional
    threshold = 0.1,
    output_path = "out"
)
```

**Output**: `means.csv`, `pvalues.csv`, `significant_means.csv`, `deconvoluted.csv`

### Method 3: DEG-Based Analysis (`cpdb_degs_analysis_method`)
Retrieves interactions where all genes are expressed AND at least one is differentially expressed (user-provided DEGs).

```python
from cellphonedb.src.core.methods import cpdb_degs_analysis_method

cpdb_results = cpdb_degs_analysis_method.call(
    cpdb_file_path = "cellphonedb.zip",
    meta_file_path = "meta.txt",
    counts_file_path = "counts.h5ad",
    degs_file_path = "degs.txt",
    counts_data = 'hgnc_symbol',
    score_interactions = True,
    active_tfs_file_path = "active_tf.txt",       # optional
    microenvs_file_path = "microenvs.txt",          # optional
    threshold = 0.1,
    output_path = "out"
)
```

**Output**: `means.csv`, `relevant_interactions.csv`, `significant_means.csv`, `deconvoluted.csv`

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `counts_data` | Gene ID type: `ensembl`, `gene_name`, or `hgnc_symbol` | `ensembl` |
| `threshold` | Min fraction of cells expressing gene | `0.1` |
| `iterations` | Permutations for statistical method | `1000` |
| `threads` | Number of threads | `4` |
| `pvalue` | P-value cutoff for significance | `0.05` |
| `score_interactions` | Enable interaction scoring | `False` |
| `result_precision` | Decimal digits in output | `3` |
| `subsampling` | Enable geometric sketching subsampling | `False` |
| `debug_seed` | Random seed (`-1` to disable) | `-1` |

## Output Files

For detailed schema, see `references/output_schema.md`.

All output files (except deconvoluted) have:
- **Rows**: interacting protein pairs
- **Columns**: cell-type pairs (e.g., `clusterA|clusterB`)

Key files:
- **`means.csv`**: Mean expression for each interaction in each cell-pair
- **`pvalues.csv`**: P-values for interaction specificity (Method 2)
- **`significant_means.csv`**: Means only where significant/relevant; ranked by `rank` column
- **`relevant_interactions.csv`**: Binary matrix of DEG-relevant interactions (Method 3)
- **`deconvoluted.csv`**: Per-gene breakdown of complex subunit expression
- **`interaction_scores.csv`**: Specificity-based interaction ranking (if `score_interactions=True`)

> **Interactions are NOT symmetric**: `clusterA|clusterB` ≠ `clusterB|clusterA`. Partner A expression is from the first cluster, partner B from the second.

## Querying Results

```python
from cellphonedb.utils import search_utils

search_results = search_utils.search_analysis_results(
    query_cell_types_1 = ['T cells', 'NK cells'],
    query_cell_types_2 = ['Macrophages', 'Dendritic cells'],
    query_genes = ['CD274', 'PDCD1'],
    query_interactions = ['PD-L1_PD-1'],
    significant_means = cpdb_results['significant_means'],
    deconvoluted = cpdb_results['cpdb_deconvoluted'],
    interaction_scores = cpdb_results['interaction_scores'],  # optional
    query_minimum_score = 50,
    query_classifications = ['checkpoint'],  # optional pathway filter
    separator = '|',
    long_format = True
)
```

## CellSign Module (v5)

Leverages transcription factor activity downstream of receptors. Requires:
1. `active_tfs_file_path` — user-provided active TFs per cell type
2. TF activity can be estimated via DoRothEA, ChromVAR, SCENIC, or gene expression

The module highlights interactions where the downstream TF is active, adding biological confidence.

## Scoring Module (v5)

Ranks interactions by expression specificity:
1. Excludes lowly expressed genes
2. Calculates mean expression per gene per cell type  
3. Aggregates complex subunits via geometric mean
4. Scales expression 0–10 across cell types
5. Computes product of scaled values as interaction score

> Requires **log-normalized** expression data. Avoid z-scaling that transforms zeros.

## Visualization

For plotting, see `references/visualization.md` for detailed examples.

Recommended tools:
- **ktplotspy** (Python): `pip install ktplotspy`
- **ktplots** (R): `install.packages("ktplots")`

Quick examples:
```python
import ktplotspy as kpy

# Dot plot of interactions
kpy.plot_cpdb(
    adata=adata,
    cell_type1="T cells",
    cell_type2="Macrophages",
    means=cpdb_results['significant_means'],
    pvals=cpdb_results['pvalues'],
    celltype_key="cell_type",
    genes=["CD274", "PDCD1"]
)

# Heatmap of interaction counts
kpy.plot_cpdb_heatmap(pvals=cpdb_results['pvalues'])
```

## Custom Database

```python
from cellphonedb.utils import db_utils

# Download and modify the database files, then:
db_utils.create_db(cpdb_input_dir="./custom_db_inputs")
# Output: cellphonedb_{datetime}.zip in ./custom_db_inputs/out/
```

Do not rename the input files — CellphoneDB expects specific filenames.

## Common Pitfalls

1. **Non-human genes**: Always convert to human orthologues
2. **Wrong `counts_data`**: Specify `hgnc_symbol` if not using Ensembl
3. **Numeric cell type names**: Causes parsing errors
4. **Dashes in cell names**: Use underscores instead
5. **Asymmetric results confusion**: Remember partner A → first cluster, partner B → second cluster
6. **DEGs not filtered**: CellphoneDB uses ALL genes in the DEGs file — pre-filter with appropriate cutoffs
7. **Scoring with normalized data**: Use log-normalized counts; avoid transformations that alter zeros

## Citations

When using CellphoneDB, cite the relevant version:
- **v5**: Troule et al. Nat Protocols 2025
- **v4**: Garcia-Alonso, Lorenzi et al. Nature 2022
- **v3**: Garcia-Alonso et al. Nature Genetics 2021
- **v2**: Efremova et al. Nat Protoc 2020
- **v1**: Vento-Tormo, Efremova et al. Nature 2018
