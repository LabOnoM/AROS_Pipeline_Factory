---
name: scvi-tools
description: Deep generative models for single-cell omics. Use for probabilistic batch correction (scVI), transfer learning, uncertainty-aware differential expression, or multimodal integration (totalVI/MultiVI).
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc. and AIPOCH
---

# scvi-tools

## Overview

scvi-tools is a comprehensive Python framework for probabilistic modeling in single-cell genomics. Built on PyTorch and PyTorch Lightning, it provides deep generative models using variational inference for analyzing diverse single-cell data modalities. It excels in tasks requiring advanced modeling beyond standard pipelines.

## When to Use This Skill

Use this skill when you need probabilistic, model-based single-cell analysis, such as:

1.  **Batch correction and dataset integration** for scRNA-seq using a probabilistic latent space (e.g., scVI).
2.  **Transfer learning / semi-supervised annotation** when you have partial labels or want to map new data onto a reference (e.g., scANVI).
3.  **Uncertainty-aware differential expression** where effect sizes and posterior uncertainty matter (Bayesian DE).
4.  **Multimodal integration** across RNA+protein (CITE-seq) or RNA+ATAC (multiome), including paired/unpaired settings (e.g., totalVI, MultiVI).
5.  **Analyzing single-cell ATAC-seq or chromatin accessibility data**
6.  **Analyzing spatial transcriptomics data** (deconvolution, spatial mapping)
7.  **Working with specialized modalities** such as methylation, cytometry, RNA velocity, or doublet detection.
8.  **Building custom probabilistic models** for single-cell analysis

## Key Features

-   **Unified model API**: `setup_anndata(...) → Model(adata) → train() → get_*()` across model families.
-   **Probabilistic latent representations** for integration, denoising, and downstream clustering/visualization.
-   **Explicit covariate handling** (batch, donor, technical factors) via `setup_anndata`.
-   **Bayesian differential expression** with posterior-based hypothesis testing and effect-size thresholds.
-   **Multi-omics models** for joint learning across modalities (RNA/protein, RNA/ATAC; paired or unpaired).
-   **AnnData-first integration** with the Scanpy ecosystem for downstream neighbors/UMAP/clustering.
-   **GPU acceleration** via PyTorch (when available).

Model catalogs by modality (for reference):

-   scRNA-seq: `references/models-scrna-seq.md` (scVI, scANVI, AUTOZI, VeloVI, contrastiveVI, …)
-   ATAC-seq: `references/models-atac-seq.md` (PeakVI, PoissonVI, scBasset, …)
-   Multimodal: `references/models-multimodal.md` (totalVI, MultiVI, MrVI, …)
-   Spatial: `references/models-spatial.md` (DestVI, Stereoscope, Tangram, scVIVA, …)
-   Specialized: `references/models-specialized.md` (Solo, CellAssign, MethylVI/MethylANVI, CytoVI, …)

## Dependencies

-   `scvi-tools` (latest compatible with your environment)
-   `python>=3.9`
-   `pytorch>=2.0`
-   `pytorch-lightning>=2.0` (or `lightning` depending on scvi-tools version)
-   `anndata>=0.8`
-   `scanpy>=1.9`

Installation example:

```bash
uv pip install scvi-tools
# Optional GPU extras (package extra name may vary by platform/version)
uv pip install "scvi-tools[cuda]"
```

## Example Usage

A complete runnable example using **scVI** for batch correction + latent embedding, then Scanpy for neighbors/UMAP/clustering:

```python
import scanpy as sc
import scvi

# 1) Load example data (AnnData)
adata = scvi.data.heart_cell_atlas_subsampled()

# 2) Minimal preprocessing (keep raw counts available)
sc.pp.filter_genes(adata, min_counts=3)
sc.pp.highly_variable_genes(adata, n_top_genes=1200)

# 3) Register AnnData for scVI (raw counts + covariates)
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",                 # raw counts layer (not log-normalized)
    batch_key="batch",              # batch column in adata.obs
    categorical_covariate_keys=["donor"],
    continuous_covariate_keys=["percent_mito"],
)

# 4) Train model
model = scvi.model.SCVI(adata)
model.train()

# 5) Extract outputs
adata.obsm["X_scVI"] = model.get_latent_representation()
adata.layers["scvi_normalized"] = model.get_normalized_expression(library_size=1e4)

# 6) Downstream analysis with Scanpy
sc.pp.neighbors(adata, use_rep="X_scVI")
sc.tl.umap(adata)
sc.tl.leiden(adata)

# Optional: uncertainty-aware differential expression
de = model.differential_expression(
    groupby="cell_type",
    group1="TypeA",
    group2="TypeB",
    mode="change",
    delta=0.25,
)
print(de.head())
```

Model persistence:

```python
model.save("./scvi_model", overwrite=True)
model2 = scvi.model.SCVI.load("./scvi_model", adata=adata)
```

## Implementation Details

-   **Core approach**: deep generative modeling with **variational inference** (typically VAE-style architectures) to learn a latent representation and a likelihood model for counts.
-   **Data requirements**: models generally expect **raw counts** (not log-normalized values). Provide counts via `layer="counts"` or ensure `adata.X` contains counts.
-   **Covariate registration**: technical factors (e.g., `batch_key`, donor, QC metrics) are incorporated through `setup_anndata`, enabling the model to learn representations that reduce unwanted variation.
-   **Training loop**: `train()` performs amortized inference using neural networks shared across cells; GPU acceleration is used automatically when configured.
-   **Latent space usage**: `get_latent_representation()` returns batch-corrected embeddings suitable for neighbors/UMAP/clustering in Scanpy.
-   **Differential expression**: `differential_expression(...)` performs posterior-based comparisons; parameters like:

    *   `mode="change"`: composite hypothesis testing on changes
    *   `delta`: minimum effect size threshold

    help control practical significance and uncertainty-aware decisions.  
    See `references/differential-expression.md` for interpretation guidance.
-   **Model selection by modality**: choose the model family based on data type (e.g., scVI/scANVI for scRNA-seq, totalVI for CITE-seq, MultiVI for RNA+ATAC, DestVI for spatial deconvolution). For details, see the corresponding `references/models-*.md` files.
-   **Theory background**: variational inference, amortized inference, and probabilistic modeling foundations are summarized in `references/theoretical-foundations.md`.

## Best Practices

1.  **Use raw counts**: Always provide unnormalized count data to models.
2.  **Filter genes**: Remove low-count genes before analysis (e.g., `min_counts=3`).
3.  **Register covariates**: Include known technical factors (batch, donor, etc.) in `setup_anndata`.
4.  **Feature selection**: Use highly variable genes for improved performance.
5.  **Model saving**: Always save trained models to avoid retraining.
6.  **GPU usage**: Enable GPU acceleration for large datasets (`accelerator="gpu"`).
7.  **Scanpy integration**: Store outputs in AnnData objects for downstream analysis.

## Additional Resources

-   **Workflows**: `references/workflows.md` contains common workflows, best practices, hyperparameter tuning, and GPU optimization.
-   **Model References**: Detailed documentation for each model category in the `references/` directory.
-   **Official Documentation**: https://docs.scvi-tools.org/en/stable/
-   **Tutorials**: https://docs.scvi-tools.org/en/stable/tutorials/index.html
-   **API Reference**: https://docs.scvi-tools.org/en/stable/api/index.html