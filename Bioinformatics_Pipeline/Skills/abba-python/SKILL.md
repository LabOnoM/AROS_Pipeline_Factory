---
name: abba-python
description: Guide for using ABBA Python (Aligning Big Brains & Atlases) to register serial brain tissue sections to brain atlases via Python. Use when the user mentions ABBA, abba_python, aligning big brains, brain section registration, serial section atlas registration, QuPath brain registration, Fiji brain atlas registration, brain slice to atlas alignment, DeepSlice registration, elastix brain registration, BigWarp registration, or wants to register histological brain sections (coronal, sagittal, horizontal) to reference atlases (Allen Mouse Brain, Waxholm Rat, BrainGlobe atlases) and export results to QuPath for downstream analysis.
---

# ABBA Python — Aligning Big Brains & Atlases

ABBA registers thin serial brain sections to multiple brain atlases in coronal, sagittal, or horizontal orientations. It is a Java application (Fiji plugin) with full Python API access. Supports all BrainGlobe atlases, QuPath integration for downstream analysis, and multiple registration methods (DeepSlice, Elastix, BigWarp).

**Package**: `pip install abba_python`  
**Import**: `from abba_python import abba` / `from abba_python.abba import Abba`  
**Docs**: https://abba-documentation.readthedocs.io  
**GitHub**: https://github.com/BIOP/abba_python  
**Citation**: Chiaruttini et al., Cell Reports (2025). https://doi.org/10.1016/j.celrep.2025.115876

---

## Installation

### Full Environment Setup (conda/mamba required)

```bash
# 1. Create environment with required Java dependencies
mamba create -c conda-forge -n abba-env python=3.10 openjdk=11 pip maven pyimagej
mamba activate abba-env

# 2. Install ABBA Python
pip install abba_python

# 3. For Jupyter notebooks:
pip install jupyterlab ipywidgets

# 4. (Optional) Install DeepSlice in separate environment:
mamba create -n deepslice python=3.7
mamba activate deepslice
pip install DeepSlice==1.1.5
pip install urllib3==1.26.6

# 5. Elastix/Transformix: Install separately from
#    https://github.com/SuperElastix/elastix (v5.2.0)
```

> **Warning**: The GUI does not work on macOS due to threading issues.
> **Note**: OpenJDK must be from conda-forge to avoid certificate issues.

## Quick Start

### GUI Mode

```python
from abba_python import abba

# Launch Fiji with ABBA and all BrainGlobe atlases
abba.start_imagej()
# Use ABBA within the Fiji GUI
```

### Python API (Headless / Scripted)

```python
from abba_python.abba import Abba

# Create an ABBA instance with Allen Mouse Brain Atlas
aligner = Abba(
    atlas_name="allen_mouse_25um",  # any BrainGlobe atlas name
    headless=True,
)

# Import brain section images
aligner.import_from_files(
    filepaths=["/path/to/section_001.tif", "/path/to/section_002.tif"],
    z_location=0,            # initial position in mm along cutting axis
    z_increment=0.02,        # step between slices in mm
    split_rgb=False,
)

# Select all slices for registration
aligner.select_all_slices()

# Register with DeepSlice (automated, deep-learning)
aligner.register_slices_deepslice_local(
    allow_slicing_angle_change=True,
    channels="0",
    ensemble=True,
    model="mouse",           # "mouse" or "rat"
    post_processing="Keep order + ensure regular spacing",
    px_size_micron=10.0,
    slices_spacing_micrometer=100.0,
)

# Refine with Elastix affine registration
aligner.register_slices_elastix_affine(
    channels_atlas_csv="0",
    channels_slice_csv="0",
    pixel_size_micrometer=20.0,
)

# Refine with Elastix spline (non-rigid) registration
aligner.register_slices_elastix_spline(
    channels_atlas_csv="0",
    channels_slice_csv="0",
    nb_control_points_x=5,
    pixel_size_micrometer=20.0,
)

# Wait for all tasks to complete
aligner.wait_for_end_of_tasks()

# Save state
aligner.state_save(state_file="/path/to/registration_state.json")

# Export to QuPath
aligner.export_registration_to_qupath(erase_previous_file=True)

# Close
aligner.close()
```

## Available Atlases

| Atlas | Name in API |
|-------|------------|
| Allen Mouse Brain V3 (built-in Java) | `'Adult Mouse Brain - Allen Brain Atlas V3p1'` |
| Waxholm Rat V4 (built-in Java) | `'Rat - Waxholm Sprague Dawley V4p2'` |
| Any BrainGlobe atlas | Use BrainGlobe name, e.g. `'allen_mouse_25um'`, `'mpin_zfish_1um'` |

## Key API Methods

### Configuration

```python
aligner.set_elastix_path("/path/to/elastix")
aligner.set_transformix_path("/path/to/transformix")
aligner.set_deepslice_env("/path/to/deepslice/conda/env", "1.1.5")
aligner.set_atlas_cache_dir("/path/to/atlas/cache")
aligner.print_config()
```

### Import Methods

| Method | Description |
|--------|-------------|
| `import_from_files(filepaths, z_location, z_increment)` | Import image files (Bio-Formats compatible) |
| `import_slices_from_qupath(qupath_project, ...)` | Import from QuPath project |
| `import_slices_from_quicknii(quicknii_project, ...)` | Import from QuickNII project |
| `import_slice_from_image_plus(image, slice_axis_mm)` | Import current ImageJ image |
| `import_demo_slices(demo_dataset, ...)` | Load demo brain sections |
| `state_load(state_file)` | Load previous registration state |

