---
name: pydeseq2
description: Differential gene expression analysis for bulk RNA-seq count matrices using a DESeq2-like workflow in Python; use when you need Wald tests, FDR correction, and optional LFC shrinkage for condition/batch/covariate designs.
license: MIT
skill-author: K-Dense Inc. & AIPOCH
---

## Overview

PyDESeq2 is a Python implementation for differential expression analysis with bulk RNA-seq data, mirroring the DESeq2 workflow. Design and execute complete analyses from data loading to result interpretation, including single-factor and multi-factor designs, Wald tests with multiple testing correction, optional apeGLM shrinkage, and integration with pandas and AnnData.

## When to Use

Use this skill when you need to run DESeq2-style differential expression in Python, especially in these scenarios:

1.  **Case vs control bulk RNA-seq** from a raw integer count matrix (e.g., treated vs control).
2.  **Multi-factor designs** to adjust for batch effects or covariates (e.g., `~ batch + condition`, `~ age + condition`).
3.  **DESeq2 migration** when converting an R DESeq2 workflow into a Python pipeline.
4.  **Pipeline integration** where results must stay in Python objects (pandas/AnnData) for downstream QC, plots, or reporting.
5.  **Requests mentioning** "DESeq2", "differential expression", "Wald test", "FDR/padj", "volcano plot", "MA plot", or "PyDESeq2".

## Key Features

*   End-to-end DESeq2-like workflow: normalization (size factors), dispersion estimation/shrinkage, LFC fitting, outlier handling.
*   **Wald tests** for differential expression with **Benjamini–Hochberg FDR** (`padj`).
*   **Design formulas** in Wilkinson/R-style notation (single-factor and multi-factor).
*   **Contrast-based comparisons**: `[variable, test_group, reference_group]`.
*   Optional **Cook’s distance** outlier filtering and refitting.
*   Optional **LFC shrinkage** (apeGLM-style) for visualization/ranking.
*   Works naturally with **pandas** and can interoperate with **AnnData**.

## Dependencies

Minimum environment:

*   Python **3.10–3.11**
*   `pydeseq2` (install via pip/uv)
*   `pandas` **>= 1.4.3**
*   `numpy` **>= 1.23.0**
*   `scipy` **>= 1.11.0**
*   `scikit-learn` **>= 1.1.1**
*   `anndata` **>= 0.8.0** (optional, for AnnData I/O)

Optional plotting:

*   `matplotlib` (recommended)
*   `seaborn` (optional)

Installation:

```bash
uv pip install pydeseq2
```

## Quick Start Workflow

For users who want to perform a standard differential expression analysis:

```python
import pandas as pd
import numpy as np
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# 1. Load data
counts_df = pd.read_csv("counts.csv", index_col=0).T  # Transpose to samples × genes
metadata = pd.read_csv("metadata.csv", index_col=0)

# Ensure sample alignment
common = counts_df.index.intersection(metadata.index)
counts_df = counts_df.loc[common]
metadata = metadata.loc[common]

# 2. Filter low-count genes
min_total_counts = 10
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= min_total_counts]
counts_df = counts_df[genes_to_keep]

# 3. Initialize and fit DESeq2
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True,
    n_cpus=1
)
dds.deseq2()

# 4. Perform statistical testing
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()

# 5. Access results
results = ds.results_df
significant = results[results.padj < 0.05]
print(f"Found {len(significant)} significant genes")
```

## Core Workflow Steps

### Step 1: Data Preparation

**Input requirements:**

*   **Count matrix:** Samples × genes DataFrame with non-negative integer read counts.
*   **Metadata:** Samples × variables DataFrame with experimental factors.

**Common data loading patterns:**

```python
# From CSV (typical format: genes × samples, needs transpose)
counts_df = pd.read_csv("counts.csv", index_col=0).T
metadata = pd.read_csv("metadata.csv", index_col=0)

# From TSV
counts_df = pd.read_csv("counts.tsv", sep="\t", index_col=0).T

# From AnnData
import anndata as ad
adata = ad.read_h5ad("data.h5ad")
counts_df = pd.DataFrame(adata.X, index=adata.obs_names, columns=adata.var_names)
metadata = adata.obs
```

