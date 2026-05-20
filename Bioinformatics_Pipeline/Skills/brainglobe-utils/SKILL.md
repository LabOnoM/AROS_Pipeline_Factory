---
name: brainglobe-utils
description: Guide for using brainglobe-utils, a shared utility library for BrainGlobe tools providing image I/O, cell transformation, and citation generation. Use when the user mentions brainglobe-utils, BrainGlobe utilities, BrainGlobe image I/O, brainglobe image loading, cell coordinate transformation, brainmapper cell transform widget, BrainGlobe citation generation, or needs to use shared utility functions from the BrainGlobe ecosystem such as reading/writing image stacks, transforming cell coordinates, or generating citations for BrainGlobe tools.
---

# brainglobe-utils — Shared BrainGlobe Utilities

brainglobe-utils contains shared functions and classes used across the BrainGlobe ecosystem. Key user-facing features include image I/O, cell coordinate transformation, and citation generation.

**Package**: `pip install brainglobe-utils`  
**Docs**: https://brainglobe.info/documentation/brainglobe-utils/index.html  
**GitHub**: https://github.com/brainglobe/brainglobe-utils

---

## Installation

```bash
pip install brainglobe-utils
# Or via brainglobe meta-package:
pip install brainglobe
```

## Image I/O

```python
from brainglobe_utils.IO.image import load, save

# Load image stacks (TIFF, NIfTI, etc.)
stack = load.load_any("/path/to/image_or_directory")

# Load specific planes
stack = load.load_any("/path/to/tiff_series/", load_parallel=True)

# Save images
save.to_tiff(stack, "/path/to/output.tiff")
save.to_nii(stack, "/path/to/output.nii.gz")
```

## Cell Transformation Widget (napari)

A napari widget for transforming cell coordinates between sample and atlas space using brainreg registration data:

1. Open napari
2. Plugins > brainglobe-utils > Transform cells
3. Select the brainreg output directory
4. Load cell coordinates
5. Transform between sample ↔ atlas space

## Citation Generation

```python
from brainglobe_utils.citations import cite_brainglobe

# Generate citation text for BrainGlobe tools you used
citations = cite_brainglobe(
    tools=["brainreg", "cellfinder", "brainglobe-atlasapi"],
    format="bibtex"  # or "apa", "text"
)
print(citations)
```

---

## Troubleshooting & Online Resources

### Search Priority Order

1. **BrainGlobe Docs**: https://brainglobe.info/documentation/brainglobe-utils/index.html
2. **GitHub Issues**: https://github.com/brainglobe/brainglobe-utils/issues
3. **BrainGlobe Forum**: https://forum.image.sc/tag/brainglobe
4. **General Web Search**: `"brainglobe-utils" <error or topic>`

### Common Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Image loading fails | `"load" "image" brainglobe-utils` | GitHub Issues |
| Cell transform widget not showing | `"transform widget" napari brainglobe-utils` | GitHub Issues |
| Citation format | `"citation" brainglobe-utils` | Docs |
| TIFF series loading | `"tiff" "series" "parallel" brainglobe-utils` | GitHub Issues |
