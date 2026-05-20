---
name: browse-ui-test
description: >
  AI-powered adversarial UI testing via the browse CLI. Analyzes git diffs to test only what changed,
  or explores the full app to find bugs. Tests functional correctness, accessibility, responsive layout,
  and UX heuristics. Use when the user asks to test UI changes, QA a pull request, audit accessibility,
  or run exploratory testing on a web application.
skill-author: Browserbase (adapted for AROS)
license: MIT
original-source: https://github.com/browserbase/skills
---

# UI Test — Agentic UI Testing

Test UI changes in a real browser. Your job is to **try to break things**, not confirm they work.

## Three Workflows

- **Diff-driven** — analyze a git diff, test only what changed
- **Exploratory** — navigate the app, find bugs the developer didn't think about
- **Parallel** — fan out independent test groups across multiple browser sessions

## Prerequisites

```bash
which browse || npm install -g @browserbasehq/browse-cli
mkdir -p .context/ui-test-screenshots
```

## Planning: Three Rounds Before Execution

**Complete all three planning rounds before launching any tests:**

**Round 1 — Functional:** What are the core user flows? Write each test as: action → expected result.

**Round 2 — Adversarial:** What did Round 1 miss? Consider: error paths, empty states, race conditions, edge inputs (empty, huge, special chars, rapid clicks).

**Round 3 — Coverage gaps:** What about: accessibility (axe-core, keyboard-only), mobile viewports, console errors, visual consistency?

**Deduplicate** into a numbered list, assign to groups, then execute.

## Testing Philosophy

- **Try to break every feature.** Don't just check "does the button exist?" — click it twice rapidly, submit empty forms, paste 500 characters.
- **Test what the developer didn't think about.** Empty states, error recovery, keyboard-only navigation.
- **Every assertion must be evidence-based.** Compare before/after snapshots. Never report PASS without concrete evidence.

## Assertion Protocol

### Step Markers
```
STEP_PASS|<step-id>|<evidence>
STEP_FAIL|<step-id>|<expected> → <actual>|<screenshot-path>
```

### Verification Hierarchy (strongest → weakest)
1. **Deterministic check** — `browse eval` returns structured data (axe-core violations, console errors, element count)
2. **Snapshot element match** — specific element with specific role/text exists in accessibility tree
3. **Before/after comparison** — snapshot before action, act, snapshot after, verify change
4. **Screenshot + visual judgment** — only for visual-only properties (color, spacing, layout)

### Before/After Pattern (Core Loop)
```bash
browse snapshot            # BEFORE: record state
browse click @0-12         # ACT
browse snapshot            # AFTER: compare changes
# ASSERT: emit STEP_PASS or STEP_FAIL
```

## Workflow A: Diff-Driven Testing

### Phase 1: Analyze Diff
```bash
git diff --name-only HEAD~1
git diff HEAD~1 -- <file>
```

Categorize: component (tsx/jsx), route (pages/), style (css), form, modal, navigation.

### Phase 2: Map Files to URLs (by framework)

| Framework | Port | Pattern |
|-----------|------|---------|
| Next.js App Router | 3000 | `app/dashboard/page.tsx` → `/dashboard` |
| Vite | 5173 | Check router config |
| SvelteKit | 5173 | `src/routes/+page.svelte` → `/` |

### Phase 3: Verify Dev Server
```bash
for port in 3000 3001 5173 4200 8080; do
  s=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port" 2>/dev/null)
  if [ "$s" != "000" ]; then echo "Dev server on port $port (HTTP $s)"; fi
done
```

### Phase 4: Execute Tests
```bash
browse env local
browse open http://localhost:3000/path
# Before/after pattern for each test
```

### Phase 5: Report Results
```
## UI Test Results
Tests: 20 | Passed: 14 | Failed: 4 | Skipped: 2 | Pass rate: 70%
```

## Workflow B: Exploratory Testing

No diff — explore and break:
1. Discover the app, navigate everything
2. Apply adversarial patterns (forms, modals, keyboard, errors)
3. Run deterministic checks (axe-core, console, broken images)
4. Report findings with reproduction steps

## Deterministic Checks

| Check | What it catches | How |
|-------|----------------|-----|
| axe-core | WCAG violations | `browse eval` with axe-core script |
| Console errors | Runtime exceptions | Capture console output |
| Broken images | Missing image loads | Check `naturalWidth === 0` |
| Form labels | Inputs without accessible labels | Check `hasLabel` property |

## Adversarial Test Patterns

Apply to every interactive element:
- **Forms**: empty submit, XSS payloads, 500+ char strings, rapid double-submit
- **Modals**: Escape key, click outside, focus trap verification
- **Navigation**: broken links, 404 pages, back button after form submit
- **Keyboard**: Tab-only flow through all interactive elements
- **Mobile**: viewport at 375px width, check for overflow

## Best Practices

1. Be adversarial — try to break things
2. Every assertion needs evidence (snapshot ref, eval result, before/after diff)
3. Screenshot every failure immediately
4. Deterministic checks first, visual judgment last
5. `browse stop` when done
6. Report failures with exact reproduction steps

## AROS Integration

This skill is ideal for:
- QA testing SCRIB, BSGOU, or other web apps before deployment
- Pre-commit UI regression testing via `/qa-system-audit` workflow
- Validating AROS Dashboard UI changes
