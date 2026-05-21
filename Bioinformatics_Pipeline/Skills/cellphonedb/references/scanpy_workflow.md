# Scanpy → CellphoneDB Workflow

Complete workflow for going from a Scanpy AnnData object to CellphoneDB results.

## Step 1: Prepare Counts and Meta from AnnData

```python
import scanpy as sc
import pandas as pd

# Load processed AnnData
adata = sc.read_h5ad("processed.h5ad")

# Ensure cell type annotations exist
# (adata.obs should have a cell type column, e.g., 'cell_type' or 'leiden')

# Option A: Save as h5ad directly (recommended)
adata.write_h5ad("cpdb_counts.h5ad")

# Option B: Save as text (for small datasets only)
# pd.DataFrame(adata.X.toarray(), index=adata.obs_names, columns=adata.var_names).T.to_csv("cpdb_counts.txt", sep='\t')

# Create meta file
meta = pd.DataFrame({
    'Cell': adata.obs_names,
    'cell_type': adata.obs['cell_type'].values
})
meta.to_csv("cpdb_meta.txt", sep='\t', index=False)
```

## Step 2: Generate DEGs (for Method 3)

```python
# Standard one-vs-rest DEG analysis
sc.tl.rank_genes_groups(adata, groupby='cell_type', method='wilcoxon')

# Extract DEGs with filters
degs_list = []
for ct in adata.obs['cell_type'].unique():
    result = sc.get.rank_genes_groups_df(adata, group=ct)
    # Filter: adjusted p-value < 0.05 and log2FC > 0.5
    sig_genes = result[(result['pvals_adj'] < 0.05) & (result['logfoldchanges'] > 0.5)]
    for gene in sig_genes['names']:
        degs_list.append([ct, gene])

degs_df = pd.DataFrame(degs_list, columns=['cell_type', 'gene'])
degs_df.to_csv("cpdb_degs.txt", sep='\t', index=False, header=False)
```

### Alternative: Hierarchical DEG (within a lineage)

```python
# Compare subtypes within a lineage
lineage_adata = adata[adata.obs['lineage'] == 'Epithelial']
sc.tl.rank_genes_groups(lineage_adata, groupby='cell_type', method='wilcoxon')

# Extract as above
```

### Alternative: Disease vs Control DEG

```python
# Per cell-type comparison between conditions
for ct in adata.obs['cell_type'].unique():
    ct_adata = adata[adata.obs['cell_type'] == ct].copy()
    if ct_adata.obs['condition'].nunique() < 2:
        continue
    sc.tl.rank_genes_groups(ct_adata, groupby='condition', reference='Control', method='wilcoxon')
    result = sc.get.rank_genes_groups_df(ct_adata, group='Disease')
    sig_genes = result[(result['pvals_adj'] < 0.05) & (result['logfoldchanges'] > 0.5)]
    for gene in sig_genes['names']:
        degs_list.append([ct, gene])
```

## Step 3: Create Microenvironments File (optional)

```python
# From prior knowledge
microenvs = pd.DataFrame({
    'cell_type': ['T cells', 'Macrophages', 'Fibroblasts', 'Epithelial', 'Endothelial'],
    'microenvironment': ['immune_zone', 'immune_zone', 'stromal_zone', 'epithelial_zone', 'vascular_zone']
})
microenvs.to_csv("cpdb_microenvs.txt", sep='\t', index=False, header=False)
```

## Step 4: Estimate Active TFs (optional, for CellSign)

```python
# Using DoRothEA (via decoupler)
import decoupler as dc

# Get TF activities
dc.run_mlm(adata, net=dc.get_dorothea(), source='source', target='target', weight='weight', use_raw=False)
tf_acts = adata.obsm['mlm_estimate']

# Determine active TFs per cell type (z-score > 2)
active_tfs_list = []
for ct in adata.obs['cell_type'].unique():
    ct_mask = adata.obs['cell_type'] == ct
    mean_acts = tf_acts[ct_mask].mean(axis=0)
    active = mean_acts[mean_acts > 2].index.tolist()
    for tf in active:
        active_tfs_list.append([ct, tf])

active_tfs_df = pd.DataFrame(active_tfs_list, columns=['cell_type', 'tf'])
active_tfs_df.to_csv("cpdb_active_tfs.txt", sep='\t', index=False, header=False)
```

## Step 5: Run CellphoneDB

```python
from cellphonedb.src.core.methods import cpdb_degs_analysis_method

cpdb_results = cpdb_degs_analysis_method.call(
    cpdb_file_path = "cpdb_data/cellphonedb.zip",
    meta_file_path = "cpdb_meta.txt",
    counts_file_path = "cpdb_counts.h5ad",
    degs_file_path = "cpdb_degs.txt",
    counts_data = 'hgnc_symbol',
    score_interactions = True,
    active_tfs_file_path = "cpdb_active_tfs.txt",
    microenvs_file_path = "cpdb_microenvs.txt",
    threshold = 0.1,
    output_path = "cpdb_output"
)
```

## Step 6: Explore and Visualize

```python
import ktplotspy as kpy

# Overview heatmap
kpy.plot_cpdb_heatmap(pvals=cpdb_results['pvalues'])

# Detailed dot plot
kpy.plot_cpdb(
    adata=adata,
    cell_type1="T cells",
    cell_type2="Macrophages",
    means=cpdb_results['significant_means'],
    pvals=cpdb_results['pvalues'],
    celltype_key="cell_type",
    figsize=(12, 8)
)

# Query specific interactions
from cellphonedb.utils import search_utils
results = search_utils.search_analysis_results(
    query_cell_types_1=['T cells'],
    query_cell_types_2=['Macrophages'],
    significant_means=cpdb_results['significant_means'],
    deconvoluted=cpdb_results['cpdb_deconvoluted'],
    long_format=True
)
```

## Gene ID Conversion (Mouse → Human)

```python
import pandas as pd

# Using biomart
# pip install pybiomart
from pybiomart import Dataset

# Get mouse-human orthology mapping
dataset = Dataset(name='mmusculus_gene_ensembl', host='http://www.ensembl.org')
orthologs = dataset.query(attributes=['external_gene_name', 'hsapiens_homolog_associated_gene_name'])
orthologs = orthologs.dropna()
gene_map = dict(zip(orthologs['Gene name'], orthologs['Human gene name']))

# Convert
adata.var['human_gene'] = adata.var_names.map(gene_map)
adata = adata[:, adata.var['human_gene'].notna()]
adata.var_names = adata.var['human_gene'].values
adata.var_names_make_unique()
```
