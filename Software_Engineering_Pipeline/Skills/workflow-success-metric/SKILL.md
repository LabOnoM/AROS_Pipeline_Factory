---
name: workflow-success-metric
description: A policy defining how to measure the success of a workflow, incorporating the GEPA error prevention rule for functional completeness.
license: MIT
skill-author: AROS-Mutation-Sweeper
version: 1.5
---

# Policy: Workflow Success Metric

**ID:** AROS-POLICY-WSM-V1.5

---

## 1. Preamble

This document establishes the mandatory criteria for evaluating the success of any workflow within the Antigravity Research OS (AROS). It ensures that success metrics reflect the true utility and functional completeness of the final output, not just the technical execution or completion status of the workflow's steps.

## 2. Core Principle

The success of a workflow is not determined by its ability to run without error, but by its ability to produce an artifact that fully and correctly satisfies the user's original goal. Technical completion is a prerequisite, not the final metric of success.

## 3. GEPA Error Prevention Rule: Functional Completeness and Upstream Failure Propagation

**Overall workflow success metrics must accurately reflect the functional completeness and utility of the final output artifact relative to the original user goal, considering upstream critical failures.**

This rule is designed to prevent 'hollow victories' where a workflow technically completes but produces a useless, incomplete, or flawed artifact due to an unhandled error or data integrity issue in an early, critical step.

## 4. Implementation Requirements

To comply with this policy, all workflows must adhere to the following:

1.  **Define Explicit Success Criteria:** The workflow's definition must include a specific, measurable, and testable definition of what a 'successful' final artifact constitutes. This should be declared within the workflow's metadata.
2.  **Validate Final Output:** The workflow must include a final validation step that programmatically checks the output artifact against the predefined success criteria. This step should leverage skills like , data integrity checkers, or artifact-specific validation logic.
3.  **Propagate Upstream Failures:** A failure in a critical dependency or an early-stage tool (e.g., ) must result in the failure of the entire workflow, even if a subsequent step could technically execute without error. Error states must be propagated and handled, not suppressed or ignored. Returning empty or default values from a failed step is a policy violation.

## 5. Example

-   **User Goal:** 'Analyze the provided dataset  and generate a bar chart visualizing the top 5 most frequent categories.'
-   **Workflow Steps:**
    1.   reads the dataset.
    2.   calculates category frequencies.
    3.   creates a PNG image.
-   **Scenario of Violation:** The  skill fails to access  but, instead of throwing a critical error, it returns an empty dataset. The subsequent  and  steps run without technical error, but the final output is a blank, useless PNG image.
-   **Policy Application:** Under this policy, the workflow is considered a **FAILURE**. A validation step should have been in place to check if the loaded data was empty, and the  skill itself should have propagated its failure state, halting the workflow immediately.

---


--- AUTO-CORRECTION BASED ON FEEDBACK ---
The content lacks depth and clarity. Automated check failed.
--- END CORRECTION ---

--- AUTO-CORRECTION BASED ON FEEDBACK ---
The content lacks depth and clarity. Automated check failed.
--- END CORRECTION ---

--- AUTO-CORRECTION BASED ON FEEDBACK ---
External review feedback: The structure is illogical and lacks a concluding summary. Please revise.
--- END CORRECTION ---