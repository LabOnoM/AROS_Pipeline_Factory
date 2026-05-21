# CellphoneDB Output File Schema

## Common Columns (all files except deconvoluted)

| Column | Description |
|--------|-------------|
| `id_cp_interaction` | Unique CellphoneDB interaction identifier |
| `interacting_pair` | Interacting partners separated by `\|` (e.g., `CD274\|PDCD1`) |
| `partner_a` | First partner ID (prefix: `simple:` for UniProt or `complex:` for complex) |
| `partner_b` | Second partner ID |
| `gene_a` | Gene identifier for partner A |
| `gene_b` | Gene identifier for partner B |
| `secreted` | `True` if one partner is secreted |
| `receptor_a` | `True` if partner A is annotated as receptor |
| `receptor_b` | `True` if partner B is annotated as receptor |
| `annotation_strategy` | `curated` or source database name |
| `is_integrin` | `True` if one partner is integrin |
| `classification` | Signaling pathway classification (v5) |

## File-Specific Columns

### means.csv
| Column | Description |
|--------|-------------|
| `clusterA\|clusterB` | Mean expression value: average of partner A mean in clusterA and partner B mean in clusterB. Set to 0 if either partner mean is 0. |

### pvalues.csv (Method 2 only)
| Column | Description |
|--------|-------------|
| `clusterA\|clusterB` | P-value for enrichment of this interaction in this cell pair. Lower = more cell-type specific. |

### significant_means.csv
| Column | Description |
|--------|-------------|
| `rank` | Number of significant p-values / number of comparisons. Lower rank = more broadly significant. |
| `clusterA\|clusterB` | Mean expression value if p < 0.05 (Method 2) or interaction is relevant (Method 3). Otherwise 0. |

### relevant_interactions.csv (Method 3 only)
| Column | Description |
|--------|-------------|
| `clusterA\|clusterB` | `1` if interaction is relevant (gene is DEG and all participants expressed), `0` otherwise. |

### deconvoluted.csv
Different structure — one row per gene per interaction:

| Column | Description |
|--------|-------------|
| `gene_name` | Gene identifier for a subunit |
| `uniprot` | UniProt identifier |
| `is_complex` | `True` if part of complex |
| `protein_name` | Protein name |
| `complex_name` | Complex name (empty if simple) |
| `id_cp_interaction` | Interaction identifier |
| `mean` (per cluster) | Mean expression of this gene in each cluster |

### interaction_scores.csv (if `score_interactions=True`)
Same structure as means/pvalues files. Values represent the specificity score (product of scaled expression values).

## Asymmetry of Results

**Critical**: Results are directional.

- `clusterA|clusterB`: partner A is expressed in clusterA, partner B in clusterB
- `clusterB|clusterA`: partner A is expressed in clusterB, partner B in clusterA
- These will have **different values**

For a ligand-receptor pair like `IL12|IL12R`:
- `T_cells|Macrophages` = IL12 in T cells, IL12R in Macrophages
- `Macrophages|T_cells` = IL12 in Macrophages, IL12R in T cells

## Accessing Results Programmatically

Results are returned as a dictionary of DataFrames:

```python
cpdb_results.keys()
# dict_keys(['means', 'pvalues', 'significant_means', 'cpdb_deconvoluted', 'interaction_scores'])

# Access individual results
means_df = cpdb_results['means']
pvals_df = cpdb_results['pvalues']
sig_means_df = cpdb_results['significant_means']
deconv_df = cpdb_results['cpdb_deconvoluted']
scores_df = cpdb_results['interaction_scores']
```