**Data filtering:**

```python
# Remove low-count genes
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

# Remove samples with missing metadata
samples_to_keep = ~metadata.condition.isna()
counts_df = counts_df.loc[samples_to_keep]
metadata = metadata.loc[samples_to_keep]
```

### Step 2: Design Specification

The design formula specifies how gene expression is modeled.

*   Use strings like:
    *   `~ condition` (single factor)
    *   `~ batch + condition` (batch-adjusted)
    *   `~ age + condition` (continuous covariate)
    *   `~ group + condition + group:condition` (interaction)
*   Put **adjustment variables first** (e.g., `~ batch + condition`) so the primary effect is interpreted cleanly.

**Single-factor designs:**

```python
design = "~condition"  # Simple two-group comparison
```

**Multi-factor designs:**

```python
design = "~batch + condition"  # Control for batch effects
design = "~age + condition"     # Include continuous covariate
design = "~group + condition + group:condition"  # Interaction effects
```

### Step 3: DESeq2 Fitting

Initialize the DeseqDataSet and run the complete pipeline:

```python
from pydeseq2.dds import DeseqDataSet

dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True,  # Refit after removing outliers
    n_cpus=1           # Parallel processing (adjust as needed)
)

# Run the complete DESeq2 pipeline
dds.deseq2()
```

The fitting pipeline typically includes:

1.  **Size factor** estimation (library-size normalization)
2.  **Gene-wise dispersion** estimation
3.  Dispersion **trend** fitting and **prior** estimation
4.  **MAP dispersion** shrinkage
5.  **Log2 fold change** fitting under the specified design
6.  **Cook’s distance** outlier detection
7.  Optional **refitting** after outlier handling (`refit_cooks=True`)

### Step 4: Statistical Testing

Perform Wald tests to identify differentially expressed genes:

```python
from pydeseq2.ds import DeseqStats

ds = DeseqStats(
    dds,
    contrast=["condition", "treated", "control"],  # Test treated vs control
    alpha=0.05,                # Significance threshold
    cooks_filter=True,         # Filter outliers
    independent_filter=True    # Filter low-power tests
)

ds.summary()
```

Output columns commonly include:

*   `baseMean`: mean normalized expression
*   `log2FoldChange`, `lfcSE`, `stat`
*   `pvalue`: raw p-value
*   `padj`: **Benjamini–Hochberg FDR** adjusted p-value

Use `padj < alpha` (commonly 0.05) for significance.

**Contrast specification:**

*   Format: `[variable, test_level, reference_level]`
*   Example: `["condition", "treated", "control"]` tests treated vs control
*   If `None`, uses the last coefficient in the design

### Step 5: Optional LFC Shrinkage

Apply shrinkage to reduce noise in fold change estimates:

```python
ds.lfc_shrink()  # Applies apeGLM shrinkage
```

Shrinkage is intended for **visualization and prioritization**; statistical significance is still based on the (unshrunken) Wald test p-values.

### Step 6: Result Export

Save results and intermediate objects:

```python
import pickle

# Export results as CSV
ds.results_df.to_csv("deseq2_results.csv")

# Save significant genes only
significant = ds.results_df[ds.results_df.padj < 0.05]
significant.to_csv("significant_genes.csv")

# Save DeseqDataSet for later use
with open("dds_result.pkl", "wb") as f:
    pickle.dump(dds.to_picklable_anndata(), f)
```

## Example Usage (Complete Script)

The following script is a complete, runnable example for a standard treated-vs-control analysis.

