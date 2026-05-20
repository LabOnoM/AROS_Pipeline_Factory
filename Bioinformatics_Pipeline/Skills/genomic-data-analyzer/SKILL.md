---
name: genomic-data-analyzer
description: Analyzes genomic data files (FASTQ, BAM) to identify gene variants and performs annotation using a specified reference genome.
license: MIT
skill-author: AROS Mutation Sweeper
---
# Genomic Data Analyzer

This skill processes genomic data to identify and annotate genetic variants. It serves as a template for demonstrating the Proactive Input Acquisition mechanism.

## When to Use
- Use when a user needs to find genetic variants from raw sequencing data.
- Use when the required inputs (file path, reference genome) are available or can be acquired.

## Parameters
- `input_filepath`: (Required) Path to the genomic data file (e.g., `/path/to/data.fastq`).
- `reference_genome`: (Required) The identifier for the reference genome to use for alignment (e.g., `hg38`, `GRCh38`).
- `output_format`: (Optional) Desired output format for the variant list (default: `vcf`).

## Proactive Input Acquisition

This section defines the procedure for autonomously acquiring critical inputs that are missing from the user's initial request. Follow these steps in order.

### 1. Identify Missing Critical Inputs
Before execution, verify the presence of the following mandatory inputs:
- `input_filepath`: The path to the source genomic data file.
- `reference_genome`: The identifier for the reference genome.

### 2. Internal Acquisition Strategy
If a critical input is missing, attempt to acquire it without user interaction first.

- **For `reference_genome`**:
  - **Action**: Query the AROS `brain.db` to find the most recently used or contextually relevant reference genome for genomic analyses.
  - **Tool Call**: `query_brain_db(sql_query="SELECT fact FROM world_facts WHERE entity = 'genomics' AND fact LIKE '%reference_genome%' ORDER BY last_updated DESC LIMIT 1")`
  - **Condition**: If a plausible value (e.g., 'hg38') is returned, use it for the analysis. You MUST state this assumption in your response, for example: "Proceeding with the `hg38` reference genome based on recent project context. Please specify a different `reference_genome` if this is incorrect."

### 3. External Acquisition (User Prompting)
If internal acquisition fails or is not applicable (e.g., for a unique file path), prompt the user for the specific missing information. Ask for inputs one by one as they are needed.

- **If `input_filepath` is missing**:
  - **Prompt**: "I need the path to the genomic data file you want to analyze. Please provide the full path to the FASTQ or BAM file."

- **If `reference_genome` is still missing after the internal check**:
  - **Prompt**: "Which reference genome should I use for the analysis? (e.g., hg38, GRCh38)"

### 4. Graceful Failure
If a critical input cannot be acquired through either internal search or user prompting, terminate the workflow with a clear message.

- **Response for missing `input_filepath`**: "Workflow terminated. I cannot proceed without the path to the genomic data file. Please provide the `input_filepath` to continue."
- **Response for missing `reference_genome`**: "Workflow terminated. I cannot proceed without a `reference_genome`. Please specify one to continue."

## Workflow
1. **Validate Inputs**: Execute the `Proactive Input Acquisition` workflow to ensure all required parameters are present.
2. **Execute Analysis**: Run the hypothetical analysis script: `python scripts/run_analysis.py --input "{input_filepath}" --ref "{reference_genome}" --outformat "{output_format}"`.
3. **Return Results**: Present the generated variant file to the user and summarize key findings.
