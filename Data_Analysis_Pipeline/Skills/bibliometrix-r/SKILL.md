---
name: bibliometrix-r
description: Perform comprehensive science mapping, bibliometric analysis, co-authorship networks, and life cycle analysis using Massimo Aria's bibliometrix CRAN package via R. Make sure to use this skill whenever the user mentions bibliometrix, scientometrics, science mapping, thematic maps, or co-citation networks from PubMed/WoS/Scopus exports.
---

# Bibliometrix via R Scripting

This skill enables you (the AI) to leverage the powerful R package **bibliometrix** for quantitative science mapping and comprehensive scientometrics. 

You should use this skill when the user provides export files (from Web of Science, Scopus, PubMed, OpenAlex, etc.) and wants to perform high-level analysis such as:
- Descriptive bibliometric statistics (authors, citations, references).
- Conceptual structure mapping (co-word analysis, thematic maps).
- Intellectual/Social structure exploration (co-citation, historiography, collaboration networks).

## Usage Workflow

1. **Verify R Environment**: Check that `R` is installed in the user's system by running `Rscript --version` via `run_command`. If the `bibliometrix` package is not installed, prompt the user to install it or automatically run `Rscript -e 'install.packages("bibliometrix", repos="https://cloud.r-project.org/")'`.
2. **Understand Dataset**: Determine the source of the user's dataset (e.g., WoS, Scopus, PubMed, OpenAlex) and the format (`plaintext`, `bibtex`, etc.).
3. **Write R Script**: Generate an R script (`.R` file) that imports the data via `convert2df()`, performs the desired analysis, and saves the output (dataframes or plots) to the workspace using the templates in `references/r_scripts_templates.md`. Save the script in a temporary or appropriate workspace directory.
4. **Execute & Interpret**: Run the R script using `run_command` (e.g., `Rscript my_analysis.R`). Read the resulting textual output or display the generated plot images to the user.
5. **Synthesize**: Use the metrics (Annual Growth Rate, Most Productive Authors, Co-Citations) to answer the user's specific bibliometric questions.

## Available Reference Templates

When writing the R script, always refer to the provided code templates to ensure correct syntax for the `bibliometrix` functions:
- **See `references/r_scripts_templates.md`** for standard scripting patterns including Data Loading, Basic Summary, Author Mapping, and Life Cycle Analysis.

## Best Practices
- **Data Completeness**: If the user's queries are failing due to missing NA fields (e.g., missing Authors or Keywords), use `missingData(M)` to assess the dataset quality before running complex visualizations.
- **Plot Saving**: When R generates plots, always save them to a file (e.g., `png("network.png"); plot(...); dev.off()`) so you can display them as markdown images in your response.
- **Scientific Interpretation**: Don't just dump the R output. Synthesize the results. Explain *what* a high H-index means in this context, or *why* two topics are clustered together in the conceptual map.
