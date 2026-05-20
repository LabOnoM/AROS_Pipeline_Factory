---
name: spaceranger
description: >
  Agentic skill for running and managing 10x Genomics Space Ranger pipelines on Visium HD
  and Visium HD 3' spatial transcriptomics data. Covers installation verification,
  automated spaceranger count execution (with input validation), spaceranger segment for
  standalone nuclei segmentation, spaceranger annotate for cell type assignment, and
  spaceranger aggr for multi-sample analysis. Includes a 3-gate QC framework with
  automated metrics parsing, web summary health scoring, and mandatory user confirmation
  at critical decision points. Use this skill whenever the user mentions Space Ranger,
  spaceranger count, spaceranger segment, spaceranger annotate, spaceranger aggr, running
  Visium HD pipeline, 10x Genomics pipeline execution, processing FASTQ for spatial
  transcriptomics, Space Ranger outputs, Visium HD FASTQ to matrices, or needs to
  run/troubleshoot/parse outputs from a Space Ranger pipeline.
---

# Space Ranger Pipeline Execution Skill

This skill automates the execution, monitoring, and QC validation of 10x Genomics Space
Ranger pipelines. It is the **upstream companion** to the `visiumhd-segmentation` skill.

This skill enforces a strict, multi-gate validation process. **You MUST follow the prescribed invocation order.** Skipping validation steps will cause catastrophic failure.

## 🚨 CRITICAL: Pre-flight Validation Protocol

Bioinformatics pipelines are fragile. The `preflight.*` tools are a **mandatory gating system** to prevent common, fatal errors *before* you waste time and compute resources.

### The FASTA Header Rule

The most common failure mode for `spaceranger mkref` is a FASTA file with empty headers (e.g., a line with just `>`). This is a **fatal error**.

- **RULE:** If your workflow involves creating a reference genome with `execution.run_mkref`, you **MUST FIRST** call `preflight.validate_fasta_reference`.
- **ANTI-PATTERN / GUARANTEED FAILURE:** Do not call `execution.run_mkref` without first calling `preflight.validate_fasta_reference` and receiving a `0` (valid) response. The system will fail.

## 🛠️ Tool Interface (Schema)

This skill exposes several tools that **MUST** be called in the correct order. The `Stage / Order` column is a mandatory sequence.

| Stage / Order             | Tool                                 | Description                                                                                                                                                                     | Parameters                                                              | Pre-conditions                                                                                      | Returns                                                    |
| :------------------------ | :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------- | :--------------------------------------------------------- |
| **1. PRE-FLIGHT (If mkref)** | `preflight.validate_fasta_reference` | 🚨 **MANDATORY FIRST STEP for `mkref` workflows.** Checks a FASTA file for empty headers (`>`), which cause **fatal** pipeline errors. **DO NOT SKIP THIS.**                   | `fasta_path: str`                                                       | User intends to run `mkref`.                                                                        | `int`: `0` if valid. `>0` (count of bad headers) if invalid. |
| **2. PRE-FLIGHT**         | `preflight.validate_inputs`          | ✅ Validates paths for FASTQs and the spatial image before execution.                                                                                                             | `fastqs: str`, `image: str`                                             | `preflight.validate_fasta_reference` returned `0` (if applicable).                                    | `dict`: A status report of which inputs are valid.         |
| **3. USER CONFIRM**       | `user.confirm_inputs`                | 🛑 **MANDATORY GATE.** Presents a summary of validated inputs to the user for final confirmation before any execution begins.                                                     | `summary: str`                                                          | All `preflight.*` tools passed.                                                                     | `bool`: `True` if user confirms, `False` if user denies.   |
| **4a. EXECUTION**         | `execution.run_mkref`                | Executes `spaceranger mkref` to build a genome reference. **MUST be preceded by a successful `validate_fasta_reference` call.**                                                | `reference_path: str`, `fasta_path: str`, `gtf_path: str`               | `preflight.validate_fasta_reference` returned `0` AND `user.confirm_inputs` returned `True`.        | `str`: Path to the generated reference.                    |
| **4b. EXECUTION**         | `execution.run_count`                | Executes `spaceranger count`.                                                                                                                                                   | `id: str`, `fastqs: str`, `image: str`, `reference: str`, `area: str`   | `preflight.validate_inputs` passed AND `user.confirm_inputs` returned `True`.                         | `str`: Path to the Space Ranger output directory.          |
| **4c. EXECUTION**         | `execution.run_segment`              | Executes `spaceranger segment` for standalone nuclei segmentation.                                                                                                              | `id: str`, `image: str`, `output_dir: str`                              | `preflight.validate_inputs` passed AND `user.confirm_inputs` returned `True`.                         | `str`: Path to the segmentation output directory.          |
| **4d. EXECUTION**         | `execution.run_annotate`             | Executes `spaceranger annotate` for cell type assignment.                                                                                                                       | `id: str`, `input_dir: str`, `reference: str`                           | A compatible `run_count` or `run_aggr` output exists AND `user.confirm_inputs` returned `True`.     | `str`: Path to the annotation output directory.            |
| **4e. EXECUTION**         | `execution.run_aggr`                 | Executes `spaceranger aggr` for multi-sample aggregation.                                                                                                                       | `id: str`, `csv: str`                                                   | A valid aggregation CSV exists AND `user.confirm_inputs` returned `True`.                             | `str`: Path to the aggregation output directory.           |
| **5. QC**                 | `qc.parse_metrics`                   | Parses the `web_summary.html` to extract key QC metrics.                                                                                                                        | `web_summary_path: str`                                                 | `run_count` or `run_aggr` completed successfully.                                                     | `dict`: Extracted QC metrics.                              |
| **6. QC**                 | `qc.score_health`                    | Scores the overall health of the Space Ranger run based on QC metrics.                                                                                                          | `metrics: dict`                                                         | `qc.parse_metrics` completed successfully.                                                            | `dict`: Health score and recommendations.                  |
| **7. USER CONFIRM**       | `user.confirm_qc_results`            | 🛑 **MANDATORY GATE.** Presents QC results and health score to the user for a final go/no-go decision on the results.                                                             | `qc_summary: str`                                                       | `qc.score_health` completed successfully.                                                             | `bool`: `True` if user accepts results, `False` otherwise. |