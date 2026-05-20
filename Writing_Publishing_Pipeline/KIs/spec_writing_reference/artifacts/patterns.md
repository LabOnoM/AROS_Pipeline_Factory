# SPEC.md Writing Reference & Patterns

## Overview
This Knowledge Item captures hard-won patterns for writing industry-grade technical specifications, derived from studying OpenAI Symphony's SPEC.md (80KB, 18 sections) and authoring the AROS Cloud Federation SPEC.md.

## Key Structural Patterns from OpenAI Symphony

### 1. The RFC 2119 Boilerplate
Every specification MUST open with the normative language declaration. This is not optional decoration — it creates legally precise, machine-parseable requirements.

```markdown
The key words `MUST`, `MUST NOT`, `REQUIRED`, `SHOULD`, `SHOULD NOT`, `RECOMMENDED`, `MAY`, and
`OPTIONAL` in this document are to be interpreted as described in RFC 2119.
```

### 2. The "Important Boundary" Pattern
Symphony uses explicit boundary blocks to prevent scope creep. This is one of the most valuable patterns because it forces the author to define what the system does NOT do.

```markdown
Important boundary:

- Symphony is a scheduler/runner and tracker reader.
- Ticket writes are typically performed by the coding agent using tools.
```

**Why it works:** Without explicit boundaries, every reviewer interprets scope differently. The boundary block is a contract.

### 3. Entity Definition Format
Symphony defines every domain entity with typed fields. This pattern eliminates ambiguity about data shapes:

```markdown
#### 4.1.1 Issue

Normalized issue record used by orchestration.

Fields:

- `id` (string)
  - Stable tracker-internal ID.
- `priority` (integer or null)
  - Lower numbers are higher priority; null sorts last.
- `state` (string)
  - Current tracker state name.
- `labels` (list of strings)
  - Normalized to lowercase.
```

**Critical rules:**
- Every field has an explicit type.
- Nullable fields are marked `(type or null)`.
- Enums list all valid values.
- Normalization rules (e.g., "lowercase") are stated inline.

### 4. The Conformance Profile Pattern
Symphony splits its validation matrix into three tiers:

1. **Core Conformance** — Tests REQUIRED for all implementations.
2. **Extension Conformance** — Tests REQUIRED only for optional features that are shipped.
3. **Real Integration Profile** — Environment-dependent smoke tests RECOMMENDED before production.

This pattern lets implementers know exactly what "done" means at each quality level.

### 5. The State Machine Pattern
For any component with lifecycle states, Symphony defines explicit states and transition triggers:

```markdown
### 7.1 Issue Orchestration States

1. `Unclaimed` — Not running, no retry scheduled.
2. `Claimed` — Reserved to prevent duplicate dispatch.
3. `Running` — Worker task exists.
4. `RetryQueued` — Retry timer exists.
5. `Released` — Claim removed.
```

### 6. The Failure Taxonomy Pattern
Symphony categorizes failures into named classes, then maps each class to a recovery behavior:

```markdown
### 14.1 Failure Classes
1. `Workflow/Config Failures`
2. `Workspace Failures`
3. `Agent Session Failures`
4. `Tracker Failures`
5. `Observability Failures`

### 14.2 Recovery Behavior
- Dispatch validation failures: Skip new dispatches. Keep service alive.
- Worker failures: Convert to retries with exponential backoff.
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Correct Approach |
|-------------|-------------|-----------------|
| Vague requirements ("must be fast") | Untestable | "MUST respond in < 200ms at p99" |
| Missing Non-Goals | Scope creep | Explicit "Non-Goals" section |
| Untyped fields | Ambiguous data contracts | Every field has `(type)` |
| No failure model | System crashes are surprises | Named failure classes + recovery |
| Implementation-specific language | Locks out alternative implementations | Language-agnostic pseudocode |
| Monolithic checklist | Can't tell MVP from nice-to-have | Tiered conformance profiles |

## Worked Example
The AROS Cloud Federation SPEC.md (`/home/ubuntu4/GitHub/AROS-Cloud-Federation/SPEC.md`) demonstrates all of these patterns applied to a real cloud SaaS platform with:
- 6 domain entities (Organization, API Key, Token Usage Log, Brain Snapshot, Marketplace Skill, Synthetic Dataset)
- 5 service specifications (LLM Gateway, Brain Federation, Billing, Marketplace, Synthetic Data)
- 5 failure classes with recovery behaviors
- 3-tier implementation checklist
