---
name: neuropixels-analysis
description: End-to-end Neuropixels extracellular electrophysiology analysis (SpikeGLX/Open Ephys/NWB) including preprocessing, motion correction, Kilosort4 spike sorting, QC metrics, and Allen/IBL-style curation; use when processing Neuropixels recordings or when users mention Neuropixels, SpikeGLX, Open Ephys, Kilosort, quality metrics, drift/motion correction, or unit curation.
license: MIT
metadata:
    skill-author: AIPOCH
---

## Overview

Comprehensive toolkit for analyzing Neuropixels high-density neural recordings using current best practices from SpikeInterface, Allen Institute, and International Brain Laboratory (IBL). Supports the full workflow from raw data to publication-ready curated units.

## When to Use This Skill

Use this skill in any of the following situations:

1. **Loading and standardizing Neuropixels recordings** from SpikeGLX (`.ap.bin/.lf.bin/.meta`), Open Ephys (`.continuous/.oebin`), or NWB (`.nwb`) into a consistent analysis pipeline.
2. **Preparing raw extracellular data for spike sorting**, including high-pass filtering, phase shift correction (NP1.0), bad channel detection/removal, and common average referencing (CAR).
3. **Suspecting probe drift or tissue motion** and needing to estimate and correct motion before sorting (especially when drift is > ~10 µm).
4. **Running spike sorting** (Kilosort4 recommended; CPU alternatives supported) and then computing post-processing products (waveforms, templates, amplitudes, correlograms, unit locations).
5. **Requiring quality control and curation** using Allen/IBL-style thresholds, plus optional AI-assisted visual review for borderline units, and exports to Phy/NWB.

## Key Features

- **Multi-format ingestion**: SpikeGLX, Open Ephys, and NWB readers via SpikeInterface.
- **Neuropixels-aware preprocessing**:
  - High-pass filtering for spike band
  - Phase shift correction for Neuropixels 1.0
  - Bad channel detection and removal
  - Median CAR / referencing
- **Motion/drift workflow**:
  - Motion estimation presets (e.g., “Kilosort-like”)
  - Optional rigid/non-rigid correction presets
  - Drift visualization outputs
- **Spike sorting orchestration**:
  - Kilosort4 (GPU) recommended
  - CPU alternatives (e.g., SpykingCircus2, Mountainsort5, Tridesclous2)
- **Post-processing and QC**:
  - SortingAnalyzer-based computation of waveforms, templates, amplitudes, correlograms, unit locations, and quality metrics
- **Curation**:
  - Allen/IBL-style automated labeling
  - Optional AI-assisted visual analysis for uncertain units
- **Reporting and export**:
  - HTML report generation
  - Export to Phy and NWB
  - Save metrics tables (CSV)

## Supported Hardware & Formats

| Probe | Electrodes | Channels | Notes |
|-------|-----------|----------|-------|
| Neuropixels 1.0 | 960 | 384 | Requires phase_shift correction |
| Neuropixels 2.0 (single) | 1280 | 384 | Denser geometry |
| Neuropixels 2.0 (4-shank) | 5120 | 384 | Multi-region recording |