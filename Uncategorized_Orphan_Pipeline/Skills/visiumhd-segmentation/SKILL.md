---
name: visiumhd-segmentation
description: >
  Guide for performing nuclei segmentation and custom barcode binning on 10x Genomics
  Visium HD spatial transcriptomics data. This is the **downstream companion** to the
  `spaceranger` skill — it consumes Space Ranger `count` outputs (specifically the
  `binned_outputs/square_002um/` resolution) and a high-resolution H&E microscope image
  to produce single-cell-resolution data. The pipeline segments nuclei from the H&E image
  using StarDist (or alternatively uses Space Ranger v4.0+ built-in segmentation masks),
  then assigns 2×2 µm barcodes to individual nuclei via GeoPandas spatial joins. Includes
  a 5-gate QC framework with Space Ranger health pre-check, LLM-assisted ROI selection,
  iterative parameter optimization, and mandatory user confirmation checkpoints at every
  critical decision. Produces an AnnData object suitable for downstream clustering,
  differential expression, spatial statistics (Squidpy), and trajectory analysis
  (Monocle3). Use this skill whenever the user mentions Visium HD segmentation, Visium HD
  nuclei binning, StarDist segmentation for spatial transcriptomics, custom binning of
  Visium HD data, converting Visium HD to single-cell resolution, spatial
  barcode-to-nucleus assignment, cell-level Visium HD analysis, H&E-guided Visium HD
  binning, or wants to go beyond default 8×8/16×16 µm bins to per-nucleus gene expression
  matrices.
---

# Visium HD Nuclei Segmentation & Custom Binning

