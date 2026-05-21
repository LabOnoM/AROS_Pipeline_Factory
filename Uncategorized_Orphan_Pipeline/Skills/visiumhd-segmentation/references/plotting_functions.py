"""
Visium HD Segmentation — Visualization Helper Functions

These functions visualize nuclei segmentation masks, gene expression patterns,
cluster assignments, and QC metrics in the context of the H&E tissue image.

All functions accept a bounding box (bbox) argument as (x_min, y_min, x_max, y_max)
to zoom into a specific region of interest.

Usage:
    Copy the functions you need into your notebook or script, or import:
        from plotting_functions import plot_mask_and_save_image, ...
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from shapely.geometry import Polygon


# ──────────────────────────────────────────────────────────────────────────────
# Nuclei Mask Visualization
# ──────────────────────────────────────────────────────────────────────────────

def plot_mask_and_save_image(title, gdf, img, cmap, output_name=None, bbox=None):
    """
    Plot H&E image alongside the segmented nuclei mask.

    Parameters
    ----------
    title : str
        Plot title.
    gdf : GeoDataFrame
        Nuclei polygons with 'geometry' column.
    img : np.ndarray
        H&E image array (normalized).
    cmap : matplotlib colormap
        Colormap for nuclei polygons.
    output_name : str, optional
        Save path for the figure.
    bbox : tuple, optional
        Bounding box as (x_min, y_min, x_max, y_max).
    """
    if bbox is not None:
        cropped_img = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    else:
        cropped_img = img

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(cropped_img, cmap='gray', origin='lower')
    axes[0].set_title(title)
    axes[0].axis('off')

    if bbox is not None:
        bbox_polygon = Polygon([
            (bbox[0], bbox[1]), (bbox[2], bbox[1]),
            (bbox[2], bbox[3]), (bbox[0], bbox[3])
        ])
        intersects_bbox = gdf['geometry'].intersects(bbox_polygon)
        filtered_gdf = gdf[intersects_bbox]
    else:
        filtered_gdf = gdf

    filtered_gdf.plot(cmap=cmap, ax=axes[1])
    axes[1].axis('off')
    axes[1].legend(loc='upper left', bbox_to_anchor=(1.05, 1))

    if output_name is not None:
        plt.savefig(output_name, bbox_inches='tight')
    else:
        plt.show()


# ──────────────────────────────────────────────────────────────────────────────
# Gene Expression Visualization
# ──────────────────────────────────────────────────────────────────────────────

def plot_gene_and_save_image(title, gdf, gene, img, adata, bbox=None, output_name=None):
    """
    Plot H&E image alongside spatial gene expression on nuclei polygons.

    Parameters
    ----------
    title : str
        Plot title.
    gdf : GeoDataFrame
        Nuclei polygons with 'geometry' and 'id' columns.
    gene : str
        Gene symbol to visualize.
    img : np.ndarray
        H&E image array.
    adata : AnnData
        Nuclei-binned AnnData object.
    bbox : tuple, optional
        Bounding box as (x_min, y_min, x_max, y_max).
    output_name : str, optional
        Save path for the figure.
    """
    if bbox is not None:
        cropped_img = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    else:
        cropped_img = img

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(cropped_img, cmap='gray', origin='lower')
    axes[0].set_title(title)
    axes[0].axis('off')

    if bbox is not None:
        bbox_polygon = Polygon([
            (bbox[0], bbox[1]), (bbox[2], bbox[1]),
            (bbox[2], bbox[3]), (bbox[0], bbox[3])
        ])

    gene_expression = adata[:, gene].to_df()
    gene_expression['id'] = gene_expression.index
    merged_gdf = gdf.merge(gene_expression, left_on='id', right_on='id')

    if bbox is not None:
        intersects_bbox = merged_gdf['geometry'].intersects(bbox_polygon)
        filtered_gdf = merged_gdf[intersects_bbox]
    else:
        filtered_gdf = merged_gdf

    filtered_gdf.plot(column=gene, cmap='inferno', legend=True, ax=axes[1])
    axes[1].set_title(gene)
    axes[1].axis('off')
    axes[1].legend(loc='upper left', bbox_to_anchor=(1.05, 1))

    if output_name is not None:
        plt.savefig(output_name, bbox_inches='tight')
    else:
        plt.show()


# ──────────────────────────────────────────────────────────────────────────────
# Cluster Visualization
# ──────────────────────────────────────────────────────────────────────────────

def plot_clusters_and_save_image(title, gdf, img, adata, bbox=None,
                                 color_by_obs=None, output_name=None, color_list=None):
    """
    Plot H&E image alongside spatial cluster assignments on nuclei polygons.

    Parameters
    ----------
    title : str
        Plot title.
    gdf : GeoDataFrame
        Nuclei polygons with 'geometry' and 'id' columns.
    img : np.ndarray
        H&E image array.
    adata : AnnData
        Nuclei-binned AnnData with cluster annotations in .obs.
    bbox : tuple, optional
        Bounding box as (x_min, y_min, x_max, y_max).
    color_by_obs : str
        Column name in adata.obs for cluster coloring.
    output_name : str, optional
        Save path.
    color_list : list, optional
        Custom color list. Defaults to 30 distinct colors.
    """
    if color_list is None:
        color_list = [
            "#7f0000", "#808000", "#483d8b", "#008000", "#bc8f8f",
            "#008b8b", "#4682b4", "#000080", "#d2691e", "#9acd32",
            "#8fbc8f", "#800080", "#b03060", "#ff4500", "#ffa500",
            "#ffff00", "#00ff00", "#8a2be2", "#00ff7f", "#dc143c",
            "#00ffff", "#0000ff", "#ff00ff", "#1e90ff", "#f0e68c",
            "#90ee90", "#add8e6", "#ff1493", "#7b68ee", "#ee82ee"
        ]

    if bbox is not None:
        cropped_img = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    else:
        cropped_img = img

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(cropped_img, cmap='gray', origin='lower')
    axes[0].set_title(title)
    axes[0].axis('off')

    if bbox is not None:
        bbox_polygon = Polygon([
            (bbox[0], bbox[1]), (bbox[2], bbox[1]),
            (bbox[2], bbox[3]), (bbox[0], bbox[3])
        ])

    unique_values = adata.obs[color_by_obs].astype('category').cat.categories
    num_categories = len(unique_values)

    if len(color_list) >= num_categories:
        custom_cmap = ListedColormap(color_list[:num_categories], name='custom_cmap')
    else:
        tab20_colors = plt.cm.tab20.colors[:num_categories]
        custom_cmap = ListedColormap(tab20_colors, name='custom_tab20_cmap')

    merged_gdf = gdf.merge(
        adata.obs[color_by_obs].astype('category'),
        left_on='id', right_index=True
    )

    if bbox is not None:
        intersects_bbox = merged_gdf['geometry'].intersects(bbox_polygon)
        filtered_gdf = merged_gdf[intersects_bbox]
    else:
        filtered_gdf = merged_gdf

    plot = filtered_gdf.plot(column=color_by_obs, cmap=custom_cmap, ax=axes[1], legend=True)
    axes[1].set_title(color_by_obs)
    legend = axes[1].get_legend()
    legend.set_bbox_to_anchor((1.05, 1))
    axes[1].axis('off')
    plot.get_legend().set_bbox_to_anchor((1.25, 1))

    if output_name is not None:
        plt.savefig(output_name, bbox_inches='tight')
    else:
        plt.show()


# ──────────────────────────────────────────────────────────────────────────────
# QC Metric Plots
# ──────────────────────────────────────────────────────────────────────────────

def plot_nuclei_area(gdf, area_cut_off):
    """
    Plot nuclei area distribution before and after filtering.

    Parameters
    ----------
    gdf : GeoDataFrame
        Nuclei polygons with 'area' column.
    area_cut_off : float
        Maximum area threshold for filtering.
    """
    fig, axs = plt.subplots(1, 2, figsize=(15, 4))

    axs[0].hist(gdf['area'], bins=50, edgecolor='black')
    axs[0].set_title('Nuclei Area')

    axs[1].hist(gdf[gdf['area'] < area_cut_off]['area'], bins=50, edgecolor='black')
    axs[1].set_title(f'Nuclei Area Filtered: {area_cut_off}')

    plt.tight_layout()
    plt.show()


def total_umi(adata_, cut_off):
    """
    Plot total UMI count distribution before and after filtering.

    Parameters
    ----------
    adata_ : AnnData
        AnnData object with 'total_counts' in .obs (run sc.pp.calculate_qc_metrics first).
    cut_off : float
        Minimum UMI count threshold.
    """
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    axs[0].boxplot(
        adata_.obs["total_counts"], vert=False, widths=0.7,
        patch_artist=True, boxprops=dict(facecolor='skyblue')
    )
    axs[0].set_title('Total Counts')

    axs[1].boxplot(
        adata_.obs["total_counts"][adata_.obs["total_counts"] > cut_off],
        vert=False, widths=0.7,
        patch_artist=True, boxprops=dict(facecolor='skyblue')
    )
    axs[1].set_title(f'Total Counts > {cut_off}')

    for ax in axs:
        ax.get_yaxis().set_visible(False)

    plt.tight_layout()
    plt.show()
