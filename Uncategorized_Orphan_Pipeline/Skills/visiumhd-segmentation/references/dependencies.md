# Dependency Reference

Documentation and API notes for the four core dependencies of the Visium HD segmentation skill.

## Table of Contents

1. [StarDist](#stardist)
2. [GeoPandas](#geopandas)
3. [Squidpy](#squidpy)
4. [fastparquet](#fastparquet)

---

## StarDist

**Repository**: https://github.com/stardist/stardist
**License**: BSD-3-Clause
**Stars**: ~1.2k

StarDist is a deep-learning library for star-convex object detection of cells and nuclei in 2D and 3D microscopy images.

### Key Concepts

- Uses star-convex polygon representation: predicts distances to object boundary along fixed rays, plus object probabilities
- Overcomplete set of candidate polygons → Non-Maximum Suppression (NMS) → final instance segmentation
- Works on 2D images and 3D volumes

### Pretrained Models (2D)

| Model Name | Training Data | Use Case |
|------------|---------------|----------|
| `2D_versatile_fluo` | Various fluorescence microscopy | General fluorescence nuclei |
| `2D_versatile_he` | MoNuSeg 2018 + TNBC (Naylor 2018) | **H&E stained tissue** ← use this for Visium HD |
| `2D_paper_dsb2018` | DSB 2018 challenge | Nuclei segmentation benchmark |

### Critical API

```python
from stardist.models import StarDist2D

# Load pretrained
model = StarDist2D.from_pretrained('2D_versatile_he')

# Predict on small images
labels, details = model.predict_instances(img_normalized)

# Predict on large/whole-slide images (RECOMMENDED for Visium HD)
labels, polys = model.predict_instances_big(
    img,
    axes='YXC',           # Image axis order: Y, X, Color-channels
    block_size=4096,      # Process in 4096×4096 blocks
    prob_thresh=0.01,     # Detection probability threshold
    nms_thresh=0.001,     # Non-maximum suppression threshold (low = less overlap)
    min_overlap=128,      # Overlap between blocks for stitching
    context=128,          # Context padding around each block
    normalizer=None,      # None if pre-normalized; or use PercentileNormalizer
    n_tiles=(4,4,1)       # Tiling within each block (increase for GPU memory)
)
```

### Output Format

- `labels`: Integer label image (same shape as input, each nucleus has unique ID)
- `polys`: Dictionary with keys:
  - `coord`: Array of shape `(n_nuclei, 2, n_rays)` — polygon vertex coordinates
  - `points`: Centroid coordinates
  - `prob`: Detection probabilities

### Normalization Utility

```python
from csbdeep.utils import normalize

# Percentile normalization
img_norm = normalize(img, pmin=5, pmax=95)  # Clips to [5th, 95th] percentile and scales to [0, 1]
```

### Installation Notes

- Requires TensorFlow (1.x or 2.x)
- For GPU: must match TensorFlow version with compatible CUDA/cuDNN versions
- `pip install stardist` (TF2) or `pip install "stardist[tf1]"` (TF1)
- Compatible with Python 3.6–3.13

### Custom Model Training

StarDist can be trained on custom datasets. Requirements:
- Pairs of raw images + fully annotated label images (every pixel labeled with unique object ID or 0)
- Annotation tools: Fiji/Labkit (2D or 3D), QuPath (2D)
- Multi-class prediction supported (cell type classification during segmentation)

---

## GeoPandas

**Repository**: https://github.com/geopandas/geopandas
**Documentation**: https://geopandas.org
**License**: BSD-3-Clause

GeoPandas extends pandas with geospatial data types. In this pipeline, it provides the backbone for spatial operations — storing nucleus polygons and barcode point coordinates, then performing spatial joins to assign barcodes to nuclei.

### Key Usage in This Pipeline

```python
import geopandas as gpd
from shapely.geometry import Polygon, Point

# Create GeoDataFrame of nucleus polygons
gdf = gpd.GeoDataFrame(geometry=[Polygon(coords) for coords in polygon_list])

# Create GeoDataFrame of barcode point locations
geometry = [Point(x, y) for x, y in zip(cols, rows)]
gdf_barcodes = gpd.GeoDataFrame(df, geometry=geometry)

# Spatial join: find which nucleus each barcode falls within
result = gpd.sjoin(gdf_barcodes, gdf_nuclei, how='left', predicate='within')
```

### Critical Methods

| Method | Purpose |
|--------|---------|
| `gpd.sjoin(left, right, how, predicate)` | Spatial join — point-in-polygon assignment |
| `gdf.plot(column, cmap, ax, legend)` | Choropleth-style spatial plot |
| `gdf['geometry'].intersects(polygon)` | Boolean mask: which geometries intersect a query polygon |
| `gdf['geometry'].area` | Compute area of each polygon |
| `gdf.merge(df, ...)` | Standard pandas merge with spatial awareness |
| `Polygon.buffer(distance)` | Expand polygon boundaries by a distance |

### Spatial Join Predicates

- `'within'`: Point is inside polygon (used in this pipeline)
- `'contains'`: Polygon contains point
- `'intersects'`: Geometries share any space
- `'crosses'`, `'overlaps'`, `'touches'`: Other spatial relationships

---

## Squidpy

**Repository**: https://github.com/scverse/squidpy
**Documentation**: https://squidpy.readthedocs.io
**License**: BSD-3-Clause
**Stars**: ~560

Squidpy is the scverse toolkit for spatial molecular data analysis. In this pipeline, it provides the scanpy and anndata imports used for:
- Reading 10x H5 files (`sc.read_10x_h5`)
- QC metrics (`sc.pp.calculate_qc_metrics`)
- Normalization and preprocessing (`sc.pp.normalize_total`, `sc.pp.log1p`)
- Feature selection (`sc.pp.highly_variable_genes`)
- Dimensionality reduction (`sc.pp.pca`, `sc.pp.neighbors`)
- Clustering (`sc.tl.leiden`)

### Key Capabilities Beyond This Pipeline

- Spatial neighbor graphs from Visium, Slide-seq, Xenium data
- Spatial statistics: neighborhood enrichment, co-occurrence, Moran's I
- Image featurization with scikit-image
- Interactive visualization via napari-spatialdata

### In This Pipeline

```python
import scanpy as sc

# Read Space Ranger output
adata = sc.read_10x_h5('filtered_feature_bc_matrix.h5')

# QC
sc.pp.calculate_qc_metrics(adata, inplace=True)

# Standard preprocessing
sc.pp.normalize_total(adata, inplace=True)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, flavor="seurat", n_top_genes=2000)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.leiden(adata, resolution=0.35, key_added="clusters")
```

---

## fastparquet

**Repository**: https://github.com/dask/fastparquet
**License**: Apache-2.0

fastparquet is a Python implementation of the Apache Parquet columnar file format, optimized for efficient reading and writing. In this pipeline, it is the backend engine for `pd.read_parquet()` when loading the `tissue_positions.parquet` file from Space Ranger output.

### Key Usage

```python
import pandas as pd

# Read tissue positions (fastparquet is used as the engine automatically if installed)
df = pd.read_parquet('tissue_positions.parquet')

# Or explicitly specify engine
df = pd.read_parquet('tissue_positions.parquet', engine='fastparquet')
```

### The tissue_positions.parquet File

This file from Space Ranger contains one row per 2×2 µm barcode square:

| Column | Type | Description |
|--------|------|-------------|
| `barcode` | str | Unique barcode identifier |
| `in_tissue` | int | 1 if barcode is under tissue, 0 otherwise |
| `array_row` | int | Row position in the barcode array |
| `array_col` | int | Column position in the barcode array |
| `pxl_row_in_fullres` | int | Y pixel coordinate in full-resolution image |
| `pxl_col_in_fullres` | int | X pixel coordinate in full-resolution image |

### Why fastparquet?

- Faster than pyarrow for single-file reads of moderate size
- Lower memory footprint
- Pure Python implementation (no C++ Arrow dependency)
- Suitable for the tissue_positions.parquet files which are typically 10-100 MB
