---
name: antspy
description: Guide for using ANTsPy (Advanced Normalization Tools in Python) for medical image analysis including registration, segmentation, visualization, bias correction, cortical thickness, and image I/O. Use this skill whenever the user mentions ANTsPy, ANTs, medical image registration, brain image processing, SyN registration, diffeomorphic registration, N4 bias correction, Atropos segmentation, cortical thickness estimation, NIfTI image processing, or wants to align/warp/register medical images. Also use when the user needs to work with ANTsImage objects, apply transforms, create deformation fields, perform atlas-based segmentation, or generate publication-quality neuroimaging visualizations. Trigger even for generic medical imaging tasks where ANTs methods would be appropriate.
---

# ANTsPy — Advanced Normalization Tools in Python

ANTsPy is a Python library wrapping the well-established C++ ANTs biomedical image processing framework. It provides blazing-fast I/O for medical images, state-of-the-art registration (including SyN diffeomorphic), segmentation (Atropos, joint label fusion), bias correction (N3/N4), cortical thickness (DiReCT), statistical learning, and publication-ready visualization.

**Package**: `pip install antspyx` (or `conda install conda-forge::antspyx`)  
**Import**: `import ants`  
**Docs**: https://antspy.readthedocs.io  
**GitHub**: https://github.com/ANTsX/ANTsPy  
**Deep learning companion**: [ANTsPyNet](https://github.com/ANTsX/ANTsPyNet)

---

## Table of Contents

1. [Installation](#installation)
2. [Core Concepts](#core-concepts)
3. [Image I/O & Properties](#image-io--properties)
4. [Registration](#registration)
5. [Applying Transforms](#applying-transforms)
6. [Segmentation](#segmentation)
7. [Bias Correction](#bias-correction)
8. [Cortical Thickness](#cortical-thickness)
9. [Utilities](#utilities)
10. [Visualization](#visualization)
11. [Statistical Learning](#statistical-learning)
12. [Numpy Interop](#numpy-interop)
13. [Common Workflows](#common-workflows)
14. [Troubleshooting & Online Resources](#troubleshooting--online-resources)

---

## Installation

```bash
# Pre-compiled (recommended)
pip install antspyx

# Or via conda
conda install conda-forge::antspyx

# Mac OS compatibility fix (if pip fails to find binary)
SYSTEM_VERSION_COMPAT=0 pip install antspyx

# Windows: requires Microsoft Visual C++ Redistributable

# Build from source
git clone https://github.com/antsx/antspy
cd antspy
python -m pip install .
```

---

## Core Concepts

### ANTsImage
The fundamental data type. Wraps a C++ ITK image with metadata (spacing, origin, direction, pixel type, dimensions).

```python
import ants

# Built-in test data
img = ants.image_read(ants.get_ants_data('r16'))     # 2D brain slice
img = ants.image_read(ants.get_ants_data('mni'))      # 3D MNI template
img = ants.image_read(ants.get_ants_data('r64'))      # another 2D brain

# Properties (pythonic access)
img.spacing        # tuple, e.g. (1.0, 1.0, 1.0)
img.origin         # tuple
img.direction      # numpy array
img.shape          # tuple of dimensions
img.components     # number of components (1 for scalar)
img.pixeltype      # 'float', 'unsigned int', etc.
img.dimension      # int: 2 or 3

# Set properties
img.set_spacing((2.0, 2.0, 2.0))
img.set_origin((0, 0, 0))
img.set_direction(np.eye(3))
```

### Naming Convention (ANTsR → ANTsPy)
- camelCase → underscore_case: `resampleImage` → `resample_image`
- Remove `ants`/`antsr` prefix: `antsImageRead` → `ants.image_read`

---

## Image I/O & Properties

```python
import ants

# Reading (supports NIfTI, NRRD, MHA, DICOM dir, etc.)
img = ants.image_read('path/to/image.nii.gz')
img = ants.image_read('path/to/image.nii.gz', dimension=3)
img = ants.image_read('path/to/image.nii.gz', pixeltype='float')
img = ants.dicom_read('path/to/dicom_directory/')

# Writing
ants.image_write(img, 'output.nii.gz')

# Clone
img_copy = img.clone()
img_copy = ants.image_clone(img)

# Image info
print(img)  # summary: dimensions, spacing, origin, direction, pixel type
ants.image_header_info('path/to/image.nii.gz')  # read header without loading

# Resampling
img_resampled = ants.resample_image(img, (128, 128, 128), use_voxels=True, interp_type=0)
# interp_type: 0=linear, 1=nearest-neighbor, 2=gaussian, 3=windowed sinc, 4=bspline
img_resampled = ants.resample_image_to_target(img, target_img)

# Create from scratch
img_new = ants.make_image((100, 100), voxval=0)
```

---

## Registration

The crown jewel of ANTs. `ants.registration()` provides a unified interface for linear and nonlinear registration.

### Quick Registration

```python
import ants

fixed = ants.image_read(ants.get_ants_data('r16'))
moving = ants.image_read(ants.get_ants_data('r64'))

# Basic SyN (recommended default for deformable registration)
result = ants.registration(
    fixed=fixed,
    moving=moving,
    type_of_transform='SyN'
)

# Result is a dict:
# result['warpedmovout']   - moving image warped to fixed space
# result['warpedfixout']   - fixed image warped to moving space
# result['fwdtransforms']  - list of forward transform filenames
# result['invtransforms']  - list of inverse transform filenames
```

### Transform Types Reference

| Type | Description | Stages |
|------|-------------|--------|
| `Translation` | Translation only | 1 |
| `Rigid` | Rotation + translation | 1 |
| `Similarity` | Uniform scaling + rotation + translation | 1 |
| `QuickRigid` | Quick rigid for visualization | 1 |
| `DenseRigid` | Rigid with dense sampling | 1 |
| `Affine` | Rigid + scaling + shear (12 params) | 1 |
| `AffineFast` | Fast affine | 1 |
| `ElasticSyN` | Affine + deformable (elastic regularization) | 2 |
| `SyN` | Symmetric normalization (MI metric) | 3 |
| `SyNRA` | Rigid + Affine + SyN | 3 |
| `SyNOnly` | SyN without rigid/affine stages | 1 |
| `SyNCC` | SyN with cross-correlation metric | 3 |
| `SyNAggro` | SyN with aggressive deformation | 3 |
| `SyNBold` | SyN for BOLD-to-T1 registration | 3 |
| `BOLDRigid` | Rigid for BOLD intrasubject | 1 |
| `BOLDAffine` | Affine for BOLD intrasubject | 1 |
| `TRSAA` | Translation→rigid→similarity→affine (×2) | 5 |
| `TV[n]` | Time-varying diffeomorphism (n time points) | 1 |
| `antsRegistrationSyN[x]` | Full ANTs pipeline (t/r/a/s/sr/so/b/br/bo) | varies |
| `antsRegistrationSyNQuick[x]` | Quick version of above | varies |

**antsRegistrationSyN codes**: t=translation, r=rigid, a=rigid+affine, s=rigid+affine+SyN, sr=rigid+SyN, so=SyN only, b/br/bo=B-spline variants

### Advanced Registration Parameters

```python
result = ants.registration(
    fixed=fixed,
    moving=moving,
    type_of_transform='SyN',
    # Affine stage
    aff_metric='mattes',           # GC, mattes, meansquares
    aff_sampling=32,               # MI bins
    aff_random_sampling_rate=0.2,  # fraction of points
    aff_iterations=(2100, 1200, 1200, 10),
    aff_shrink_factors=(6, 4, 2, 1),
    aff_smoothing_sigmas=(3, 2, 1, 0),
    # SyN stage
    syn_metric='CC',               # CC, mattes, meansquares, demons
    syn_sampling=4,                # CC radius or MI bins
    reg_iterations=(100, 70, 50, 0),
    grad_step=0.2,
    flow_sigma=3,
    total_sigma=0,
    # Masks
    mask=fixed_mask,               # in fixed space
    moving_mask=moving_mask,       # in moving space
    mask_all_stages=True,
    # Options
    initial_transform='Identity',  # or list of transform files
    verbose=True,
    write_composite_transform=False,
    singleprecision=True,          # for large datasets
)
```

### Multi-Metric Registration

```python
result = ants.registration(
    fixed=fixed,
    moving=moving,
    type_of_transform='SyNOnly',
    multivariate_extras=[
        ('MeanSquares', fixed2, moving2, 0.5, 0),
        ('CC', fixed3, moving3, 0.5, 2)
    ]
)
```

### Affine Initializer

```python
# Multi-start optimizer to find good initial alignment
txfile = ants.affine_initializer(fixed, moving)
tx = ants.read_transform(txfile, dimension=2)
```

---

## Applying Transforms

```python
import ants

# Apply forward transforms (moving → fixed space)
warped = ants.apply_transforms(
    fixed=fixed,
    moving=moving,
    transformlist=result['fwdtransforms']
)

# Apply inverse transforms (fixed → moving space)
warped_inv = ants.apply_transforms(
    fixed=moving,
    moving=fixed,
    transformlist=result['invtransforms']
)

# Interpolation options
warped = ants.apply_transforms(
    fixed=fixed,
    moving=moving,
    transformlist=result['fwdtransforms'],
    interpolator='nearestNeighbor'  # for label images
)
# Interpolators: linear, nearestNeighbor, genericLabel (for labels),
#   gaussian, bSpline, cosineWindowedSinc, lanczosWindowedSinc

# Apply to label images
warped_labels = ants.apply_transforms(
    fixed=fixed,
    moving=label_img,
    transformlist=result['fwdtransforms'],
    interpolator='genericLabel'
)

# Compose transforms
composite_file = ants.apply_transforms(
    fixed=fixed,
    moving=moving,
    transformlist=result['fwdtransforms'],
    compose='/tmp/composite_transform'
)

# Jacobian determinant (measure of local volume change)
jac = ants.create_jacobian_determinant_image(
    domain_image=fixed,
    tx=result['fwdtransforms'][0],  # warp field
    do_log=True                      # log Jacobian
)

# Warped grid visualization
grid = ants.create_warped_grid(
    image=moving,
    grid_step=10,
    grid_width=2,
    transform=result['fwdtransforms'],
    fixed_reference_image=fixed
)
```

### Transform I/O

```python
# Read/write transforms
tx = ants.read_transform('transform.mat')
ants.write_transform(tx, 'output.mat')

# Transform properties
tx.dimension
tx.precision     # 'float' or 'double'
tx.transform_type
tx.parameters
tx.fixed_parameters

# Apply a transform to a point
transformed_point = tx.apply_to_point((10.0, 20.0, 30.0))
```

---

## Segmentation

### Atropos (Finite Mixture Model)

```python
import ants

img = ants.image_read(ants.get_ants_data('r16'))
img = ants.resample_image(img, (64, 64), 1, 0)
mask = ants.get_mask(img)

# K-Means initialization
seg = ants.atropos(
    a=img,                # image(s) to segment (can be list for multivariate)
    m='[0.2,1x1]',        # MRF: [smoothing, neighborhood]
    c='[2,0]',            # convergence: [iterations, threshold]
    i='kmeans[3]',        # initialization: kmeans with 3 classes
    x=mask                # mask
)

# Result dict:
# seg['segmentation']        - segmentation image
# seg['probabilityimages']   - list of probability images per class

# Re-segment using prior probabilities
seg2 = ants.atropos(
    a=img,
    m='[0.2,1x1]',
    c='[2,0]',
    i=seg['probabilityimages'],   # use prior probabilities
    x=mask,
    priorweight=0.25
)
```

### K-Means Segmentation (Wrapper)

```python
seg = ants.kmeans_segmentation(img, k=3, kmask=mask, mrf=0.1)
# Returns dict with 'segmentation' and 'probabilityimages'
```

### Fuzzy Spatial C-Means

```python
seg = ants.fuzzy_spatial_cmeans_segmentation(
    image=img,
    mask=mask,
    number_of_clusters=3,
    m=2,       # fuzziness
    p=1,       # membership importance
    q=1,       # spatial constraint (0 = conventional FCM)
    radius=1,
    max_number_of_iterations=20,
    convergence_threshold=0.02
)
```

### Joint Label Fusion (Multi-Atlas)

```python
# Register atlases to target, then fuse labels
pp = ants.joint_label_fusion(
    target_image=ref,
    target_image_mask=refmask,
    atlas_list=registered_atlas_images,   # list of ANTsImages
    label_list=registered_label_images,   # list of label ANTsImages
    r_search=2,
    rad=[2] * ref.dimension,
    beta=2,
    verbose=True
)
# Returns dict with 'segmentation', 'intensity', 'probabilityimages'
```

### Cortical Thickness (DiReCT / Kelly Kapowski)

```python
# Requires segmentation with GM and WM probability maps
segs = ants.kmeans_segmentation(img, k=3, kmask=mask)
thick = ants.kelly_kapowski(
    s=segs['segmentation'],
    g=segs['probabilityimages'][1],   # gray matter
    w=segs['probabilityimages'][2],   # white matter
    its=45,      # iterations
    r=0.5,       # gradient descent parameter
    m=1          # smoothing parameter
)
```

---

## Bias Correction

```python
import ants

img = ants.image_read(ants.get_ants_data('r16'))

# N4 Bias Field Correction (recommended)
img_corrected = ants.n4_bias_field_correction(
    image=img,
    mask=None,                # optional mask
    shrink_factor=4,          # multi-resolution (typically 2-4)
    convergence={'iters': [50, 50, 30, 20], 'tol': 1e-7},
    spline_param=200,         # B-spline spacing
    rescale_intensities=False,
    return_bias_field=False,
    verbose=False
)

# Get the bias field instead
bias_field = ants.n4_bias_field_correction(img, return_bias_field=True)

# N3 Bias Field Correction (legacy)
img_n3 = ants.n3_bias_field_correction(img, downsample_factor=3)

# ABP N4: truncate outliers + N4 in one step
img_abp = ants.abp_n4(img, intensity_truncation=(0.025, 0.975, 256))
```

---

## Utilities

### Masking

```python
mask = ants.get_mask(img)
mask = ants.get_mask(img, low_thresh=img.mean(), cleanup=2)

# Morphological operations on masks
mask_dilated = ants.morphology(mask, operation='dilate', radius=2, mtype='binary')
mask_eroded = ants.morphology(mask, operation='erode', radius=1, mtype='binary')
mask_closed = ants.morphology(mask, operation='close', radius=3, mtype='binary')
mask_opened = ants.morphology(mask, operation='open', radius=2, mtype='binary')
# Also works as method: img.morphology(...)
```

### Image Math (iMath)

```python
# General-purpose image mathematics
img_normalized = ants.iMath(img, 'Normalize')          # [0,1] normalization
img_truncated = ants.iMath(img, 'TruncateIntensity', 0.025, 0.975)
img_sharp = ants.iMath(img, 'Sharpen')
img_padded = ants.iMath(img, 'PadImage', 10)

# Morphological via iMath
mask_dilated = ants.iMath(mask, 'MD', 2)    # Dilate
mask_eroded = ants.iMath(mask, 'ME', 2)     # Erode
mask_closed = ants.iMath(mask, 'MC', 2)     # Close
mask_opened = ants.iMath(mask, 'MO', 2)     # Open

# Distance map
dmap = ants.iMath(mask, 'MaurerDistance')

# Fill holes
filled = ants.iMath(mask, 'FillHoles')

# Get largest component
largest = ants.iMath(mask, 'GetLargestComponent')

# Gradient computation
grad = ants.iMath(img, 'Grad', 1.0)

# Laplacian
lap = ants.iMath(img, 'Laplacian', 1.0, 1)

# Canny edge detection
edges = ants.iMath(img, 'Canny', 1, 5, 2)
```

### Image Operations

```python
# Thresholding
binary = ants.threshold_image(img, low_thresh=100, high_thresh=200)
otsu = ants.threshold_image(img, 'Otsu', 3)    # Otsu with 3 classes

# Smoothing
smoothed = ants.smooth_image(img, sigma=2)
smoothed = ants.smooth_image(img, sigma=2, sigma_in_physical_coordinates=True)

# Cropping
cropped = ants.crop_image(img)                      # crop to non-zero region
cropped = ants.crop_image(img, label_image=mask)     # crop to mask bounding box
cropped = ants.crop_indices(img, (10, 10, 10), (100, 100, 100))

# Padding
padded = ants.pad_image(img, pad_width=[(10, 10), (10, 10), (10, 10)])

# Histogram matching
matched = ants.histogram_match_image(source_img, reference_img)
matched2 = ants.histogram_match_image2(source_img, reference_img)

# Denoise
denoised = ants.denoise_image(img, mask=mask)

# Image similarity
mi = ants.image_mutual_information(img1, img2)

# Label statistics
stats = ants.label_stats(img, label_img)

# Multi-channel
merged = ants.merge_channels([img1, img2, img3])
channels = ants.split_channels(merged)

# Weingarten shape
shape = ants.weingarten_image_curvature(img)
```

---

## Visualization

```python
import ants

img = ants.image_read(ants.get_ants_data('mni'))

# Basic plot (3D images shown as multi-slice montage)
ants.plot(img)

# With overlay
ants.plot(img, overlay=img > img.mean(), overlay_alpha=0.5)

# Customized
ants.plot(
    img,
    overlay=seg_img,
    cmap='gray',
    overlay_cmap='jet',
    overlay_alpha=0.4,
    axis=2,              # 0=sagittal, 1=coronal, 2=axial
    nslices=12,
    ncol=4,
    title='Brain Segmentation',
    black_bg=True,
    filename='output.png',
    dpi=300,
    crop=True
)

# Specific slices
ants.plot(img, slices=(0.3, 0.4, 0.5, 0.6, 0.7))   # relative positions
ants.plot(img, slices=(80, 100, 120))                  # absolute indices

# Ortho view (all three planes)
ants.plot_ortho(img, flat=True)
ants.plot_ortho(img, overlay=overlay_img, reorient=True)

# Plot directory of images
ants.plot_directory('path/to/images/', overlay_alpha=0.5)
```

---

## Statistical Learning

### Sparse CCA (Canonical Correlation)

```python
import ants
import numpy as np

# Sparse CCA between two matrices
result = ants.sparse_decom2(
    inmatrix=(mat1, mat2),   # n×p and n×q
    sparseness=(0.01, 0.1),   # sparseness per view
    nvecs=3,                   # number of components
    its=20,                    # iterations
    cthresh=(0, 0),
    perms=0                    # set >0 for significance testing
)
```

### Eigen-Image Decomposition

```python
# PCA-like decomposition of image matrix
result = ants.sparse_decom(
    inmatrix=mat,
    inmask=mask,
    sparseness=-0.1,    # negative = keep this fraction
    nvecs=5,
    its=10
)
```

---

## Numpy Interop

Conversions are instantaneous (zero-copy via shared memory buffers).

```python
import ants
import numpy as np

img = ants.image_read(ants.get_ants_data('mni'))

# ANTsImage → numpy
arr = img.numpy()          # returns ndarray (no copy)
arr = img.numpy(single=True)  # force float32

# numpy → ANTsImage
new_img = ants.from_numpy(arr)                          # no metadata
new_img = ants.from_numpy(arr, spacing=img.spacing,
                           origin=img.origin,
                           direction=img.direction)    # with metadata
new_img = img.new_image_like(arr * 2)                  # copy metadata from img

# Indexing (returns images)
slice_img = img[100, :, :]        # get a 2D slice
img[50, :, :] = 1                 # set values

# Arithmetic (operator overloading)
result = img + img2
result = img - img2
result = img * 2
result = img > img.mean()
```

---

## Common Workflows

### Brain Registration Pipeline

```python
import ants

template = ants.image_read('MNI152_T1_1mm_brain.nii.gz')
subject = ants.image_read('subject_T1.nii.gz')

# 1. Bias correction
subject_n4 = ants.n4_bias_field_correction(subject, shrink_factor=4)

# 2. Brain extraction (use mask or ANTsPyNet)
mask = ants.get_mask(subject_n4)
brain = subject_n4 * mask

# 3. Register to template
reg = ants.registration(
    fixed=template,
    moving=brain,
    type_of_transform='SyN',
    syn_metric='CC',
    syn_sampling=4,
    reg_iterations=(100, 70, 50, 20),
    verbose=True
)

# 4. Apply to other modalities
warped_flair = ants.apply_transforms(
    fixed=template,
    moving=flair_img,
    transformlist=reg['fwdtransforms']
)

# 5. Visualize result
ants.plot(template, overlay=reg['warpedmovout'], overlay_alpha=0.4)
```

### Multi-Atlas Label Propagation

```python
import ants

target = ants.image_read('target.nii.gz')
target = ants.iMath(target, 'Normalize')
target_mask = ants.get_mask(target)

# Register each atlas to target
atlas_images = []
label_images = []
for atlas_path, label_path in zip(atlas_paths, label_paths):
    atlas = ants.iMath(ants.image_read(atlas_path), 'Normalize')
    labels = ants.image_read(label_path)
    
    reg = ants.registration(fixed=target, moving=atlas, type_of_transform='SyN')
    
    atlas_images.append(ants.apply_transforms(
        fixed=target, moving=atlas, transformlist=reg['fwdtransforms']))
    label_images.append(ants.apply_transforms(
        fixed=target, moving=labels, transformlist=reg['fwdtransforms'],
        interpolator='genericLabel'))

# Fuse labels
result = ants.joint_label_fusion(
    target_image=target,
    target_image_mask=target_mask,
    atlas_list=atlas_images,
    label_list=label_images,
    r_search=2,
    rad=[2] * target.dimension
)
```

### Longitudinal Processing

```python
import ants

# Register timepoint 2 to timepoint 1
reg = ants.registration(
    fixed=tp1_img,
    moving=tp2_img,
    type_of_transform='SyN'
)

# Compute Jacobian to measure volume change
jac = ants.create_jacobian_determinant_image(
    domain_image=tp1_img,
    tx=reg['fwdtransforms'][0],
    do_log=True
)
# Positive log-Jacobian = expansion, negative = contraction
```

---

## Troubleshooting & Online Resources

When you encounter issues with ANTsPy, follow this search order to find solutions quickly. This section guides you on *where* and *what* to search.

### Search Priority Order

1. **Official ANTsPy Docs**: https://antspy.readthedocs.io/en/latest/
2. **ANTsPy GitHub Issues**: https://github.com/ANTsX/ANTsPy/issues
3. **ANTsPy Wiki**: https://github.com/ANTsX/ANTsPy/wiki
4. **ANTs (C++) Documentation**: https://github.com/ANTsX/ANTs/wiki (the underlying algorithms)
5. **ANTsR Documentation**: https://antsx.github.io/ANTsR/ (R counterpart, same algorithms)
6. **Stack Overflow**: Search `[antspy]` or `[ants] python`
7. **Neurostars Forum**: https://neurostars.org (search "ANTs" or "ANTsPy")
8. **General Web Search**: `"ANTsPy" <error message or topic>`

### Common Issues & What to Search

#### Installation Failures

| Problem | Search Query | Where |
|---------|-------------|-------|
| Mac pip can't find wheel | `"SYSTEM_VERSION_COMPAT" ANTsPy` | GitHub Wiki |
| Build from source fails | `"build from source" ANTsPy <OS>` | GitHub Issues |
| Windows DLL errors | `"Microsoft Visual C++ Redistributable" ANTsPy` | GitHub Issues |
| Conda conflicts | `"conda install antspyx" conflict` | GitHub Issues |
| Version mismatch | `"python version" ANTsPy wheel` → check [Releases](https://github.com/ANTsX/ANTsPy/releases) | GitHub |

**Quick fix**: `SYSTEM_VERSION_COMPAT=0 pip install antspyx` (Mac). Windows: install [VC++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist).

#### Registration Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Registration fails / poor results | `"registration quality" OR "poor registration" ANTsPy` | GitHub Issues, Neurostars |
| Choosing transform type | `"type_of_transform" SyN comparison ANTsPy` | Docs, GitHub Wiki |
| Out of memory | `"out of memory" OR "singleprecision" ANTsPy registration` | GitHub Issues |
| Slow registration | `"performance" OR "speed" ANTsPy registration` | GitHub Issues |
| Transform file formats | `"transform file" ".mat" ".nii.gz" ANTsPy` | Docs |
| Registration crashes (segfault) | `"segmentation fault" OR "crash" ANTsPy registration` | GitHub Issues |
| Multi-modal registration | `"multivariate" OR "multi-metric" ANTsPy` | Docs, Tutorials |

**Troubleshooting tips**:
- Always try `verbose=True` to see what's happening
- Start with simpler transforms (Rigid → Affine → SyN)
- Use `singleprecision=True` for large 3D datasets
- Ensure both images are in the same orientation
- Try `ants.resample_image()` to reduce resolution for testing

#### Segmentation Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Atropos poor results | `"atropos" parameters tuning ANTs` | Neurostars, ANTs Wiki |
| MRF parameter tuning | `"MRF" "smoothing" atropos ANTs` | ANTs Wiki |
| K-means init issues | `"kmeans" initialization atropos` | GitHub Issues |
| Joint label fusion slow | `"ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS" ANTsPy` | Docs |

#### Image I/O Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Can't read DICOM | `"dicom_read" ANTsPy` | Docs, GitHub Issues |
| NIfTI header issues | `"header" "orientation" ANTsPy nifti` | GitHub Issues |
| Spacing/origin wrong | `"spacing" "origin" ANTsPy image_read` | Docs |
| Memory issues with large files | `"memory" "large image" ANTsPy` | GitHub Issues |

#### Visualization Issues

| Problem | Search Query | Where |
|---------|-------------|-------|
| Plot not showing | `"matplotlib backend" ANTsPy plot` | Stack Overflow |
| Overlay alignment | `"plot overlay" alignment ANTsPy` | GitHub Issues |
| Save to file | `"filename" "dpi" ANTsPy plot` | Docs |

### Environment Variables

```bash
# Control ITK threading for parallel operations
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8

# Mac OS compatibility
export SYSTEM_VERSION_COMPAT=0

# For headless servers (visualization)
import matplotlib
matplotlib.use('Agg')
```

### Getting Help

If the documentation and search do not resolve your issue:

1. **Check version**: `ants.__version__` — ensure you're on a recent release
2. **Minimal reproducer**: Create a small example with built-in data (`ants.get_ants_data()`)
3. **File an issue**: https://github.com/ANTsX/ANTsPy/issues/new with:
   - Python version, OS, ANTsPy version
   - Full traceback
   - Minimal reproducing code
4. **Community resources**:
   - [ANTsX ecosystem examples](https://gist.github.com/ntustison/12a656a5fc2f6f9c4494c88dc09c5621/)
   - [ANTs Google Scholar](https://scholar.google.com/scholar?q=advanced+normalization+tools+ants+image+registration) for methodology papers
   - ANTsPyNet for deep learning extensions: https://github.com/ANTsX/ANTsPyNet
