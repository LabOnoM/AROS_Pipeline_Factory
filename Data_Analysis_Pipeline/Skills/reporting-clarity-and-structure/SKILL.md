---
name: reporting-clarity-and-structure
description: A policy to ensure all analysis steps and outputs are reported clearly, comprehensively, and in a structured manner.
license: MIT
skill-author: AROS-GEPA
---

# Policy: Reporting Clarity and Structure

This policy mandates a standardized, clear, and comprehensive structure for reporting the results of any analytical task, code execution, or data processing workflow. Its purpose is to ensure full transparency and reproducibility of actions taken by AROS agents.

## When to Use

- This policy is mandatory when reporting the outcome of any executed skill or tool.
- Apply this policy when summarizing the steps taken to arrive at a conclusion or generate an artifact.
- Use this as the default reporting format for any task involving multiple steps or complex outputs.

## GEPA Rule: Comprehensive and Structured Reporting

**GEPA-Rule-RCS-001: Comprehensive Analysis Reporting**

To ensure clarity and reproducibility, all reports on executed analysis steps and generated outputs must be comprehensive, clearly explained, and structured. The report must explicitly detail the inputs used, the exact steps executed, the resulting outputs, and a concluding summary.

### Core Requirements:

1.  **Inputs Section:** Clearly list all initial data, files, parameters, or configurations used in the analysis.
2.  **Execution Steps Section:** Provide a sequential, step-by-step description of the actions performed. Each step should be unambiguous and easy to follow. For code or commands, include the exact syntax used.
3.  **Outputs Section:** Detail all results generated from the execution steps. This includes terminal output, file paths of generated artifacts, and any messages or errors produced.
4.  **Conclusion Section:** Provide a brief summary of the outcome, interpreting the results in the context of the original goal.

## Example Application

**Context:** An agent is asked to count the number of lines in a file named `data.csv`.

#### **Non-Compliant Output (Lacks Structure and Detail):**
> I ran the `wc -l` command and the file has 150 lines.

#### **GEPA-Compliant Output (Clear, Structured, and Comprehensive):**

**Analysis Report: Line Count for `data.csv`**

*   **Inputs:**
    *   File: `data.csv`
    *   Request: Count the number of lines in the file.

*   **Execution Steps:**
    1.  Executed the following shell command to count the lines in the specified file:
        ```bash
        wc -l data.csv
        ```

*   **Outputs:**
    *   The command produced the following output to standard output:
        ```
        150 data.csv
        ```

*   **Conclusion:**
    *   The file `data.csv` contains exactly 150 lines.
