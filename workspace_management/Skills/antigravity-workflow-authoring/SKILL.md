---
name: antigravity-workflow-authoring
description: "Canonical specification for authoring workflow .md files that are fully compatible with the Google Antigravity AI IDE. Covers filename conventions, YAML frontmatter requirements, content size limits, structural patterns, and the KI-companion pattern for large workflows."
license: MIT
skill-author: AROS-System-Architect
version: 1.0
tags: [workflow, ide, authoring, format, antigravity]
---

# Skill: Antigravity Workflow Authoring

**Version:** 1.0
**ID:** AROS-SKILL-WORKFLOW-AUTHORING-V1

## 1. Purpose

This skill defines the **mandatory format specification** for creating workflow `.md` files that are recognized, indexed, and executable by the Google Antigravity AI IDE. Failure to follow these rules results in workflows being invisible to the IDE's `/slash-command` system or displaying red-box validation errors.

## 2. Workflow File Location

All workflow files MUST be placed in:
```
~/.gemini/antigravity/global_workflows/<workflow-name>.md
```

## 3. Filename Convention (MANDATORY)

| Rule | Specification |
|------|---------------|
| **Format** | `kebab-case.md` (lowercase, hyphens only) |
| **Trigger mapping** | Filename = slash trigger. `grant-write.md` → `/grant-write` |
| **Forbidden** | Underscores (`_`), CamelCase, spaces, uppercase letters |
| **Examples** | ✅ `kakenhi-annual-report.md` ❌ `KAKENHI_annual_report_pipeline.md` |

> [!CAUTION]
> The IDE derives the `/slash-command` trigger directly from the filename. If the filename does not match, the workflow will NOT appear in the IDE's autocomplete or workflow list.

## 4. YAML Frontmatter (MANDATORY)

Every workflow file MUST begin with a YAML frontmatter block containing at minimum a `description` field:

```yaml
---
description: Short, single-sentence description of what this workflow does.
---
```

### Constraints

| Field | Requirement |
|-------|-------------|
| `description` | **REQUIRED**. Single sentence, max ~250 characters. |
| Delimiter | Must use exactly `---` on its own line (no spaces, no extra dashes). |
| Position | Must be the **very first content** in the file (line 1). |
| Encoding | UTF-8. Em-dashes (`—`), Japanese characters are OK. |

> [!WARNING]
> Workflows **without** YAML frontmatter will NOT be recognized by the IDE. They will be treated as plain markdown files and excluded from the `/` command autocomplete.

## 5. Content Size Limits (CRITICAL)

Based on empirical analysis of all working workflows in production:

| Metric | Safe Range | Hard Limit | Action if Exceeded |
|--------|------------|------------|-------------------|
| **File size** | 1–8 KB | ~10 KB | Split into workflow + KI companion |
| **Line count** | 20–150 lines | ~230 lines | Split into workflow + KI companion |
| **Description** | 40–200 chars | 250 chars | Truncate or simplify |

> [!CAUTION]
> Exceeding the content size limit causes a **red box validation error** in the IDE's workflow preview. The workflow may still appear in the list but its content will be flagged as invalid.

### The KI-Companion Pattern (for large workflows)

When a workflow exceeds ~8KB, split it into two files:

1. **Workflow file** (`~/.gemini/antigravity/global_workflows/<name>.md`): Lean orchestration steps only. Include a "Required AROS Context" section that instructs the agent to load the companion.
2. **KI companion artifact** (`~/.gemini/antigravity/knowledge/<ki_name>/artifacts/<Reference>.md`): All heavy reference material — tables, code templates, detailed specifications, rubrics.

```markdown
## Required AROS Context

Before execution, load the companion reference guide:
- **KI**: `read_ki_document(ki_name="<ki_name>", document_path="artifacts/<Reference>.md")`
```

## 6. Structural Template

```markdown
---
description: <Single sentence, max 250 chars>
---

# `/trigger-name` — Human-Readable Workflow Title

> Brief context: trigger conditions, input/output summary.

## Required AROS Context

Before execution, ensure the following context is loaded:
- **KIs**: `ki_name_1`, `ki_name_2`
- **Skills**: `skill-name-1`, `skill-name-2`
- **Policies**: `policy_name_1`

## Pre-Conditions Checklist

1. Condition 1
2. Condition 2

## Step 1: First Action

Instructions for the agent.

## Step 2: Second Action

Instructions for the agent.

## Step N: Final Action

Delegate to `/lab-commit` for archival.
```

## 7. Annotation Conventions

The IDE recognizes special annotations that control auto-execution:

| Annotation | Scope | Effect |
|------------|-------|--------|
| `// turbo` | Single step | The next `run_command` can auto-run (`SafeToAutoRun=true`) |
| `// turbo-all` | Entire workflow | ALL `run_command` steps can auto-run |

Place annotations on their own line, immediately before or at the start of the relevant section.

## 8. Anti-Patterns (Common Mistakes)

| Anti-Pattern | Why It Fails | Fix |
|--------------|-------------|-----|
| Filename with underscores: `my_workflow.md` | IDE cannot derive `/my_workflow` trigger | Use `my-workflow.md` |
| No YAML frontmatter | IDE ignores the file entirely | Add `---\ndescription: ...\n---` |
| File >10KB with inline tables/code | Red box overflow error | Extract to KI companion |
| Using `---` extensively as section separators | Can confuse YAML parser in some edge cases | Use `##` headings for separation |
| Hardcoded paths in workflow steps | Breaks on other PCs/workspaces | Use `{PLACEHOLDER}` variables or `~/.gemini/` paths |
| Inline git commands | Conflicts with `/lab-commit` governance | Delegate to `/lab-commit` |

## 9. Validation Checklist

Before deploying a new workflow, verify:

- [ ] Filename is kebab-case, matches the intended `/trigger`
- [ ] YAML frontmatter present with `description` field (≤250 chars)
- [ ] File size ≤ 8KB (or split with KI companion)
- [ ] Line count ≤ 150 (or split with KI companion)
- [ ] No hardcoded researcher/project data (use `{PLACEHOLDERS}`)
- [ ] No hardcoded absolute paths (use `~/.gemini/` or relative paths)
- [ ] Heavy reference material extracted to KI artifact
- [ ] Final step delegates to `/lab-commit` (not inline git commands)
- [ ] File copied to `~/.gemini/antigravity/global_workflows/`
- [ ] Trigger registered in workspace `AGENTS.md`

## 10. Production Reference Data

Size distribution of all 21 production workflows (as of 2026-05-11):

```
Percentile | Size    | Lines
-----------|---------|------
Min        | 1.2 KB  | 23
25th       | 1.9 KB  | 36
Median     | 3.1 KB  | 52
75th       | 5.7 KB  | 133
Max        | 9.7 KB  | 232
```

*Last Updated: 2026-05-11 | AROS v2.0*
