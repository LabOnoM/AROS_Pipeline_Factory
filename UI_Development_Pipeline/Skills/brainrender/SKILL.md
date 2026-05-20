---
name: brainrender
description: Guide for using brainrender for 3D visualization and rendering of neuroanatomical data registered to brain atlases. Use when the user mentions brainrender, 3D brain visualization, brain region rendering, neuroanatomy visualization, brain atlas 3D rendering, creating brain visualizations, brain region meshes, or wants to visualize cells/probes/regions in 3D brain space, create animated brain videos, render brain atlas regions, or export 3D brain scenes. Also covers Scene, Actor classes, animations, and integration with BrainGlobe Atlas API.
---

# brainrender — 3D Neuroanatomy Visualization

brainrender creates publication-quality 3D visualizations of neuroanatomical data registered to a brain atlas. It renders brain regions, cells, probes, neurons, and custom data in interactive 3D scenes. Fully integrated with BrainGlobe Atlas API for multi-species support.

**Package**: `pip install brainrender`  
**Import**: `from brainrender import Scene`  
**Docs**: https://brainglobe.info/documentation/brainrender/index.html  
**GitHub**: https://github.com/brainglobe/brainrender

---

## Installation

```bash
pip install brainrender
# Or via brainglobe meta-package:
pip install brainglobe
```

## Quick Start

```python
from brainrender import Scene

# Create a scene with default atlas (Allen Mouse 25µm)
scene = Scene(title="My Brain")

# Add brain regions by acronym
scene.add_brain_region("VIS", "TH", alpha=0.3, color="salmon")

# Render interactively
scene.render()
```

## Core Concepts

### Scene

The `Scene` object is the central class. It holds all actors and handles rendering.

```python
from brainrender import Scene

# Create scene with different atlas
scene = Scene(atlas_name="allen_mouse_25um", title="Analysis")

# Scene properties
scene.atlas          # the BrainGlobeAtlas object
scene.root           # the whole-brain mesh actor

# Add regions
scene.add_brain_region("CTX", "HIP", "TH",
                       alpha=0.2,
                       color="lightblue",
                       hemisphere="right")  # "left", "right", or "both"

# Render
scene.render()          # interactive window
scene.render(zoom=1.5)  # zoomed
scene.close()
```

### Actors

Actors are 3D objects added to the scene:

```python
from brainrender import Scene
from brainrender.actors import Points, Cylinder, Line, Volume

scene = Scene()

# Cell positions (N×3 array of coordinates in atlas space)
import numpy as np
coords = np.array([[5000, 3000, 4000],
                    [5500, 3200, 3800],
                    [6000, 3100, 4200]])
cells = Points(coords, name="cells", colors="red", radius=30)
scene.add(cells)

# Probe track as cylinder
probe = Cylinder(
    pos=[5000, 1000, 5000],
    target=[5000, 6000, 5000],
    radius=50,
    color="blue"
)
scene.add(probe)

# Lines
track = Line(coords, linewidth=3, color="green")
scene.add(track)

# Volume data (3D numpy array)
vol = Volume(np.random.rand(100, 100, 100), voxel_size=25)
scene.add(vol)

scene.render()
```

### Custom Meshes and Data

```python
from brainrender import Scene
from brainrender.actors import Mesh

scene = Scene()

# Load custom mesh from file
mesh = Mesh("/path/to/mesh.obj", color="salmon", alpha=0.5)
scene.add(mesh)

# From neuron morphology (with morphapi)
from morphapi.api.mouselight import MouseLightAPI
api = MouseLightAPI()
neurons = api.get_neurons(1)  # gets morphology data
scene.add(*neurons)

scene.render()
```

## Screenshots and Videos

```python
from brainrender import Scene
from brainrender import VideoMaker

# Screenshot
scene = Scene()
scene.add_brain_region("VIS")
scene.render()
scene.screenshot(name="my_brain", scale=2)

# Animated video (camera rotation)
vm = VideoMaker(scene, save_fld="/path/to/output", name="rotation")
vm.make_video(
    azimuth=1,      # rotation per frame (degrees)
    duration=5,     # seconds
    fps=30,
)
```

## Using with Jupyter Notebooks

```python
from brainrender import Scene
from vedo import embedWindow

# Must be called before creating Scene
embedWindow('k3d')  # or 'itkwidgets'

scene = Scene()
scene.add_brain_region("VIS")
scene.render()
```

---

## Troubleshooting & Online Resources

### Search Priority Order

1. **BrainGlobe Docs**: https://brainglobe.info/documentation/brainrender/index.html
2. **GitHub Issues**: https://github.com/brainglobe/brainrender/issues
3. **BrainGlobe Forum**: https://forum.image.sc/tag/brainglobe
4. **General Web Search**: `"brainrender" brainglobe <error or topic>`

### Common Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Render window doesn't open | `"render" "display" brainrender` | GitHub Issues |
| Notebook rendering fails | `"notebook" "jupyter" brainrender embedWindow` | Docs: using-notebooks |
| Region not found | `"brain region" "acronym" brainrender` | Check atlas region list |
| Screenshot saves blank | `"screenshot" brainrender` | GitHub Issues |
| Slow rendering | `"performance" "slow" brainrender` | GitHub Issues |
| Video export fails | `"VideoMaker" brainrender` | GitHub Issues |
| VTK errors | `"VTK" "vedo" brainrender` | GitHub Issues |
| Custom mesh orientation | `"mesh" "orientation" "coordinates" brainrender` | Docs |
