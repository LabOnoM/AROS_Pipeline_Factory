# Policy: Sub-task First-Attempt Success

## 1. GEPA Principle

This policy codifies the Global Evolution & Policy Architecture (GEPA) rule: **"Strive for efficient task completion by ensuring all sub-tasks succeed on the first attempt, minimizing retries."**

The primary goal is to increase the operational efficiency and reliability of all AROS agents. Retries are computationally expensive, introduce latency, and often indicate a flaw in planning or validation. By optimizing for first-attempt success, the system becomes more robust and predictable.

## 2. Operational Meta-Guidelines

To implement this principle, all agents MUST adhere to the following meta-guidelines before executing any non-trivial command, skill, or workflow.

### Guideline A: Pre-Execution Parameter Validation

Before executing any function or command, the agent MUST perform a validation pass on all its inputs and parameters.

- **Completeness Check:** Verify that all required parameters are present.
- **Format & Type Check:** Ensure all parameters are of the expected data type and format.
- **Sanity Check:** Check for logically invalid values (e.g., a file path that doesn't exist for a read operation, a negative timeout).
- **Explicit Halting:** If any parameter is missing, ambiguous, or invalid, the agent MUST halt execution and report the issue. Do not proceed with default or guessed values. This mirrors the `protocol-standardization` skill's practice of explicitly marking missing information as "To be supplemented/Not provided" rather than fabricating it.

### Guideline B: Scope & Constraint Confirmation

Before beginning the core logic of a task, the agent MUST confirm that the request aligns with the documented capabilities of the tools being used.

- **Confirm Objectives:** Re-state the user's objective and the planned approach.
- **Validate Scope:** Cross-reference the planned actions against the `SKILL.md` or documentation for the relevant tools. Ensure the task does not require unsupported actions.
- **Identify Constraints:** Explicitly list non-negotiable constraints (e.g., "must not use external APIs," "must preserve original file").
- **Stop Early:** If the validation reveals a mismatch between the request and the tool's capabilities, the agent MUST stop and report the conflict immediately, as mandated by skills like `adverse-event-narrative`.

### Guideline C: Pre-Flight Validation & Dry Runs

For any operation that modifies system state (e.g., writing files, installing packages, configuring services), agents MUST perform a pre-flight check to predict the outcome without causing side effects.

- **Use Dry-Run Flags:** When available, use command-line flags like `--dry-run`, `--pretend`, or `--check`.
- **Leverage Validators:** For generating content (code, skills, policies), use dedicated validation tools. For example, new AROS components MUST be validated against the Golden Test Battery (GTB) *before* being written to the filesystem, using the `gtb-validator` skill.
- **Lint and Compile:** Before executing newly generated code, run a linter or compiler to catch syntax errors and potential bugs.
- **Simulate Logic:** In the absence of a dry-run feature, the agent should outline the sequence of steps and manually check each one for potential failures (e.g., checking if a target directory exists before a write operation).

### Guideline D: Hypothesis-Driven Action

Frame every execution step as a scientific experiment. This forces a deliberate, evidence-based approach over impulsive action.

- **State a Hypothesis:** Before running a command, explicitly state the expected outcome (e.g., "Hypothesis: Running `pip install pandas` will make the `pandas` library importable in the current Python environment.").
- **Define Success Criteria:** Define what a successful outcome looks like.
- **Observe the Result:** After execution, compare the actual outcome to the expected outcome.
- **Learn from Deviation:** If the outcome deviates, do not immediately retry. Instead, analyze the discrepancy to refine the next attempt. This proactive application of the `debug-hypothesis` skill's principles helps prevent repeated failures.
