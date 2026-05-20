---
name: cellxgene-census
description: Programmatically query the CZ CELLxGENE Census (61M+ cells) when you need cross-tissue, disease, or cell-type expression data for population-scale queries and reference atlas comparisons. Best for population-scale queries, reference atlas comparisons, and training models on curated atlas data.
license: MIT
metadata:
    skill-author: K-Dense Inc. & AIPOCH
---
---

## Overview

The CZ CELLxGENE Census provides programmatic access to a comprehensive, versioned collection of standardized single-cell genomics data from CZ CELLxGENE Discover. This skill enables efficient querying and analysis of millions of cells across thousands of datasets.

The Census includes:
- **61+ million cells** from human and mouse
- **Standardized metadata** (cell types, tissues, diseases, donors)
- **Raw gene expression** matrices
- **Pre-calculated embeddings** and statistics
- **Integration with PyTorch, scanpy, and other analysis tools**

## When to Use

- **Cross-tissue or cross-disease expression comparisons** (e.g., macrophages across lung/liver/brain; COVID-19 vs control).
- **Reference atlas lookups** to contextualize findings from your own single-cell dataset (marker validation, expected expression patterns).
- **Population-scale metadata exploration** (what tissues/cell types/datasets exist; cell counts by cohort attributes).
- **Large-scale expression statistics** where results exceed RAM and require out-of-core iteration.
- **Model training on curated atlas data** (e.g., cell-type classifiers) using the experimental PyTorch integration.

## Key Features

- Programmatic access to **versioned** CZ CELLxGENE Census data (human and mouse).
- Query **cell (obs) metadata** and **gene (var) metadata** with expressive filter syntax.
- Retrieve expression as **AnnData** for small/medium queries via `get_anndata()`.
- Perform **out-of-core** expression access via SOMA `axis_query()` and chunked iteration.
- Optional **experimental ML utilities** (PyTorch dataloaders/datasets).
- Works well with **scanpy** workflows after loading AnnData.

## Dependencies

- `cellxgene-census` (latest)
- `tiledbsoma` (latest; required for `axis_query()` workflows)
- `pyarrow` (latest; used for chunked table batches)
- `anndata` (latest; for `get_anndata()` results)
- `scanpy` (latest; optional, for downstream analysis)
- `torch` (latest; optional, for experimental ML integration)

Install:
```bash
uv pip install cellxgene-census
```

Optional (experimental ML helpers):
```bash
uv pip install cellxgene-census[experimental]
```

## Core Workflow Patterns

### 1. Opening the Census

Always use the context manager to ensure proper resource cleanup:

```python
import cellxgene_census

# Open latest stable version
with cellxgene_census.open_soma() as census:
    # Work with census data

# Open specific version for reproducibility
with cellxgene_census.open_soma(census_version="2023-07-25") as census:
    # Work with census data
```

**Key points:**
- Use context manager (`with` statement) for automatic cleanup.
- Specify `census_version` for reproducible analyses.
- Default opens latest "stable" release.

### 2. Exploring Census Information

Before querying expression data, explore available datasets and metadata.

**Access summary information:**
```python
# Get summary statistics
import cellxgene_census
with cellxgene_census.open_soma() as census:
    summary = census["census_info"]["summary"].read().concat().to_pandas()
    print(f"Total cells: {summary['total_cell_count'][0]}")

    # Get all datasets
    datasets = census["census_info"]["datasets"].read().concat().to_pandas()

    # Filter datasets by criteria
    covid_datasets = datasets[datasets["disease"].str.contains("COVID", na=False)]
```

**Query cell metadata to understand available data:**
```python
import cellxgene_census
with cellxgene_census.open_soma() as census:
    # Get unique cell types in a tissue
    cell_metadata = cellxgene_census.get_obs(
        census,
        "homo_sapiens",
        value_filter="tissue_general == 'brain' and is_primary_data == True",
        column_names=["cell_type"]
    )
    unique_cell_types = cell_metadata["cell_type"].unique()
    print(f"Found {len(unique_cell_types)} cell types in brain")

    # Count cells by tissue
    tissue_counts = cell_metadata.groupby("tissue_general").size()
```

