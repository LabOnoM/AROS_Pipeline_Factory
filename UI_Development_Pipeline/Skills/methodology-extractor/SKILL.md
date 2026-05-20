---
name: methodology-extractor
description: Precisely identify and extract all methodologies, experimental designs, and parameters from bioinformatics reports, flagging missing information required for reproducibility.
license: MIT
skill-author: AIPOCH
---
# Methodology Extractor

Extract, structure, and validate experimental protocols and parameters from scientific texts.

## When to Use

- Use this skill to parse the Methods section of a bioinformatics paper for a structured summary of its techniques.
- Use this skill to identify missing or under-specified parameters critical for experimental reproducibility.
- Use this skill to convert a prose description of a method into a standardized, machine-readable format.
- Use this skill for evidence insight tasks that require explicit assumptions, bounded scope, and a reproducible output format.

## Key Features

- **High-Precision Extraction**: Identifies specific methodologies (e.g., RNA-Seq, ChIP-Seq), experimental designs, and their associated parameters.
- **Parameter Completeness Check**: Audits extracted methods against a knowledge base of required parameters to ensure all critical details are present.
- **Structured Output**: Formats the extracted information into a standardized JSON or Markdown deliverable.
- **Explicit Null-Handling**: Clearly flags missing or unstated parameters as "Not Provided", preventing ambiguity and enforcing reproducibility standards.

## Dependencies

- `Python`: `3.10+`. Repository baseline for current packaged skills.
- `Third-party packages`: `not explicitly version-pinned in this skill package`. Add pinned versions if this skill needs stricter environment control.
- **Knowledge Asset**: Leverages logic and checklists adapted from `reproducibility-check` and `protocol-standardization` skills.

## Example Usage

```bash
# Example command to run the enhanced extraction script
python ~/.gemini/skills/methodology-extractor/scripts/main.py --input-file "path/to/methods_section.txt" --output-format "json"
```
