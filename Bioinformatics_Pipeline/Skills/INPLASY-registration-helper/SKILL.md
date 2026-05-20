---
name: INPLASY-registration-helper
description: Assists researchers in generating INPLASY registration content for systematic reviews and meta-analyses from a title and an optional protocol. Use when the user wants to draft an INPLASY registration form.
license: MIT
skill-author: AIPOCH
---
# INPLASY Registration Helper

This skill helps researchers draft an INPLASY (International Platform of Registered Systematic Review and Meta-analysis Protocols) registration form. It generates the required fields based on a study title and an optional protocol document.

## When to Use

- Use this skill when a user wants to draft an INPLASY registration form for a systematic review or meta-analysis.
- Use this skill to structure the generation of a study protocol in a reproducible and standardized way.

## Key Features

- **Structured Generation**: Creates a complete registration draft based on official INPLASY fields.
- **Timeline Calculation**: Automatically calculates the start and anticipated completion dates.
- **Template-Driven**: Uses guided prompts from `references/registration_templates.md` to ensure all required sections are addressed.

## Preconditions and Input Validation

> [!WARNING]
> The quality of the generated draft is entirely dependent on the quality of the input. You **must** validate the inputs before proceeding. Failure to do so will result in a generic and unusable output.

Before running the workflow, verify the following:

1.  **Title Specificity**:
    *   The title must be descriptive and clearly state the subject of the review.
    *   It should contain keywords related to the Population, Intervention/Exposure, and primary Outcomes.
    *   **Bad Example**: "A meta-analysis"
    *   **Good Example**: "The effect of metformin on cardiovascular events in patients with type 2 diabetes: a systematic review and meta-analysis."

2.  **Protocol Content (if provided)**:
    *   The protocol document must contain sufficient detail to inform the registration fields.
    *   Crucially, it **must** clearly define the **PICO** elements (Population, Intervention, Comparison, Outcome).
    *   If the protocol is vague or missing PICO, the generated eligibility criteria and search strategy will be of poor quality.

If the inputs do not meet these criteria, you **must inform the user** and request a more detailed title or protocol before proceeding.

## Workflow

1.  **Validate Input**:
    *   Confirm the **Title** of the review meets the specificity criteria outlined above.
    *   If a **Protocol** is provided, verify it contains clearly defined PICO elements.
    *   If inputs are insufficient, halt and request clarification from the user.

2.  **Calculate Timeline**:
    *   Run `scripts/date_utils.py` to obtain the *Start Date* (today) and *Anticipated Completion Date* (today + 28 days).

3.  **Generate Content**:
    *   Using the validated title and protocol, use the prompts in `references/registration_templates.md` to generate the content for each registration section.

## Quality Rules

*   **Language**: All generated content **must be in English**.
*   **Placeholder Handling**:
    *   **Keep `{}`**: Content inside curly braces `{}` (e.g., `{Select the country...}`) must be preserved exactly as is. These represent dropdown options in the INPLASY system.
    *   **Fill `<>`**: Content inside angle brackets `<>` must be replaced with your AI-generated analysis based on the input title and protocol.
*   **PICO Extraction**: Ensure PICO elements are clearly identified from the source material and used consistently to inform the search strategy and eligibility criteria sections.