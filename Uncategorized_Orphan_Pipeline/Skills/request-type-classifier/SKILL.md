---
name: request-type-classifier
description: A policy for accurately classifying user requests to differentiate between requests for new information/assistance and requests for summaries of past work.
license: MIT
skill-author: AROS-GEPA-Compliance
---

# Policy: Request Type Classification

This policy provides a mandatory framework for classifying user requests. Its primary purpose is to distinguish between two fundamentally different types of user intent:

1.  **Generative / New Concept:** The user is asking for information on a new topic, help with a new task, or the creation of a new artifact.
2.  **Retrospective / Past Project:** The user is asking for a summary, report, or analysis of a task, project, or event that has already occurred.

Accurate classification is critical for selecting the correct downstream skill (e.g., `code-generator` vs. `log-analyzer`).

---

## GEPA Rule: Strict Distinction of Intent

All orchestrator agents MUST apply the following heuristics to classify user requests before assigning a skill. This prevents misallocation of resources, such as attempting to generate a new KI when the user is asking for a report on an existing one.

### 1. Identify **Retrospective (Past Project)** Requests

A request is considered **Retrospective** if it meets one or more of the following criteria:

- **Explicit Keywords:** Contains words like "summary," "summarize," "report on," "what happened with," "find the results of," "recap," "review."
- **Past-Tense Verbs:** Refers to a project or task using past-tense verbs (e.g., "What *was* the outcome of the simulation?").
- **Presence of Identifiers:** Mentions a specific, known project name, KI identifier, date, or other unique token that points to a past event. (e.g., "Give me the logs for the `protein-folding-run-alpha` experiment.").
- **Goal is Retrieval and Aggregation:** The user's goal is to retrieve and condense information that already exists within the AROS memory (brain.db, logs, KIs).

**Examples of Retrospective Requests:**
- "Summarize the findings from the Q2-2023 sentiment analysis project."
- "Generate a report on the `ares-v` rocket test."
- "What were the key takeaways from last week's `gtb-validator` performance analysis?"
- "Find the KI related to the 'Manticore' project."

**Appropriate Downstream Skills:** `ki-retriever`, `log-analyzer`, `project-reporter`, `query-brain-db`.

---

### 2. Identify **Generative (New Concept)** Requests

A request is considered **Generative** if it is not classified as Retrospective and meets one or more of the following criteria:

- **Explicit Keywords:** Contains words like "explain," "how do I," "what is," "create," "draft," "write a," "implement," "design."
- **Future-Tense Verbs:** Describes a task to be performed (e.g., "How *can* I build a pipeline...").
- **Absence of Identifiers:** The request describes a general concept, a task to be started, or an artifact to be created. It lacks specific project names or identifiers pointing to a past event.
- **Goal is Creation or Explanation:** The user's goal is either to create a new artifact (code, KI, plan) or to receive an explanation of a concept.

**Examples of Generative Requests:**
- "Explain the theory of general relativity."
- "How do I set up a Python virtual environment?"
- "Create a new skill that can interact with the GitHub API."
- "Draft a plan for migrating the database."

**Appropriate Downstream Skills:** `code-generator`, `ki-creator`, `documentation-retriever`, `planning-agent`.

---

### 3. Distinguish Action-Oriented vs. Information-Seeking Requests (NEW GEPA Error Prevention Rule)

To prevent misinterpretation of user intent within the **Generative** category, all agents MUST further classify requests to distinguish between a command to perform an action and a request for information.

#### A. Identify **Action-Oriented** Requests

A request is considered **Action-Oriented** if the user's primary goal is to have the agent *perform a task* or *create an artifact*.

- **Heuristics:**
    - **Imperative Verbs:** The request is structured as a command, often starting with a verb (e.g., "Create," "Write," "Generate," "Run," "Build").
    - **Goal is Artifact Creation:** The user expects a tangible output, such as a script, a file, a configuration, or a started process.
    - **Keywords:** "implement," "design," "draft," "develop," "execute," "code a..."

- **Examples of Action-Oriented Requests:**
    - "Write a Python script to parse the latest log file."
    - "Generate a new KI with the data from this conversation."
    - "Build a Docker container for the `ares-v` web server."
    - "Execute the `gtb-validator` on the new policy draft."

- **Appropriate Downstream Skills:** `code-generator`, `ki-creator`, `run-shell-command`, `gtb-validator`.

#### B. Identify **Information-Seeking** Requests

A request is considered **Information-Seeking** if the user's primary goal is to *understand a concept*, *learn how to do something*, or *get an example*.

- **Heuristics:**
    - **Interrogative Words:** The request is a question, often starting with "What," "How," "Explain," or "Describe."
    - **Goal is Knowledge Acquisition:** The user wants a description, an explanation, or an example to enhance their own understanding. They are not asking the agent to perform the task for them directly.
    - **Keywords:** "what is," "how do I," "explain," "describe," "show me an example of," "what are the steps to," "tell me about."

- **Examples of Information-Seeking Requests:**
    - "How do I write a Python script to parse a log file?"
    - "Explain the process for generating a new KI."
    - "What's an example of a Dockerfile for a web server?"
    - "Describe how the `gtb-validator` works."

- **Appropriate Downstream Skills:** `documentation-retriever`, `example-generator`, `query-brain-db`.