```python
import pandas as pd
import numpy as np

from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# -----------------------------
# 1) Load inputs
# -----------------------------
# counts.csv is commonly stored as genes x samples; transpose to samples x genes.
counts_df = pd.read_csv("counts.csv", index_col=0).T
metadata = pd.read_csv("metadata.csv", index_col=0)

# Ensure sample alignment
common = counts_df.index.intersection(metadata.index)
counts_df = counts_df.loc[common]
metadata = metadata.loc[common]

# -----------------------------
# 2) Basic filtering
# -----------------------------
# Remove genes with very low total counts
min_total_counts = 10
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= min_total_counts]
counts_df = counts_df[genes_to_keep]

# Drop samples with missing condition
metadata = metadata.dropna(subset=["condition"])
counts_df = counts_df.loc[metadata.index]

# -----------------------------
# 3) Fit DESeq2 model
# -----------------------------
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~ condition",
    refit_cooks=True,
    n_cpus=1,
)
dds.deseq2()

# -----------------------------
# 4) Wald test with contrast
# -----------------------------
ds = DeseqStats(
    dds,
    contrast=["condition", "treated", "control"],
    alpha=0.05,
    cooks_filter=True,
    independent_filter=True,
)
ds.summary()

# -----------------------------
# 5) Results + optional shrinkage
# -----------------------------
res = ds.results_df.copy()
sig = res[res["padj"] < 0.05].sort_values("padj")
print(f"Significant genes (padj < 0.05): {len(sig)}")

# Optional: shrink LFC for visualization/ranking (p-values do not change)
ds.lfc_shrink()
res_shrunk = ds.results_df.copy()

# Export
res.to_csv("deseq2_results.csv")
res_shrunk.to_csv("deseq2_results_shrunk_lfc.csv")
sig.to_csv("significant_genes.csv")

# -----------------------------
# 6) Minimal volcano plot (optional)
# -----------------------------
try:
    import matplotlib.pyplot as plt

    plot_df = res.copy()
    plot_df["neglog10_padj"] = -np.log10(plot_df["padj"].clip(lower=1e-300))
    is_sig = plot_df["padj"] < 0.05

    plt.figure(figsize=(9, 5))
    plt.scatter(
        plot_df.loc[~is_sig, "log2FoldChange"],
        plot_df.loc[~is_sig, "neglog10_padj"],
        s=10,
        alpha=0.3,
        c="gray",
        label="Not significant",
    )
    plt.scatter(
        plot_df.loc[is_sig, "log2FoldChange"],
        plot_df.loc[is_sig, "neglog10_padj"],
        s=10,
        alpha=0.6,
        c="red",
        label="padj < 0.05",
    )
    plt.axhline(-np.log10(0.05), linestyle="--", color="blue", alpha=0.5)
    plt.xlabel("Log2 Fold Change")
    plt.ylabel("-Log10(adjusted p-value)")
    plt.title("Volcano Plot")
    plt.legend()
    plt.tight_layout()
    plt.savefig("volcano_plot.png", dpi=300)
except ImportError:
    pass
```

## Common Analysis Patterns

### Two-Group Comparison

Standard case-control comparison:

```python
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition")
dds.deseq2()

ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()

results = ds.results_df
significant = results[results.padj < 0.05]
```

### Multiple Comparisons

Testing multiple treatment groups against control:

```python
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition")
dds.deseq2()

treatments = ["treatment_A", "treatment_B", "treatment_C"]
all_results = {}

for treatment in treatments:
    ds = DeseqStats(dds, contrast=["condition", treatment, "control"])
    ds.summary()
    all_results[treatment] = ds.results_df

    sig_count = len(ds.results_df[ds.results_df.padj < 0.05])
    print(f"{treatment}: {sig_count} significant genes")
```

### Accounting for Batch Effects

Control for technical variation:

```python
# Include batch in design
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~batch + condition")
dds.deseq2()

# Test condition while controlling for batch
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()
```

### Continuous Covariates

Include continuous variables like age or dosage:

```python
# Ensure continuous variable is numeric
metadata["age"] = pd.to_numeric(metadata["age"])

dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~age + condition")
dds.deseq2()

ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()
```

## Result Interpretation

### Identifying Significant Genes

