# CellphoneDB Visualization Guide

CellphoneDB relies on external tools for visualization. The recommended library is **ktplotspy** (Python) or **ktplots** (R).

## Setup

```bash
pip install ktplotspy
```

## Dot Plot of Interactions

The classic CellphoneDB visualization — shows interaction significance and expression strength between cell type pairs.

```python
import ktplotspy as kpy

# Basic dot plot
fig = kpy.plot_cpdb(
    adata=adata,                   # AnnData object with expression data
    cell_type1="T cells",          # First cell type to show
    cell_type2="Macrophages",      # Second cell type to show
    means=cpdb_results['significant_means'],
    pvals=cpdb_results['pvalues'],
    celltype_key="cell_type",      # Column in adata.obs with cell type labels
)
fig.show()

# Filter to specific genes
fig = kpy.plot_cpdb(
    adata=adata,
    cell_type1=".",                 # Regex: all cell types
    cell_type2=".",                 # Regex: all cell types
    means=cpdb_results['significant_means'],
    pvals=cpdb_results['pvalues'],
    celltype_key="cell_type",
    genes=["CD274", "PDCD1", "CTLA4", "CD80"],
    figsize=(15, 10),
    title="Immune Checkpoint Interactions"
)
```

## Heatmap of Interaction Counts

Shows the total number of significant interactions between each pair of cell types.

```python
# Basic heatmap
fig = kpy.plot_cpdb_heatmap(
    pvals=cpdb_results['pvalues'],
    figsize=(8, 8),
    title="Number of significant interactions"
)

# With specific cell types
fig = kpy.plot_cpdb_heatmap(
    pvals=cpdb_results['pvalues'],
    cell_types=["T cells", "NK cells", "Macrophages", "Fibroblasts"],
)
```

## Chord Diagram

Circular plot showing interaction networks.

```python
fig = kpy.plot_cpdb_chord(
    pvals=cpdb_results['pvalues'],
    cell_type1="T cells",
    cell_type2="Macrophages",
    means=cpdb_results['significant_means'],
    deconvoluted=cpdb_results['cpdb_deconvoluted'],
    celltype_key="cell_type",
)
```

## Custom Seaborn/Matplotlib Visualizations

For fully custom plots, work directly with the DataFrames:

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load results
sig_means = cpdb_results['significant_means']
pvals = cpdb_results['pvalues']

# Count significant interactions per cell pair
# (p-value < 0.05)
cell_pair_cols = [c for c in pvals.columns if '|' in c]
sig_counts = (pvals[cell_pair_cols] < 0.05).sum()

# Bar plot of interaction counts
fig, ax = plt.subplots(figsize=(12, 6))
sig_counts.sort_values(ascending=False).head(20).plot(kind='bar', ax=ax)
ax.set_ylabel("Number of significant interactions")
ax.set_title("Top 20 interacting cell type pairs")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("top_interactions.png", dpi=300)
```

## Filtering Interactions for Visualization

```python
# Get significant interactions between specific cell types
cell_pair = "T cells|Macrophages"
sig = sig_means[sig_means[cell_pair] > 0][['interacting_pair', cell_pair]]
sig = sig.sort_values(cell_pair, ascending=False)

# Top interactions by score
if 'interaction_scores' in cpdb_results:
    scores = cpdb_results['interaction_scores']
    top_scored = scores.nlargest(20, cell_pair)[['interacting_pair', cell_pair]]
```

## Network Visualization

For network-style plots showing interaction communities:

```python
import networkx as nx

# Build network from significant interactions
G = nx.Graph()
for col in cell_pair_cols:
    ct1, ct2 = col.split('|')
    n_sig = (pvals[col] < 0.05).sum()
    if n_sig > 0:
        G.add_edge(ct1, ct2, weight=n_sig)

# Draw
pos = nx.spring_layout(G, k=2, seed=42)
weights = [G[u][v]['weight'] for u, v in G.edges()]
nx.draw(G, pos, with_labels=True, node_size=2000,
        width=[w/max(weights)*5 for w in weights],
        font_size=10, node_color='skyblue')
```

## Preparing AnnData for Visualization

ktplotspy needs the original AnnData object. Ensure it matches the CellphoneDB analysis:

```python
import scanpy as sc

adata = sc.read_h5ad("counts.h5ad")

# Ensure cell type column exists
assert "cell_type" in adata.obs.columns

# Filter to same cells used in analysis
meta = pd.read_csv("meta.txt", sep='\t')
adata = adata[adata.obs.index.isin(meta['Cell'])]
```
