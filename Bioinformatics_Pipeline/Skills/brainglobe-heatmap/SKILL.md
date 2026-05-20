---
name: brainglobe-heatmap
description: Guide for using brainglobe-heatmap to create 2D and 3D brain region heatmaps from scalar data. Use when the user mentions brain heatmap, brain region heatmap, neuroanatomical heatmap, brain region coloring, brain slice visualization, mapping values to brain regions, or wants to visualize scalar data (e.g., cell counts, gene expression) mapped onto brain atlas regions in 2D matplotlib plots or 3D brainrender scenes. Supports all atlases via BrainGlobe Atlas API.
---

# brainglobe-heatmap — Brain Region Heatmaps

brainglobe-heatmap maps scalar values for each brain region (e.g., cell counts, expression levels) to colors, creating 2D (matplotlib) or 3D (brainrender) visualizations. Compatible with all atlases via BrainGlobe Atlas API.

**Package**: `pip install brainglobe-heatmap`  
**Import**: `import brainglobe_heatmap as bgh`  
**Docs**: https://brainglobe.info/documentation/brainglobe-heatmap/index.html  
**GitHub**: https://github.com/brainglobe/brainglobe-heatmap

---

## Installation

```bash
pip install brainglobe-heatmap
# Or via brainglobe meta-package:
pip install brainglobe
```

## Quick Start

```python
import brainglobe_heatmap as bgh

# Define scalar values per brain region (by acronym)
values = dict(
    TH=1, RSP=0.2, AI=0.4, SS=-3, MO=2.6,
    VIS=1.5, AUD=-0.3, HIP=2.1, STR=0.8
)

# Create 2D heatmap (frontal slice)
f = bgh.Heatmap(
    values,
    position=8000,              # slice position in µm
    orientation="frontal",      # "frontal", "sagittal", "horizontal"
    thickness=2000,             # slice thickness in µm
    format="2D",                # "2D" (matplotlib) or "3D" (brainrender)
    title="Brain Region Activity",
    vmin=-5,
    vmax=3,
    cmap="RdBu_r",
    annotate_regions=True,
).show()
```

## Detailed Usage

### Planning Slice Position

```python
import brainglobe_heatmap as bgh

# Use the planner to interactively find the right slice
planner = bgh.plan(
    values,
    position=(8000, 5000, 5000),
    orientation="frontal",
    thickness=2000,
)
```

### 2D Heatmaps (matplotlib)

```python
f = bgh.Heatmap(
    values,
    position=8000,
    orientation="frontal",
    thickness=1000,
    format="2D",
    title="Frontal View",
    vmin=-5, vmax=3,
    cmap="Reds",
    annotate_regions=True,       # True, or list ["VIS", "HIP"], or dict {"VIS": "V1"}
).show(xlabel="ML (µm)", ylabel="DV (µm)")
```

### 3D Heatmaps (brainrender)

```python
bgh.Heatmap(
    values,
    position=(8000, 5000, 5000),
    orientation="frontal",
    thickness=2000,
    format="3D",
    cmap="viridis",
).show()
```

### Custom Orientations

```python
# Standard orientations
bgh.Heatmap(values, orientation="sagittal", position=5000, ...)
bgh.Heatmap(values, orientation="horizontal", position=4000, ...)

# Custom orientation via normal vector
bgh.Heatmap(values, orientation=(1, 1, 0), position=(8000, 5000, 5000), ...)
```

### Using Other Atlases

```python
# Works with any brainglobe atlas
bgh.Heatmap(
    values,
    position=None,               # center of brain
    orientation="sagittal",
    thickness=1000,
    atlas_name="mpin_zfish_1um",  # zebrafish atlas
    format="2D",
    title="Zebrafish Heatmap"
).show()
```

### Getting Region Coordinates

```python
regions = ["TH", "RSP", "AI", "SS", "MO", "VIS", "HIP"]
coordinates = bgh.get_structures_slice_coords(
    regions,
    position=(8000, 5000, 5000),
    orientation="frontal",
)
```

---

## Troubleshooting & Online Resources

### Search Priority Order

1. **BrainGlobe Docs**: https://brainglobe.info/documentation/brainglobe-heatmap/index.html
2. **GitHub Issues**: https://github.com/brainglobe/brainglobe-heatmap/issues
3. **BrainGlobe Forum**: https://forum.image.sc/tag/brainglobe
4. **General Web Search**: `"brainglobe-heatmap" <error or topic>`

### Common Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Region not visible in slice | `"position" "thickness" brainglobe-heatmap` | Docs |
| Region acronym not found | `"region" "acronym" atlas brainglobe` | Atlas API docs |
| Blank 2D plot | `"matplotlib" "show" brainglobe-heatmap` | GitHub Issues |
| Wrong atlas | `"atlas_name" brainglobe-heatmap` | Docs |
| Colormap range issues | `"vmin" "vmax" "cmap" brainglobe-heatmap` | Docs |
