---
name: morphapi
description: Guide for using morphapi to download and visualize neuronal morphological reconstructions from public databases. Use when the user mentions morphapi, neuron morphology, neuronal reconstruction, SWC files, dendrite visualization, axon morphology, Allen Cell Types, neuromorpho, MouseLight, neuron 3D rendering, or wants to download neuron morphology data from Allen Brain Atlas Cell Types database, neuromorpho.org, Janelia MouseLight, or Kunst zebrafish neuron datasets and render them in 3D with brainrender.
---

# morphapi — Neuronal Morphology Downloads & Visualization

morphapi downloads neuronal morphological reconstructions from publicly available databases and creates 3D meshes for visualization with brainrender. It wraps multiple neuron morphology databases under a unified API.

**Package**: `pip install morphapi`  
**Docs**: https://brainglobe.info/documentation/morphapi/index.html  
**GitHub**: https://github.com/brainglobe/morphapi

---

## Installation

```bash
pip install morphapi
# Or via brainglobe meta-package:
pip install brainglobe
```

## Supported Databases

| Database | API Class | Description |
|----------|-----------|-------------|
| [Allen Cell Types](https://celltypes.brain-map.org/) | `AllenMorphology` | Mouse brain cell type morphologies |
| [neuromorpho.org](https://neuromorpho.org/) | `NeuroMorphoAPI` | 200k+ neurons across species |
| [Janelia MouseLight](https://www.janelia.org/project-team/mouselight) | `MouseLightAPI` | Full mouse brain neuron tracings |
| [Kunst et al. 2019](https://mapzebrain.org) | `MpinMorphologyAPI` | Zebrafish neuron morphologies |

## Usage

### Downloading from Allen Cell Types

```python
from morphapi.api.allenmorphology import AllenMorphology

api = AllenMorphology()

# Get all available neurons metadata
neurons = api.neurons

# Download specific neurons by ID
morphology = api.download_neurons(ids=[485909730, 529766780])
```

### Downloading from MouseLight

```python
from morphapi.api.mouselight import MouseLightAPI

api = MouseLightAPI()

# Get available neurons
neurons_metadata = api.fetch_neurons_metadata()

# Download first 5 neurons
neurons = api.download_neurons(neurons_metadata[:5])
```

### Downloading from neuromorpho.org

```python
from morphapi.api.neuromorpho import NeuroMorphoAPI

api = NeuroMorphoAPI()

# Search for neurons
metadata = api.get_neurons_metadata(
    species="mouse",
    brain_region="hippocampus",
    cell_type="pyramidal",
    size=10
)

# Download
neurons = api.download_neurons(metadata)
```

### Rendering with brainrender

```python
from brainrender import Scene
from morphapi.api.mouselight import MouseLightAPI

scene = Scene()
api = MouseLightAPI()

neurons_meta = api.fetch_neurons_metadata(
    filterby="soma",
    filter_regions=["VIS"]
)

neurons = api.download_neurons(neurons_meta[:3])
scene.add(*neurons)
scene.render()
```

---

## Troubleshooting & Online Resources

### Search Priority Order

1. **BrainGlobe Docs**: https://brainglobe.info/documentation/morphapi/index.html
2. **GitHub Issues**: https://github.com/brainglobe/morphapi/issues
3. **BrainGlobe Forum**: https://forum.image.sc/tag/brainglobe
4. **General Web Search**: `"morphapi" brainglobe <error or topic>`

### Common Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Download fails / timeout | `"download" "timeout" morphapi` | GitHub Issues |
| API authentication error | `"API" "key" morphapi Allen` | GitHub Issues |
| SWC file parsing error | `"SWC" "parse" morphapi neurom` | GitHub Issues |
| Mesh rendering issues | `"mesh" "vedo" morphapi brainrender` | GitHub Issues |
| neuromorpho.org unavailable | `"neuromorpho" "connection" morphapi` | GitHub Issues |
