---
name: spaceranger_wrapper
description: >
  A Python-based agentic skill for running and managing 10x Genomics Space Ranger pipelines.
  This skill provides a structured wrapper around the 'spaceranger' command-line tool,
  incorporating a 3-gate QC framework for input validation, output review, and final confirmation.
  Use this skill to execute 'spaceranger count' and other subcommands in a controlled,
  automated, and validated manner. This is the primary tool for processing Visium spatial
  transcriptomics data from FASTQs to feature-barcode matrices.

MANDATORY SKILL INSTRUCTIONS:

This skill executes the `spaceranger_wrapper.py` script to run Space Ranger pipelines. The agent
must follow the 3-gate QC framework implemented in the script.

## Execution Flow

1.  **Construct the command**: The agent must gather all the required arguments for the
    `spaceranger count` command (`--id`, `--transcriptome`, `--fastqs`, `--image`, `--slide`, `--area`).
2.  **Execute the script**: Call the Python script with the appropriate subcommand and arguments.
    Example:
    ```bash
    python ~/.gemini/skills/spaceranger_wrapper/scripts/spaceranger_wrapper.py count --id=sample01 \\
    --transcriptome=/path/to/ref \\
    --fastqs=/path/to/fastqs \\
    --image=/path/to/image.tiff \\
    --slide=V11A11-111 \\
    --area=A1
    ```
3.  **Monitor the Output**: The script will print the progress of the 3-gate QC framework.
    -   **QC Gate 1**: The script will display the inputs and ask for confirmation (currently simulated).
    -   **spaceranger execution**: The script will stream the `stdout` and `stderr` from the actual
        `spaceranger` process. The agent should monitor this for errors.
    -   **QC Gate 2**: The script will parse the `metrics_summary.csv` and `web_summary.html`,
        display key metrics and a health score, and ask for confirmation (simulated).
    -   **QC Gate 3**: The script will provide a final confirmation with the path to the output files.
4.  **Report Results**: The agent should parse the final output from the script, confirm the
    location of the results, and report the key QC metrics to the user.

## Available Subcommands

-   `count`: Runs the main pipeline to process FASTQs, align reads, and generate feature-barcode matrices.

## Parameters for `count`

-   `--id`: A unique identifier for the sample. This will also be the name of the output directory.
-   `--transcriptome`: The path to the 10x Genomics transcriptome reference directory.
-   `--fastqs`: The path to the directory containing the FASTQ files.
-   `--image`: Path to the high-resolution tissue image (`.tiff` or `.jpg`).
-   `--slide`: The serial number of the Visium slide (e.g., `V11A11-111`).
-   `--area`: The capture area on the slide to be analyzed (e.g., `A1`).
---