**Important:** Always filter for `is_primary_data == True` to avoid counting duplicate cells unless specifically analyzing duplicates.

### 3. Querying Expression Data (Small to Medium Scale)

For queries returning < 100k cells that fit in memory, use `get_anndata()`:

```python
import cellxgene_census
with cellxgene_census.open_soma() as census:
    # Basic query with cell type and tissue filters
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",  # or "Mus musculus"
        obs_value_filter="cell_type == 'B cell' and tissue_general == 'lung' and is_primary_data == True",
        obs_column_names=["assay", "disease", "sex", "donor_id"],
    )

    # Query specific genes with multiple filters
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19', 'FOXP3']",
        obs_value_filter="cell_type == 'T cell' and disease == 'COVID-19' and is_primary_data == True",
        obs_column_names=["cell_type", "tissue_general", "donor_id"],
    )
```

**Filter syntax:**
- Use `obs_value_filter` for cell filtering
- Use `var_value_filter` for gene filtering
- Combine conditions with `and`, `or`
- Use `in` for multiple values: `tissue in ['lung', 'liver']`
- Select only needed columns with `obs_column_names`

**Getting metadata separately:**
```python
import cellxgene_census
with cellxgene_census.open_soma() as census:
    # Query cell metadata
    cell_metadata = cellxgene_census.get_obs(
        census, "homo_sapiens",
        value_filter="disease == 'COVID-19' and is_primary_data == True",
        column_names=["cell_type", "tissue_general", "donor_id"]
    )

    # Query gene metadata
    gene_metadata = cellxgene_census.get_var(
        census, "homo_sapiens",
        value_filter="feature_name in ['CD4', 'CD8A']",
        column_names=["feature_id", "feature_name", "feature_length"]
    )
```

### 4. Large-Scale Queries (Out-of-Core Processing)

For queries exceeding available RAM, use `axis_query()` with iterative processing:

```python
import tiledbsoma as soma
import cellxgene_census

with cellxgene_census.open_soma() as census:
    # Create axis query
    query = census["census_data"]["homo_sapiens"].axis_query(
        measurement_name="RNA",
        obs_query=soma.AxisQuery(
            value_filter="tissue_general == 'brain' and is_primary_data == True"
        ),
        var_query=soma.AxisQuery(
            value_filter="feature_name in ['FOXP2', 'TBR1', 'SATB2']"
        )
    )

    # Iterate through expression matrix in chunks
    iterator = query.X("raw").tables()
    for batch in iterator:
        # batch is a pyarrow.Table with columns:
        # - soma_data: expression value
        # - soma_dim_0: cell (obs) coordinate
        # - soma_dim_1: gene (var) coordinate
        process_batch(batch) # Replace with your processing logic
```

**Computing incremental statistics:**
```python
import tiledbsoma as soma
import cellxgene_census
import numpy as np

with cellxgene_census.open_soma() as census:
    # Create axis query
    query = census["census_data"]["homo_sapiens"].axis_query(
        measurement_name="RNA",
        obs_query=soma.AxisQuery(
            value_filter="tissue_general == 'brain' and is_primary_data == True"
        ),
        var_query=soma.AxisQuery(
            value_filter="feature_name in ['FOXP2', 'TBR1', 'SATB2']"
        )
    )
    # Example: Calculate mean expression
    n_observations = 0
    sum_values = 0.0

    iterator = query.X("raw").tables()
    for batch in iterator:
        values = batch["soma_data"].to_numpy()
        n_observations += len(values)
        sum_values += values.sum()

    mean_expression = sum_values / n_observations
    print(f"Mean Expression: {mean_expression}")
```

### 5. Machine Learning with PyTorch

For training models, use the experimental PyTorch integration:

```python
from cellxgene_census.experimental.ml import experiment_dataloader
import cellxgene_census

with cellxgene_census.open_soma() as census:
    # Create dataloader
    dataloader = experiment_dataloader(
        census["census_data"]["homo_sapiens"],
        measurement_name="RNA",
        X_name="raw",
        obs_value_filter="tissue_general == 'liver' and is_primary_data == True",
        obs_column_names=["cell_type"],
        batch_size=128,
        shuffle=True,
    )

    # Training loop
    for epoch in range(num_epochs): # Replace num_epochs with a number
        for batch in dataloader:
            X = batch["X"]  # Gene expression tensor
            labels = batch["obs"]["cell_type"]  # Cell type labels

            # Forward pass (replace with your model)
            # outputs = model(X)
            # loss = criterion(outputs, labels)

            # Backward pass (replace with your training logic)
            # optimizer.zero_grad()
            # loss.backward()
            # optimizer.step()
            pass
```

