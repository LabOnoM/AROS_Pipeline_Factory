---
name: brainglobe-segmentation
description: Guide for using brainglobe-segmentation to segment and analyze brain regions/objects (injection sites, probes, implants) in atlas-registered brain images. Use when the user mentions brainglobe-segmentation, brain region segmentation after registration, segmenting injection sites, probe track segmentation, implant localization, ROI analysis in registered brains, or wants to analyze brain region distribution of manually or automatically segmented structures after atlas registration with brainreg.
---

# brainglobe-segmentation — Post-Registration Brain Segmentation

brainglobe-segmentation is a napari plugin companion to brainreg that enables segmentation of structures (injection sites, probes, implants) within atlas-registered brain images. It provides automated analysis of brain region distribution and visualization via brainrender.

**Package**: `pip install brainglobe-segmentation`  
**Docs**: https://brainglobe.info/documentation/brainglobe-segmentation/index.html  
**GitHub**: https://github.com/brainglobe/brainglobe-segmentation

---

## Installation

```bash
# With brainreg (recommended)
pip install brainreg[napari]
# This includes brainglobe-segmentation

# Standalone
pip install brainglobe-segmentation

# Or via brainglobe meta-package:
pip install brainglobe
```

## Prerequisites

1. **Register your brain** using brainreg first
2. Open the brainreg output directory in napari

## Usage (napari Plugin)

### Loading Data

```python
import napari
viewer = napari.Viewer()
# Use Plugins > brainglobe-segmentation > Region segmentation
# Select the brainreg output directory
```

### Segmentation Methods

1. **Manual 2D segmentation**: Draw ROIs on individual slices
   - Use napari's drawing tools (paintbrush, fill)
   - Segment across multiple slices for 3D volumes

2. **1D track tracing**: For probes/electrode tracks
   - Place points along the track
   - Tool fits a spline and identifies crossed regions

3. **3D region segmentation**: For larger structures
   - Paint/fill in 3D
   - Automatic region assignment from atlas

### Analysing External Segmentation

If you've segmented with another napari plugin:

```python
# Load your segmentation as a labels layer
# Use brainglobe-segmentation's analysis tools
# to identify brain regions in your segmentation
```

### Output

- **Region summary**: CSV with brain region distribution
- **Visualizations**: Compatible with brainrender for 3D rendering
- **Coordinates**: Atlas-space coordinates of segmented structures

---

## Troubleshooting & Online Resources

### Search Priority Order

1. **BrainGlobe Docs**: https://brainglobe.info/documentation/brainglobe-segmentation/index.html
2. **GitHub Issues**: https://github.com/brainglobe/brainglobe-segmentation/issues
3. **BrainGlobe Forum**: https://forum.image.sc/tag/brainglobe
4. **General Web Search**: `"brainglobe-segmentation" <error or topic>`

### Common Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Plugin not appearing in napari | `"plugin" "napari" brainglobe-segmentation` | GitHub Issues |
| Can't load brainreg output | `"brainreg" "output" brainglobe-segmentation` | Docs |
| Region assignment incorrect | `"region" "assignment" brainglobe-segmentation` | GitHub Issues |
| Export fails | `"export" "CSV" brainglobe-segmentation` | GitHub Issues |
