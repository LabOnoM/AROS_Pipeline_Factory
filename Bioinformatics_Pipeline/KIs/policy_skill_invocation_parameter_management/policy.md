**Policy Name:** `skill_invocation_and_parameter_management`
**Policy ID:** AROS-POL-003
**Version:** 1.1
**Status:** DRAFT
**Effective Date:** YYYY-MM-DD

### 1.0 Purpose

This policy establishes the mandatory requirements for the invocation of skills, with a specific focus on parameter validation for specialized bioinformatics and computational biology skills. The primary goal is to ensure the reliability, reproducibility, and correctness of scientific workflows by preventing errors caused by invalid, missing, or out-of-bounds parameters.

### 2.0 Scope

This policy applies to all AROS agents, orchestrators, and workflows that invoke skills classified as `bioinformatics`, `genomics`, `proteomics`, `computational_biology`, or any other skill that consumes structured scientific data as input.

### 3.0 Core Principle

Skill invocation must be a trusted and predictable process. Parameters provided to skills, especially those performing scientific data analysis or database interaction, represent critical inputs that directly affect the outcome. Therefore, all such parameters must be rigorously validated *prior* to skill execution to safeguard against data corruption, failed runs, and invalid scientific conclusions.

### 4.0 Policy Directives

#### 4.1. Mandatory Parameter Schema Definition

Every skill falling within the scope of this policy must include a machine-readable schema that formally defines its expected parameters.

*   **Format:** The schema shall be defined in a `parameters.json` or `parameters.yaml` file within the skill's directory.
*   **Content:** The schema must, for each parameter, define:
    *   `name`: The parameter's name.
    *   `description`: A human-readable description of the parameter.
    *   `type`: The data type (e.g., `string`, `integer`, `float`, `boolean`, `list`).
    *   `required`: A boolean indicating if the parameter is mandatory.
    *   `allowed_values` (optional): An enumeration of permissible values for string types.
    *   `range` (optional): A minimum and maximum value for numeric types.
    *   `pattern` (optional): A regular expression for string validation (e.g., for accession IDs).

#### 4.2. Pre-Invocation Validation Mandate

The AROS orchestrator, or any agent invoking a skill, **must** perform a validation check on the provided parameters against the skill's defined schema *before* the skill's core logic is executed.

*   Execution of the skill is contingent on the successful completion of this validation step.

#### 4.3. Strict Error Handling

If parameter validation fails, the skill invocation **must be aborted**.

*   A structured error message must be generated and logged, clearly indicating:
    *   Which parameter(s) failed validation.
    *   The reason for the failure (e.g., "Type mismatch", "Value not in allowed set", "Required parameter missing").
    *   The value that was provided.
*   The error must be propagated back to the calling agent or workflow to allow for corrective action.

#### 4.4. Auditable Logging

All parameter validation events (both success and failure) must be logged in the AROS system logs. This creates an auditable trail for debugging and ensuring policy compliance.

*   Logs must include the skill name, the parameters provided (with sensitive data masked where appropriate), and the validation outcome.

#### 4.5. Data and Output Accessibility

Provide accessible links to all supporting output files, including scripts, raw data, figures, and supplementary materials, to ensure reproducibility and transparency.

### 5.0 Example Schema (`jaspar-api/parameters.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "JASPAR API Skill Parameters",
  "type": "object",
  "properties": {
    "query": {
      "description": "The search term, such as a gene name or matrix ID.",
      "type": "string"
    },
    "search_by": {
      "description": "The type of search to perform.",
      "type": "string",
      "enum": ["name", "matrix_id", "tf_family"]
    },
    "tax_id": {
      "description": "NCBI Taxonomy ID to filter results (e.g., 9606 for Human).",
      "type": "integer",
      "minimum": 1
    },
    "collection": {
        "description": "The JASPAR collection to query.",
        "type": "string",
        "enum": ["CORE", "CNE", "PHYLOFACTS", "SPLICE", "POLII", "FAM", "PBM", "PBM_HOMEO", "PBM_HLH"]
    },
    "version": {
        "description": "The version of the JASPAR database to use.",
        "type": "string",
        "pattern": "^[0-9]{4}$"
    }
  },
  "required": ["query", "search_by"]
}
```

### 6.0 Enforcement

This policy will be enforced through automated checks in the AROS skill management and orchestration layers. Non-compliant skills may be disabled or flagged until they are updated to meet these requirements. The GTB (Golden Test Battery) will include tests to verify the presence and correctness of parameter schemas for relevant skills.
