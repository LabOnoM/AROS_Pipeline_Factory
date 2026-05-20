name: debug-hypothesis
description: Use when debugging any non-trivial bug — wrong output, crash, flaky test, performance regression, or "it works locally but not in CI." Forces a scientific-method loop (Observe → Hypothesize → Experiment → Conclude) so the agent stops guessing and starts reasoning. Prevents the #1 AI debugging failure mode — bulldozing through a wrong idea instead of falsifying it.
original-source: addyosmani/agent-skills/debugging-and-error-recovery
---

# Hypothesis-Driven Debugging

A four-phase loop that turns debugging from "try random fixes and hope" into
a disciplined investigation. Each phase has a goal, hard rules, and a
rationalization table for the excuses an agent will invent to skip it.

The core principle: **you may not write a fix until you have evidence that
your hypothesis is correct.** Guessing is not debugging.

## When to Use

- A test fails and the cause is not immediately obvious
- The same bug has been "fixed" twice and came back
- The agent tried a fix that didn't work — stop it from trying another
- A crash or error message you haven't seen before
- Performance regression with no obvious culprit
- Behavior differs between environments (local vs CI, dev vs prod)
- The agent is stuck in a loop, applying the same wrong fix

## When NOT to Use

- Typos, missing imports, or syntax errors — just fix them
- Build failures with an obvious single-line cause
- Compiler/linter messages that tell you exactly what and where
- You already know the root cause and just need to write the fix

If the bug survived one fix attempt, switch to this skill immediately.

## The Debug Loop

```
  OBSERVE  ──▶  HYPOTHESIZE  ──▶  EXPERIMENT  ──▶  CONCLUDE
     │              │                  │               │
     ▼              ▼                  ▼               ▼
  Gather          List 3-5         One minimal       Root cause
  symptoms,       possible         test per          confirmed
  reproduce       causes +         hypothesis,       or loop
  reliably        evidence         max 5 lines       back
     │              │                  │               │
     └──────────────┴──────────────────┴───────────────┘
              write everything to DEBUG.md
```

Hard rules:

1. Everything gets written to `DEBUG.md`. Context compaction will eat your
   reasoning if it only lives in the conversation.
2. You may not write fix code during Observe, Hypothesize, or Experiment.
3. You may not skip Hypothesize. "I think I know what it is" is a hypothesis —
   write it down and test it like the others.
4. Each experiment changes at most 5 lines. If your experiment needs more,
   your hypothesis is too vague — split it.

## Phase 1: OBSERVE

**Goal.** Collect raw facts. Reproduce the bug. Separate what you *know*
from what you *assume*.

**Steps.**

1. Reproduce the bug. Get the exact error message, stack trace, or wrong output.
   If you cannot reproduce it, that is your first finding.
2. Find the minimal reproduction. Strip away unrelated code until the bug
   still appears.
3. Record the environmen