**Train/test splitting:**
```python
from cellxgene_census.experimental.ml import ExperimentDataset
import cellxgene_census
import tiledbsoma as soma

with cellxgene_census.open_soma() as census:
    query = census["census_data"]["homo_sapiens"].axis_query(
        measurement_name="RNA",
        obs_query=soma.AxisQuery(value_filter="is_primary_data == True"),
        var_query=soma.AxisQuery()
    )
    # Create dataset from experiment
    dataset = ExperimentDataset(
        query,
        layer_name="raw",
        obs_column_names=["cell_type"],
        batch_size=128,
    )

    # Split into train and test
    train_dataset, test_dataset = dataset.random_split(
        split=[0.8, 0.2],
        seed=42
    )
```

### 6. Integration with Scanpy

Seamlessly integrate Census data with scanpy workflows:

```python
import scanpy as sc
import cellxgene_census

with cellxgene_census.open_soma() as census:
    # Load data from Census
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter="cell_type == 'neuron' and tissue_general == 'cortex' and is_primary_data == True",
    )

    # Standard scanpy workflow
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=2000)

    # Dimensionality reduction
    sc.pp.pca(adata, n_comps=50)
    sc.pp.neighbors(adata)
    sc.tl.umap(adata)

    # Visualization
    sc.pl.umap(adata, color=["cell_type", "tissue", "disease"])
```

### 7. Multi-Dataset Integration

Query and integrate multiple datasets:

```python
import cellxgene_census
import scanpy as sc

with cellxgene_census.open_soma() as census:
    # Strategy 1: Query multiple tissues separately
    tissues = ["lung", "liver", "kidney"]
    adatas = []

    for tissue in tissues:
        adata = cellxgene_census.get_anndata(
            census=census,
            organism="Homo sapiens",
            obs_value_filter=f"tissue_general == '{tissue}' and is_primary_data == True",
        )
        adata.obs["tissue"] = tissue
        adatas.append(adata)

    # Concatenate
    combined = adatas[0].concatenate(adatas[1:])

    # Strategy 2: Query multiple datasets directly
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter="tissue_general in ['lung', 'liver', 'kidney'] and is_primary_data == True",
    )
```

## Example Usage

The following script is a complete, runnable example that:
1) opens a pinned Census version,
2) explores metadata,
3) loads a small AnnData slice, and
4) runs an out-of-core query to compute a simple statistic.

```python
import numpy as np
import cellxgene_census
import tiledbsoma as soma

def main():
    # Pin a version for reproducibility (replace with a valid release if needed)
    census_version = "2023-07-25"

    with cellxgene_census.open_soma(census_version=census_version) as census:
        # 1) Explore summary info
        summary = census["census_info"]["summary"].read().concat().to_pandas()
        total_cells = int(summary["total_cell_count"].iloc[0])
        print(f"Census version: {census_version}")
        print(f"Total cells: {total_cells:,}")

        # 2) Explore obs metadata (always filter primary data unless you want duplicates)
        obs = cellxgene_census.get_obs(
            census,
            "homo_sapiens",
            value_filter="tissue_general == 'brain' and is_primary_data == True",
            column_names=["cell_type", "tissue_general", "disease", "donor_id"],
        )
        print(f"Brain (primary) cells returned (metadata only): {len(obs):,}")
        print("Top cell types:")
        print(obs["cell_type"].value_counts().head(10))

        # 3) Small/medium query -> AnnData in memory
        adata = cellxgene_census.get_anndata(
            census=census,
            organism="Homo sapiens",
            obs_value_filter=(
                "cell_type == 'T cell' and disease == 'COVID-19' and is_primary_data == True"
            ),
            var_value_filter="feature_name in ['CD4', 'CD8A', 'FOXP3']",
            obs_column_names=["cell_type", "tissue_general", "disease", "donor_id", "sex"],
        )
        print(adata)
        print("AnnData X shape:", adata.X.shape)

        # 4) Large-scale pattern -> out-of-core iteration with axis_query()
        # Example: compute mean of non-zero expression values for a few genes in brain.
        query = census["census_data"]["homo_sapiens"].axis_query(
            measurement_name="RNA",
            obs_query=soma.AxisQuery(
                value_filter="tissue_general == 'brain' and is_primary_data == True"
            ),
            var_query=soma.AxisQuery(
                value_filter="feature_name in ['FOXP2', 'TBR1', 'SATB2']"
            ),
        )

        n = 0
        s = 0.0
        for batch in query.X("raw").tables():
            # batch is a pyarrow.Table with at least: soma_data, soma_dim_0, soma_dim_1
            values = batch["soma_data"].to_numpy(zero_copy_only=False)
            n += values.size
            s += float(values.sum())

        mean_expr = s / n if n else np.nan
        print(f"Out-of-core mean expression (over returned entries): {mean_expr:.6g}")

if __name__ == "__main__":
    main()
```

