---
name: modular-task-breakdown
description: A policy that mandates the systematic decomposition of complex tasks into discrete, manageable sub-tasks to improve clarity, reduce errors, and align with GEPA principles.
license: MIT
skill-author: AROS-Core
---

# Policy: Modular Task Breakdown

## 1. Core Principle

This policy establishes a mandatory operational standard for all AROS agents. To ensure clarity, reduce cognitive load, and minimize error rates, **complex tasks must be systematically decomposed into discrete, manageable, and logically separate sub-tasks.** A "complex task" is any operation that involves multiple logical steps, requires the use of more than one skill, or combines data manipulation with system interaction (e.g., reading a file, processing its content, and writing a new file).

## 2. Mandatory Procedure

When faced with a complex task, all agents MUST adhere to the following workflow:

1.  **Analyze and Decompose:** Before execution, explicitly break down the high-level goal into a clear, sequential list of smaller sub-tasks. Each sub-task should represent a single logical unit of work.
2.  **Execute and Verify:** Process each sub-task independently. After each step, perform a brief verification to ensure the outcome was successful before proceeding to the next.
3.  **Report with Structure:** When reporting the final result, the output should reflect the modular breakdown, allowing for easier debugging and validation of the process.

## 3. GEPA Error Prevention Rules

This policy is a core component of the GEPA (Genetic Evolution and Policy Adaptation) error prevention strategy. By enforcing modularity, the system gains the following advantages:

*   **Error Isolation:** Failures are contained within a small, specific sub-task, making the root cause immediately obvious and preventing cascading failures.
*   **Enhanced Testability:** Each sub-task, having a discrete input and output, can be independently validated, aligning with the principles of the Golden Test Battery (GTB).
*   **Reduced Complexity:** Simple, linear workflows are less prone to logical flaws than monolithic, aexecution blocks.

### 3.1. Task Decomposition

**The agent must decompose complex tasks into smaller, manageable sub-tasks and execute them in an organized and logical sequence to achieve the overall objective.**

### 3.2. Persona-Based Task Assignment

**Objectives must be decomposed into logical, sequential tasks, with appropriate personas assigned to each task to leverage specialized capabilities effectively.**
### 3.3. Sub-task First-Attempt Success

This policy codifies the Global Evolution & Policy Architecture (GEPA) rule: **"Strive for efficient task completion by ensuring all sub-tasks succeed on the first attempt, minimizing retries."**

The primary goal is to increase the operational efficiency and reliability of all AROS agents. Retries are computationally expensive, introduce latency, and often indicate a flaw in planning or validation. By optimizing for first-attempt success, the system becomes more robust and predictable.

To implement this principle, all agents MUST adhere to the following meta-guidelines before executing any non-trivial command, skill, or workflow.

#### Pre-Execution Parameter Validation

Before executing any function or command, the agent MUST perform a validation pass on all its inputs and parameters.

- **Completeness Check:** Verify that all required parameters are present.
- **Format & Type Check:** Ensure all parameters are of the expected data type and format.
- **Sanity Check:** Check for logically invalid values (e.g., a file path that doesn't exist for a read operation, a negative timeout).
- **Explicit Halting:** If any parameter is missing, ambiguous, or invalid, the agent MUST halt execution and report the issue. Do not proceed with default or guessed values.

---

## 4. Examples

### Example of NON-COMPLIANT (Monolithic) Execution

**Goal:** Read a user's name from a file, capitalize it, and write a greeting to a new file.

*   **Bad Action:** A single thought process that attempts to chain all actions into one command or a single, uninterrupted code block. This is difficult to debug if any single part fails.

### Example of COMPLIANT (Modular) Execution

**Goal:** Read a user's name 
