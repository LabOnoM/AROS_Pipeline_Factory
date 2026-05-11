---
description: Maintain, lint, and synthesize the LLM-Wiki to ensure consistency and prevent knowledge rot.
---

# Wiki Update & Lint Workflow

// Note: All commands must execute from the active project root.

Run this workflow periodically (e.g., once a week, or after a massive batch of `/wiki-ingest` operations) to ensure the `.wiki/` knowledge base remains structurally sound and conceptually coherent.

## Step 1: Structural Audit (Linting)

Run the following command in the bash terminal to check for basic structural issues in the `.wiki/` directory.

```bash
# // turbo

echo "=== Orphan Pages (No inbound links) ==="
# Find all markdown files (excluding index, log, SCHEMA) and check if they are referenced anywhere else
for file in $(find .wiki -name "*.md" -not -name "index.md" -not -name "log.md" -not -name "SCHEMA.md"); do
    basename=$(basename "$file" .md)
    # Search for the wikilink [[basename]] in other files
    if ! grep -q "\[\[$basename\]\]" -R .wiki/; then
        echo "Orphan detected: $file"
    fi
done
```

## Step 1.5: Agent Version Control (re_gent) Audit

Before making changes, verify that this workspace is protected by the AI audit layer. This acts as a self-healing mechanism for legacy workspaces.

```bash
# // turbo
if [ ! -d ".regent" ]; then
    echo "re_gent audit layer missing. Initializing for legacy workspace..."
    if ! command -v rgt &> /dev/null; then
        go install github.com/regent-vcs/regent/cmd/rgt@latest
    fi
    rgt init --skip-hook
    grep -qxF ".regent/" .gitignore || echo ".regent/" >> .gitignore
    echo "Agent version control deployed."
else
    echo "re_gent audit layer is active."
fi
```

## Step 2: Resolve Orphans & Consistency Checks (Check)

This is the semantic linting phase. Make sure the knowledge base is internally consistent:

1. **Resolve Orphans**: If Step 1 reveals orphans, prompt the LLM to read them and add `[[wikilinks]]` to them from relevant entities.
2. **Conflict Detection**: Prompt the agent to check for logical contradictions.
> "Review the recently modified `.wiki/entities/` and `.wiki/sources/`. Identify if any new findings contradict older statements in the wiki. Flag these contradictions for human review."


## Step 3: Global Synthesis

After ingesting new experimental data or papers, the global narrative may have shifted.
Prompt the LLM agent:
> "Please review the recent entries in `.wiki/log.md`. Based on the newly ingested information, do we need to update the theory outined in `.wiki/overview.md` or append an event to `.wiki/timeline.md`?"

## Step 4: Index Rebuild

Ensure `.wiki/index.md` acts as a complete table of contents.
Prompt the agent:
> "Rebuild `.wiki/index.md` so that it categorizes and links to every file within the `.wiki/` directory."

## Step 5: Auto-Commit

Delegate to the canonical `/lab-commit` workflow. Do NOT write inline `git add` / `git commit` commands here — the lab-commit workflow handles staging, Obsidian symlink verification, INDEX.csv updates, and commit message formatting automatically.
