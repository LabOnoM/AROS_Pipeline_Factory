---
name: logic-pattern-reuse
description: A policy that mandates the reuse of established and reliable logic patterns to improve system stability and predictability.
license: MIT
skill-author: AROS-Core
---

# Policy: Logic Pattern Reuse

**Version:** 1.0
**ID:** AROS-POLICY-LPR-V1

---

## 1. Preamble

This policy establishes a mandate for all AROS agents to prioritize the reuse of existing, proven logic patterns over the creation of novel, untested solutions. The goal is to enhance the reliability, predictability, and maintainability of the AROS ecosystem by building upon components and architectures that have been verified through successful operation.

## 2. GEPA Error Prevention Rule: Reuse of Established Patterns

**Rule ID:** GEPA-Rule-LPR-001

**Statement:** New implementations or modifications should, where appropriate, mimic or reuse established and verified reliable logic patterns from existing systems. This reduces the likelihood of introducing new, unforeseen errors and accelerates development by leveraging proven solutions.

## 3. Implementation Guidelines

Agents must adhere to the following guidelines when generating or modifying code, workflows, or system configurations:

### 3.1. Pattern Identification

Before implementing a new feature or modification, agents must perform a search of the existing AROS skills, KIs, and workflows to identify analogous logic patterns. This includes, but is not limited to:
- Error handling and retry mechanisms (e.g., `gepa_error_prevention_patch`).
- Validation and self-correction loops (e.g., `iterative-validator`).
- State management and data flow architectures.
- Quality assurance pipelines (e.g., `code-generation-quality-assurance-process`).

### 3.2. Prioritization

- **Direct Reuse:** Whenever possible, directly invoke an existing skill or workflow that accomplishes the required task.
- **Mimicry:** If direct reuse is not feasible, the new implementation should closely follow the structure, control flow, and error handling patterns of a trusted, relevant example.
- **Justification for Novelty:** If a novel pattern is required, the agent must provide explicit justification for why existing patterns are unsuitable. This justification will be logged for review and may be used to identify gaps in the current system's capabilities.

### 3.3. Verification

Any new implementation, even one that mimics an existing pattern, must still pass the complete multi-stage verification process as defined by the `code-generation-quality-assurance-process` policy to ensure it has been integrated correctly.