```python
# Filter by adjusted p-value
significant = ds.results_df[ds.results_df.padj < 0.05]

# Filter by both significance and effect size
sig_and_large = ds.results_df[
    (ds.results_df.padj < 0.05) &
    (abs(ds.results_df.log2FoldChange) > 1)
]

# Separate up- and down-regulated
upregulated = significant[significant.log2FoldChange > 0]
downregulated = significant[significant.log2FoldChange < 0]

print(f"Upregulated: {len(upregulated)}")
print(f"Downregulated: {len(downregulated)}")
```

### Ranking and Sorting

```python
# Sort by adjusted p-value
top_by_padj = ds.results_df.sort_values("padj").head(20)

# Sort by absolute fold change (use shrunk values)
ds.lfc_shrink()
ds.results_df["abs_lfc"] = abs(ds.results_df.log2FoldChange)
top_by_lfc = ds.results_df.sort_values("abs_lfc", ascending=False).head(20)

# Sort by a combined metric
ds.results_df["score"] = -np.log10(ds.results_df.padj) * abs(ds.results_df.log2FoldChange)
top_combined = ds.results_df.sort_values("score", ascending=False).head(20)
```

### Quality Metrics

```python
# Check normalization (size factors should be close to 1)
print("Size factors:", dds.obsm["size_factors"])

# Examine dispersion estimates
import matplotlib.pyplot as plt
plt.hist(dds.varm["dispersions"], bins=50)
plt.xlabel("Dispersion")
plt.ylabel("Frequency")
plt.title("Dispersion Distribution")
plt.show()

# Check p-value distribution (should be mostly flat with peak near 0)
plt.hist(ds.results_df.pvalue.dropna(), bins=50)
plt.xlabel("P-value")
plt.ylabel("Frequency")
plt.title("P-value Distribution")
plt.show()
```

## Visualization Guidelines

### Volcano Plot

Visualize significance vs effect size:

```python
import matplotlib.pyplot as plt
import numpy as np

results = ds.results_df.copy()
results["-log10(padj)"] = -np.log10(results.padj)

plt.figure(figsize=(10, 6))
significant = results.padj < 0.05

plt.scatter(
    results.loc[~significant, "log2FoldChange"],
    results.loc[~significant, "-log10(padj)"],
    alpha=0.3, s=10, c='gray', label='Not significant'
)
plt.scatter(
    results.loc[significant, "log2FoldChange"],
    results.loc[significant, "-log10(padj)"],
    alpha=0.6, s=10, c='red', label='padj < 0.05'
)

plt.axhline(-np.log10(0.05), color='blue', linestyle='--', alpha=0.5)
plt.xlabel("Log2 Fold Change")
plt.ylabel("-Log10(Adjusted P-value)")
plt.title("Volcano Plot")
plt.legend()
plt.savefig("volcano_plot.png", dpi=300)
```

### MA Plot

Show fold change vs mean expression:

```python
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(10, 6))

plt.scatter(
    np.log10(results.loc[~significant, "baseMean"] + 1),
    results.loc[~significant, "log2FoldChange"],
    alpha=0.3, s=10, c='gray'
)
plt.scatter(
    np.log10(results.loc[significant, "baseMean"] + 1),
    results.loc[significant, "log2FoldChange"],
    alpha=0.6, s=10, c='red'
)

plt.axhline(0, color='blue', linestyle='--', alpha=0.5)
plt.xlabel("Log10(Base Mean + 1)")
plt.ylabel("Log2 Fold Change")
plt.title("MA Plot")
plt.savefig("ma_plot.png", dpi=300)
```

## Troubleshooting Common Issues

### Data Format Problems

**Issue:** "Index mismatch between counts and metadata"

**Solution:** Ensure sample names match exactly

```python
print("Counts samples:", counts_df.index.tolist())
print("Metadata samples:", metadata.index.tolist())

# Take intersection if needed
common = counts_df.index.intersection(metadata.index)
counts_df = counts_df.loc[common]
metadata = metadata.loc[common]
```

**Issue:** "All genes have zero counts"

