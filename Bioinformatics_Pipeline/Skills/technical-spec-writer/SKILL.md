name: technical-spec-writer
description: "A comprehensive framework for generating industry-grade, RFC 2119 compliant technical specifications (SPEC.md) for software services, cloud platforms, AI agent systems, and major features. Modeled after OpenAI Symphony's specification standard, it ensures high-quality, language-agnostic contracts for new projects, services, or structural updates, including AI model capability specs, and explicitly covers non-functional requirements."
---

# Technical Specification Writing Guide (Symphony-Grade)

## When to Use This Skill
- You are starting a new project, service, cloud platform, or major feature.
- A user asks to write, refine, or structuralize a technical specification (SPEC.md).
- You need to produce a language-agnostic contract that captures the *what*, *why*, *how*, domain model, failure modes, validation criteria, and expected boundaries before any implementation begins.
- You are defining an API surface, a multi-component system, or a SaaS architecture.

## Core Principles

### RFC 2119 Normative Language
Every SPEC.md MUST use RFC 2119 normative keywords to eliminate ambiguity:

- `MUST` / `MUST NOT` — Absolute requirements. Non-negotiable.
- `REQUIRED` — Synonym for MUST.
- `SHOULD` / `SHOULD NOT` — Strong recommendations. Deviation requires documented justification.
- `RECOMMENDED` — Synonym for SHOULD.
- `MAY` / `OPTIONAL` — Truly optional. Implementations can omit without penalty.

Include the following boilerplate at the top of every SPEC:

```markdown
The key words `MUST`, `MUST NOT`, `REQUIRED`, `SHOULD`, `SHOULD NOT`, `RECOMMENDED`, `MAY`, and
`OPTIONAL` in this document are to be interpreted as described in RFC 2119.

`Implementation-defined` means the behavior is part of the implementation contract, but this
specification does not prescribe one universal policy. Implementations MUST document the selected
behavior.
```

### Language-Agnostic Design
Specifications MUST be implementation-language agnostic. Define *behaviors* and *contracts*, not code. Use pseudocode in `Reference Algorithms` sections only when clarifying complex logic.

### Living Document
Specs SHOULD evolve with the project. Include a `Status:` line (Draft, Review, Active, Deprecated) and a version number.

---

## The 7 Essential Parts of a Technical Specification
A high-quality technical specification MUST contain these core sections to ensure alignment and manage complexity:

### 1. Front Matter
```markdown
# [Service Name] Specification

Status: Draft v1 (language-agnostic)

Purpose: [One sentence defining what this specification covers.]
```
- **Title / Codename:** Short, identifiable name.
- **Author & Status:** Who is responsible and the current document state (Draft, Review, Active).
- **Metadata:** Last updated timestamp, version, and reference links.

### 2. Introduction
- **Context & Problem Statement:** Clearly explain the background and the specific problem being solved. What is the current bottleneck?
- **Project Goals:** Bullet points of the primary objectives and desired outcomes.
- **Non-Goals / Out of Scope:** What are we *not* building? Keep the scope tightly bounded to prevent scope creep.

### 3. Solutions Design & Architecture
- **Global Architecture:** Diagram out the components (use Mermaid.js graphs `graph TD` or `sequenceDiagram`). Show how modules, databases, and APIs interact.
- **Data Models / State:** How will data be structured and held? (e.g., SQL schemas, Vector arrays, Context objects).
- **System Components:** Define the logic flow between subsystems.

### 4. Operational & Technical Requirements
- **Functional Requirements:** Use cases or user stories. What actions must be available to the user/system?
- **Non-Functional Requirements:** 
  - *Performance/Scale:* Latency budgets, ingestion speeds, max throughput.
  - *Security & Integrity:* Guardrails against destructive paths, role limitations, user permissions.
  - *Reliability / Portability:* Hardware/OS limits, graceful degradation, fallback mechanisms.

### 5. Success Evaluation
- **Metrics:** What measurable metrics define success? (e.g., "Error decay rate drops by 50%", "Sub-2-second latency").
- **Verification Plan:** How will this be tested? Unit tests, user acceptance, rollback strategies, or automated CI/CD pipelines.

### 6. Work Plan & Milestones
- **Breakdown of Tasks:** An ordered list of steps to implement the solution. 
- **Priorities & Dependencies:** What must be done first (e.g., foundational database structures) before higher-level logic is built.

### 7. Deliberation & Open Questions
- **Risks & Unknowns:** Highlight missing assumptions, edge cases, and unresolved technical debt or blocking questions. 
- **Trade-offs:** Explain why a certain path was chosen (e.g., choosing SQLite over Pos