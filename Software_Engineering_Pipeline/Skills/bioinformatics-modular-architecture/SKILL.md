---
name: bioinformatics-modular-architecture
description: A policy enforcing that bioinformatics pipelines are constructed from modular, reusable skills rather than monolithic scripts, integrating specialized tools via the Agent/MCP/Skill framework.
license: MIT
skill-author: AROS-mutation-sweeper
type: Policy-Enforcement
status: active
---

# Policy: Bioinformatics Pipeline Modular Architecture

This policy mandates a modular, skill-based architecture for all bioinformatics pipelines within the AROS ecosystem. It extends the general principle of `modular-task-breakdown` to the level of pipeline design, ensuring reusability, maintainability, and robust integration.

## 1. Core Rule: Skill-Based Composition

All bioinformatics pipelines MUST be architected as a series of discrete, modular skills orchestrated by a workflow. Each significant, reusable processing stage must be encapsulated within its own AROS skill, rather than being part of a single, monolithic script.

This rule explicitly forbids the creation of long, multi-stage scripts that are not broken down into reusable components managed by the AROS framework.

## 2. Rationale

The goal of this policy is to create a robust, maintainable, and extensible bioinformatics ecosystem.
-   **Reusability:** A `differential-expression` skill can be reused across multiple RNA-seq workflows without modification.
-   **Maintainability:** If an underlying tool (e.g., an R package) is updated, only the specific skill wrapping it needs to be changed, not every pipeline that uses it.
-   **Testability:** Each skill can be independently validated with the Golden Test Battery (GTB), ensuring each component of the pipeline is reliable.
-   **Clarity:** A workflow that orchestrates well-defined skills is easier to understand, debug, and modify than a complex, monolithic script.

## 3. Mandatory Implementation via Agent/MCP/Skill Framework

To comply with this policy, specialized bioinformatics tools (e.g., R scripts, Python analysis scripts, command-line tools) MUST be integrated into the AROS ecosystem by being "wrapped" in a skill.

A compliant skill wrapper includes:
1.  A `SKILL.md` file defining the skill's name, description, inputs, and outputs.
2.  An execution script (e.g., `run.sh`, `run.py`) that the Master Control Program (MCP) can invoke, which in turn executes the specialized tool.
3.  Clear documentation on its dependencies and expected data formats.

## 4. Examples

### Example of a NON-COMPLIANT Monolithic Pipeline

A single skill or script named `run_full_rnaseq_analysis.sh` that contains the following logic internally:
```bash
#!/bin/bash
# NON-COMPLIANT: All steps are locked inside one script

# Step 1: Run FastQC
fastqc $1 -o ./qc_results

# Step 2: Run STAR Aligner
STAR --genomeDir /ref/hg38 --readFilesIn $1 --outFileNamePrefix ./aligned/

# Step 3: Run featureCounts
featureCounts -a /ref/genes.gtf -o ./counts/counts.txt ./aligned/Aligned.out.sam

# Step 4: Call an R script for DESeq2
Rscript --vanilla /scripts/run_deseq2.R ./counts/counts.txt

echo "Pipeline finished."
```
This approach is brittle, hard to debug, and not reusable.

### Example of a COMPLIANT Modular Architecture

The same pipeline is broken down into an orchestration of independent skills:

1.  **`quality-control` Skill:** Wraps the `fastqc` command.
2.  **`read-alignment-star` Skill:** Wraps the `STAR` aligner command.
3.  **`gene-quantification-featurecounts` Skill:** Wraps the `featureCounts` command.
4.  **`differential-expression-deseq2` Skill:** Wraps the `run_deseq2.R` script.

An agent or workflow would then execute these skills sequentially, passing the output of one as the input to the next. This is the **required** architectural pattern for all AROS bioinformatics pipelines.
