---
name: brainglobe-atlasapi
description: Guide for using the BrainGlobe Atlas API (brainglobe-atlasapi) to programmatically access neuroanatomical brain atlases across species. Use when the user mentions BrainGlobe Atlas API, brain atlas, Allen Mouse Brain Atlas, atlas reference images, annotation images, brain region meshes, brain region hierarchy, atlas downloading, or wants to programmatically access neuroanatomical data for mouse, rat, zebrafish, human, or other species brain atlases. Also use when accessing brain region structures, looking up brain regions by acronym or ID, or working with atlas coordinate systems.
---

# BrainGlobe Atlas API (brainglobe-atlasapi)

A common interface for programmatically downloading and processing neuroanatomical atlas data from multiple sources. Each atlas provides: a reference image (.tiff), an annotation image with unique region IDs (.tiff), surface meshes per region (.obj), region name/hierarchy mappings (.json), and metadata (.json).

**Package**: `pip install brainglobe-atlasapi`  
**Import**: `from brainglobe_atlasapi import BrainGlobeAtlas`  
**Docs**: https://brainglobe.info/documentation/brainglobe-atlasapi/index.html  
**GitHub**: https://github.com/brainglobe/brainglobe-atlasapi

---

## Installation

```bash
pip install brainglobe-atlasapi
# Or install all BrainGlobe tools:
pip install brainglobe
```

## Quick Start

```python
from brainglobe_atlasapi import BrainGlobeAtlas

# Download and load the Allen Mouse Brain Atlas at 25µm resolution
atlas = BrainGlobeAtlas("allen_mouse_25um")

# Access the reference (template) image as numpy array
reference = atlas.reference   # 3D numpy array

# Access annotation (label) image
annotation = atlas.annotation  # 3D numpy array with region IDs

# Get info about a brain region
structure = atlas.structures["VIS"]  # by acronym
# Or by ID:
structure = atlas.structures[997]

# Get the mesh for a brain region
mesh = atlas.mesh_from_structure("VIS")

# Hemisphere data
hemisphere = atlas.hemispheres  # 3D array: 0=left, 1=right, 2=both
```

## Available Atlases (30+)

| Species | Atlas Name in API | Resolution |
|---------|------------------|------------|
| Mouse | `allen_mouse_10um`, `allen_mouse_25um`, `allen_mouse_50um`, `allen_mouse_100um` | 10-100µm |
| Mouse | `kim_mouse_10um`, `kim_mouse_25um`, `kim_mouse_50um`, `kim_mouse_100um` | 10-100µm |
| Mouse | `osten_mouse_10um`, `osten_mouse_25um`, `osten_mouse_50um`, `osten_mouse_100um` | 10-100µm |
| Mouse | `perens_lsfm_mouse_20um` | 20µm |
| Mouse | `princeton_mouse_20um` | 20µm |
| Rat | `whs_sd_rat_39um` | 39µm |
| Rat | `swc_female_rat_50um` | 50µm |
| Zebrafish | `mpin_zfish_1um` | 1µm |
| Zebrafish | `azba_zfish_4um` | 4µm |
| Human | `allen_human_500um` | 500µm |
| Spinal cord | `allen_cord_20um` | 20µm |
| Developing mouse | `admba_3d_e*`, `admba_3d_p*` | 16-25µm |

Use `brainglobe_atlasapi.list_atlases.get_all_atlases_lastversions()` for a complete list.

## Key API Methods

```python
from brainglobe_atlasapi import BrainGlobeAtlas, show_atlases

# List all available atlases
show_atlases()

# Atlas properties
atlas = BrainGlobeAtlas("allen_mouse_25um")
atlas.resolution        # tuple, e.g. (25, 25, 25) in µm
atlas.shape             # tuple of volume dimensions
atlas.orientation       # e.g. "asl" (anterior-superior-left)
atlas.metadata          # dict with species, citation, etc.
atlas.space             # AnatomicalSpace object (from brainglobe-space)

# Region lookup
atlas.structures.tree   # full hierarchy tree
atlas.structures["VIS"]          # lookup by acronym
atlas.structures[997]            # lookup by integer ID
atlas.structures.acronym_to_id   # dict mapping acronym → ID

# Get children/parent regions
children = atlas.get_structure_descendants("CTX")  # all descendants
parent = atlas.get_structure_ancestors("VIS")       # ancestors to root

# Region mask
mask = atlas.get_structure_mask("VIS")  # 3D boolean array for the region

# Meshes
mesh = atlas.mesh_from_structure("VIS")  # returns mesh file path
meshes_dict = atlas.meshfile_from_structure("VIS")

# Coordinate lookups
structure_id = atlas.structure_from_coords((100, 200, 300))
# Returns the region ID at the given atlas coordinates
```

## Command Line Interface

```bash
# List available atlases
brainglobe list

# Download a specific atlas
brainglobe install allen_mouse_25um

# Update an atlas
brainglobe update allen_mouse_25um
```

## Common Workflows

### Region Analysis

```python
from brainglobe_atlasapi import BrainGlobeAtlas
import numpy as np

atlas = BrainGlobeAtlas("allen_mouse_25um")

# Get all voxels belonging to a region
mask = atlas.get_structure_mask("VIS")
region_volume = np.sum(mask) * np.prod(atlas.resolution)  # in µm³

# Find which region a coordinate belongs to
region_id = atlas.structure_from_coords((200, 150, 300))
region_info = atlas.structures[region_id]
print(f"Region: {region_info['name']} ({region_info['acronym']})")
```

---

## Troubleshooting & Online Resources

### Search Priority Order

1. **BrainGlobe Docs**: https://brainglobe.info/documentation/brainglobe-atlasapi/index.html
2. **GitHub Issues**: https://github.com/brainglobe/brainglobe-atlasapi/issues
3. **BrainGlobe Forum**: https://forum.image.sc/tag/brainglobe
4. **BrainGlobe Zulip Chat**: https://brainglobe.zulipchat.com
5. **General Web Search**: `"brainglobe-atlasapi" <error or topic>`

### Common Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Atlas download fails | `"atlas download" brainglobe-atlasapi` | GitHub Issues |
| Atlas not found | `"atlas name" available brainglobe` | Docs (atlas list) |
| Region acronym lookup fails | `"structure" "acronym" brainglobe-atlasapi` | GitHub Issues |
| Disk space for atlases | `"disk space" "storage" brainglobe atlas` | GitHub Issues |
| Adding custom atlas | `"adding a new atlas" brainglobe` | Docs |
| Version compatibility | `"version" "compatibility" brainglobe-atlasapi` | GitHub Issues |

### Getting Help

1. Check version: `pip show brainglobe-atlasapi`
2. File an issue: https://github.com/brainglobe/brainglobe-atlasapi/issues/new
3. Community: https://forum.image.sc/tag/brainglobe
