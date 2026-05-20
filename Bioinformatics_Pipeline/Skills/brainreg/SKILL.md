---
name: brainreg
description: Guide for using brainreg for automated brain image registration to atlas templates. Use when the user mentions brainreg, brain registration, atlas registration, whole-brain registration, NiftyReg, registering brain images to atlas space, template-to-sample alignment, brain image alignment, or wants to register microscopy brain images (e.g. serial two-photon, lightsheet) to a reference atlas like Allen Mouse Brain Atlas. Also covers the brainreg napari plugin and CLI.
---

# brainreg — Brain Image Registration

brainreg registers brain images to atlas templates using NiftyReg. It aligns a template brain (e.g., Allen Mouse Brain Atlas) to your sample image through reorientation, affine, and freeform registration stages. Any atlas supported by brainglobe-atlasapi can be used.

**Package**: `pip install brainreg[napari]`  
**Docs**: https://brainglobe.info/documentation/brainreg/index.html  
**GitHub**: https://github.com/brainglobe/brainreg

---

## Installation

```bash
# With napari plugin (recommended)
pip install brainreg[napari]

# Or via brainglobe meta-package
pip install brainglobe

# macOS users also need NiftyReg:
conda install -c conda-forge niftyreg
```

## Command Line Usage

```bash
# Basic registration
brainreg /path/to/sample/image /path/to/output -v 5 2 2 --orientation psl

# Required arguments:
#   input_data      - path to sample brain data (TIFF series or directory)
#   output_dir      - directory for registration results
#   -v / --voxel-sizes  - voxel sizes in µm (z y x order)
#   --orientation   - anatomical orientation of your data (e.g., "psl", "asr")

# Key optional arguments:
#   --atlas          - atlas to use (default: allen_mouse_25um)
#   --additional     - path to additional channels to transform
#   --debug          - save intermediate files
#   --affine-n-steps - number of affine registration steps
#   --freeform-n-steps - number of freeform registration steps
#   --brain_geometry - geometry type: full (default), hemisphere_l, hemisphere_r
```

### Orientation Specification

Three-letter code specifying the origin of the image stack:
- **a/p**: anterior/posterior
- **s/i**: superior/inferior
- **l/r**: left/right

Example: `psl` = origin is Posterior-Superior-Left

## Napari Plugin

```python
import napari

viewer = napari.Viewer()
# Load your image data
# Then use Plugins > brainreg > Register
# Set voxel sizes, orientation, atlas, and output directory
```

## Python API

```python
from brainreg.core.main import main as brainreg_run

brainreg_run(
    atlas="allen_mouse_25um",
    data_orientation="psl",
    voxel_sizes=(5, 2, 2),           # z, y, x in µm
    target_folder="/path/to/input",
    brainreg_directory="/path/to/output",
    additional_images_downsample=None,
)
```

## Output Files

The output directory contains:
- `registered_atlas.tiff` — atlas annotations in sample space
- `registered_hemispheres.tiff` — hemisphere labels in sample space
- `downsampled.tiff` — downsampled sample image
- `downsampled_standard.tiff` — sample image aligned to atlas space
- `boundaries.tiff` — region boundaries overlay
- `deformation_field_*.tiff` — deformation field components
- Transform files (`.txt`) for NiftyReg

## Checking Registration Quality

1. Open output in napari: `napari /path/to/output`
2. Compare `registered_atlas.tiff` overlay on `downsampled.tiff`
3. Check orientation is correct (most common source of errors)
4. Verify boundaries align with brain structures

---

## Troubleshooting & Online Resources

### Search Priority Order

1. **BrainGlobe Docs**: https://brainglobe.info/documentation/brainreg/index.html
2. **brainreg Troubleshooting Page**: https://brainglobe.info/documentation/brainreg/troubleshooting.html
3. **GitHub Issues**: https://github.com/brainglobe/brainreg/issues
4. **BrainGlobe Forum**: https://forum.image.sc/tag/brainglobe
5. **General Web Search**: `"brainreg" <error or topic>`

### Common Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Poor registration quality | `"registration quality" OR "improving registration" brainreg` | Troubleshooting page |
| Wrong orientation | `"orientation" "checking" brainreg` | Docs: checking-orientation |
| NiftyReg not found (macOS) | `"niftyreg" "conda" brainreg macOS` | GitHub Issues |
| Out of memory | `"memory" "RAM" brainreg` | GitHub Issues |
| Atlas not downloading | `"atlas download" brainreg` | GitHub Issues |
| Incorrect voxel sizes | `"voxel sizes" "resolution" brainreg` | Docs |
| Additional channel transform fails | `"additional" "channel" brainreg` | GitHub Issues |

**Key troubleshooting tip**: The most common cause of poor registration is incorrect orientation specification. Always verify orientation first.