This skill implements the [10x Genomics Analysis Guide](https://www.10xgenomics.com/analysis-guides/segmentation-visium-hd) workflow for segmenting nuclei from a high-resolution H&E image and creating custom nuclei-specific bins of Visium HD gene expression data. The result is a pseudo-single-cell AnnData object where each observation corresponds to one segmented nucleus rather than an arbitrary square bin.

## Pipeline Position

```
┌──────────────────────┐        ┌───────────────────────────┐
│   spaceranger skill  │        │ visiumhd-segmentation     │
│   (upstream)         │───────▶│ (THIS skill)              │
│                      │        │                           │
│ FASTQ + images       │        │ 2µm bins + H&E image      │
│   → count pipeline   │        │   → nuclei AnnData        │
│   → binned_outputs/  │        │   → clusters, markers     │
│   → segmented_outputs│        │   → spatial statistics    │
│   → metrics QC       │        │   → trajectory (Monocle3) │
└──────────────────────┘        └───────────────────────────┘
```

> **Prerequisite**: The `spaceranger count` pipeline must have completed successfully.
> Use the `spaceranger` skill to run it, or verify that outputs already exist.

## Agentic Execution Model

This pipeline is NOT a fire-and-forget script. It contains **six mandatory checkpoints** — one pre-flight validation plus five QC gates — where the agent must stop, present evidence to the user, and wait for explicit confirmation before proceeding. Between gates, the agent performs iterative self-optimization loops to find optimal parameters automatically.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       PIPELINE EXECUTION FLOW                               │
│                                                                              │
│  ┌──────────────────────────────────────────────┐                            │
│  │ 🏥 PRE-FLIGHT: Space Ranger Health Check     │                            │
│  │    Validate outputs exist, parse metrics,    │                            │
│  │    check alignment images, load scale factors│                            │
│  │    → Confirm SR Grade ≥ B before proceeding  │◄── AUTO (warn if < B)      │
│  └──┬───────────────────────────────────────────┘                            │
│     │                                                                        │
│  Step 1: Load H&E Image + Decide Segmentation Strategy                      │
│     │  Option A: StarDist custom segmentation (default)                      │
│     │  Option B: Use SR v4.0+ built-in segmentation masks                    │
│     │                                                                        │
│  ┌──▼───────────────────────────────────────────┐                            │
│  │ 🔁 OPTIMIZATION LOOP: Normalization          │                            │
│  │    Try percentile ranges, score contrast     │                            │
│  └──┬───────────────────────────────────────────┘                            │
│     │                                                                        │
│  ┌──▼───────────────────────────────────────────┐                            │
│  │ 🚦 QC GATE 1: ROI Selection                  │                            │
│  │    LLM proposes ROIs → USER CONFIRMS         │◄── STOP & WAIT             │
│  └──┬───────────────────────────────────────────┘                            │
│     │                                                                        │
│  ┌──▼───────────────────────────────────────────┐                            │
│  │ 🔁 OPTIMIZATION LOOP: StarDist Params        │                            │
│  │    Iterate prob_thresh/nms_thresh on ROI     │                            │
│  └──┬───────────────────────────────────────────┘                            │
│     │                                                                        │
│  ┌──▼───────────────────────────────────────────┐                            │
│  │ 🚦 QC GATE 2: Segmentation Validation        │                            │
│  │    Show mask overlays → USER CONFIRMS        │◄── STOP & WAIT             │
│  └──┬───────────────────────────────────────────┘                            │
│     │                                                                        │
│  Step 5-8: Full segmentation + Spatial join + Binning                        │
│     │                                                                        │
│  ┌──▼───────────────────────────────────────────┐                            │
│  │ 🔁 OPTIMIZATION LOOP: QC Thresholds          │                            │
│  │    Sweep area/UMI cutoffs, score quality     │                            │
│  └──┬───────────────────────────────────────────┘                            │
│     │                                                                        │
│  ┌──▼───────────────────────────────────────────┐                            │
│  │ 🚦 QC GATE 3: Filtering Thresholds           │                            │
│  │    Show distributions → USER CONFIRMS        │◄── STOP & WAIT             │
│  └──┬───────────────────────────────────────────┘                            │
│     │                                                                        │
│  ┌──▼───────────────────────────────────────────┐                            │
│  │ 🔁 OPTIMIZATION LOOP: Clustering             │                            │
│  │    Sweep Leiden resolution, evaluate         │                            │
│  └──┬───────────────────────────────────────────┘                            │
│     │                                                                        │
│  ┌──▼───────────────────────────────────────────┐                            │
│  │ 🚦 QC GATE 4: Clustering Validation          │                            │
│  │    Show spatial clusters → USER CONFIRMS     │◄── STOP & WAIT             │
│  └──┬───────────────────────────────────────────┘                            │
│     │                                                                        │
│  ┌──▼───────────────────────────────────────────┐                            │
│  │ 🚦 QC GATE 5: Marker Gene Validation         │                            │
│  │    Show marker expr vs morphology            │◄── STOP & WAIT             │
│  │    → USER CONFIRMS final AnnData             │                            │
│  └──┬───────────────────────────────────────────┘                            │
│     │                                                                        │
│  ✅ DONE: Export final AnnData                                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### Required Input Files — Space Ranger Output Map

All inputs come from a completed `spaceranger count` run. The expected directory
structure is:

```
<run_id>/outs/
├── web_summary.html                                # Pipeline QC report
├── metrics_summary.csv                             # Machine-readable QC metrics
├── binned_outputs/
│   ├── square_002um/                               # ⭐ PRIMARY INPUT for this skill
│   │   ├── filtered_feature_bc_matrix.h5           # 2µm barcode × gene HDF5 matrix
│   │   ├── raw_feature_bc_matrix.h5
│   │   └── spatial/
│   │       └── tissue_positions.parquet            # Barcode pixel coordinates
│   ├── square_008um/                               # Standard analysis resolution
│   │   └── (same structure)
│   └── square_016um/                               # Quick exploratory resolution
│       └── (same structure)
├── segmented_outputs/                              # v4.0+ only (if segmentation ran)
│   ├── filtered_feature_bc_matrix.h5               # Nuclei-level matrix (SR built-in)
│   ├── nucleus_instance_mask.tiff                  # Instance mask image
│   └── nucleus_segmentations.geojson               # Polygon boundaries
├── spatial/
│   ├── scalefactors_json.json                      # ⭐ Pixel-to-micron conversion
│   ├── tissue_hires_image.png
│   ├── tissue_lowres_image.png
│   ├── aligned_fiducials.jpg                       # Fiducial alignment QC
│   └── detected_tissue_image.jpg                   # Tissue detection QC
└── analysis/
    ├── clustering/
    ├── diffexp/
    ├── pca/
    ├── tsne/
    └── umap/
```

### Input File Summary

| File | Source Path | Purpose |
|------|------------|---------|
| **2µm barcode matrix** | `<run_id>/outs/binned_outputs/square_002um/filtered_feature_bc_matrix.h5` | Highest-resolution barcode data for nuclei binning |
| **Tissue positions** | `<run_id>/outs/binned_outputs/square_002um/spatial/tissue_positions.parquet` | Pixel coordinates for each 2µm barcode |
| **Scale factors** | `<run_id>/outs/spatial/scalefactors_json.json` | Convert between pixel and physical (µm) coordinates |
| **Metrics summary** | `<run_id>/outs/metrics_summary.csv` | Pipeline QC metrics for pre-flight validation |
| **H&E microscope image** | User-provided (`.btf`, `.tif`, `.tiff`, `.qptiff`) | Original high-res image for StarDist segmentation |
| **SR segmentation** (optional) | `<run_id>/outs/segmented_outputs/nucleus_segmentations.geojson` | Alternative to StarDist — use Space Ranger's built-in masks |

> **⚠️ CRITICAL: CytAssist Image vs Microscope Image**
>
> The **CytAssist image** (`--cytaimage`) is a low-resolution capture that contains
> primarily eosin (cytoplasmic) staining. It is used by Space Ranger for fiducial
> alignment only. **DO NOT** use the CytAssist image for nuclei segmentation — it
> lacks the hematoxylin (nuclear) stain contrast required by StarDist.
>
> Use the original **microscope image** (`--image` in `spaceranger count`) which
> contains both hematoxylin and eosin staining at full scanning resolution.

### Required Python Packages

```
stardist        # StarDist2D nuclei segmentation (star-convex object detection)
geopandas       # Spatial joins between barcode points and nucleus polygons
squidpy         # Spatial transcriptomics analysis (wraps scanpy + anndata)
fastparquet     # Efficient reading of tissue_positions.parquet
scanpy          # Single-cell analysis (installed with squidpy)
anndata         # Annotated data matrices (installed with squidpy)
tifffile        # Reading high-resolution TIFF/BTF images
csbdeep         # Percentile normalization utility (installed with stardist)
shapely         # Geometric operations — Polygon, Point (installed with geopandas)
scipy           # Sparse matrices for count summation
matplotlib      # Visualization
```

### Installation

```bash
# Option A: conda (recommended)
conda create -n visiumhd-seg python=3.11
conda activate visiumhd-seg
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install -c conda-forge stardist geopandas squidpy fastparquet

# Option B: pip
pip install stardist geopandas squidpy fastparquet
```

For GPU-accelerated StarDist, ensure TensorFlow is installed with CUDA support first.

---

## Pre-Flight: Space Ranger Health Check

Before starting segmentation, validate that the upstream Space Ranger pipeline completed
successfully and outputs are intact. This step runs **automatically** and issues warnings
but does not require user confirmation unless the health grade is C or F.

```python
import os
import json
import csv

def preflight_check(spaceranger_dir):
    """
    Validate Space Ranger outputs and return a health report.
    
    Parameters
    ----------
    spaceranger_dir : str
        Path to the spaceranger run directory (e.g., '<run_id>')
    
    Returns
    -------
    dict
        Health report with grade (A/B/C/F), metrics, and file inventory.
    """
    outs = os.path.join(spaceranger_dir, "outs")
    report = {"grade": "A", "warnings": [], "errors": [], "paths": {}}
    
    # ── Check required files exist ────────────────────────────────
    required_files = {
        "matrix_2um": os.path.join(outs, "binned_outputs", "square_002um",
                                    "filtered_feature_bc_matrix.h5"),
        "positions_2um": os.path.join(outs, "binned_outputs", "square_002um",
                                       "spatial", "tissue_positions.parquet"),
        "scale_factors": os.path.join(outs, "spatial", "scalefactors_json.json"),
        "metrics_summary": os.path.join(outs, "metrics_summary.csv"),
        "web_summary": os.path.join(outs, "web_summary.html"),
    }
    
    optional_files = {
        "matrix_8um": os.path.join(outs, "binned_outputs", "square_008um",
                                    "filtered_feature_bc_matrix.h5"),
        "aligned_fiducials": os.path.join(outs, "spatial", "aligned_fiducials.jpg"),
        "detected_tissue": os.path.join(outs, "spatial", "detected_tissue_image.jpg"),
        "sr_segmentation": os.path.join(outs, "segmented_outputs",
                                         "nucleus_segmentations.geojson"),
        "sr_instance_mask": os.path.join(outs, "segmented_outputs",
                                          "nucleus_instance_mask.tiff"),
        "sr_seg_matrix": os.path.join(outs, "segmented_outputs",
                                       "filtered_feature_bc_matrix.h5"),
    }
    
    for name, path in required_files.items():
        exists = os.path.exists(path)
        report["paths"][name] = path if exists else None
        if not exists:
            report["errors"].append(f"Missing required: {name} ({path})")
            report["grade"] = "F"
    
    for name, path in optional_files.items():
        report["paths"][name] = path if os.path.exists(path) else None
    
    # ── Parse QC metrics ──────────────────────────────────────────
    metrics_path = required_files["metrics_summary"]
    if os.path.exists(metrics_path):
        with open(metrics_path) as f:
            reader = csv.DictReader(f)
            metrics = next(reader, {})
        
        report["raw_metrics"] = metrics
        
        # Key thresholds
        thresholds = {
            "Fraction Reads in Spots Under Tissue": {"min": 50.0, "warn": 30.0},
            "Valid Barcodes": {"min": 75.0, "warn": 50.0},
        }
        for metric, limits in thresholds.items():
            val_str = metrics.get(metric, "")
            if val_str:
                val = float(val_str.replace("%", "").replace(",", ""))
                if val < limits["warn"]:
                    report["warnings"].append(f"🔴 {metric} = {val}% (critical)")
                    report["grade"] = "C"
                elif val < limits["min"]:
                    report["warnings"].append(f"🟡 {metric} = {val}% (below recommended)")
                    if report["grade"] == "A":
                        report["grade"] = "B"
    
    # ── Load scale factors ────────────────────────────────────────
    sf_path = required_files["scale_factors"]
    if os.path.exists(sf_path):
        with open(sf_path) as f:
            report["scale_factors"] = json.load(f)
    
    # ── Detect if SR segmentation is available ────────────────────
    report["sr_segmentation_available"] = (
        report["paths"].get("sr_segmentation") is not None
    )
    
    return report

# Run pre-flight
sr_report = preflight_check("/path/to/spaceranger_run")

# Auto-gate: warn and stop if grade is C or F
if sr_report["grade"] in ("C", "F"):
    print("⚠️  Space Ranger health grade:", sr_report["grade"])
    print("Errors:", sr_report["errors"])
    print("Warnings:", sr_report["warnings"])
    print("\n→ Please review web_summary.html and address issues before proceeding.")
    # STOP: Ask user whether to proceed despite poor upstream quality
else:
    print(f"✅ Space Ranger health grade: {sr_report['grade']}")
    if sr_report["sr_segmentation_available"]:
        print("ℹ️  Space Ranger built-in segmentation detected.")
        print("   You can compare SR segmentation vs StarDist at Gate 2.")
```

### Segmentation Strategy Decision

If Space Ranger v4.0+ segmentation outputs exist, present both options:

| Strategy | Pros | Cons | When to Use |
|----------|------|------|-------------|
| **StarDist custom** (default) | Full parameter control, tissue-specific tuning, higher accuracy on H&E | Requires GPU, longer compute time | Default for all projects |
| **SR built-in masks** | No extra compute, already available, consistent with 10x pipeline | No parameter tuning, may miss tissue-specific features | Quick analysis, when SR grade is A |
| **Hybrid comparison** | Best of both worlds | Double the compute | When unsure, or for validation studies |

---

## Step-by-Step Implementation

### Step 1: Import Libraries and Set Paths

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import anndata
import geopandas as gpd
import scanpy as sc
import json
from tifffile import imread
from csbdeep.utils import normalize
from stardist.models import StarDist2D
from shapely.geometry import Polygon, Point
from scipy import sparse
from matplotlib.colors import ListedColormap

# ── Paths from Space Ranger output ──
spaceranger_dir = '/path/to/spaceranger_run'
outs_dir = f'{spaceranger_dir}/outs'

# Primary inputs (from pre-flight report)
matrix_h5 = f'{outs_dir}/binned_outputs/square_002um/filtered_feature_bc_matrix.h5'
positions_parquet = f'{outs_dir}/binned_outputs/square_002um/spatial/tissue_positions.parquet'
scalefactors_json = f'{outs_dir}/spatial/scalefactors_json.json'

# H&E image — the MICROSCOPE image, NOT the CytAssist capture
he_image_path = '/path/to/microscope_image.btf'
```

### Step 2: Load Scale Factors and H&E Image

```python
# Load scale factors for pixel-to-micron conversion
with open(scalefactors_json) as f:
    scale_factors = json.load(f)

# Key values:
#   tissue_hires_scalef:  fullres → hires scale factor
#   tissue_lowres_scalef: fullres → lowres scale factor
#   spot_diameter_fullres: diameter of one spot in full-res pixels
print(f"Scale factors: {json.dumps(scale_factors, indent=2)}")

# Compute pixel-to-micron ratio (Visium HD: 2µm bins)
# Each 2µm bin is 1 pixel at the 2µm grid → for full-res image, need scale conversion
# This depends on the microscope resolution; typical values: 0.25-0.5 µm/pixel

# Load and normalize image
img = imread(he_image_path)

# Load pretrained StarDist H&E model
model = StarDist2D.from_pretrained('2D_versatile_he')

# Percentile normalization — adjust min/max percentiles for your image
min_percentile = 5
max_percentile = 95
img_normalized = normalize(img, min_percentile, max_percentile)
```

---

## 🚦 QC GATE 1: ROI Selection & Normalization Confirmation

**This is a mandatory stop-and-confirm gate.** The agent must present the H&E image to the user and propose regions of interest (ROIs) before proceeding.

### Why This Gate Exists

The 10x guide states: *"multiple regions should be inspected to determine if the normalization parameters and the model prediction parameters need further refinement."* Choosing informative ROIs is critical — they must cover diverse tissue morphologies (dense nuclei, sparse regions, tissue edges, different cell types) to properly evaluate segmentation quality.

### Agent Behavior at This Gate

1. **Validate tissue alignment using Space Ranger outputs** — load the `aligned_fiducials.jpg` and `detected_tissue_image.jpg` from `outs/spatial/` to verify tissue-image registration:

```python
# Show SR alignment QC images to verify fiducial detection
aligned_path = f'{outs_dir}/spatial/aligned_fiducials.jpg'
tissue_path = f'{outs_dir}/spatial/detected_tissue_image.jpg'

fig, axes = plt.subplots(1, 2, figsize=(16, 8))
if os.path.exists(aligned_path):
    axes[0].imshow(plt.imread(aligned_path))
    axes[0].set_title('Fiducial Alignment (from Space Ranger)')
if os.path.exists(tissue_path):
    axes[1].imshow(plt.imread(tissue_path))
    axes[1].set_title('Tissue Detection (from Space Ranger)')
for ax in axes:
    ax.axis('off')
plt.savefig(f'{outs_dir}/qc_sr_alignment_check.png', dpi=150, bbox_inches='tight')
```

2. **Generate a downsampled overview** of the full H&E image and save it as a PNG:

```python
from PIL import Image
overview = Image.fromarray((img_normalized * 255).astype(np.uint8))
downsample_factor = max(1, max(overview.size) // 2048)  # Fit within 2048px
overview_small = overview.resize(
    (overview.size[0] // downsample_factor, overview.size[1] // downsample_factor)
)
overview_path = f'{outs_dir}/qc_overview_fullimage.png'
overview_small.save(overview_path)
```

3. **Use the multimodal LLM (view_file on the image)** to analyze the tissue morphology and propose 3–5 representative ROIs as bounding boxes `(x_min, y_min, x_max, y_max)`. The LLM should:
   - Identify regions with **high nuclei density** (test segmentation sensitivity)
   - Identify regions with **sparse/scattered nuclei** (test false positive rate)
   - Identify regions at **tissue boundaries/edges** (test edge artifacts)
   - Identify regions with **distinct morphological features** (crypts, villi, vessels, bone, marrow, etc.)
   - Each ROI should be approximately 800–1200 px wide/tall for adequate zoom

4. **Present to user with rationale** — show the overview image with proposed ROI boxes drawn, explain why each region was selected, and ask:
   > "I've selected these ROIs for segmentation QC. They cover [rationale]. Should I proceed with these, or would you like to adjust the regions?"

5. **Also show normalization comparison** — render 2–3 ROIs at different percentile settings (e.g., 1/99, 3/97, 5/95) side by side. Let the user see how normalization affects nuclear visibility:

```python
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for ax, (pmin, pmax) in zip(axes, [(1, 99), (3, 97), (5, 95)]):
    img_test = normalize(img, pmin, pmax)
    cropped = img_test[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    ax.imshow(cropped)
    ax.set_title(f'Percentile {pmin}/{pmax}')
    ax.axis('off')
plt.savefig(f'{outs_dir}/qc_normalization_comparison.png', dpi=150, bbox_inches='tight')
```

6. **STOP AND WAIT** for user confirmation before proceeding.

### User Confirmation Required

The user must either:
- ✅ Approve the selected ROIs and normalization settings
- 🔄 Request different ROIs or normalization percentiles
- ➕ Add additional ROIs to inspect

**Do NOT proceed to StarDist segmentation until the user explicitly confirms.**

---

### Step 3: Segment Nuclei with StarDist

```python
labels, polys = model.predict_instances_big(
    img_normalized,
    axes='YXC',
    block_size=4096,
    prob_thresh=0.01,
    nms_thresh=0.001,
    min_overlap=128,
    context=128,
    normalizer=None,
    n_tiles=(4, 4, 1)
)
```

### Step 4: Convert StarDist Output to GeoDataFrame

```python
geometries = []
for nuclei in range(len(polys['coord'])):
    coords = [(y, x) for x, y in zip(polys['coord'][nuclei][0], polys['coord'][nuclei][1])]
    geometries.append(Polygon(coords))

gdf = gpd.GeoDataFrame(geometry=geometries)
gdf['id'] = [f"ID_{i+1}" for i, _ in enumerate(gdf.index)]
gdf['area'] = gdf['geometry'].area
```

### Step 4b (Optional): Load Space Ranger Built-in Segmentation for Comparison

If Space Ranger v4.0+ segmentation outputs are available, load them for side-by-side
comparison with StarDist:

```python
# Check if SR segmentation exists
sr_geojson_path = f'{outs_dir}/segmented_outputs/nucleus_segmentations.geojson'
sr_mask_path = f'{outs_dir}/segmented_outputs/nucleus_instance_mask.tiff'

if os.path.exists(sr_geojson_path):
    # Load SR segmentation as GeoDataFrame
    gdf_sr = gpd.read_file(sr_geojson_path)
    gdf_sr['area'] = gdf_sr['geometry'].area
    gdf_sr['id'] = [f"SR_{i+1}" for i in range(len(gdf_sr))]
    
    print(f"Space Ranger segmentation: {len(gdf_sr)} nuclei detected")
    print(f"StarDist segmentation:     {len(gdf)} nuclei detected")
    
    # Compare: median area and count differences
    print(f"\nSR median area:       {gdf_sr['area'].median():.1f} px²")
    print(f"StarDist median area: {gdf['area'].median():.1f} px²")

if os.path.exists(sr_mask_path):
    sr_mask = imread(sr_mask_path)
    print(f"SR instance mask shape: {sr_mask.shape}, max label: {sr_mask.max()}")
```

---

## 🔁 OPTIMIZATION LOOP: StarDist Parameter Tuning

Before asking the user to validate segmentation, the agent should run an automated parameter sweep on the **user-confirmed ROIs** to find the best `prob_thresh` and `nms_thresh` combination.

### Self-Regression Loop Protocol

The goal is to find parameters that produce segmentation masks where nuclear boundaries look biologically reasonable. Since this runs on small ROI crops, it's fast.

```python
def evaluate_segmentation_on_roi(img_crop, model, prob_thresh, nms_thresh):
    """Run StarDist on a single ROI crop and return quality metrics."""
    labels_roi, polys_roi = model.predict_instances(
        img_crop,
        prob_thresh=prob_thresh,
        nms_thresh=nms_thresh,
        n_tiles=(2, 2, 1),
        normalizer=None
    )

    n_nuclei = labels_roi.max()
    if n_nuclei == 0:
        return {'n_nuclei': 0, 'mean_area': 0, 'std_area': 0, 'overlap_frac': 0}

    # Compute areas of detected nuclei
    areas = []
    for i in range(1, n_nuclei + 1):
        areas.append(np.sum(labels_roi == i))
    areas = np.array(areas)

    # Coefficient of variation as a regularity metric (lower = more uniform)
    cv = np.std(areas) / np.mean(areas) if np.mean(areas) > 0 else float('inf')

    return {
        'n_nuclei': n_nuclei,
        'mean_area': np.mean(areas),
        'median_area': np.median(areas),
        'std_area': np.std(areas),
        'cv_area': cv,
        'very_large_frac': np.mean(areas > np.median(areas) * 5),  # merger artifacts
        'very_small_frac': np.mean(areas < 20),  # noise fragments
    }

# Parameter sweep
param_grid = [
    {'prob_thresh': pt, 'nms_thresh': nt}
    for pt in [0.005, 0.01, 0.03, 0.05, 0.1]
    for nt in [0.001, 0.01, 0.05, 0.1]
]

results = []
for roi_bbox in user_confirmed_rois:
    crop = img_normalized[roi_bbox[1]:roi_bbox[3], roi_bbox[0]:roi_bbox[2]]
    for params in param_grid:
        metrics = evaluate_segmentation_on_roi(crop, model, **params)
        metrics.update(params)
        metrics['roi'] = str(roi_bbox)
        results.append(metrics)

results_df = pd.DataFrame(results)
```

### Scoring Heuristic

The agent ranks parameter combinations using this composite score (lower = better):

```python
# Penalize: too many tiny fragments, too many merged blobs, high area variability
results_df['score'] = (
    results_df['very_small_frac'] * 3.0 +    # false detections
    results_df['very_large_frac'] * 5.0 +    # merger artifacts (worse)
    results_df['cv_area'] * 1.0              # area uniformity
)
# Average score across all ROIs for each parameter combo
mean_scores = results_df.groupby(['prob_thresh', 'nms_thresh'])['score'].mean()
best_params = mean_scores.idxmin()
```

The agent should cycle through 2–3 rounds:
1. **Coarse sweep**: Wide parameter ranges (as above)
2. **Fine sweep**: Narrow range around the best parameters from round 1
3. **Final check**: Verify on all ROIs with the selected parameters

---

## 🚦 QC GATE 2: Segmentation Validation

**This is a mandatory stop-and-confirm gate.** The agent must present segmentation results to the user.

### What the Agent Must Present

For **each user-confirmed ROI**, generate a side-by-side visualization:

```python
for i, roi_bbox in enumerate(user_confirmed_rois):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Panel 1: Raw H&E crop
    crop = img_normalized[roi_bbox[1]:roi_bbox[3], roi_bbox[0]:roi_bbox[2]]
    axes[0].imshow(crop)
    axes[0].set_title('H&E Image')
    axes[0].axis('off')

    # Panel 2: Segmentation mask overlay
    bbox_polygon = Polygon([
        (roi_bbox[0], roi_bbox[1]), (roi_bbox[2], roi_bbox[1]),
        (roi_bbox[2], roi_bbox[3]), (roi_bbox[0], roi_bbox[3])
    ])
    roi_nuclei = gdf[gdf['geometry'].intersects(bbox_polygon)]
    cmap = ListedColormap(['grey'])
    roi_nuclei.plot(cmap=cmap, ax=axes[1])
    axes[1].set_title(f'Detected Nuclei (n={len(roi_nuclei)})')
    axes[1].axis('off')

    # Panel 3: Area histogram for this ROI
    axes[2].hist(roi_nuclei['area'], bins=30, edgecolor='black')
    axes[2].set_title(f'Nuclei Area Distribution')
    axes[2].set_xlabel('Area (px²)')

    plt.suptitle(f'ROI {i+1}: Segmentation QC')
    plt.savefig(f'{outs_dir}/qc_segmentation_ROI{i+1}.png', dpi=150, bbox_inches='tight')
```

### If SR Segmentation Is Available — Show Comparison

```python
if sr_segmentation_available:
    for i, roi_bbox in enumerate(user_confirmed_rois[:2]):
        fig, axes = plt.subplots(1, 3, figsize=(21, 6))
        crop = img_normalized[roi_bbox[1]:roi_bbox[3], roi_bbox[0]:roi_bbox[2]]
        bbox_poly = Polygon([
            (roi_bbox[0], roi_bbox[1]), (roi_bbox[2], roi_bbox[1]),
            (roi_bbox[2], roi_bbox[3]), (roi_bbox[0], roi_bbox[3])
        ])

        axes[0].imshow(crop)
        axes[0].set_title('H&E Image')

        roi_sd = gdf[gdf['geometry'].intersects(bbox_poly)]
        roi_sd.plot(ax=axes[1], facecolor='none', edgecolor='blue', linewidth=0.5)
        axes[1].set_title(f'StarDist ({len(roi_sd)} nuclei)')

        roi_sr = gdf_sr[gdf_sr['geometry'].intersects(bbox_poly)]
        roi_sr.plot(ax=axes[2], facecolor='none', edgecolor='red', linewidth=0.5)
        axes[2].set_title(f'Space Ranger ({len(roi_sr)} nuclei)')

        for ax in axes:
            ax.axis('off')
        plt.suptitle(f'ROI {i+1}: StarDist vs Space Ranger Segmentation')
        plt.savefig(f'{outs_dir}/qc_comparison_ROI{i+1}.png', dpi=150, bbox_inches='tight')
```

### QC Report to Present

Present a summary table per ROI:

| ROI | Total Nuclei | Mean Area (px²) | Median Area (px²) | CV | Small Frac (<20px²) | Large Frac (>5×median) |
|-----|-------------|-----------------|--------------------|----|---------------------|----------------------|
| ROI 1 | ... | ... | ... | ... | ... | ... |

Plus the **parameters used**: `prob_thresh`, `nms_thresh`, `min_percentile`, `max_percentile`

If SR comparison is available, add a comparison table:

| Metric | StarDist | Space Ranger | Winner |
|--------|----------|-------------|--------|
| Nuclei count | ... | ... | ... |
| Median area (px²) | ... | ... | ... |
| CV (area) | ... | ... | ... |
| Boundary sharpness | visual | visual | ... |

### User Decision

The user must either:
- ✅ Approve StarDist segmentation → proceed to barcode binning
- ✅ Choose SR built-in segmentation → use `gdf_sr` instead of `gdf`
- 🔄 Request parameter re-tuning (agent re-enters optimization loop)
- 🔧 Request a different segmentation approach (Cellpose, custom model)

**Do NOT proceed to spatial joining until the user explicitly confirms segmentation quality.**

---

### Step 5–8: Barcode Binning (after Gate 2 approval)

These steps execute automatically after segmentation is confirmed.

#### Step 5: Load Visium HD Data

```python
adata = sc.read_10x_h5(matrix_h5)

df_tissue_positions = pd.read_parquet(positions_parquet)
df_tissue_positions = df_tissue_positions.set_index('barcode')
df_tissue_positions['index'] = df_tissue_positions.index

adata.obs = pd.merge(adata.obs, df_tissue_positions, left_index=True, right_index=True)

geometry = [Point(xy) for xy in zip(
    df_tissue_positions['pxl_col_in_fullres'],
    df_tissue_positions['pxl_row_in_fullres']
)]
gdf_coordinates = gpd.GeoDataFrame(df_tissue_positions, geometry=geometry)
```

#### Step 5b: Coordinate System Cross-Validation

```python
# Verify coordinate alignment between barcode positions and H&E image
img_h, img_w = img.shape[:2]
max_barcode_x = df_tissue_positions['pxl_col_in_fullres'].max()
max_barcode_y = df_tissue_positions['pxl_row_in_fullres'].max()

print(f"H&E image dimensions:  {img_w} × {img_h} pixels")
print(f"Max barcode X (col):   {max_barcode_x}")
print(f"Max barcode Y (row):   {max_barcode_y}")

# Warn if barcodes extend beyond image bounds
if max_barcode_x > img_w * 1.05 or max_barcode_y > img_h * 1.05:
    print("⚠️  WARNING: Barcode coordinates exceed image dimensions!")
    print("   This may indicate a CytAssist/microscope image mismatch.")
    print("   Verify that you are using the MICROSCOPE image, not the CytAssist image.")
elif max_barcode_x < img_w * 0.5 or max_barcode_y < img_h * 0.5:
    print("⚠️  WARNING: Barcodes cover less than half the image.")
    print("   This may indicate a registration offset. Check aligned_fiducials.jpg")
else:
    print("✅ Coordinate cross-validation passed.")

# Also verify scale factors agreement
if 'scale_factors' in dir():
    print(f"\nScale factors from Space Ranger:")
    print(f"  tissue_hires_scalef:    {scale_factors.get('tissue_hires_scalef', 'N/A')}")
    print(f"  tissue_lowres_scalef:   {scale_factors.get('tissue_lowres_scalef', 'N/A')}")
    print(f"  spot_diameter_fullres:  {scale_factors.get('spot_diameter_fullres', 'N/A')}")
```

#### Step 6: Spatial Join

```python
result_spatial_join = gpd.sjoin(gdf_coordinates, gdf, how='left', predicate='within')

result_spatial_join['is_within_polygon'] = ~result_spatial_join['index_right'].isna()
barcodes_in_overlapping = pd.unique(
    result_spatial_join[result_spatial_join.duplicated(subset=['index'])]['index']
)
result_spatial_join['is_not_in_overlap'] = ~result_spatial_join['index'].isin(barcodes_in_overlapping)

barcodes_in_one_polygon = result_spatial_join[
    result_spatial_join['is_within_polygon'] & result_spatial_join['is_not_in_overlap']
]

filtered_obs_mask = adata.obs_names.isin(barcodes_in_one_polygon['index'])
filtered_adata = adata[filtered_obs_mask, :]

filtered_adata.obs = pd.merge(
    filtered_adata.obs,
    barcodes_in_one_polygon[['index', 'geometry', 'id', 'is_within_polygon', 'is_not_in_overlap']],
    left_index=True, right_index=True
)
```

#### Step 7: Gene-wise UMI Count Summation

```python
groupby_object = filtered_adata.obs.groupby(['id'], observed=True)
counts = filtered_adata.X
N_groups = groupby_object.ngroups
N_genes = counts.shape[1]

summed_counts = sparse.lil_matrix((N_groups, N_genes))
polygon_id = []
row = 0

for polygons, idx_ in groupby_object.indices.items():
    summed_counts[row] = counts[idx_].sum(0)
    row += 1
    polygon_id.append(polygons)

summed_counts = summed_counts.tocsr()
grouped_filtered_adata = anndata.AnnData(
    X=summed_counts,
    obs=pd.DataFrame(polygon_id, columns=['id'], index=polygon_id),
    var=filtered_adata.var
)
```

#### Step 8: Compute Binning Summary Statistics

```python
gdf['area'] = gdf['geometry'].area
sc.pp.calculate_qc_metrics(grouped_filtered_adata, inplace=True)

# Print summary for the agent to report
total_barcodes = adata.n_obs
assigned_barcodes = filtered_adata.n_obs
n_nuclei = grouped_filtered_adata.n_obs
assignment_rate = assigned_barcodes / total_barcodes * 100

print(f"Total 2µm barcodes: {total_barcodes:,}")
print(f"Barcodes assigned to nuclei: {assigned_barcodes:,} ({assignment_rate:.1f}%)")
print(f"Barcodes in overlapping nuclei (discarded): {len(barcodes_in_overlapping):,}")
print(f"Final nuclei count: {n_nuclei:,}")
print(f"Median UMI per nucleus: {grouped_filtered_adata.obs['total_counts'].median():.0f}")
print(f"Median genes per nucleus: {grouped_filtered_adata.obs['n_genes_by_counts'].median():.0f}")

# Store pipeline provenance in AnnData
grouped_filtered_adata.uns['pipeline'] = {
    'spaceranger_dir': spaceranger_dir,
    'he_image': he_image_path,
    'segmentation_method': 'StarDist_2D_versatile_he',  # or 'SpaceRanger_v4_builtin'
    'prob_thresh': best_params[0] if 'best_params' in dir() else 0.01,
    'nms_thresh': best_params[1] if 'best_params' in dir() else 0.001,
    'min_percentile': min_percentile,
    'max_percentile': max_percentile,
    'sr_health_grade': sr_report.get('grade', 'unknown'),
    'scale_factors': scale_factors if 'scale_factors' in dir() else {},
}
```

---

## 🔁 OPTIMIZATION LOOP: QC Threshold Tuning

Before presenting QC thresholds to the user, the agent should automatically identify sensible cutoffs.

### Automated Threshold Estimation

```python
def suggest_area_cutoff(gdf):
    """Use distribution statistics to suggest an area upper bound."""
    areas = gdf['area']
    q75 = areas.quantile(0.75)
    iqr = areas.quantile(0.75) - areas.quantile(0.25)
    upper_fence = q75 + 3 * iqr  # Generous outlier fence
    # Also check: areas > 5× median are likely merged nuclei
    size_based = areas.median() * 5
    return min(upper_fence, size_based)

def suggest_umi_cutoff(adata):
    """Use distribution knee-point to suggest minimum UMI threshold."""
    counts = adata.obs['total_counts'].sort_values()
    # Use 5th percentile as floor
    floor = counts.quantile(0.05)
    # Also check: cells with < 50 UMI are likely empty/noise
    return max(floor, 50)

suggested_area = suggest_area_cutoff(gdf)
suggested_umi = suggest_umi_cutoff(grouped_filtered_adata)
```

### Impact Preview

The agent should compute how many nuclei survive at different cutoff combinations:

```python
def preview_filtering(gdf, adata, area_cutoffs, umi_cutoffs):
    """Show how many nuclei survive each threshold combination."""
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

# Sweep around the suggested values
area_range = [suggested_area * f for f in [0.5, 0.75, 1.0, 1.5, 2.0]]
umi_range = [max(10, suggested_umi * f) for f in [0.25, 0.5, 1.0, 1.5, 2.0]]
preview_df = preview_filtering(gdf, grouped_filtered_adata, area_range, umi_range)
```

---

## 🚦 QC GATE 3: Filtering Thresholds Confirmation

**This is a mandatory stop-and-confirm gate.**

### What the Agent Must Present

1. **Nuclei area distribution** — histogram with suggested cutoff line:

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(gdf['area'], bins=50, edgecolor='black')
axes[0].axvline(suggested_area, color='red', linestyle='--', label=f'Suggested cutoff: {suggested_area:.0f}')
axes[0].set_title('Nuclei Area Distribution (all)')
axes[0].legend()
axes[1].hist(gdf[gdf['area'] < suggested_area]['area'], bins=50, edgecolor='black')
axes[1].set_title(f'After filtering (area < {suggested_area:.0f})')
plt.savefig(f'{outs_dir}/qc_area_distribution.png', dpi=150, bbox_inches='tight')
```

2. **Total UMI distribution** — boxplot with suggested cutoff:

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].boxplot(grouped_filtered_adata.obs['total_counts'], vert=False, patch_artist=True,
                boxprops=dict(facecolor='skyblue'))
axes[0].set_title('Total UMI per Nucleus (all)')
axes[1].boxplot(grouped_filtered_adata.obs['total_counts'][
    grouped_filtered_adata.obs['total_counts'] > suggested_umi
], vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
axes[1].set_title(f'After filtering (UMI > {suggested_umi:.0f})')
plt.savefig(f'{outs_dir}/qc_umi_distribution.png', dpi=150, bbox_inches='tight')
```

3. **Filtering impact table** — showing nuclei retained at different thresholds

4. **Recommended thresholds** with reasoning

### User Decision

The user must either:
- ✅ Approve the suggested thresholds
- 🔄 Provide custom thresholds
- 📊 Request additional visualizations (e.g., genes_by_counts, specific area ranges)

**Do NOT proceed to clustering until the user confirms thresholds.**

After user approval, apply the filters:

```python
mask_area = grouped_filtered_adata.obs['id'].isin(gdf[gdf['area'] < area_cutoff].id)
mask_count = grouped_filtered_adata.obs['total_counts'] > umi_cutoff
count_area_filtered_adata = grouped_filtered_adata[mask_area & mask_count, :]
sc.pp.calculate_qc_metrics(count_area_filtered_adata, inplace=True)
```

---

## 🔁 OPTIMIZATION LOOP: Clustering Resolution

The agent should sweep Leiden resolution to find a value that produces biologically meaningful clusters.

```python
def evaluate_clustering(adata, resolution):
    """Run clustering and return summary metrics."""
    adata_copy = adata.copy()
    sc.pp.normalize_total(adata_copy, inplace=True)
    sc.pp.log1p(adata_copy)
    sc.pp.highly_variable_genes(adata_copy, flavor="seurat", n_top_genes=2000)
    sc.pp.pca(adata_copy)
    sc.pp.neighbors(adata_copy)
    sc.tl.leiden(adata_copy, resolution=resolution, key_added="clusters")

    n_clusters = adata_copy.obs['clusters'].nunique()
    cluster_sizes = adata_copy.obs['clusters'].value_counts()
    min_cluster_pct = cluster_sizes.min() / adata_copy.n_obs * 100

    return {
        'resolution': resolution,
        'n_clusters': n_clusters,
        'min_cluster_size': cluster_sizes.min(),
        'min_cluster_pct': min_cluster_pct,
        'max_cluster_size': cluster_sizes.max(),
        'adata': adata_copy
    }

# Sweep resolutions
resolution_results = []
for res in [0.1, 0.2, 0.3, 0.5, 0.7, 1.0]:
    result = evaluate_clustering(count_area_filtered_adata, res)
    resolution_results.append(result)
    print(f"Resolution {res}: {result['n_clusters']} clusters, "
          f"smallest = {result['min_cluster_pct']:.1f}%")
```

---

## 🚦 QC GATE 4: Clustering Validation

**This is a mandatory stop-and-confirm gate.**

### What the Agent Must Present

1. **Resolution sweep summary table**:

| Resolution | Clusters | Smallest Cluster (%) | Largest Cluster (%) |
|-----------|---------|---------------------|---------------------|
| 0.1 | ... | ... | ... |
| 0.3 | ... | ... | ... |

2. **Spatial cluster overlays** for 2–3 resolution values on the user-confirmed ROIs
   (using `plot_clusters_and_save_image` from `references/plotting_functions.py`)

3. **Recommended resolution** with rationale (the agent should favor resolutions where
   clusters align visually with distinct tissue morphologies)

### User Decision

- ✅ Approve a specific resolution → proceed to marker validation
- 🔄 Request finer resolution sweep in a specific range
- 🔧 Request trying different preprocessing (e.g., different n_top_genes)

---

## 🚦 QC GATE 5: Marker Gene Validation & Final Approval

**This is the final mandatory gate.** The result of the entire pipeline is evaluated here.

### Tissue-Type-Aware Marker Gene Tables

The agent should select marker genes appropriate to the tissue under analysis. Common
reference panels:

#### Mouse Calvaria / Bone

| Cell Type | Marker Genes | Expected Location |
|-----------|-------------|-------------------|
| Osteoblasts | *Bglap*, *Spp1*, *Runx2*, *Col1a1* | Bone surface / periosteum |
| Osteoclasts | *Ctsk*, *Acp5* (TRAP), *Mmp9* | Resorption lacunae |
| Osteocytes | *Dmp1*, *Sost*, *Fgf23* | Embedded in bone matrix |
| MSCs | *Lepr*, *Cxcl12*, *Pdgfra* | Bone marrow / perivascular |
| Chondrocytes | *Col2a1*, *Acan*, *Sox9* | Growth plate / sutures |
| Endothelial | *Pecam1* (CD31), *Cdh5*, *Emcn* | Vasculature |
| Macrophages | *Adgre1* (F4/80), *Csf1r*, *Cd68* | Throughout marrow |
| Neutrophils | *S100a8*, *S100a9*, *Ly6g* | BM / inflammatory foci |

#### Mouse Knee / Articular

| Cell Type | Marker Genes | Expected Location |
|-----------|-------------|-------------------|
| Articular chondrocytes | *Prg4* (lubricin), *Col2a1* | Joint surface |
| Hypertrophic chondrocytes | *Col10a1*, *Ihh*, *Mmp13* | Growth plate |
| Synoviocytes | *Cdh11*, *Thy1*, *Prg4* | Synovial membrane |
| Meniscal cells | *Col1a1*, *Col2a1* (mixed) | Meniscus |

#### Mouse Small Intestine (10x demo tissue)

| Cell Type | Marker Genes | Expected Location |
|-----------|-------------|-------------------|
| Paneth cells | *Lyz1*, *Defa5* | Crypt base |
| Goblet cells | *Muc2*, *Tff3* | Scattered along villi |
| Enterocytes | *Fabp2*, *Alpi* | Villus surface |
| Stem cells | *Lgr5*, *Ascl2* | Crypt base |
| Plasma cells | *Jchain*, *Igha* | Lamina propria |

#### Human Tissue (Generic)

| Cell Type | Marker Genes |
|-----------|-------------|
| Epithelial | *EPCAM*, *KRT18*, *CDH1* |
| Fibroblasts | *COL1A1*, *DCN*, *VIM* |
| Endothelial | *PECAM1*, *VWF*, *CDH5* |
| T cells | *CD3D*, *CD3E*, *CD8A* |
| B cells | *CD79A*, *MS4A1* (CD20) |
| Macrophages | *CD68*, *CD163*, *CSF1R* |
| Smooth muscle | *ACTA2*, *MYH11* |

### What the Agent Must Present

1. **Spatial marker gene plots** — for known cell-type markers relevant to the tissue:

```python
marker_genes = marker_tables[tissue_type]  # Select appropriate table

for cell_type, gene in marker_genes.items():
    if gene in count_area_filtered_adata.var_names:
        for roi_bbox in user_confirmed_rois[:2]:  # Show on first 2 ROIs
            plot_gene_and_save_image(
                title=f"{cell_type} ({gene})",
                gdf=gdf, gene=gene, img=img_normalized,
                adata=count_area_filtered_adata,
                bbox=roi_bbox,
                output_name=f'{outs_dir}/qc_marker_{gene}_ROI.tiff'
            )
```

2. **Cluster-marker correspondence** — show whether marker genes are enriched in specific clusters:

```python
sc.tl.rank_genes_groups(count_area_filtered_adata, 'clusters', method='wilcoxon')
sc.pl.rank_genes_groups(count_area_filtered_adata, n_genes=10, save='_qc_markers.png')
```

3. **Final summary statistics**:
   - Number of final cells (nuclei)
   - Number of clusters
   - Median UMI per cell
   - Median genes per cell
   - Assignment rate (barcodes → nuclei)
   - Parameters used at every step
   - Space Ranger health grade (from pre-flight)
   - Segmentation method used (StarDist / SR built-in)

4. **Biological validation question** to the user:
   > "Do the spatial expression patterns match expected tissue morphology? For example, [marker X] should be expressed in [expected region]. Please review the marker plots and confirm whether the segmentation results are biologically plausible."

### User Decision

- ✅ Approve → export final AnnData to `.h5ad`
- 🔄 Request going back to a specific gate (segmentation, thresholds, or clustering)
- ❌ Reject → start over with different parameters or segmentation method

### Final Export (after approval)

```python
# Save the final nuclei-binned AnnData
output_path = f'{outs_dir}/visiumhd_nuclei_binned.h5ad'
count_area_filtered_adata.write(output_path)
print(f"Saved: {output_path}")
print(f"Shape: {count_area_filtered_adata.shape[0]} nuclei × {count_area_filtered_adata.shape[1]} genes")

# Also export the nuclei GeoDataFrame for downstream spatial analysis
gdf_output_path = f'{outs_dir}/nuclei_segmentation.geojson'
gdf.to_file(gdf_output_path, driver='GeoJSON')
print(f"Saved nuclei polygons: {gdf_output_path}")
```

---

## Critical Parameters Summary

| Parameter | Step | Default | Impact | Optimized By |
|-----------|------|---------|--------|-------------|
| `min_percentile` / `max_percentile` | Image norm | 5 / 95 | Contrast; affects segmentation | Gate 1 (user) |
| `prob_thresh` | StarDist | 0.01 | Detection sensitivity | Auto-loop → Gate 2 |
| `nms_thresh` | StarDist | 0.001 | Overlap tolerance | Auto-loop → Gate 2 |
| `block_size` | StarDist | 4096 | Tiling for large images | Fixed default |
| `area_cutoff` | QC filter | auto | Remove merged nuclei | Auto-loop → Gate 3 |
| `umi_cutoff` | QC filter | auto | Remove empty nuclei | Auto-loop → Gate 3 |
| `resolution` | Leiden | 0.35 | Cluster granularity | Auto-loop → Gate 4 |

---

## Advanced Considerations

See `references/dependencies.md` for detailed API documentation on StarDist, GeoPandas, Squidpy, and fastparquet.

### Alternative Segmentation Models

StarDist's `2D_versatile_he` works well for many H&E images. For specialized tissue:
- **Space Ranger v4.0+ built-in** segmentation (automatically compared at Gate 2 if available)
- Train a **custom StarDist model** on your tissue type
- Try **Cellpose** (`cyto2` or `nuclei`) as an alternative
- Use **image thresholding + watershed** for simple cases

### Nucleus Boundary Expansion

Expanding each nucleus polygon by 2–5 µm via `Polygon.buffer()` captures peri-nuclear
transcripts but risks creating overlaps. If using Space Ranger's custom segmentation
pathway, set `--nucleus-expansion-distance-micron` in `spaceranger count`.

### Feeding StarDist Segmentation Back to Space Ranger

If you want Space Ranger to perform the binning instead of this pipeline, export the
StarDist results as GeoJSON and pass them back:

```bash
# Re-run spaceranger count with custom segmentation
spaceranger count \
  ... \
  --custom-segmentation-file=nuclei_segmentation.geojson \
  --nucleus-expansion-distance-micron=5
```

This produces `segmented_outputs/` with nuclei-level matrices directly from Space Ranger.

### Memory Considerations

- Always use `predict_instances_big` for whole-slide images
- Increase `n_tiles` if GPU memory is insufficient
- Consider chunking the spatial join for million-barcode datasets

### Coordinate System Notes

- StarDist: `(row, col)` = `(y, x)` ordering
- tissue_positions.parquet: `pxl_row_in_fullres`, `pxl_col_in_fullres`
- Shapely: `Point(x, y)` = `Point(col, row)`
- `scalefactors_json.json`: provides conversion factors between full-res, hires, and lowres images

---

## Bundled Resources

| Resource | Path | Description |
|----------|------|-------------|
| Plotting helpers | `references/plotting_functions.py` | Visualization for masks, genes, clusters, QC metrics |
| Dependency docs | `references/dependencies.md` | Detailed API docs (StarDist, GeoPandas, Squidpy, fastparquet) |
| QC optimization | `scripts/qc_optimization.py` | Self-regression: StarDist sweep, threshold estimation, clustering resolution |

## Related Skills

| Skill | Role | Relationship |
|-------|------|-------------|
| **spaceranger** | Upstream pipeline | Produces the `binned_outputs/` and `segmented_outputs/` consumed by this skill |
| **scanpy** | Analysis framework | Core library used for preprocessing, clustering, and DE |
| **squidpy** | Spatial statistics | Neighborhood enrichment, co-occurrence, Moran's I on the output AnnData |
