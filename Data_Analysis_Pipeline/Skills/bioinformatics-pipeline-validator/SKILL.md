---
name: bioinformatics-pipeline-validator
description: Validates bioinformatics pipelines to ensure they follow the end-to-end completeness policy, from raw data to functional analysis.
license: MIT
skill-author: AROS-GEPA
type: Policy-Enforcement
status: active
---

# Bioinformatics Workflow Completeness Validator

This skill enforces the GEPA proposal regarding the completeness of bioinformatics workflows. It ensures that any new or modified bioinformatics pipeline adheres to a standard structure, promoting reproducibility, completeness, and biological relevance.

## When to Use

- **Before creating or committing a new bioinformatics skill:** Use this validator to check if the proposed workflow meets the AROS standards.
- **When reviewing an existing bioinformatics workflow:** Assess its compliance with current best practices.
- **When an agent is tasked with a bioinformatics analysis:** This skill should be invoked to guide the agent in constructing a complete and valid pipeline.

## Policy Rule: GEPA-Bio-Completeness-001

A compliant bioinformatics pipeline **MUST** represent an end-to-end analysis, beginning with raw experimental data and concluding with downstream functional interpretation. A workflow is considered **NON-COMPLIANT** if it starts with intermediate data (e.g., count matrices) or terminates before providing biological context.

The pipeline **MUST** include the following three distinct stages:

### Stage 1: Raw Data Ingestion & QC

The pipeline's entry point must be raw, unprocessed data. The skill or workflow must be designed to handle primary data files directly and perform initial quality control.

-   **Accepted Raw Data Formats:** FASTQ, BCL, SRA, FASTA, FAST5, IDAT, CEL, etc.
-   **Required Actions:** Raw data loading, initial quality assessment (e.g., FastQC).
-   **Rationale:** Ensures that the full analysis history is captured and avoids starting from pre-processed, "black box" data which may hide upstream issues.

### Stage 2: Core Processing & Quantification

The pipeline must explicitly include the necessary data processing steps that transform raw data into a quantified, analyzable matrix.

-   **Examples for NGS data (RNA-seq/DNA-seq):**
    -   Adapter/Quality Trimming (e.g., Trimmomatic, Cutadapt)
    -   Alignment to a reference genome/transcriptome (e.g., STAR, BWA, Bowtie2)
    -   Post-alignment QC (e.g., SAMtools stats, Qualimap)
    -   Quantification (e.g., featureCounts, RSEM, Kallisto)
    -   Normalization
-   **Rationale:** Ensures the pipeline is robust and that data quality is assessed and controlled throughout the process.

### Stage 3: Downstream Functional Analysis

The pipeline's final output **MUST** be a form of biological interpretation, not just a list of genes, variants, or peaks. This stage translates the quantitative results into biological meaning.

-   **Required Action:** The workflow must conclude with at least one downstream analysis that provides biological context or functional 
