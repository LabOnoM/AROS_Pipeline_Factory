---
name: temporal-analysis-communication
description: Analyzes and communicates temporal evolution of systems by structuring outputs to clearly map changes over time.
license: MIT
skill-author: AROS-Code-Generator
---

# Temporal Analysis & Communication Skill

## When to Use

Use this skill when you need to analyze and communicate changes in a system over time. This skill is particularly useful for:

- Tracking the evolution of metrics or parameters.
- Comparing system states at different points in time.
- Identifying trends and patterns in time-series data.
- Generating reports that clearly illustrate temporal changes.

## MANDATORY SKILL INSTRUCTIONS

### GEPA Error Prevention Rule: Structural Mapping of Temporal Evolution

To ensure that the outputs of this skill structurally map the temporal evolution of a system, all outputs MUST adhere to the following format. This is a strict requirement and acts as a guardrail to prevent unstructured or ambiguous responses.

---

### Output Structure

**1. Initial State (T0):**
   - **Timestamp/Identifier:** [Specify the starting point in time, e.g., "2023-01-01", "Baseline"]
   - **Description:** A detailed description of the system at the beginning of the timeline.
   - **Key Metrics:**
     - Metric A: [Value]
     - Metric B: [Value]
     - ...

**2. Intermediate State(s) (T1, T2, ...):**
   - **Timestamp/Identifier:** [Specify the intermediate point in time]
   - **Description:** A description of the system at this point in time, highlighting changes from the previous state.
   - **Key Metrics:**
     - Metric A: [Value]
     - Metric B: [Value]
     - ...

**3. Final State (Tn):**
   - **Timestamp/Identifier:** [Specify the end point in time]
   - **Description:** A description of the system at the end of the timeline, highlighting changes from the previous state.
   - **Key Metrics:**
     - Metric A: [Value]
     - Metric B: [Value]
     - ...

**4. Trend Analysis:**
   - **Summary of Evolution:** A high-level summary of the overall temporal evolution of the system.
   - **Identified Trends:** A list of any significant trends, patterns, or anomalies observed in the data.
   - **Projections/Insights:** (Optional) Any projections or insights based on the observed trends.

---

### GEPA Error Prevention Rule: Dynamic Fallback on Formatting Failure

If the agent fails to generate an output that adheres to the "Structural Mapping of Temporal Evolution" format, the attempt is considered a failure. After two (2) consecutive failures on the same task, a dynamic fallback mechanism MUST be triggered.

-   **Fallback Action:** The agent MUST escalate the task to a 'larger model persona' for more complex reasoning. The agent must explicitly state that it is activating a fallback due to repeated formatting failures.
-   **Rationale:** This prevents the agent from getting stuck in a loop of generating improperly structured data and ensures that complex temporal analysis tasks that may be causing the formatting failure are handled by a more capable reasoning process.


## Example Usage

### Input

"Analyze the temporal evolution of a cell culture from day 1 to day 5.
- Day 1: 1 million cells, 95% viability.
- Day 3: 4 million cells, 90% viability.
- Day 5: 8 million cells, 85% viability."

### Expected Output

**1. Initial State (T0):**
   - **Timestamp/Identifier:** Day 1
   - **Description:** The initial state of the cell culture.
   - **Key Metrics:**
     - Cell Count: 1 million
     - Viability: 95%

**2. Intermediate State (T1):**
   - **Timestamp/Identifier:** Day 3
   - **Description:** The cell culture after 2 days of growth.
   - **Key Metrics:**
     - Cell Count: 4 million
     - Viability: 90%

**3. Final State (T2):**
   - **Timestamp/Identifier:** Day 5
   - **Description:** The final state of the cell culture after 4 days of growth.
   - **Key Metrics:**
     - Cell Count: 8 million
     - Viability: 85%

**4. Trend Analysis:**
   - **Summary of Evolution:** The cell culture exhibited exponential growth over the 5-day period, with a corresponding decrease in viability.
   - **Identified Trends:**
     - The cell count doubled approximately every 2 days.
     - The viability decreased by 5% every 2 days.
   - **Projections/Insights:** The decreasing viability may indicate that the culture is reaching confluency or that nutrient depletion is occurring.

## For complex analysis, use the provided python script:

`python ~/.gemini/skills/temporal-analysis-communication/main.py --data '<json_data>'`
