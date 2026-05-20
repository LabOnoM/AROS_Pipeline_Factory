---
name: geniml
description: Machine learning toolkit for genomic interval (BED) data; use it when you need to tokenize BED collections and train embeddings for regions/cells/labels, build consensus peak universes, or run similarity search and downstream ML on chromatin accessibility datasets.
license: BSD-2-Clause license
metadata:
    skill-author: K-Dense Inc. & AIPOCH
---

## Overview

Geniml is a Python package for building machine learning models on genomic interval data (BED files). It provides unsupervised methods for learning embeddings of genomic regions, single cells, and metadata labels, enabling similarity searches, clustering, and downstream ML tasks.

## When to Use

- **You have many BED files and need numeric features** for clustering, similarity search, or downstream supervised learning (e.g., ChIP-seq/ATAC-seq region sets).
- **You want unsupervised embeddings of genomic regions** to compare region sets across experiments (Region2Vec).
- **You need joint embeddings of regions and metadata labels** (e.g., tissue/cell type/condition) to enable cross-modal queries like *Region → Label* or *Label → Region* (BEDspace).
- **You are analyzing single-cell ATAC-seq** and want cell embeddings for clustering/annotation and integration with Scanpy workflows (scEmbed).
- **You need a consensus peak set (“universe”)** built from multiple BED files to standardize tokenization and region definitions across datasets (Universe construction).

## Key Features

- **Region2Vec**: Word2vec-style unsupervised embeddings for genomic regions from tokenized BED data.
- **BEDspace**: StarSpace-based joint embedding space for region sets and metadata labels; supports similarity search and cross-modal retrieval.
- **scEmbed**: Single-cell ATAC-seq embedding workflow (tokenize cells → train → encode cells) compatible with Scanpy.
- **Universe (Consensus Peaks) Builder**: Generates reference peak sets using multiple statistical approaches (CC, CCF, ML, HMM).
- **Utilities**:
  - **Tokenization**: Universe-based tokenization (hard/soft tokenization patterns).
  - **Evaluation**: Embedding quality metrics (e.g., silhouette, Davies–Bouldin).
  - **BEDshift**: Region randomization/null-model generation while preserving genomic context.
  - **BBClient / caching**: Faster repeated access to BED resources.
  - **Text2BedNN**: Neural search backend for genomic queries.

> Additional details are commonly documented in: `references/region2vec.md`, `references/bedspace.md`, `references/scembed.md`, `references/consensus_peaks.md`, `references/utilities.md`.

## Installation

Install geniml using uv:

```bash
uv pip install geniml
```

For ML dependencies (PyTorch, etc.):

```bash
uv pip install 'geniml[ml]'
```

Development version from GitHub:

```bash
uv pip install git+https://github.com/databio/geniml.git
```

## Dependencies

- **Python**: 3.9+ (recommended)
- **geniml**: latest from PyPI (or GitHub main)
- **Optional ML extras**: `geniml[ml]` (typically pulls **PyTorch** and related ML dependencies)
- **Scanpy stack (for scEmbed workflows)**: `scanpy` (plus `anndata`, `numpy`, `scipy`)
- **StarSpace (for BEDspace training)**: external binary from https://github.com/facebookresearch/StarSpace
- **Universe coverage generation**: `uniwig` (used to generate coverage tracks in universe workflows)

## Core Capabilities

### 1. Region2Vec: Genomic Region Embeddings

Train unsupervised embeddings of genomic regions using word2vec-style learning.

**Use for:** Dimensionality reduction of BED files, region similarity analysis, feature vectors for downstream ML.

**Workflow:**
1. Tokenize BED files using a universe reference
2. Train Region2Vec model on tokens
3. Generate embeddings for regions

**Reference:** See `references/region2vec.md` for detailed workflow, parameters, and examples.

### 2. BEDspace: Joint Region and Metadata Embeddings

Train shared embeddings for region sets and metadata labels using StarSpace.

**Use for:** Metadata-aware searches, cross-modal queries (region→label or label→region), joint analysis of genomic content and experimental conditions, building searchable genomic databases.

**Workflow:**
1. Preprocess regions and metadata
2. Train BEDspace model
3. Compute distances
4. Query across regions and labels

**Reference:** See `references/bedspace.md` for detailed workflow, search types, and examples.

### 3. scEmbed: Single-Cell Chromatin Accessibility Embeddings

