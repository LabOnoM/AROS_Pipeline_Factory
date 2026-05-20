### Knowledge Item: Review Task Output Error Prevention

**Purpose:** To establish a mandatory review constraint for all task outputs within the AROS swarm, aimed at minimizing errors and ensuring quality.

**Policy:** Before any task output is finalized or submitted to downstream processes, it MUST undergo a systematic review by an independent agent or a predefined validation mechanism.

**Key Principles:**

*   **Independence:** The reviewing entity should not be the same entity that generated the output.
*   **Checklist-Driven:** Reviews should follow a standardized checklist to cover common error categories (e.g., factual accuracy, completeness, formatting, adherence to instructions).
*   **Automated where possible:** Leverage automated tools (e.g., linters, spell checkers, data integrity checks) as a first line of defense.
*   **Feedback Loop:** Any identified errors or discrepancies MUST be reported back to the generating agent for correction and learning.

**Activation:** This policy, once indexed, will be retrieved by swarm agents when generating task outputs, prompting them to initiate the review process.