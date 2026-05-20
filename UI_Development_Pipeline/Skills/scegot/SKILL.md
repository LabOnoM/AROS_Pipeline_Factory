---
name: scegot
description: Guide for using scEGOT (single-cell trajectory inference framework based on Entropic Gaussian mixture Optimal Transport). Covers basic preprocessing, GMM fitting, cell state graphs, cell velocities, GRN, and Waddington Landscape reconstruction.
---

# scEGOT Analysis Guide

**scEGOT** is a single-cell trajectory inference framework based on entropic Gaussian mixture optimal transport (EGOT). This skill outlines how to use the scEGOT Python module for trajectory inference, Waddington landscape reconstruction, velocity estimation, and gene regulatory network (GRN) extraction.

**Reference:** [yachimura-lab/scEGOT](https://github.com/yachimura-lab/scEGOT) 
**Installation:** `pip install scegot`

## 1. Initialization and Input

You can initiate the `scEGOT` object using AnnData or DataFrames via CSV files. 

**AnnData Approach:**
```python
import anndata
from scegot import scEGOT

input_data = anndata.read_h5ad("path_to_data.h5ad")
# Pass the observation key that identifies the time point/day
scegot_obj = scEGOT(input_data, verbose=True, adata_day_key="cluster_day")
```

**DataFrame Approach:**
```python
import pandas as pd
from scegot import scEGOT

day_names = ["day0", "day0.5", "day1", "day1.5", "day2"]
input_data = [pd.read_csv(f"{day}.csv", index_col=0).T for day in day_names]
scegot_obj = scEGOT(input_data, verbose=True, day_names=day_names)
```

## 2. Preprocessing

Preprocess runs RECODE -> UMI normalization -> Log1p normalization -> Select Variable Genes -> PCA. 
```python
PCA_N_COMPONENTS = 30
X, pca_model = scegot_obj.preprocess(
    PCA_N_COMPONENTS,
    umi_target_sum=1e5,
    pca_random_state=2023,
    apply_recode=True,
    apply_normalization_log1p=True,
    apply_normalization_umi=True,
    select_genes=True,
    n_select_genes=2000,
)
```
For non-linear low dimensional projections, UMAP can be applied subsequently:
```python
X_umap, umap_model = scegot_obj.apply_umap(n_neighbors=1000, n_components=2, random_state=2023, min_dist=0.8)
```

## 3. GMM Clustering
Apply Gaussian Mixture Models across various expected cluster numbers for each day.
```python
# Pass cluster numbers corresponding respectively to the sequential days
GMM_CLUSTER_NUMBERS = [1, 2, 4, 5, 5] 
gmm_models, gmm_labels = scegot_obj.fit_predict_gmm(
    n_components_list=GMM_CLUSTER_NUMBERS,
    covariance_type="full",
    max_iter=2000,
    n_init=10,
    random_state=2023
)

# Visualization
scegot_obj.plot_gmm_predictions(mode="pca", plot_gmm_means=True, cmap="plasma")
```

## 4. Cell State Graphs

Generate a Cell State Graph (CSG) modeling discrete temporal transitions:
```python
cluster_names = scegot_obj.generate_cluster_names_with_day()

# Create graph object
csg = scegot_obj.make_cell_state_graph_object(
    cluster_names=cluster_names, 
    mode="pca", # or "umap"
    threshold=0.2, 
    merge_clusters_by_name=False,
    require_parent=True
)

# Plotting Options
csg.plot_cell_state_graph(layout="normal", cluster_names=cluster_names, tf_gene_pick_num=5)
csg.plot_simple_cell_state_graph(layout="hierarchy", y_position="weight")
```
*Note: Clusters can be combined using `scegot_obj.merge_cluster_names_by_pathway(..., merge_method='kmeans')` before passing them to the object initialization.*

## 5. Expression Dynamics and Pathways

### Fold Change & Markers
Plot the Fold Change of specific genes between two nodes.
```python
scegot_obj.plot_fold_change(cluster_names, "day0.5-0", "day0.5-1", tf_gene_names=tf_gene_names, threshold=0.8)
```

### Continuous Distributions (Optimal Transport)
Explore the continuously shifted distribution between discrete points using EGOT interpolation.
```python
scegot_obj.animate_interpolated_distribution(cmap="gnuplot2", interpolate_interval=11)
scegot_obj.plot_true_and_interpolation_distributions(interpolate_index=2, mode="pca", n_samples=1000, t=0.5)

# For single gene trajectory
scegot_obj.animate_gene_expression("NANOG", mode="pca", interpolate_interval=11)
```

## 6. Cell Velocity

Velocity is calculated directly using the optimal transport plans.
```python
velocities = scegot_obj.calculate_cell_velocities()
scegot_obj.plot_cell_velocity(velocities, mode="pca", color_points="gmm", cmap="tab20")
```

## 7. Gene Regulatory Networks (GRN)

Compute GRNs across sequential development logic using Ridge regularization.
```python
# Compute universally
GRNs, ridgeCVs = scegot_obj.calculate_grns(alpha_range=(-2, 2), cv=3)

# Limit to pathway of interest
selected_clusters = [[0, 0], [1, 1], [2, 0], [3, 1]] # Format: [[time_point_index, cluster_idx], ...]
GRNs_sub, ridgeCVs_sub = scegot_obj.calculate_grns(selected_clusters=selected_clusters)

scegot_obj.plot_grn_graph(GRNs_sub, ridgeCVs_sub, selected_genes=["TFAP2C", "SOX17"], threshold=0.01)
```

## 8. Waddington Landscape Construction

Infer 3D Waddington potential surfaces utilizing local k-NN distributions.
```python
Wpotential, F_all = scegot_obj.calculate_waddington_potential(n_neighbors=100)

scegot_obj.plot_waddington_potential(Wpotential, mode="pca", gene_name="NANOG") # 3D Scatter View 
scegot_obj.plot_waddington_potential_surface(Wpotential, mode="umap") # 3D Surface Topology View
```
