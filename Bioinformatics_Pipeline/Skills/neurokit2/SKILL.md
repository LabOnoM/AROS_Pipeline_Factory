---
name: neurokit2
---
description: Generated skill neurokit2

---
name: neurokit2
description: Comprehensive biosignal processing for ECG/PPG/EEG/EDA/RSP/EMG/EOG; use when you need to clean, segment, and extract physiological features for HRV, event-related responses, complexity metrics, or multimodal psychophysiology pipelines.
license: MIT
metadata:
    skill-author: AIPOCH + K-Dense Inc.
---

## Overview

NeuroKit2 is a comprehensive Python toolkit for processing and analyzing physiological signals (biosignals). Use this skill to process cardiovascular, neural, autonomic, respiratory, muscular, and ocular signals for psychophysiology research, clinical applications, and human-computer interaction studies.

## When to Use This Skill

Use this skill when you need to:

1. **Run end-to-end ECG/PPG pipelines** (cleaning → peak detection → feature extraction) for cardiovascular monitoring and HRV.
2. **Compute HRV metrics** (time/frequency/nonlinear) for autonomic nervous system assessment in resting-state or continuous recordings.
3. **Analyze EEG** for band power, microstates, and complexity measures in cognitive/neuroscience experiments.
4. **Decompose EDA** into tonic/phasic components and quantify SCRs for arousal/stress and psychophysiological paradigms.
5. **Perform multimodal biosignal processing** (e.g., ECG + RSP + EDA + EMG) with unified outputs for integrated analyses.
6. **Process and analyze**: EMG for muscle activation; EOG for eye movements and blink detection.
7. **Apply general signal processing techniques**: filtering, peak detection, power spectral density (PSD) estimation.
8. **Calculate complexity and entropy measures**: for non-linear dynamics and information-theoretic insights.
9. **Conduct event-related analysis**: epoching around stimulus events and analyzing physiological responses.

Reference docs (if available in this skill package): `references/ecg_cardiac.md`, `references/hrv.md`, `references/eeg.md`, `references/eda.md`, `references/rsp.md`, `references/emg.md`, `references/eog.md`, `references/signal_processing.md`, `references/complexity.md`, `references/epochs_events.md`, `references/bio_module.md`.  Load specific reference files as needed using the Read tool to access detailed function documentation and parameters.

## Key Features

- **Cardiac (ECG/PPG)**: cleaning, R-peak detection, delineation, quality assessment, ECG-derived respiration, pulse analysis.
- **HRV**: comprehensive indices across time, frequency, and nonlinear domains; RSA and advanced metrics (e.g., RQA where applicable).
- **EEG**: band power, channel utilities, microstate segmentation, and integration patterns commonly used with MNE workflows.  Includes channel quality assessment and re-referencing. Source localization is also available (sLORETA, MNE).
- **EDA**: tonic/phasic decomposition, SCR detection, sympathetic indices, and event-related EDA analysis. Autocorrelation and changepoint detection.
- **Respiration (RSP)**: breathing rate, variability (RRV), and respiratory volume per time (RVT) s