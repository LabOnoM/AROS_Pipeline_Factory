---
name: spec-first-development-policy
description: "Enforces that every major AROS system component, cloud service, or architectural module MUST have a reviewed SPEC.md before implementation begins. Prevents premature coding, ensures architectural alignment, and creates a permanent record of design decisions."
---

# Spec-First Development Policy

## Policy Statement

Every major AROS system component, cloud service, or architectural module MUST have a `SPEC.md`
document that is reviewed and approved before any implementation code is written.

## Scope

This policy applies when ANY of the following conditions are true:

1. A new repository or major module is being created.
2. A new cloud service, API, or backend component is being designed.
3. A significant architectural change affects multiple existing components.
4. A new data model, database schema, or domain entity is being introduced.
5. A new external integration (billing, auth, third-party API) is being added.

## Exemptions

This policy does NOT apply to:

- Bug fixes and patches to existing code.
- Minor UI tweaks, styling changes, or copy edits.
- Scratch scripts, one-off analysis, or exploratory prototyping.
- Documentation-only changes (README, wiki, KI updates).
- Skill, Policy, or Workflow authoring (these have their own formats).

## Requirements

### Before Implementation

1. The agent MUST create a `SPEC.md` file using the `technical-spec-writer` skill.
2. The SPEC.md MUST include, at minimum:
   - RFC 2119 normative language boilerplate.
   - Problem Statement with explicit boundaries.
   - Goals and Non-Goals.
   - Domain Model with typed entity fields.
   - Failure Model with named failure classes and recovery behaviors.
   - Implementation Checklist with conformance tiers.
3. The SPEC.md MUST be committed to the repository root (or module root) before implementation
   code is committed.
4. The SPEC.md MUST be presented to the user for review before execution begins.

### During Implementation

5. Implementation code MUST conform to the SPEC.md contracts. Any deviation MUST be reflected
   back into the SPEC.md as an amendment with a changelog note.
6. The SPEC.md SHOULD be referenced in commit messages when implementing a specific section
   (e.g., "Implement SPEC Section 5.2: Multi-Region Routing").

### After Implementation

7. The SPEC.md MUST be updated to reflect the final implementation state if any deviations
   occurred during development.
8. The Implementation Checklist MUST be verified — every "REQUIRED for MVP" item should be
   testable and tested.

## Rationale

- **Prevents wasted effort:** A reviewed spec catches design flaws before hundreds of lines of
  code are written.
- **Creates institutional memory:** SPECs serve as permanent architectural records that survive
  team changes.
- **Enables parallel work:** Multiple agents or developers can implement different sections of
  the same spec concurrently without conflicts.
- **Improves LLM agent quality:** Agents produce dramatically better code when given a precise
  spec to follow rather than a vague prompt.

## Enforcement

Agents SHOULD check for the existence of a `SPEC.md` in the target repository before beginning
any major implementation task. If no SPEC.md exists, the agent MUST create one using the
`technical-spec-writer` skill and request user approval before proceeding.

## References

- Skill: `technical-spec-writer` — The framework for generating SPEC.md documents.
- KI: `spec_writing_reference` — Patterns and anti-patterns for high-quality specifications.
- External: [OpenAI Symphony SPEC.md](https://github.com/openai/symphony/blob/main/SPEC.md)
