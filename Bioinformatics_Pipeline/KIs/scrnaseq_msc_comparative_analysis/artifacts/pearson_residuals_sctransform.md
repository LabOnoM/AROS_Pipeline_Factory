# Pearson Residuals (SCTransform-like) Workflow in Scanpy

## Overview
For datasets with high dynamic range or significant technical variation (e.g., comparing freshly isolated cells with expanded cultured cells), standard log-normalization may not adequately model the mean-variance relationship. **Pearson Residuals** (equivalent to Seurat's **SCTransform**) provide a more robust normalization by modeling counts using a Negative Binomial distribution.

## Implementation in Scanpy

As of Scanpy 1.9+, Pearson Residuals are available in the experimental or core preprocessing modules.

### Basic Normalization
```python
import scanpy as sc

# 1. Analytic Pearson Residuals (Standard)
sc.experimental.pp.normalize_pearson_residuals(adata)

# 2. Selecting Highly Variable Genes based on Pearson Residuals
sc.experimental.pp.highly_variable_genes(
    adata, 
    flavor='pearson_residuals', 
    n_top_genes=3000
)
```

## Why use Pearson Residuals?
1. **Biological Signal Preservation**: Better preserves biological variance in high-count genes compared to log-normalization.
2. **Technical Variation Removal**: Implicitly handles library size effects without requiring explicit total count normalization.
3. **Integration Compatibility**: Often used before batch correction (e.g., Harmony) to ensure residuals rather than raw counts are integrated.

## Performance Considerations
- **Memory**: Analytic residuals are computed as sparse or dense matrices depending on implementation. 
- **Compatibility**: Many downstream tools (like `sc.tl.rank_genes_groups`) expect log-normalized data. It is often recommended to keep the Pearson Residuals in a separate layer or object for dimensionality reduction, while using log-normalized data for differential expression.

## Comparison with Standard Workflow
| Step | Standard (Logo-norm) | Pearson Residuals |
|------|----------------------|-------------------|
| **Normalization** | `sc.pp.normalize_total` + `sc.pp.log1p` | `sc.experimental.pp.normalize_pearson_residuals` |
| **HVG Selection** | `seurat` / `cell_ranger` | `pearson_residuals` |
| **Scaling** | `sc.pp.scale` | (Implicitly handled by residuals) |

## Combining with Harmony Integration

When using Pearson Residuals for integration, the Harmony alignment should be performed in the PCA space derived from normalized residuals.

```python
import harmonypy as hm

# 1. Select HVGs using pearson_residuals flavor
sc.experimental.pp.highly_variable_genes(adata, flavor='pearson_residuals', n_top_genes=3000, batch_key='batch')
adata_hvg = adata[:, adata.var.highly_variable].copy()

# 2. Normalize subset using residuals
sc.experimental.pp.normalize_pearson_residuals(adata_hvg)

# 3. PCA on residuals
sc.tl.pca(adata_hvg, n_comps=50)

# 4. Harmony integration using the residual-PCA space
ho = hm.run_harmony(adata_hvg.obsm['X_pca'][:, :30], adata_hvg.obs, 'batch')
adata.obsm['X_pca_harmony'] = np.array(ho.Z_corr)

# 5. Build neighbors/UMAP on the corrected residual space
sc.pp.neighbors(adata, use_rep='X_pca_harmony')
sc.tl.umap(adata)
```
