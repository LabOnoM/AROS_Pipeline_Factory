---
name: anndata
description: Data structure for annotated matrices in single-cell analysis; use when reading/writing .h5ad (or zarr) and exchanging data with the scverse ecosystem. This is the data format skill—for analysis workflows use scanpy; for probabilistic models use scvi-tools; for population-scale queries use cellxgene-census.
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc. & AIPOCH
---
```

## Overview

AnnData is a Python package for handling annotated data matrices, storing experimental measurements (X) alongside observation metadata (obs), variable metadata (var), and multi-dimensional annotations (obsm, varm, obsp, varp, uns). Originally designed for single-cell genomics through Scanpy, it now serves as a general-purpose framework for any annotated data requiring efficient storage, manipulation, and analysis.

## When to Use

Use AnnData when you need to:

- Load, inspect, or export annotated single-cell datasets stored as `.h5ad` (or `zarr`) for downstream tools.
- Keep a matrix (cells × features) tightly coupled with observation/feature metadata (e.g., cell types, batches, gene annotations).
- Work efficiently with large, sparse count matrices (e.g., scRNA-seq) and avoid loading everything into memory (backed mode).
- Combine multiple experiments/batches/modalities into a unified object while tracking provenance.
- Subset/filter/transform data while preserving alignment between the matrix and metadata.
- Creating, reading, or writing AnnData objects.
- Working with h5ad, zarr, or other genomics data formats.
- Performing single-cell RNA-seq analysis.
- Managing large datasets with sparse matrices or backed mode.
- Concatenating multiple datasets or experimental batches.
- Subsetting, filtering, or transforming annotated data.
- Integrating with scanpy, scvi-tools, or other scverse ecosystem tools.

## Key Features

- **Unified container**: `X` (data matrix) plus aligned annotations: `obs`, `var`, `uns`, and multi-dimensional slots (`obsm`, `varm`, `obsp`, `varp`), plus `layers` and optional `raw`.
- **Interoperable I/O**: Native `.h5ad` and `zarr`, plus common genomics formats (e.g., 10x, loom, mtx, csv).
- **Scalable workflows**: Sparse matrices and **backed mode** (`backed="r"`) for large datasets.
- **Safe subsetting**: Slicing preserves alignment across matrix and annotations; supports views vs copies.
- **Concatenation utilities**: `ad.concat(...)` with join/merge strategies and batch labeling; experimental lazy collections.

## Installation

```bash
uv pip install anndata

# With optional dependencies
uv pip install anndata[dev,test,doc]
```

## Dependencies

- `anndata` (latest compatible with your environment; install via pip/uv)
- `numpy`
- `pandas`
- `scipy` (recommended for sparse matrices)
- Optional ecosystem tools (only if needed):
  - `scanpy`
  - `muon`
  - `torch` (for deep learning) and `anndata` experimental loader utilities

## Example Usage

A complete runnable example that creates an AnnData object, writes/reads `.h5ad`, subsets, concatenates batches, and demonstrates backed mode.

```python
import numpy as np
import pandas as pd
import anndata as ad
from scipy.sparse import csr_matrix

# ----------------------------
# 1) Create an AnnData object
# ----------------------------
rng = np.random.default_rng(0)

n_cells, n_genes = 100, 500
X = rng.poisson(1.0, size=(n_cells, n_genes)).astype(np.float32)

