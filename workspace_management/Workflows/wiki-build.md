---
description: Build a cohesive final output (manuscript, report, presentation script) by compiling information strictly from the LLM-Wiki's pages.
---

# Wiki Build Workflow

Use this workflow when you are ready to construct a draft paper, thesis chapter, blog post, or vision document based on the knowledge already structured in the `.wiki/`.

## Step 1: Define Target Output

Tell the agent what exactly you want to build and which Wiki pages they should use as the foundation.
> "Build the introduction section of the SP7-uORF manuscript. Use the `.wiki/overview.md`, `.wiki/timeline.md`, and the entries under `.wiki/entities/` as your primary sources."

## Step 2: The Outline

The agent should first generate an outline based strictly on the headings and logical flow of the referenced `.wiki/` pages. The user must review and approve this outline.

## Step 3: Drafting (Compilation)

The agent acts as a compiler. Instead of hallucinating bridging text, the agent must:
1. Translate the bullet points and synthesized summaries from the `.wiki/` markdown files into flowing prose.
2. Maintain strict factual alignment with the `.wiki/` ground truth.
3. Automatically append citations where facts were drawn from `.wiki/sources/`.

## Step 4: Review against Ground Truth

Before finalizing, the agent must perform a check:
> "Verify that this generated draft contains no claims that contradict the current state of `.wiki/overview.md`."

## Step 5: Export

The agent will output the final document as an Artifact (`.md` or `.docx` format depending on the tools available) in the project workspace, separate from the `/.wiki/` internal structures.

## Step 6: Auto-Commit

Delegate to the canonical `/lab-commit` workflow. Do NOT write inline `git add` / `git commit` commands here — the lab-commit workflow handles staging, Obsidian symlink verification, INDEX.csv updates, and commit message formatting automatically.