Train Region2Vec models on single-cell ATAC-seq data for cell-level embeddings.

**Use for:** scATAC-seq clustering, cell-type annotation, dimensionality reduction of single cells, integration with scanpy workflows.

**Workflow:**
1. Prepare AnnData with peak coordinates
2. Pre-tokenize cells
3. Train scEmbed model
4. Generate cell embeddings
5. Cluster and visualize with scanpy

**Reference:** See `references/scembed.md` for detailed workflow, parameters, and examples.

### 4. Consensus Peaks: Universe Building

Build reference peak sets (universes) from BED file collections using multiple statistical methods.

**Use for:** Creating tokenization references, standardizing regions across datasets, defining consensus features with statistical rigor.

**Workflow:**
1. Combine BED files
2. Generate coverage tracks
3. Build universe using CC, CCF, ML, or HMM method

**Methods:**
- **CC (Coverage Cutoff)**: Simple threshold-based
- **CCF (Coverage Cutoff Flexible)**: Confidence intervals for boundaries
- **ML (Maximum Likelihood)**: Probabilistic modeling of positions
- **HMM (Hidden Markov Model)**: Complex state modeling

**Reference:** See `references/consensus_peaks.md` for method comparison, parameters, and examples.

### 5. Utilities: Supporting Tools

Additional tools for caching, randomization, evaluation, and search.

**Available utilities:**
- **BBClient**: BED file caching for repeated access
- **BEDshift**: Randomization preserving genomic context
- **Evaluation**: Metrics for embedding quality (silhouette, Davies-Bouldin, etc.)
- **Tokenization**: Region tokenization utilities (hard, soft, universe-based)
- **Text2BedNN**: Neural search backends for genomic queries

**Reference:** See `references/utilities.md` for detailed usage of each utility.

## Example Usage

### End-to-end: Build a universe → tokenize BEDs → train Region2Vec → evaluate

```bash
# (A) Build coverage tracks (example pattern)
cat bed_files/*.bed > combined.bed
uniwig -m 25 combined.bed chrom.sizes coverage/

# (B) Build a universe (coverage cutoff method)
geniml universe build cc \
  --coverage-folder coverage/ \
  --output-file universe.bed \
  --cutoff 5 \
  --merge 100 \
  --filter-size 50
```

```python
# (C) Tokenize BED files, train Region2Vec, and evaluate embeddings
from geniml.tokenization import hard_tokenization
from geniml.region2vec import region2vec
from geniml.evaluation import evaluate_embeddings

# 1) Tokenize BED files against the universe
hard_tokenization(
    src_folder="bed_files/",
    dst_folder="tokens/",
    universe_file="universe.bed",
    p_value_threshold=1e-9,
)

# 2) Train Region2Vec
region2vec(
    token_folder="tokens/",
    save_dir="model/",
    num_shufflings=1000,
    embedding_dim=100,
)

# 3) Evaluate (requires labels/metadata aligned to embeddings)
metrics = evaluate_embeddings(
    embeddings_file="model/embeddings.npy",
    labels_file="metadata.csv",
)

print(metrics)
```

### Single-cell ATAC-seq: tokenize cells → train scEmbed → cluster with Scanpy

```python
import scanpy as sc
from geniml.scembed import ScEmbed
from geniml.io import tokenize_cells

# 1) Load AnnData
adata = sc.read_h5ad("scatac_data.h5ad")

# 2) Tokenize cells using a universe
tokenize_cells(
    adata="scatac_data.h5ad",
    universe_file="universe.bed",
    output="tokens.parquet",
)

# 3) Train scEmbed
model = ScEmbed(embedding_dim=100)
model.train(dataset="tokens.parquet", epochs=100)

# 4) Encode cells and attach embeddings to AnnData
embeddings = model.encode(adata)
adata.obsm["scembed_X"] = embeddings

# 5) Standard Scanpy neighborhood graph + clustering + UMAP
sc.pp.neighbors(adata, use_rep="scembed_X")
sc.tl.leiden(adata)
sc.tl.umap(adata)
```

## Implementation Details

### Tokenization (Universe-based)

- **Goal**: Convert genomic intervals into discrete “tokens” defined by a reference **universe** (consensus peak set).
- **Hard tokenization**: Assigns intervals to universe bins/peaks deterministically (commonly used for Region2Vec/scEmbed pipelines).
- **Key parameter**: `p_value_threshold` controls stringency of mapping/overlap significance (lower is stricter; overly strict thresholds can reduce coverage).