obs = pd.DataFrame(
    {
        "cell_type": (["T cell", "B cell"] * (n_cells // 2)),
        "sample": (["A", "B"] * (n_cells // 2)),
        "quality_score": rng.random(n_cells),
    },
    index=[f"cell_{i}" for i in range(n_cells)],
)

var = pd.DataFrame(
    {"gene_name": [f"Gene_{j}" for j in range(n_genes)]},
    index=[f"ENSG{j:05d}" for j in range(n_genes)],
)

adata = ad.AnnData(X=X, obs=obs, var=var)

# Use sparse storage for typical count-like matrices
adata.X = csr_matrix(adata.X)

# Convert string columns to categoricals to reduce memory and speed up ops
adata.strings_to_categoricals()

print(f"Created: {adata.n_obs} obs × {adata.n_vars} vars")

# ----------------------------
# 2) Write and read .h5ad
# ----------------------------
adata.write_h5ad("example.h5ad", compression="gzip")

adata2 = ad.read_h5ad("example.h5ad")
print(f"Reloaded: {adata2.n_obs} obs × {adata2.n_vars} vars")

# ----------------------------
# 3) Subset (keeps alignment)
# ----------------------------
t_cells = adata2[adata2.obs["cell_type"] == "T cell", :]
high_quality = adata2[adata2.obs["quality_score"] > 0.8, :]

print(f"T cells: {t_cells.n_obs}")
print(f"High quality: {high_quality.n_obs}")

# ----------------------------
# 4) Concatenate batches
# ----------------------------
adata_a = adata2[adata2.obs["sample"] == "A", :].copy()
adata_b = adata2[adata2.obs["sample"] == "B", :].copy()

combined = ad.concat(
    [adata_a, adata_b],
    axis=0,                 # concatenate observations (cells)
    join="inner",           # keep shared variables
    label="batch",          # add a column in .obs
    keys=["A", "B"],        # batch labels
)

print(combined.obs["batch"].value_counts().to_dict())

# ----------------------------
# 5) Backed mode for large files
# ----------------------------
adata_backed = ad.read_h5ad("example.h5ad", backed="r")
# Slicing in backed mode is metadata-friendly; load to memory when needed:
subset_mem = adata_backed[:10, :50].to_memory()
print(f"Backed subset loaded: {subset_mem.shape}")
```

## Core Concepts

### Data model (core slots)

- `X`: primary data matrix (dense `numpy.ndarray` or sparse `scipy.sparse`), shape `(n_obs, n_vars)`.
- `obs`: per-observation metadata (`pandas.DataFrame`), indexed by `obs_names` (e.g., cell IDs).
- `var`: per-variable metadata (`pandas.DataFrame`), indexed by `var_names` (e.g., gene IDs).
- `layers`: named alternative matrices aligned to `X` (e.g., `"counts"`, `"log1p"`).
- `obsm` / `varm`: multi-dimensional embeddings aligned to obs/var (e.g., PCA, UMAP coordinates).
- `obsp` / `varp`: pairwise graphs/matrices (e.g., kNN graph in `obsp["connectivities"]`).
- `uns`: unstructured metadata (dict-like), often used for parameters and plotting configs.
- `raw` (optional): snapshot of unfiltered/untransformed data for reproducibility.

### Views vs copies

- Slicing like `adata_subset = adata[mask, :]` typically returns a **view** (lightweight reference).
- Use `.copy()` when you need an independent object (e.g., before in-place modifications).

### Backed mode (large datasets)

- `ad.read_h5ad(path, backed="r")` keeps the matrix on disk and loads data lazily.
- Convert a slice to memory with `.to_memory()` when you need in-memory computation.
- Backed mode is best for filtering by metadata, chunked processing, and avoiding OOM.

### Concatenation behavior

- `ad.concat([...], axis=0)` stacks observations; `axis=1` stacks variables.
- `join="inner"` keeps intersection of variables; `join="outer"` unions variables (may introduce missing values).
- `label` + `keys` records dataset/batch provenance in `.obs[label]`.
- Merge strategies control how conflicting `.uns` and annotation columns are handled (choose based on your data governance needs).

### Practical performance parameters

- Prefer sparse matrices (`csr_matrix`) for count-like data.
- Convert repeated strings to categoricals (`adata.strings_to_categoricals()`).
- Use compression when writing `.h5ad` (e.g., `compression="gzip"`) to reduce storage; consider `zarr` for chunked/cloud-friendly access.

## Common Workflows

### Single-cell RNA-seq analysis
```python
import anndata as ad
import scanpy as sc

# 1. Load data
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')

# 2. Quality control
adata.obs['n_genes'] = (adata.X > 0).sum(axis=1)
adata.obs['n_counts'] = adata.X.sum(axis=1)
adata = adata[adata.obs['n_genes'] > 200]
adata = adata[adata.obs['n_counts'] < 50000]

# 3. Store raw
adata.raw = adata.copy()

# 4. Normalize and filter
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var['highly_variable']]

# 5. Save processed data
adata.write_h5ad('processed.h5ad')
```

### Batch integration
```python
# Load multiple batches
adata1 = ad.read_h5ad('batch1.h5ad')
adata2 = ad.read_h5ad('batch2.h5ad')
adata3 = ad.read_h5ad('batch3.h5ad')

# Concatenate with batch labels
adata = ad.concat(
    [adata1, adata2, adata3],
    label='batch',
    keys=['batch1', 'batch2', 'batch3'],
    join='inner'
)

# Apply batch correction
import scanpy as sc
sc.pp.combat(adata, key='batch')

# Continue analysis
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
```

### Working with large datasets
```python
# Open in backed mode
adata = ad.read_h5ad('100GB_dataset.h5ad', backed='r')

# Filter based on metadata (no data loading)
high_quality = adata[adata.obs['quality_score'] > 0.8]

# Load filtered subset
adata_subset = high_quality.to_memory()

# Process subset
process(adata_subset)

# Or process in chunks
chunk_size = 1000
for i in range(0, adata.n_obs, chunk_size):
    chunk = adata[i:i+chunk_size, :].to_memory()
    process(chunk)
```

## Troubleshooting

### Out of memory errors
Use backed mode or convert to sparse matrices:
```python
# Backed mode
adata = ad.read_h5ad('file.h5ad', backed='r')

# Sparse matrices
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)
```

### Slow file reading
Use compression and appropriate formats:
```python
# Optimize for storage
adata.strings_to_categoricals()
adata.write_h5ad('file.h5ad', compression='gzip')

# Use Zarr for cloud storage
adata.write_zarr('file.zarr', chunks=(1000, 1000))
```

### Index alignment issues
Always align external data on index:
```python
# Wrong
adata.obs['new_col'] = external_data['values']

# Correct
adata.obs['new_col'] = external_data.set_index('cell_id').loc[adata.obs_names, 'values']
```

## Integration with Scverse Ecosystem

AnnData serves as the foundational data structure for the scverse ecosystem:

### Scanpy (Single-cell analysis)
```python
import scanpy as sc

# Preprocessing
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)

# Dimensionality reduction
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata, n_neighbors=15)
sc.tl.umap(adata)
sc.tl.leiden(adata)

# Visualization
sc.pl.umap(adata, color=['cell_type', 'leiden'])
```

### Muon (Multimodal data)
```python
import muon as mu

# Combine RNA and protein data
mdata = mu.MuData({'rna': adata_rna, 'protein': adata_protein})
```

### PyTorch integration
```python
from anndata.experimental import AnnLoader

# Create DataLoader for deep learning
dataloader = AnnLoader(adata, batch_size=128, shuffle=True)

for batch in dataloader:
    X = batch.X
    # Train model
```

## Additional Resources

- **Official documentation**: https://anndata.readthedocs.io/
- **Scanpy tutorials**: https://scanpy.readthedocs.io/
- **Scverse ecosystem**: https://scverse.org/
- **GitHub repository**: https://github.com/scverse/anndata