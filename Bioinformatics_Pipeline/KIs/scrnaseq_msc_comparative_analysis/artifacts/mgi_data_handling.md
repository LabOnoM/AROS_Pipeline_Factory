# MGI DNBelab C4 Data Handling & Doublet Detection

## Data Loading
MGI DNBelab C4 data processed via `dnbc4tools` and `PISA` generates 10X-compatible matrix files. 

```python
# Load standard 10X-compatible output
adata = sc.read_10x_mtx(
    'path/to/outs/filtered_feature_bc_matrix',
    var_names='gene_symbols', cache=False
)
```

### Observations on Gene IDs
- Features include standard gene symbols (`Xkr4`, `Sox17`).
- Unannotated genes may appear as Ensembl IDs (`ENSMUSG...`).
- Mitochondrial genes use standard mouse prefix `mt-` (case-sensitive check recommended: `adata.var_names.str.lower().str.startswith('mt-')`).

## Doublet Detection: Solo vs. DoubletDecom

A critical insight from this analysis was the discrepancy between **Solo (scvi-tools)** and **DoubletDecom**.

### Solo failure mode
On homogeneous cultured MSC populations, Solo flagged an extremely high doublet rate (~45%). 
- **Cause**: The Variational Autoencoder (VAE) model in Solo may struggle to learn a diverse manifold for highly uniform cell types (expanded culture), leading to false positive doublet labels.
- **Recommendation**: Be cautious of Solo's results when the cell population is expected to be very similar.

### DoubletDecom robustness
**DoubletDecom** (using PMF) provided more realistic results for cultured cells (~0.5%) while maintaining sensitivity for bone marrow samples (~15-20%).
- **Implementation Note**: DoubletDecom results often use string booleans (`"TRUE"`, `"FALSE"`) in CSV outputs.

```python
def load_doubletdecom(path, prefix):
    drs = pd.read_csv(path, sep='\t', index_col=0)
    # Filter using string comparison as isADoublet is often a string
    doublets = drs[drs['isADoublet'].astype(str).str.upper() == 'TRUE'].index.tolist()
    return set(prefix + bc for bc in doublets)
```