## Implementation Details

- **Opening the Census**
  - Use a context manager to ensure resources are released:
    - `with cellxgene_census.open_soma(...) as census: ...`
  - For reproducibility, set `census_version="YYYY-MM-DD"`; otherwise the latest stable release is used.

- **Data model (high level)**
  - Census data is stored in **SOMA** collections.
  - `census["census_info"]` provides summary tables (e.g., datasets, counts).
  - `census["census_data"][organism]` provides the experiment for an organism (e.g., `homo_sapiens`).

- **Filtering semantics**
  - `obs_value_filter` filters **cells** (obs); `var_value_filter` filters **genes** (var).
  - Combine predicates with `and` / `or`; use `in [...]` for multi-value membership.
  - Best practice: include `is_primary_data == True` to avoid double-counting cells that appear in multiple source datasets.

- **Choosing an access pattern**
  - Use `get_anndata()` when the result is expected to fit in memory (commonly < ~100k cells, depending on gene count and sparsity).
  - Use `axis_query()` + `query.X("raw").tables()` for **out-of-core** iteration and incremental statistics.

- **Expression layers / matrices**
  - Examples commonly use `X("raw")` to access raw expression.
  - Chunk iteration yields Arrow tables with:
    - `soma_data`: expression values
    - `soma_dim_0`: obs (cell) coordinates
    - `soma_dim_1`: var (gene) coordinates

- **Optional ML integration**
  - The `cellxgene_census.experimental.ml` utilities provide PyTorch-friendly datasets/dataloaders for training workflows, typically driven by the same obs/var filtering concepts used elsewhere.

## Key Concepts and Best Practices

### Always Filter for Primary Data
Unless analyzing duplicates, always include `is_primary_data == True` in queries to avoid counting cells multiple times:
```python
obs_value_filter="cell_type == 'B cell' and is_primary_data == True"
```

### Specify Census Version for Reproducibility
Always specify the Census version in production analyses:
```python
census = cellxgene_census.open_soma(census_version="2023-07-25")
```

### Estimate Query Size Before Loading
For large queries, first check the number of cells to avoid memory issues:
```python
import cellxgene_census

with cellxgene_census.open_soma() as census:
    # Get cell count
    metadata = cellxgene_census.get_obs(
        census, "homo_sapiens",
        value_filter="tissue_general == 'brain' and is_primary_data == True",
        column_names=["soma_joinid"]
    )
    n_cells = len(metadata)
    print(f"Query will return {n_cells:,} cells")

    # If too large (>100k), use out-of-core processing
```

### Use tissue_general for Broader Groupings
The `tissue_general` field provides coarser categories than `tissue`, useful for cross-tissue analyses:
```python
# Broader grouping
obs_value_filter="tissue_general == 'immune system'"

# Specific tissue
obs_value_filter="tissue == 'peripheral blood mononuclear cell'"
```

### Select Only Needed Columns
Minimize data transfer by specifying only required metadata columns:
```python
obs_column_names=["cell_type", "tissue_general", "disease"]  # Not all columns
```

