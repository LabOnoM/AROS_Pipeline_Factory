# MSC Comparative scRNAseq Analysis Overview

This knowledge item documents the analysis workflow and technical insights from comparing freshly isolated mouse bone marrow (BM) cells with day-3 cultured MSCs using the **MGI DNBelab C4** system.

## Analysis Goals
- Identify transcriptomic shifts induced by *in vitro* culture expansion.
- Characterize the loss of niche-resident populations.
- Define markers and pathways associated with cultured MSC adaptation.

## Pipeline Summary
The finalized pipeline follows these steps:
1. **Preprocessing**: Loading MGI/PISA 10X-compatible matrices.
2. **Doublet Removal**: Selection of DoubletDecom over Solo based on manifold homogeneity.
3. **Stricter QC**: Applying tight mitochondrial (<5%) and gene count thresholds.
4. **Normalization**: Standard (log-normalization) or Analytic Pearson Residuals (SCTransform-like) for robust modeling.
5. **Primary Dimensionality Reduction**: PCA and UMAP. **Note**: Avoiding Harmony batch correction is recommended when visual separation of conditions is the analytical goal.
6. **Clustering & Annotation**: Leiden clustering followed by marker-based and gene set score-based cell type identification.
7. **Differential Expression**: Global and per-cluster Wilcoxon rank-sum testing.
8. **Pathway Enrichment**: GO/KEGG/MSigDB analysis via Enrichr.

## Key Software Components
- **Scanpy / sc.experimental**: Core analysis and Pearson Residual normalization.
- **DoubletDecom**: Robust doublet detection using PMF.
- **Harmony (harmonypy)**: Integration (used selectively).
- **gseapy**: Pathway enrichment.
