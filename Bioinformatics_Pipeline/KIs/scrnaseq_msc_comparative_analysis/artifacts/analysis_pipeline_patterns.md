# Analysis Pipeline Patterns

## Stricter QC for MSC Culture
Cultured MSCs often show higher gene detectability. Stricter thresholds are recommended to ensure high-quality separation.

| Parameter | Recommended Threshold |
|-----------|-----------------------|
| `min_genes` | 500+ |
| `min_counts`| 1,000+ |
| `max_genes` | < 7,000 (remove potential doublets/stochastic high counts) |
| `pct_mito`  | < 5% |

## Integration: Harmony vs. Separation
When comparing distinct conditions (e.g., BM vs. Culture), the decision to use **Harmony** integration depends on the goal:

1. **Integrated View**: Use Harmony if you want to identify shared populations and perform sub-clustering based on shared identity.
2. **Separated View**: Skip Harmony if the goal is to visualize the dramatic transcriptomic shift as distinct clusters on UMAP.

### Implementation: Uncorrected PCA (Separated)
```python
sc.pp.neighbors(adata, use_rep='X_pca', n_neighbors=15, n_pcs=40)
sc.tl.umap(adata, min_dist=0.3)
```

## Gene Set Scoring Pattern
Scoring multiple biological signatures (MSC markers, stress, adipogenic, etc.) using `sc.tl.score_genes`.

```python
marker_dict = {
    'MSC_Stromal':   ['Lepr', 'Cxcl12', 'Kitl', 'Pdgfra'],
    'Culture_stress': ['Hspa1a', 'Jun', 'Fos'],
    # ...
}

for cat, genes in marker_dict.items():
    found = [g for g in genes if g in adata.raw.var_names]
    if len(found) >= 2:
        sc.tl.score_genes(adata, found, score_name=f'{cat}_score', use_raw=True)
```
**Tip**: Avoid forward slashes in dictionary keys (e.g., use `MSC_Stromal` instead of `MSC/Stromal`) to prevent file-system-like write errors in `.h5ad` formats.
## Aggregating Cluster Information
Automating the identification of cluster-specific properties (median genes, UMI, top signatures). This pattern is effective for biological interpretation.

```python
clusters = sorted(adata.obs['leiden'].unique(), key=int)
rows = []
score_cols = [c for c in adata.obs.columns if c.endswith('_score')]

for c in clusters:
    sub = adata[adata.obs['leiden'] == c]
    # Identify top biological signature based on mean gene set scores
    best_score = score_means.loc[c].idxmax() if 'score_means' in locals() else 'N/A'
    
    # Calculate medians for QC metrics
    med_genes = sub.obs['n_genes_by_counts'].median()
    med_counts = sub.obs['total_counts'].median()
    
    rows.append({
        'Cluster': c,
        'Count': sub.n_obs,
        'Med_Genes': int(med_genes),
        'Med_UMI': int(med_counts),
        'Top_Signature': best_score,
        'Top_Markers': ', '.join(sub.uns['rank_genes_groups']['names'][c][:5])
    })
df_summary = pd.DataFrame(rows)
print(df_summary.to_string(index=False))
```
## Iterative Refinement Strategy
In comparing two dramatically distinct conditions like BM vs. Cultured Cells, it is often necessary to iterate on the analysis to ensure reliable biological interpretation.

1. **Initial Exploration (Standard Normalize)**: Start with 20% mito and log-normalization + Harmony integration. This serves as a baseline for determining if cell populations exist in both conditions.
2. **Stricter QC (Mito < 5%)**: After initial QC patterns are understood, tighten mitochondrial (%) and gene count thresholds to reduce stochasticity, particularly in high-metabolic-activity cultured cells.
3. **Condition Separation (Native PCA)**: For publication-quality visualization of the *global* transcriptomic shift, skip integration (Harmony) in one version of the analysis. This forces conditions to cluster apart if their biological states are truly divergent.
4. **Variance Stabilization (SCTransform/Pearson Residuals)**: If sequencing depth or technical variation is suspected to be driving the clusters, re-run using Analytic Pearson Residuals (`sc.experimental.pp.normalize_pearson_residuals`). This provides more robust variance stabilization while retaining significant biological signal.