**Solution:** Check if data needs transposition

```python
print(f"Counts shape: {counts_df.shape}")
# If genes > samples, transpose is needed
if counts_df.shape[1] < counts_df.shape[0]:
    counts_df = counts_df.T
```

### Design Matrix Issues

**Issue:** "Design matrix is not full rank"

**Cause:** Confounded variables (e.g., all treated samples in one batch)

**Solution:** Remove confounded variable or add interaction term

```python
# Check confounding
print(pd.crosstab(metadata.condition, metadata.batch))

# Either simplify design or add interaction
design = "~condition"  # Remove batch
# OR
design = "~condition + batch + condition:batch"  # Model interaction
```

### No Significant Genes

**Diagnostics:**

```python
# Check dispersion distribution
import matplotlib.pyplot as plt
plt.hist(dds.varm["dispersions"], bins=50)
plt.show()

# Check size factors
print(dds.obsm["size_factors"])

# Look at top genes by raw p-value
print(ds.results_df.nsmallest(20, "pvalue"))
```

**Possible causes:**

*   Small effect sizes
*   High biological variability
*   Insufficient sample size
*   Technical issues (batch effects, outliers)

## Using the Analysis Script

If your repository includes it, use:

```bash
# Basic usage
python scripts/run_deseq2_analysis.py \
  --counts counts.csv \
  --metadata metadata.csv \
  --design "~condition" \
  --contrast condition treated control \
  --output results/

# With additional options
python scripts/run_deseq2_analysis.py \
  --counts counts.csv \
  --metadata metadata.csv \
  --design "~batch + condition" \
  --contrast condition treated control \
  --output results/ \
  --min-counts 10 \
  --alpha 0.05 \
  --n-cpus 4 \
  --plots
```

**Script features:**

*   Automatic data loading and validation
*   Gene and sample filtering
*   Complete DESeq2 pipeline execution
*   Statistical testing with customizable parameters
*   Result export (CSV, pickle)
*   Optional visualization (volcano and MA plots)

Refer users to `scripts/run_deseq2_analysis.py` when they need a standalone analysis tool or want to batch process multiple datasets.

## Reference Documentation

If your repository includes them, use:

*   `references/api_reference.md` for parameter/object details.
*   `references/workflow_guide.md` for extended workflows and troubleshooting.

Load these references into context when users need:

*   Detailed API documentation: `Read references/api_reference.md`
*   Comprehensive workflow examples: `Read references/workflow_guide.md`
*   Troubleshooting guidance: `Read references/workflow_guide.md` (see Troubleshooting section)

## Key Reminders

1.  **Data orientation matters:** Count matrices typically load as genes × samples but need to be samples × genes. Always transpose with `.T` if needed.
2.  **Sample filtering:** Remove samples with missing metadata before analysis to avoid errors.
3.  **Gene filtering:** Filter low-count genes (e.g., < 10 total reads) to improve power and reduce computational time.
4.  **Design formula order:** Put adjustment variables before the variable of interest (e.g., `"~batch + condition"` not `"~condition + batch"`).
5.  **LFC shrinkage timing:** Apply shrinkage after statistical testing and only for visualization/ranking purposes. P-values remain based on unshrunken estimates.
6.  **Result interpretation:** Use `padj < 0.05` for significance, not raw p-values. The Benjamini-Hochberg procedure controls false discovery rate.
7.  **Contrast specification:** The format is `[variable, test_level, reference_level]` where test_level is compared against reference_level.
8.  **Save intermediate objects:** Use pickle to save DeseqDataSet objects for later use or additional analyses without re-running the expensive fitting step.

## Additional Resources

*   **Official Documentation:** https://pydeseq2.readthedocs.io
*   **GitHub Repository:** https://github.com/owkin/PyDESeq2
*   **Publication:** Muzellec et al. (2023) Bioinformatics, DOI: 10.1093/bioinformatics/btad547
*   **Original DESeq2 (R):** Love et al. (2014) Genome Biology, DOI: 10.1186/s13059-014-0550-8