### Registration Methods

| Method | Description |
|--------|-------------|
| `register_slices_deepslice_local(...)` | DeepSlice deep-learning registration (local) |
| `register_slices_deepslice_web(...)` | DeepSlice via web API |
| `register_slices_elastix_affine(...)` | Elastix affine in-plane registration |
| `register_slices_elastix_spline(...)` | Elastix B-spline (non-rigid) registration |
| `register_slices_bigwarp(...)` | BigWarp manual landmark registration |
| `register_slices_copy_and_apply(model_slice_index, ...)` | Copy registration from one slice to others |
| `register_slices_edit_last(...)` | Edit last registration |
| `register_slices_remove_last()` | Undo last registration |

### Slice Management

| Method | Description |
|--------|-------------|
| `select_all_slices()` / `deselect_all_slices()` | Select/deselect all |
| `select_slices(indices)` | Select by index |
| `set_slices_selected(slices_csv)` / `set_slices_deselected(slices_csv)` | CSV-based selection |
| `get_n_slices()` | Number of imported slices |
| `rotate_slices(angle_degrees, axis_string)` | Rotate slices |
| `mirror_do(mirror_side)` / `mirror_undo()` | Mirror half-section |
| `set_slices_thickness(thickness_in_micrometer)` | Set slice thickness |
| `change_display_settings(channel_index, range_min, range_max)` | Adjust display |

### Export Methods

| Method | Description |
|--------|-------------|
| `export_registration_to_qupath(erase_previous_file)` | Export atlas regions to QuPath |
| `export_atlas_to_imagej(atlas_channels, ...)` | Export atlas as ImageJ stack |
| `export_transformed_atlas_to_imagej(...)` | Export transformed atlas |
| `export_deformation_field_to_imagej(...)` | Export deformation fields |
| `export_slices_original_data_to_imagej(...)` | Export original slice data |
| `export_slices_to_bdv(tag)` | Export to BigDataViewer |
| `export_resampled_slices_to_bdv_source(...)` | Registered slices in atlas coordinates |
| `export_slices_to_quicknii_dataset(...)` | Export to QuickNII format |
| `export_std_zip_state(...)` | Downscaled portable project for sharing |
| `state_save(state_file)` | Save registration state |

### Utility

| Method | Description |
|--------|-------------|
| `show_bdv_ui()` | Open BigDataViewer visualization |
| `wait_for_end_of_tasks()` | Wait for async operations |
| `raster_slices(interpolate, pixel_size_micrometer)` | Cache slice display |
| `generate_methods_prompt()` | Generate publication methods text |
| `close()` | Close ABBA session |

## Typical Workflow

1. **Import**: Load sections from files, QuPath project, or QuickNII
2. **Position**: Arrange slices along the atlas cutting axis
3. **DeepSlice**: Automated initial atlas-to-section alignment
4. **Elastix Affine**: Automated affine refinement
5. **Elastix Spline**: Automated non-rigid deformation
6. **BigWarp** (optional): Manual landmark-based fine-tuning
7. **Export**: Send results to QuPath, ImageJ, or BDV
8. **Save**: Persist state for reproducibility

## Integration with QuPath

ABBA is designed to work with [QuPath](https://qupath.github.io/):
1. Create a QuPath project with your serial sections
2. Import the QuPath project into ABBA: `import_slices_from_qupath(...)`
3. Register sections to atlas
4. Export back to QuPath: `export_registration_to_qupath(...)`
5. In QuPath: use atlas regions for cell detection/quantification per region

## BraiAn Integration

After ABBA registration, use [BraiAn](https://silvalab.codeberg.page/BraiAn/) in QuPath for:
- Automated whole-brain mapping analysis
- Cell counting per atlas region
- Statistical comparisons

---

## Troubleshooting & Online Resources

### Search Priority Order

1. **ABBA Documentation**: https://abba-documentation.readthedocs.io
2. **GitHub Issues**: https://github.com/BIOP/abba_python/issues
3. **image.sc Forum**: https://forum.image.sc/tag/abba (use tag `abba`)
4. **BIOP EPFL**: https://www.epfl.ch/research/facilities/ptbiop/
5. **General Web Search**: `"abba_python" OR "ABBA brain" <error or topic>`

### Common Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Java/JVM crashes | `"java" "JVM" abba_python pyimagej` | GitHub Issues |
| Certificate errors | `"certificate" openjdk conda-forge pyimagej` | pyimagej docs |
| Elastix not found | `"elastix path" abba_python` | GitHub Issues |
| DeepSlice env setup | `"deepslice" "conda" abba_python` | README |
| macOS GUI crash | `"macOS" "threading" abba_python` | README (known issue) |
| Atlas download fails | `"atlas" "download" abba_python brainglobe` | GitHub Issues |
| QuPath export fails | `"qupath" "export" abba_python` | GitHub Issues |
| Out of memory | `"memory" "java heap" abba_python` | image.sc forum |
| Headless mode issues | `"headless" abba_python` | GitHub Issues |
| State save/load errors | `"state_save" "state_load" abba_python` | GitHub Issues |
| Poor registration | `"registration quality" ABBA` | image.sc forum |

### Key Tips

- **OpenJDK version**: Use OpenJDK 11 from conda-forge (required for certificate validity)
- **Orientation**: Most common registration issue is incorrect slice orientation
- **Memory**: Java heap size can be increased via `_JAVA_OPTIONS=-Xmx16g`
- **Elastix v5.2.0**: Required specifically; other versions may not work