### Check Dataset Presence for Gene-Specific Queries
When analyzing specific genes, verify which datasets measured them:
```python
presence = cellxgene_census.get_presence_matrix(
    census,
    "homo_sapiens",
    var_value_filter="feature_name in ['CD4', 'CD8A']"
)
```

### Two-Step Workflow: Explore Then Query
First explore metadata to understand available data, then query expression:
```python
import cellxgene_census

with cellxgene_census.open_soma() as census:
    # Step 1: Explore what's available
    metadata = cellxgene_census.get_obs(
        census, "homo_sapiens",
        value_filter="disease == 'COVID-19' and is_primary_data == True",
        column_names=["cell_type", "tissue_general"]
    )
    print(metadata.value_counts())

    # Step 2: Query based on findings
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter="disease == 'COVID-19' and cell_type == 'T cell' and is_primary_data == True",
    )
```

## Available Metadata Fields

### Cell Metadata (obs)
Key fields for filtering:
- `cell_type`, `cell_type_ontology_term_id`
- `tissue`, `tissue_general`, `tissue_ontology_term_id`
- `disease`, `disease_ontology_term_id`
- `assay`, `assay_ontology_term_id`
- `donor_id`, `sex`, `self_reported_ethnicity`
- `development_stage`, `development_stage_ontology_term_id`
- `dataset_id`
- `is_primary_data` (Boolean: True = unique cell)

### Gene Metadata (var)
- `feature_id` (Ensembl gene ID, e.g., "ENSG00000161798")
- `feature_name` (Gene symbol, e.g., "FOXP2")
- `feature_length` (Gene length in base pairs)

## Common Use Cases

### Use Case 1: Explore Cell Types in a Tissue
```python
import cellxgene_census

with cellxgene_census.open_soma() as census:
    cells = cellxgene_census.get_obs(
        census, "homo_sapiens",
        value_filter="tissue_general == 'lung' and is_primary_data == True",
        column_names=["cell_type"]
    )
    print(cells["cell_type"].value_counts())
```

### Use Case 2: Query Marker Gene Expression
```python
import cellxgene_census

with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19']",
        obs_value_filter="cell_type in ['T cell', 'B cell'] and is_primary_data == True",
    )
```

### Use Case 3: Train Cell Type Classifier
```python
from cellxgene_census.experimental.ml import experiment_dataloader
import cellxgene_census

with cellxgene_census.open_soma() as census:
    dataloader = experiment_dataloader(
        census["census_data"]["homo_sapiens"],
        measurement_name="RNA",
        X_name="raw",
        obs_value_filter="is_primary_data == True",
        obs_column_names=["cell_type"],
        batch_size=128,
        shuffle=True,
    )

    # Train model
    for epoch in range(epochs): # Replace epochs with a number
        for batch in dataloader:
            # Training logic (replace with your logic)
            pass
```

### Use Case 4: Cross-Tissue Analysis
```python
import cellxgene_census
import scanpy as sc

with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter="cell_type == 'macrophage' and tissue_general in ['lung', 'liver', 'brain'] and is_primary_data == True",
    )

    # Analyze macrophage differences across tissues
    sc.tl.rank_genes_groups(adata, groupby="tissue_general")
```

## Troubleshooting

### Query Returns Too Many Cells
- Add more specific filters to reduce scope
- Use `tissue` instead of `tissue_general` for finer granularity
- Filter by specific `dataset_id` if known
- Switch to out-of-core processing for large queries

### Memory Errors
- Reduce query scope with more restrictive filters
- Select fewer genes with `var_value_filter`
- Use out-of-core processing with `axis_query()`
- Process data in batches

### Duplicate Cells in Results
- Always include `is_primary_data == True` in filters
- Check if intentionally querying across multiple datasets

### Gene Not Found
- Verify gene name spelling (case-sensitive)
- Try Ensembl ID with `feature_id` instead of `feature_name`
- Check dataset presence matrix to see if gene was measured
- Some genes may have been filtered during Census construction

### Version Inconsistencies
- Always specify `census_version` explicitly
- Use same version across all analyses
- Check release notes for version-specific changes