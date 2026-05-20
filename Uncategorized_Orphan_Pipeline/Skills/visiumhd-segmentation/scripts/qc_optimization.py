# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

"""
Visium HD Segmentation — QC Optimization Utilities

Self-regression parameter optimization loops and automated threshold estimation
for the Visium HD nuclei segmentation pipeline. These utilities are called by the
agent between QC gates to find optimal parameters before presenting to the user.

Usage:
    from qc_optimization import (
        evaluate_segmentation_on_roi,
        run_stardist_param_sweep,
        suggest_area_cutoff,
        suggest_umi_cutoff,
        preview_filtering,
        evaluate_clustering
    )
"""

import numpy as np
import pandas as pd
import scanpy as sc
from csbdeep.utils import normalize


# ──────────────────────────────────────────────────────────────────────────────
# StarDist Parameter Optimization
# ──────────────────────────────────────────────────────────────────────────────

def evaluate_segmentation_on_roi(img_crop, model, prob_thresh, nms_thresh):
    """
    Run StarDist on a single ROI crop and return quality metrics.

    Parameters
    ----------
    img_crop : np.ndarray
        Cropped and normalized H&E image region.
    model : StarDist2D
        Loaded StarDist model.
    prob_thresh : float
        Detection probability threshold.
    nms_thresh : float
        Non-maximum suppression threshold.

    Returns
    -------
    dict
        Quality metrics including n_nuclei, area stats, artifact fractions.
    """
    labels_roi, polys_roi = model.predict_instances(
        img_crop,
        prob_thresh=prob_thresh,
        nms_thresh=nms_thresh,
        n_tiles=(2, 2, 1),
        normalizer=None
    )

    n_nuclei = labels_roi.max()
    if n_nuclei == 0:
        return {
            'n_nuclei': 0, 'mean_area': 0, 'median_area': 0,
            'std_area': 0, 'cv_area': float('inf'),
            'very_large_frac': 0, 'very_small_frac': 0
        }

    areas = np.array([np.sum(labels_roi == i) for i in range(1, n_nuclei + 1)])
    cv = np.std(areas) / np.mean(areas) if np.mean(areas) > 0 else float('inf')

    return {
        'n_nuclei': n_nuclei,
        'mean_area': np.mean(areas),
        'median_area': np.median(areas),
        'std_area': np.std(areas),
        'cv_area': cv,
        'very_large_frac': np.mean(areas > np.median(areas) * 5),
        'very_small_frac': np.mean(areas < 20),
    }


def run_stardist_param_sweep(img_normalized, model, rois, param_grid=None):
    """
    Sweep StarDist parameters across multiple ROIs and rank by quality.

    Parameters
    ----------
    img_normalized : np.ndarray
        Full normalized H&E image.
    model : StarDist2D
        Loaded StarDist model.
    rois : list of tuple
        List of bounding boxes as (x_min, y_min, x_max, y_max).
    param_grid : list of dict, optional
        Parameter combinations to test. Defaults to a standard grid.

    Returns
    -------
    pd.DataFrame
        Results with one row per (roi, params) combination, plus a 'score' column.
    tuple
        Best (prob_thresh, nms_thresh) combination.
    """
    if param_grid is None:
        param_grid = [
            {'prob_thresh': pt, 'nms_thresh': nt}
            for pt in [0.005, 0.01, 0.03, 0.05, 0.1]
            for nt in [0.001, 0.01, 0.05, 0.1]
        ]

    results = []
    for roi_bbox in rois:
        crop = img_normalized[roi_bbox[1]:roi_bbox[3], roi_bbox[0]:roi_bbox[2]]
        for params in param_grid:
            metrics = evaluate_segmentation_on_roi(crop, model, **params)
            metrics.update(params)
            metrics['roi'] = str(roi_bbox)
            results.append(metrics)

    results_df = pd.DataFrame(results)

    # Composite quality score (lower = better)
    results_df['score'] = (
        results_df['very_small_frac'] * 3.0 +    # false detections
        results_df['very_large_frac'] * 5.0 +    # merger artifacts (worse)
        results_df['cv_area'] * 1.0              # area uniformity
    )

    # Average score across ROIs for each parameter combo
    mean_scores = results_df.groupby(['prob_thresh', 'nms_thresh'])['score'].mean()
    best_params = mean_scores.idxmin()

    return results_df, best_params


