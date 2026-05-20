---
name: gtars
description: High-performance Rust toolkit (Python bindings & CLI) for genomic interval analysis. Fast overlap queries, coverage tracks, genomic tokenization (ML), reference sequence verification, and fragment processing.
license: MIT
metadata:
    skill-author: AIPOCH/K-Dense Inc.
---
---

## Overview

Gtars is a high-performance toolkit for manipulating, analyzing, and processing genomic interval data. It provides specialized tools for overlap detection, coverage analysis, tokenization for machine learning, reference sequence management, and fragment processing.

## When to Use

Use this skill when you need:

- **Overlap and set operations on genomic intervals:** (e.g., peak/promoter overlap, variant annotation, shared-feature detection).
- **Coverage track generation:** from interval-like inputs (e.g., ATAC-seq/ChIP-seq/RNA-seq coverage for visualization in genome browsers).
- **Machine-learning preprocessing:** where genomic regions must be converted into discrete **tokens** (e.g., Transformer models, geniml pipelines).
- **Reference sequence management and verification:** (e.g., subsequence retrieval, digest calculation aligned with GA4GH refget concepts).
- **Single-cell fragment workflows:** (e.g., splitting fragments by barcode/cluster, scoring fragments against reference region sets).

## Key Features

- **Rust performance**: Fast execution with low memory overhead, designed for large genomic datasets.
- **Python bindings**: For integration into analysis notebooks and pipelines.
- **CLI tooling**: For batch processing and shell workflows.
- **Fast overlap detection**: via IGD-style indexing and interval operations.
- **Coverage track generation**: (WIG/BigWig workflows via the `uniwig` functionality).
- **Genomic tokenizers**: For ML-ready representations of genomic regions.
- **Reference sequence utilities**: (FASTA-backed stores, subsequence retrieval, digesting).
- **Fragment processing and scoring**: For common single-cell genomics tasks.

> Additional module-specific guidance is available in: `references/overlap.md`, `references/coverage.md`, `references/tokenizers.md`, `references/refget.md`, `references/python-api.md`, and `references/cli.md`.

## Installation

### Python Installation

Install gtars Python bindings:

```bash
uv uv pip install gtars
```

### CLI Installation

Install command-line tools (requires Rust/Cargo):

```bash
# Install with all features
cargo install gtars-cli --features "uniwig overlaprs igd bbcache scoring fragsplit"

# Or install specific features only
cargo install gtars-cli --features "uniwig overlaprs"
```

### Rust Library

Add to Cargo.toml for Rust projects:

```toml
[dependencies]
gtars = { version = "0.1", features = ["tokenizers", "overlaprs"] }
```

## Core Capabilities & Examples

### 1. Overlap Detection and IGD Indexing

Efficiently detect overlaps between genomic intervals using the Integrated Genome Database (IGD) data structure.

```python
import gtars

# Build IGD index and query overlaps
igd = gtars.igd.build_index("regions.bed")
overlaps = igd.query("chr1", 1000, 2000)
```

### 2. Coverage Track Generation

Generate coverage tracks from sequencing data with the uniwig module.

```bash
# Generate BigWig coverage track
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig
```

### 3. Genomic Tokenization

Convert genomic regions into discrete tokens for machine learning applications.

```python
import gtars
from gtars.tokenizers import TreeTokenizer

tokenizer = TreeTokenizer.from_bed_file("training_regions.bed")
token = tokenizer.tokenize("chr1", 1000, 2000)
```

### 4. Reference Sequence Management

Handle reference genome sequences and compute digests following the GA4GH refget protocol.

```python
# Load reference and extract sequences
store = gtars.RefgetStore.from_fasta("hg38.fa")
sequence = store.get_subsequence("chr1", 1000, 2000)
```

### 5. Fragment Processing

Split and analyze fragment files, particularly useful for single-cell genomics data.

```bash
# Split fragments by clusters
gtars fragsplit cluster-split --input fragments.tsv --clusters clusters.txt --output-dir ./by_cluster/
```

### 6. Fragment Scoring

Score fragment overlaps against reference datasets.

```bash
# Score fragments against reference
gtars scoring score --fragments fragments.bed --reference reference.bed --output scores.txt
```

## Common Workflows

### Workflow 1: Peak Overlap Analysis

Identify overlapping genomic features:

```python
import gtars

# Load two region sets
peaks = gtars.RegionSet.from_bed("chip_peaks.bed")
promoters = gtars.RegionSet.from_bed("promoters.bed")

# Find overlaps
overlapping_peaks = peaks.filter_overlapping(promoters)

# Export results
overlapping_peaks.to_bed("peaks_in_promoters.bed")
```

### Workflow 2: Coverage Track Pipeline

Generate coverage tracks for visualization:

```bash
# Step 1: Generate coverage
gtars uniwig generate --input atac_fragments.bed --output coverage.wig --resolution 10

# Step 2: Convert to BigWig for genome browsers
gtars uniwig generate --input atac_fragments.bed --output coverage.bw --format bigwig
```

### Workflow 3: ML Preprocessing

Prepare genomic data for machine learning:

```python
import gtars
from gtars.tokenizers import TreeTokenizer

# Step 1: Load training regions
regions = gtars.RegionSet.from_bed("training_peaks.bed")

# Step 2: Create tokenizer
tokenizer = TreeTokenizer.from_bed_file("training_peaks.bed")

# Step 3: Tokenize regions
tokens = [tokenizer.tokenize(r.chromosome, r.start, r.end) for r in regions]

# Step 4: Use tokens in ML pipeline
# (integrate with geniml or custom models)
```

## Python vs CLI Usage

**Use Python API when:**
- Integrating with analysis pipelines
- Need programmatic control
- Working with NumPy/Pandas
- Building custom workflows

**Use CLI when:**
- Quick one-off analyses
- Shell scripting
- Batch processing files
- Prototyping workflows

## Reference Documentation

Comprehensive module documentation:

- **`references/python-api.md`** - Complete Python API reference with RegionSet operations, NumPy integration, and data export
- **`references/overlap.md`** - IGD indexing, overlap detection, and set operations
- **`references/coverage.md`** - Coverage track generation with uniwig
- **`references/tokenizers.md`** - Genomic tokenization for ML applications
- **`references/refget.md`** - Reference sequence management and digests
- **`references/cli.md`** - Command-line interface complete reference

## Integration with geniml

Gtars serves as the foundation for the geniml Python package, providing core genomic interval operations for machine learning workflows. When working on geniml-related tasks, use gtars for data preprocessing and tokenization.

## Performance Characteristics

- **Native Rust performance**: Fast execution with low memory overhead
- **Parallel processing**: Multi-threaded operations for large datasets
- **Memory efficiency**: Streaming and memory-mapped file support
- **Zero-copy operations**: NumPy integration with minimal data copying

## Data Formats

Gtars works with standard genomic formats:

- **BED**: Genomic intervals (3-column or extended)
- **WIG/BigWig**: Coverage tracks
- **FASTA**: Reference sequences
- **Fragment TSV**: Single-cell fragment files with barcodes

## Error Handling and Debugging

Enable verbose logging for troubleshooting:

```python
import gtars

# Enable debug logging
gtars.set_log_level("DEBUG")
```

```bash
# CLI verbose mode
gtars --verbose <command>