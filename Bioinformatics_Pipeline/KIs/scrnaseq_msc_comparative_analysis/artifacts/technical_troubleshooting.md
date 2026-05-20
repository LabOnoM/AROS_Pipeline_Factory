# scRNAseq Technical Troubleshooting

## 1. h5py: Slashes in Metadata Keys
**Error**: `ValueError: Forward slashes are not allowed in keys.`
- **Context**: Occurs when saving `.h5ad` files with `adata.obs` column names containing `/`.
- **Solution**: Replace slashes with underscores in column and gene score names.
- **Example**: `MSC/Stromal_score` -> `MSC_Stromal_score`.

## 2. Harmonypy: Z_corr Shape Mismatch
**Error**: `ValueError: Value passed for key 'X_pca_harmony' is of incorrect shape.`
- **Context**: Transposing the `ho.Z_corr` output incorrectly.
- **Solution**: `ho.Z_corr` is already `(n_cells, n_pcs)`. Do not use `.T` unless the input was transposed.
- **Correct usage**: `adata.obsm['X_pca_harmony'] = np.array(ho.Z_corr)`.

## 3. AnnData: varm Dimension Mismatch
**Error**: `ValueError: Value passed for key 'PCs' is of incorrect shape.`
- **Context**: Attempting to copy `varm` (e.g., PCA loadings) from an HVG-subsetted AnnData back to the full AnnData.
- **Solution**: Only copy `obsm` (cell-wise data) back. If `varm` is needed, it must be re-calculated or handled via indices.

## 4. Matplotlib: Shared Axes Indexing
**Error**: `AttributeError: 'numpy.ndarray' object has no attribute 'barh'`
- **Context**: When index `i` is used on an `axes` object from `plt.subplots`, the behavior changes depending on whether 1, 2, or more subplots were created.
- **Solution**: Force `axes` to be a list for consistent iteration.
```python
fig, axes = plt.subplots(1, n_panels)
if n_panels == 1:
    axes = [axes]
else:
    # Convert numpy array to list for consistent list indexing
    axes = list(axes)
```

## 5. QC Sensitivity: Mito% Thresholding
- **Observation**: For fresh vs. cultured comparisons, mitochondrial (%) content can differ greatly between conditions. Fresh marrow often contains populations sensitivity to isolation stress (erythroid/myeloid) with slightly higher mito%. 
- **Recommendation**: Stricter thresholds (e.g., `< 5%`) are better for identifying discrete fibroblast sub-states in the cultured sample, although this may prune some sensitive niche populations from the BM. In this study, 5% mito threshold only filtered 50 out of 9,000 cells but sharpened the cluster boundaries.

## 6. DoubletDecom: Boolean vs. String Comparison
**Error**: `doublets` returns 0 cells even when the DRS table shows doublets.
- **Context**: The `isADoublet` column in the `DoubletDecom` output `.csv` often contains strings 'TRUE' or 'FALSE' rather than native Python booleans.
- **Solution**: Explicitly convert to uppercase string before comparison.
```python
dr_table['isADoublet'] = dr_table['isADoublet'].astype(str).str.upper()
doublets = dr_table[dr_table['isADoublet'] == 'TRUE']['barcode'].tolist()
```

## 7. Scanpy: rank_genes_groups Warning on Pearson Residuals
**Warning**: `WARNING: It seems you use rank_genes_groups on the raw count data. Please logarithmize your data...`
- **Context**: Occurs when running differential expression on `adata.X` containing **Pearson Residuals** (SCTransform output). Scanpy's heuristic detects non-log normalized data.
- **Solution**: 
  - **Option 1**: Ignore the warning. Rank-sum tests (Wilcoxon) are non-parametric and perform well on residuals.
  - **Option 2**: Maintain a separate layer for log-normalized counts and point the function to it: `sc.tl.rank_genes_groups(adata, layer='lognorm', ...)`.