# ──────────────────────────────────────────────────────────────────────────────
# QC Threshold Estimation
# ──────────────────────────────────────────────────────────────────────────────

def suggest_area_cutoff(gdf):
    """
    Use distribution statistics to suggest an area upper bound.

    Uses the more conservative of:
    - Upper fence: Q75 + 3×IQR (generous outlier exclusion)
    - Size-based: 5× median area (catches merged nuclei)
    """
    areas = gdf['area']
    q75 = areas.quantile(0.75)
    iqr = q75 - areas.quantile(0.25)
    upper_fence = q75 + 3 * iqr
    size_based = areas.median() * 5
    return min(upper_fence, size_based)


def suggest_umi_cutoff(adata):
    """
    Use distribution knee-point to suggest minimum UMI threshold.

    Uses the 5th percentile as floor, with a hard minimum of 50.
    """
    counts = adata.obs['total_counts'].sort_values()
    floor = counts.quantile(0.05)
    return max(floor, 50)


def preview_filtering(gdf, adata, area_cutoffs, umi_cutoffs):
    """
    Show how many nuclei survive each threshold combination.

    Parameters
    ----------
    gdf : GeoDataFrame
        Nuclei polygons with 'area' and 'id' columns.
    adata : AnnData
        Nuclei-binned AnnData with 'total_counts' in .obs.
    area_cutoffs : list of float
        Area thresholds to test.
    umi_cutoffs : list of float
        UMI thresholds to test.

    Returns
    -------
    pd.DataFrame
        One row per combination with n_nuclei and pct_retained.
    """
    results = []
    for ac in area_cutoffs:
        for uc in umi_cutoffs:
            mask_a = adata.obs['id'].isin(gdf[gdf['area'] < ac].id)
            mask_u = adata.obs['total_counts'] > uc
            n_survive = (mask_a & mask_u).sum()
            results.append({
                'area_cutoff': ac, 'umi_cutoff': uc,
                'n_nuclei': n_survive,
                'pct_retained': n_survive / adata.n_obs * 100
            })
    return pd.DataFrame(results)


# ──────────────────────────────────────────────────────────────────────────────
# Clustering Optimization
# ──────────────────────────────────────────────────────────────────────────────

def evaluate_clustering(adata, resolution):
    """
    Run Leiden clustering at a given resolution and return summary metrics.

    Parameters
    ----------
    adata : AnnData
        Filtered, raw-count nuclei-binned AnnData.
    resolution : float
        Leiden resolution parameter.

    Returns
    -------
    dict
        Metrics including n_clusters, cluster sizes, and the clustered AnnData.
    """
    adata_copy = adata.copy()
    sc.pp.normalize_total(adata_copy, inplace=True)
    sc.pp.log1p(adata_copy)
    sc.pp.highly_variable_genes(adata_copy, flavor="seurat", n_top_genes=2000)
    sc.pp.pca(adata_copy)
    sc.pp.neighbors(adata_copy)
    sc.tl.leiden(adata_copy, resolution=resolution, key_added="clusters")

    n_clusters = adata_copy.obs['clusters'].nunique()
    cluster_sizes = adata_copy.obs['clusters'].value_counts()

    return {
        'resolution': resolution,
        'n_clusters': n_clusters,
        'min_cluster_size': cluster_sizes.min(),
        'min_cluster_pct': cluster_sizes.min() / adata_copy.n_obs * 100,
        'max_cluster_size': cluster_sizes.max(),
        'max_cluster_pct': cluster_sizes.max() / adata_copy.n_obs * 100,
        'adata': adata_copy
    }


def run_clustering_sweep(adata, resolutions=None):
    """
    Sweep Leiden resolutions and return summary table.

    Parameters
    ----------
    adata : AnnData
        Filtered nuclei-binned AnnData.
    resolutions : list of float, optional
        Resolutions to test. Defaults to [0.1, 0.2, 0.3, 0.5, 0.7, 1.0].

    Returns
    -------
    list of dict
        One entry per resolution with metrics and clustered AnnData.
    """
    if resolutions is None:
        resolutions = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0]

    results = []
    for res in resolutions:
        result = evaluate_clustering(adata, res)
        results.append(result)
        print(f"  Resolution {res:.2f}: {result['n_clusters']} clusters, "
              f"smallest = {result['min_cluster_pct']:.1f}%, "
              f"largest = {result['max_cluster_pct']:.1f}%")

    return results
