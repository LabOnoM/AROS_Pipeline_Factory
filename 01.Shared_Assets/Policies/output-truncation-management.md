---
name: output-truncation-management
description: "A policy governing how AROS agents manage and communicate output truncation to ensure data integrity, user clarity, and operational reliability."
cpcp_asset: true
canonical_location: "01.Shared_Assets/Policies/output-truncation-management.md"
consumers:
  - Grant_Write_Pipeline
  - Manuscript_Write_Pipeline
last_cpcp_review: "2026-05-11"
---

# AROS Policy: Output Truncation Management

## 1. Purpose

This policy governs how AROS agents manage and communicate output truncation to ensure data integrity, user clarity, and operational reliability. Truncated outputs, especially in structured data formats like JSON, can lead to critical failures in downstream tasks. This policy aims to prevent such failures and maintain user trust by making truncation explicit and providing access to complete data.

## 2. Scope

This policy applies to all AROS agents, skills, and workflows that generate or display output to a user or pass data to another process where length limits may be encountered.

## 3. Core Rules

### 3.1. Explicit Truncation Notification

When presenting an output preview that has been truncated due to length constraints, the agent **MUST** explicitly state that the output is a preview and is incomplete.

*   **Example Statement:** `[INFO] Output preview is truncated. Full content written to /path/to/full_output.txt.`

### 3.2. Provide Access to Full Output

Alongside the truncation notification, the agent **MUST** provide a direct and unambiguous method for the user or other agents to access the complete, un-truncated output.

*   **Acceptable Methods:**
    *   A filepath to a local file where the full output has been saved.
    *   A command that the user can execute to retrieve the full output.
    *   A direct link to a resource (if applicable).
    *   For structured data, a reference to a variable or data object where the complete data is stored in memory.

### 3.3. Minimum Buffer for Structured Data

To prevent data corruption, agents handling structured data (e.g., JSON, XML) from external sources or other LLMs **MUST** configure their output buffers to a minimum of 8192 tokens/characters.

*   **Justification:** Empirical evidence from the AROS Memory Bank shows that a buffer size of 2000 can lead to silent truncation and parsing errors in structured JSON outputs. A setting of 8192 has been proven reliable for preventing such errors. This is a preventative measure to ensure data integrity at the source.