### Region2Vec (Region Embeddings)

- **Core idea**: Treat each BED file (or region set) like a “document” and each universe peak like a “word”; learn embeddings using a word2vec-style objective.
- **Important knobs**:
  - `embedding_dim`: dimensionality of learned vectors (e.g., 50–300).
  - `num_shufflings`: increases training signal by shuffling/co-occurrence augmentation; higher values increase runtime.

### BEDspace (Joint Region + Label Embeddings)

- **Core idea**: Learn a shared vector space for region sets and metadata labels using **StarSpace**, enabling:
  - **Region → Label** retrieval (predict likely labels for a query region set)
  - **Label → Region** retrieval (find region sets associated with a label)
- **Operational requirement**: StarSpace must be installed and its path provided/configured for training.

### scEmbed (Single-cell Embeddings)

- **Core idea**: Apply Region2Vec-like training on tokenized single-cell accessibility profiles to produce **cell embeddings**.
- **Best practice**: **Pre-tokenize** cells (e.g., to Parquet) to reduce repeated preprocessing and speed up training.
- **Downstream**: Use embeddings as `adata.obsm[...]` and run standard Scanpy steps (neighbors, Leiden, UMAP).

### Universe Construction (Consensus Peaks)

- **Purpose**: Create a stable reference peak set for tokenization and cross-dataset comparability.
- **Methods**:
  - **CC (Coverage Cutoff)**: threshold-based peak calling from coverage.
  - **CCF (Coverage Cutoff Flexible)**: cutoff with flexible boundaries/confidence intervals.
  - **ML (Maximum Likelihood)**: probabilistic modeling of peak positions.
  - **HMM (Hidden Markov Model)**: state-based segmentation; typically most computationally intensive.
- **Typical parameters**:
  - `--cutoff`: minimum coverage to call peaks (CC/CCF).
  - `--merge`: merge distance for nearby peaks.
  - `--filter-size`: minimum peak length to keep.

## Best Practices

### General Guidelines

- **Universe quality is critical**: Invest time in building comprehensive, well-constructed universes
- **Tokenization validation**: Check coverage (>80% ideal) before training
- **Parameter tuning**: Experiment with embedding dimensions, learning rates, and training epochs
- **Evaluation**: Always validate embeddings with multiple metrics and visualizations
- **Documentation**: Record parameters and random seeds for reproducibility

### Performance Considerations

- **Pre-tokenization**: For scEmbed, always pre-tokenize cells for faster training
- **Memory management**: Large datasets may require batch processing or downsampling
- **Computational resources**: ML/HMM universe methods are computationally intensive
- **Model caching**: Use BBClient to avoid repeated downloads

### Integration Patterns

- **With scanpy**: scEmbed embeddings integrate seamlessly as `adata.obsm` entries
- **With BEDbase**: Use BBClient for accessing remote BED repositories
- **With Hugging Face**: Export trained models for sharing and reproducibility
- **With R**: Use reticulate for R integration (see utilities reference)

## Related Projects

Geniml is part of the BEDbase ecosystem:

- **BEDbase**: Unified platform for genomic regions
- **BEDboss**: Processing pipeline for BED files
- **Gtars**: Genomic tools and utilities
- **BBClient**: Client for BEDbase repositories

## Additional Resources

- **Documentation**: https://docs.bedbase.org/geniml/
- **GitHub**: https://github.com/databio/geniml
- **Pre-trained models**: Available on Hugging Face (databio organization)
- **Publications**: Cited in documentation for methodological details

## Troubleshooting

**"Tokenization coverage too low":**
- Check universe quality and completeness
- Adjust p-value threshold (try 1e-6 instead of 1e-9)
- Ensure universe matches genome assembly

**"Training not converging":**
- Adjust learning rate (try 0.01-0.05 range)
- Increase training epochs
- Check data quality and preprocessing

**"Out of memory errors":**
- Reduce batch size for scEmbed
- Process data in chunks
- Use pre-tokenization for single-cell data

**"StarSpace not found" (BEDspace):**
- Install StarSpace separately: https://github.com/facebookresearch/StarSpace
- Set `--path-to-starspace` parameter correctly

For detailed troubleshooting and method-specific issues, consult the appropriate reference file.