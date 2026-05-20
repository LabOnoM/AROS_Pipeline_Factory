---
name: data-availability-for-content-generation-policy
description: A policy that mandates the verification of data availability and accessibility *before* initiating any content generation task.
license: MIT
skill-author: AROS-Core
---

# Data Availability for Content Generation Policy

This document outlines the 'Data Availability for Content Generation' policy. It enforces the mandatory prerequisite that all required data points must be verified as available and accessible before any content generation component is triggered.

## GEPA Rule

**GEPA-Rule-002: Pre-emptive Data Availability Verification**

Before any content generation or drafting component is triggered, all required data points, sources, and facts MUST be verified as available and accessible. Content generation MUST NOT proceed if any prerequisite data is missing or inaccessible.

## When to Use

- ALWAYS use this policy before generating any content that relies on specific data inputs, such as reports, summaries, or data-driven analyses.
- Apply this policy when a task requires information from `brain.db`, KIs, or external APIs.
- This policy is a prerequisite for any skill that generates content based on source data.

## Execution Logic

1.  **Identify Data Prerequisites:** Before executing a content generation task, first identify all the necessary data points, facts, or sources required for the task.

2.  **Verify Availability:** For each data prerequisite, perform a check to confirm its availability and accessibility.
    -   For data from `brain.db`, use `query_brain_db` to check for the existence of the required facts.
    -   For data from KIs, use `read_ki` to ensure the KI is present and contains the necessary information.
    -   For data from files, use `read_local_file` to verify the file exists and is readable.
    -   For data from APIs, perform a test call to the API endpoint to ensure it is responsive and the required data is available.

3.  **Conditional Content Generation:**
    -   **If all data prerequisites are verified:** Proceed with the content generation task.
    -   **If any data prerequisite is missing or inaccessible:**
        -   HALT the content generation process immediately.
        -   Report the specific missing data points as the reason for failure, following the `agent-communication` policy.
        -   If possible, initiate a sub-task to acquire the missing data.

## Example Application

**Task:** "Generate a summary of the latest user feedback for the 'aros-dashboard-control' skill."

**Incorrect Application (violates policy):**

1.  Immediately attempts to generate a summary, assuming the data is available.
2.  Fails midway through the process because the user feedback data is not found.
3.  Reports a generic failure message.

**Correct Application (compliant with policy):**

1.  **Identify Data Prerequisite:** The task requires user feedback data for the 'aros-dashboard-control' skill.
2.  **Verify Availability:**
    -   Query `brain.db` to check for facts related to 'user feedback' and 'aros-dashboard-control'.
    -   `query_brain_db(sql_query="SELECT fact FROM world_facts WHERE entity LIKE '%aros-dashboard-control%' AND fact LIKE '%user feedback%'")`
3.  **Conditional Content Generation:**
    -   **If the query returns results:** Proceed to generate the summary based on the retrieved facts.
    -   **If the query returns no results:**
        -   HALT the summary generation.
        -   Report: "I cannot generate the summary because no user feedback for the 'aros-dashboard-control' skill was found in `brain.db`."

## Implementation Details

-   This is a mandatory policy to be integrated into the core logic of any agent or workflow that generates content from source data.
-   The verification step should be explicit and auditable in the agent's logs.
-   Failure to adhere to this policy will result in a policy violation.
