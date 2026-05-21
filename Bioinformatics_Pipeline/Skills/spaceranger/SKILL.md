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

### The FASTA Validation Gate and the `validation_ticket`

The most common failure mode for `spaceranger mkref` is a FASTA file with empty headers (e.g., a line with just `>`). This is a **fatal error**.

To programmatically prevent this, `execution.run_mkref` is **gated**. It requires a `validation_ticket` which can **only** be obtained from a successful call to `preflight.validate_fasta_reference`. This creates a structural dependency that cannot be bypassed.

- **RULE:** If your workflow involves creating a reference genome with `execution.run_mkref`, you **MUST FIRST** call `preflight.validate_fasta_reference` to obtain a `validation_ticket`.
- **ANTI-PATTERN / GUARANTEED FAILURE:** Do not call `execution.run_mkref` without a valid `validation_ticket`. The tool call will fail.

## 🛠️ Tool Interface (Schema)

This skill exposes several tools that **MUST** be called in the correct order. The `Stage / Order` column is a mandatory sequence.

| Stage / Order             | Tool                                 | Description                                                                  | Parameters                                                              | Pre-conditions                                                              | Returns                                                    |
| :------------------------ | :----------------------------------- | :--------------------------------------------------------------------------- | :---------------------------------------------------------------------- | :-------------------------------------------------------------------------- | :--------------------------------------------------------- |
| **1 (If making ref)** | `preflight.validate_fasta_reference` | **CRITICAL:** Checks a FASTA file for empty headers (`>`), which cause fatal errors. **This is your first action.** | `fasta_path: str`                                                       | User provides a FASTA file for `mkref`.                                     | `int`: `0` if valid. `>0` (count of bad headers) if invalid. |
| **2**                 | `preflight.validate_inputs`          | Validates paths for FASTQs and the spatial image.                            | `fastqs: str`, `image: str`                                             | `validate_fasta_reference` passed (if applicable).                          | `dict`: A status report of which inputs are valid.         |
| **3**                 | `user.confirm_inputs`                | Presents a summary of validated inputs to the user for final confirmation.   | `summary: str`
