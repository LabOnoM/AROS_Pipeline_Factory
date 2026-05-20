---
name: pipeline-scope-completeness
description: A validation skill that ensures bioinformatics pipelines are comprehensive, covering the entire workflow from initial data processing to final output generation, such as biomarker discovery.
license: MIT
skill-author: AROS-Bio-Integrity-Analyst
type: Policy-Enforcement
status: active
---

# Pipeline Scope & Completeness Policy

This skill establishes a mandatory quality gate for all bioinformatics pipelines developed or executed within the AROS ecosystem. Its primary purpose is to enforce end-to-end completeness, ensuring that pipelines are not just partial solutions but comprehensive workflows that deliver actionable results.

## GEPA Rule

### GEPA-Rule-Bio-03: End-to-End Pipeline Mandate

**All bioinformatics and data analysis pipelines MUST cover the entire data analysis spectrum relevant to the task, from initial data processing to final output generation.**

This rule ensures that pipelines produce complete, interpretable, and actionable results (e.g., a final list of candidate biomarkers with functional annotations) rather than stopping at intermediate data points (e.g., a list of differentially expressed genes without context).

#### Mandatory Pipeline Stages

To comply with this rule, a pipeline must explicitly include and document the following stages, where applicable:

1.  **Data Ingestion & Quality Control (QC):**
    *   Initial loading of raw data (e.g., FASTQ, BAM, VCF, CEL files).
    *   Rigorous quality control checks (e.g., FastQC, MultiQC).
    *   Data cleaning, trimming, and filtering steps.

2.  **Core Data Processing & Analysis:**
    *   Alignment, assembly, variant calling, or expression quantification.
    *   Normalization and batch correction.
    *   Statistical analysis and modeling.

3.  **Final Output Generation & Interpretation:**
    *   Generation of summary reports, tables, and visualizations.
    *   For biomarker discovery tasks, this must include the final list of candidate biomarkers, their associated statistics, and functional annotations.
    *   For clinical or research reports, this includes the final, formatted document.

#### Example of a Compliant Pipeline (Biomarker Discovery)

A compliant pipeline for RNA-seq based biomarker discovery would start with raw FASTQ files and end with a prioritized list of differentially expressed genes, complete with functional annotations and visualizations (e.g., volcano plots, heatmaps). A pipeline that only performs alignment and quantification without the downstream differential expression analysis and interpretation would be considered incomplete and **FAIL** this quality gate.

## When to Use

-   **ALWAYS** apply this skill as a validation step before executing any bioinformatics pipeline, especially for tasks related to sequence analysis, gene expression, or biomarker discovery.
-   Use this skill during the design and development phase of new bioinformatics workflows to ensure they meet system-wide quality standards.
-   Apply this skill when reviewing or modifying existing pipelines to prevent scope regression.

## Validation

To validate a pipeline against this skill, perform the following checks:

1.  **Review Pipeline Definition:** The pipeline's documentation or workflow script (e.g., Snakefile, Nextflow script) must clearly outline all mandatory stages from data ingestion to interpretation.
2.  **Inspect Final Outputs:** Verify that the final outputs include interpretive results (e.g., annotated gene lists, pathway analysis reports, visualizations) and not just intermediate data tables.
3.  **Check for Completeness:** Ensure the pipeline does not terminate prematurely (e.g., after quantification without performing differential analysis and functional annotation for a biomarker discovery task).
