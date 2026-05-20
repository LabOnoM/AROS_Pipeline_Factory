---
name: cellfinder
description: Guide for using cellfinder for automated 3D cell detection and classification in large brain images. Use when the user mentions cellfinder, cell detection in brain images, automated cell counting, brain cell classification, brainmapper, labelled cell detection, whole-brain cell detection, serial two-photon cell detection, lightsheet cell detection, or wants to detect/classify cells in large 3D brain microscopy images. Also covers the cellfinder napari plugin, cellfinder.core Python API, and retraining the neural network.
---

# cellfinder — Automated 3D Cell Detection

cellfinder is software for automated 3D cell detection in very large 3D images (e.g., serial two-photon or lightsheet volumes of whole mouse brains). It uses a deep learning-based approach: first detecting cell candidates via image filtering, then classifying them using a pre-trained ResNet neural network.

**Package**: `pip install cellfinder[napari]`  
**Docs**: https://brainglobe.info/documentation/cellfinder/index.html  
**GitHub**: https://github.com/brainglobe/cellfinder

---

## Installation

```bash
# With napari plugin
pip install cellfinder[napari]

# Or via brainglobe meta-package
pip install brainglobe

# For brainmapper CLI workflow (cell detection + registration):
pip install brainglobe-workflows
```

## Three Ways to Use cellfinder

### 1. cellfinder.core Python API

```python
from cellfinder.core.main import main as cellfinder_run
from cellfinder.core.train.train_yml import run as train_run
import numpy as np

# Load your signal and background images as numpy arrays
signal_array = np.load("signal_planes.npy")      # 3D array (z, y, x)
background_array = np.load("background_planes.npy")

# Run cell detection
detected_cells = cellfinder_run(
    signal_array=signal_array,
    background_array=background_array,
    voxel_sizes=(5, 2, 2),    # z, y, x in µm
)

# detected_cells is a list of Cell objects
for cell in detected_cells:
    print(f"Cell at {cell.x}, {cell.y}, {cell.z} - Type: {cell.type}")
    # cell.type: 1 = rejected (not a cell), 2 = accepted (real cell)
```

### 2. cellfinder napari Plugin

1. Open napari
2. Load signal and background channels as separate layers
3. Go to Plugins > cellfinder > Cell detection
4. Select signal and background image layers
5. Set voxel sizes and detection parameters
6. Click "Run"
7. Detected cells appear as points layers (cells vs. non-cells)

### 3. brainmapper CLI (cell detection + atlas registration)

```bash
# Full workflow: cell detection + brain registration
brainmapper \
    -s /path/to/signal_images \
    -b /path/to/background_images \
    -o /path/to/output \
    -v 5 2 2 \
    --orientation psl \
    --atlas allen_mouse_25um

# Signal-only (if background not available):
brainmapper -s /path/to/signal --no-detection
```

## Detection Parameters

Key parameters for tuning cell detection:

```python
detected_cells = cellfinder_run(
    signal_array=signal,
    background_array=background,
    voxel_sizes=(5, 2, 2),
    # Detection parameters
    start_plane=0,
    end_plane=-1,
    trained_model=None,               # path to custom model
    model_weights=None,
    soma_diameter=16,                 # expected cell diameter in µm
    ball_xy_size=6,                   # filter ball size in xy
    ball_z_size=15,                   # filter ball size in z
    ball_overlap_fraction=0.6,
    log_sigma_size=0.2,
    n_sds_above_mean_thresh=10,       # detection threshold
    soma_spread_factor=1.4,
    max_cluster_size=100000,
    # Classification
    batch_size=32,
    n_free_cpus=2,
    use_gpu=True,
)
```

## Retraining the Network

If the pre-trained network doesn't perform well on your data:

```python
from cellfinder.core.train.train_yml import run as train_yml

# Prepare training data:
# - YAML file specifying training data paths
# - Curated cell/non-cell image cubes

train_yml(
    yaml_file="/path/to/training_config.yaml",
    output_directory="/path/to/trained_model",
    epochs=100,
    batch_size=32,
    learning_rate=0.0001,
    continue_training=False,          # True to fine-tune existing model
    pretrained_model=None,            # path to start from
)
```

## Downloading Pre-trained Models

```bash
# Download the default model in advance (useful for offline use)
cellfinder_download
```

---

## Troubleshooting & Online Resources

### Search Priority Order

1. **BrainGlobe Docs**: https://brainglobe.info/documentation/cellfinder/index.html
2. **cellfinder Troubleshooting**: https://brainglobe.info/documentation/cellfinder/troubleshooting/index.html
3. **GitHub Issues**: https://github.com/brainglobe/cellfinder/issues
4. **BrainGlobe Forum**: https://forum.image.sc/tag/brainglobe
5. **General Web Search**: `"cellfinder" brainglobe <error or topic>`

### Common Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Too many false positives | `"false positive" cellfinder parameters` | Troubleshooting docs |
| Too few cells detected | `"threshold" "soma diameter" cellfinder` | Troubleshooting docs |
| GPU not detected | `"GPU" "CUDA" cellfinder tensorflow` | GitHub Issues |
| Out of memory | `"memory" "batch_size" cellfinder` | GitHub Issues |
| Slow detection | `"performance" "speed" cellfinder` | GitHub Issues |
| Retraining fails | `"training" "yaml" cellfinder` | Docs: training |
| Model download fails | `"cellfinder_download" model` | GitHub Issues |
| brainmapper errors | `"brainmapper" cellfinder workflow` | GitHub Issues |

**Key tip**: The most impactful parameters to tune are `soma_diameter` (match your cells) and `n_sds_above_mean_thresh` (lower = more cells detected, higher = fewer).
