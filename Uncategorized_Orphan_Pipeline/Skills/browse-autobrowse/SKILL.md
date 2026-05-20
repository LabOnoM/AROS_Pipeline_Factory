---
name: browse-autobrowse
description: >
  Self-improving browser automation via iterative research loops. Runs a browsing task,
  reads the trace, and improves the navigation strategy until it reliably passes.
  Use when you want to build or improve browser automation skills for specific website tasks
  through trial-and-error refinement.
skill-author: Browserbase (adapted for AROS)
license: MIT
original-source: https://github.com/browserbase/skills
---

# AutoBrowse — Self-Improving Browser Skill

Build reliable browser automation skills through iterative experimentation. An inner agent browses the site. You — the outer agent — read what happened and improve the instructions (strategy.md). Repeat until it passes consistently.

## Concept

1. **Define** the task: URL, goal, expected output schema
2. **Run** inner agent with current strategy
3. **Read** the trace — find where it failed
4. **Form one hypothesis** — what single heuristic would have prevented the failure?
5. **Update** strategy.md with the fix
6. **Repeat** until it passes 2+ of the last 3 iterations
7. **Graduate** to a standalone skill

## Setup

```bash
mkdir -p ./autobrowse/tasks ./autobrowse/traces ./autobrowse/reports
```

## Task Definition Template

Create `./autobrowse/tasks/<task-name>/task.md`:
```markdown
# Task: <name>
## URL: <target URL>
## Goal: <what to accomplish>
## Steps: <ordered list of actions>
## Expected Output:
```json
{ "key": "expected_value" }
```
```

## The Loop

### For Each Iteration:

1. **Run the inner agent** — execute the browsing task with current strategy
2. **Read the trace** — identify the exact turn where things went wrong
3. **Form one hypothesis** — what single change would fix it?
4. **Update strategy.md** — keep what worked, fix the failure, add a heuristic
5. **Judge** — did it pass? Progress? If regression, revert and try different hypothesis

### Good Strategies Have:
- **Fast path**: direct URL or shortcuts to skip exploration
- **Step-by-step workflow**: exact sequence with timing notes
- **Site-specific knowledge**: selector IDs, form field names, success indicators
- **Failure recovery**: what to do when X goes wrong

## Rules

- **One hypothesis per iteration** — test one change at a time
- **Build on wins** — keep what worked, add to it
- **Trust the trace** — the inner agent shows exactly what it saw
- **Graduate when stable** — passes 2+ of last 3 iterations

## Graduation

Write to `~/.gemini/skills/<task-name>/SKILL.md` with:
- AROS-compatible frontmatter (name + description)
- Self-contained workflow (not dependent on strategy.md)
- All hard-won site-specific heuristics
- Failure recovery procedures

## AROS Integration Notes

This pattern is valuable for building robust web automation skills for:
- Recurring data extraction from specific websites
- Automated form submission workflows
- Building site-specific scraping strategies that survive layout changes
- Training agentic browsing capabilities through iterative refinement
