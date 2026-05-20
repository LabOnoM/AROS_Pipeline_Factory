# Space Ranger CLI Reference

Comprehensive argument reference for all Space Ranger pipelines. Source: [Official Documentation](https://www.10xgenomics.com/support/software/space-ranger/latest/analysis/running-pipelines/command-line-arguments)

---

## `spaceranger count`

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--id` | Unique pipeline run identifier | `hd_count_sample1` |
| `--transcriptome` | Path to reference transcriptome | `/opt/refdata-gex-GRCh38-2020-A` |
| `--fastqs` | Path to FASTQ directory | `/data/fastqs/` |
| `--cytaimage` | Path to CytAssist image (TIFF) | `CAVG_H1-YD7CDZK_A1.tif` |

### Image Arguments (at least one required for most assays)

| Argument | Image Type | Format |
|----------|-----------|--------|
| `--image` | Brightfield microscope image | TIFF, BTF, JPEG |
| `--darkimage` | Dark background fluorescence | TIFF, BTF |
| `--colorizedimage` | Composite colored fluorescence | TIFF, BTF |

### Slide Arguments

| Argument | Description | When to Use |
|----------|-------------|-------------|
| `--slide` | Slide serial number | Always (can be auto-detected from CytAssist metadata) |
| `--area` | Capture area (A1, B1, C1, D1) | Always |
| `--slidefile` | Path to slide layout file | Offline mode |
| `--unknown-slide` | Flag for unknown slide | When slide serial is unavailable |

### Probe Set

| Argument | Description | When Required |
|----------|-------------|---------------|
| `--probe-set` | Path to probe set CSV | Visium HD (FFPE/probe-based). **NOT** for Visium HD 3' |

### Segmentation Arguments (v4.0+)

| Argument | Description | Default |
|----------|-------------|---------|
| `--nucleus-segmentation` | Enable/disable segmentation | `TRUE` (if H&E image provided) |
| `--custom-segmentation-file` | Custom nuclei mask (GeoJSON/TIFF) | — |
| `--nucleus-expansion-distance-micron` | Cell body expansion distance | **Required** with custom segmentation |
| `--max-nucleus-diameter-px` | Max expected nucleus diameter | Auto |

### Cell Annotation Arguments (v4.1+)

| Argument | Description | Values |
|----------|-------------|--------|
| `--cell-annotation-model` | Annotation model selection | `auto`, `human_pca_v1_beta`, `mouse_pca_v1_beta` |
| `--tenx-cloud-token-path` | 10x Cloud access token | Path to JSON |
| `--disable-cell-annotation` | Disable all annotation | Flag |

### Resource Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--localcores` | Number of CPU cores | All available |
| `--localmem` | Memory limit (GB) | 90% of available |
| `--create-bam` | Generate BAM file | `true` |

### Alignment

| Argument | Description |
|----------|-------------|
| `--loupe-alignment` | Path to manual alignment JSON from Loupe Browser |

---

## `spaceranger segment`

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--id` | Unique job identifier | `segment_eval` |
| `--tissue-image` | Path to H&E image | `microscope_image.tif` |

### Optional Arguments

| Argument | Description |
|----------|-------------|
| `--localcores` | CPU cores to use |
| `--localmem` | Memory limit (GB) |
| `--max-nucleus-diameter-px` | Max nucleus diameter |

### Outputs

| File | Format |
|------|--------|
| `outs/nucleus_instance_mask.tiff` | TIFF (instance mask) |
| `outs/nucleus_segmentations.geojson` | GeoJSON (polygons) |
| `outs/websummary.html` | HTML (QC report) |

---

## `spaceranger annotate`

### Required Arguments

| Argument | Description |
|----------|-------------|
| `--id` | Unique job identifier |
| `--matrix` | Path to filtered feature-barcode matrix H5 |
| `--cell-annotation-model` | Model selection (`auto`, specific model) |
| `--tenx-cloud-token-path` | 10x Cloud access token |

### Supported Data

- Visium HD (human, mouse)
- Visium HD 3' (human, mouse)
- Cell segmentation must be enabled

---

## `spaceranger aggr`

### Purpose

Combine data from multiple `spaceranger count` runs.

> **Note**: Aggregation of Visium HD data is **NOT** supported.

### Required Arguments

| Argument | Description |
|----------|-------------|
| `--id` | Unique job identifier |
| `--csv` | Path to aggregation CSV |

### Aggregation CSV Format

```csv
library_id,molecule_h5
sample1,/path/to/sample1/outs/molecule_info.h5
sample2,/path/to/sample2/outs/molecule_info.h5
```

---

## Global Options

| Argument | Description |
|----------|-------------|
| `--noexit` | Keep pipeline web UI running after completion |
| `--uiport` | Port for pipeline web UI (default: 3600) |
| `--jobmode` | Execution mode: `local`, `sge`, `lsf`, `slurm` |
| `--maxjobs` | Maximum concurrent jobs (cluster mode) |
| `--jobinterval` | Interval between job submissions (ms) |
| `--overrides` | Path to overrides JSON |
| `--help` | Show help |
| `--version` | Show version |

---

## Cloud Auth Setup

```bash
# Set up 10x Cloud token for annotate/count cell annotation
spaceranger cloud auth setup
```

This stores the token at the default location. Can be overridden with `--tenx-cloud-token-path`.
