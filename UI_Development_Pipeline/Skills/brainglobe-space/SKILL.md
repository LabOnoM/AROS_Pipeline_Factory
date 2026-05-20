---
name: brainglobe-space
description: Guide for using brainglobe-space to define and transform between anatomical coordinate spaces. Use when the user mentions brainglobe-space, anatomical space, brain orientation, coordinate space transformation, atlas orientation, anatomical axes, brain stack orientation, reorientation of brain images, or needs to convert brain image stacks or point coordinates between different anatomical orientations (e.g., ASL to IPR). Also covers the AnatomicalSpace class for resolution/offset-aware transformations.
---

# brainglobe-space — Anatomical Coordinate Space Transformations

brainglobe-space defines anatomical spaces and transforms image stacks and point coordinates between different orientations. It handles axes swaps, flips, resolution changes, and offsets using only numpy index operations (no affine image transforms).

**Package**: `pip install brainglobe-space`  
**Import**: `import brainglobe_space as bgs`  
**Docs**: https://brainglobe.info/documentation/brainglobe-space/index.html  
**GitHub**: https://github.com/brainglobe/brainglobe-space

---

## Installation

```bash
pip install brainglobe-space
# Or via brainglobe meta-package:
pip install brainglobe
```

## Quick Start

```python
import brainglobe_space as bgs
import numpy as np

# Define orientations as direction tuples or 3-letter codes
source = ("Left", "Superior", "Anterior")  # or "lsa"
target = ("Inferior", "Posterior", "Right")  # or "ipr"

# Transform a stack between spaces
stack = np.random.rand(3, 2, 4)
mapped = bgs.map_stack_to("lsa", "ipr", stack)
```

## Orientation Codes

Three-letter codes define the origin of the image stack:

| Letter | Axis Direction |
|--------|---------------|
| `a` | Anterior |
| `p` | Posterior |
| `s` | Superior |
| `i` | Inferior |
| `l` | Left |
| `r` | Right |

The origin is the upper-left corner when viewing `stack[0, :, :]`.

## AnatomicalSpace Class

For transforming both stacks AND point coordinates:

```python
import brainglobe_space as bgs
import numpy as np

stack = np.random.rand(3, 2, 4)
points = np.array([[0, 0, 0], [2, 1, 3]])

source_space = bgs.AnatomicalSpace("lsa", stack.shape)

# Transform stack
mapped_stack = source_space.map_stack_to("ipr", stack)

# Transform points (preserves origin offset)
mapped_points = source_space.map_points_to("ipr", points)

# Get transformation matrix
target_space = bgs.AnatomicalSpace("ipr", stack.shape)
matrix = source_space.transformation_matrix_to(target_space)
```

### With Resolution and Offset

```python
source = bgs.AnatomicalSpace("asl", resolution=(2, 1, 2), offset=(1, 0, 0))
target = bgs.AnatomicalSpace("sal", resolution=(1, 1, 1), offset=(0, 0, 2))

# Affine transformation matrix including resampling
matrix = source.transformation_matrix_to(target)

# With target shape for padding/cropping
target_shaped = bgs.AnatomicalSpace("asl", resolution=(1, 1, 1), shape=(5, 4, 2))
matrix = source.transformation_matrix_to(target_shaped)
```

### Iterating Over Projections

```python
sc = bgs.AnatomicalSpace("asl")
for i, (plane, labels) in enumerate(zip(sc.sections, sc.axis_labels)):
    axs[i].imshow(stack.mean(i))
    axs[i].set_title(f"{plane.capitalize()} view")
    axs[i].set_ylabel(labels[0])
    axs[i].set_xlabel(labels[1])
```

---

## Troubleshooting & Online Resources

### Search Priority Order

1. **BrainGlobe Docs**: https://brainglobe.info/documentation/brainglobe-space/index.html
2. **GitHub Issues**: https://github.com/brainglobe/brainglobe-space/issues
3. **BrainGlobe Forum**: https://forum.image.sc/tag/brainglobe
4. **General Web Search**: `"brainglobe-space" <error or topic>`

### Common Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Wrong orientation code | `"orientation" "origin" brainglobe-space` | Docs |
| Transform matrix incorrect | `"transformation_matrix_to" brainglobe-space` | GitHub Issues |
| Resolution mismatch | `"resolution" "offset" AnatomicalSpace` | Docs |
| Point coordinates wrong | `"map_points_to" brainglobe-space` | GitHub Issues |
