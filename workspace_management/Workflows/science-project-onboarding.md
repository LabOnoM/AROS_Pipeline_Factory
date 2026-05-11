---
description: First-time onboarding into a scientific project — audit every file, reconstruct timeline, generate README, set up version control
---

# Science Project Onboarding Workflow

Use this workflow the first time you encounter a new or inherited scientific project folder. The goal is to fully understand the project's mission, hypotheses, results, and progress before writing a single line of new code or running any new analysis.

## Phase 1: Archaeological Audit (Read-Only)

**Do NOT move, rename, or delete anything during this phase.**

1. **Map the folder structure.** List every directory and subdirectory recursively. Note any gaps in numbering (e.g., missing `06.*` folder), empty directories, and unexpected files.
   ```bash
   find . -type d -not -name '.*' | sort
   ```

2. **Build a timestamp registry.** For every non-junk file, extract the modification date and file size. Sort chronologically to reconstruct the true project timeline.
   ```bash
   find . -type f -not -name '._*' -not -name '.DS_Store' \
     \( -name '*.xlsx' -o -name '*.csv' -o -name '*.pzfx' -o -name '*.prism' \
        -o -name '*.pptx' -o -name '*.pdf' -o -name '*.docx' -o -name '*.key' \
        -o -name '*.rtf' -o -name '*.dna' -o -name '*.txt' -o -name '*.tif' \
        -o -name '*.jpeg' -o -name '*.jpg' -o -name '*.png' -o -name '*.czi' \
        -o -name '*.mp4' \) \
     -printf '%TY-%Tm-%Td %TH:%TM  %s  %p\n' | sort
   ```

3. **Extract document contents.** Read every `.docx` (via Python zipfile XML extraction), text file, and small spreadsheet. For PDFs, use `pdftotext`. Never trust file names alone — read the actual content.
   ```python
   # For .docx files:
   import zipfile, xml.etree.ElementTree as ET
   def read_docx(path):
       with zipfile.ZipFile(path) as z:
           tree = ET.fromstring(z.read("word/document.xml"))
           ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
           return "".join([t.text for t in tree.findall(".//w:t", ns) if t.text])
   ```

4. **Read raw data spreadsheets.** Use `openpyxl` (install via conda if needed: `conda run -n base python3 -c "import openpyxl"`) to read every `.xlsx` file's sheet names, headers, and first 20 rows. This reveals the actual experimental conditions, sample names, and measurements.

5. **Identify experimental phases.** Group the file timestamps into chronological clusters. Look for:
   - Gaps of >2 months (potential project pivots)
   - New folder categories appearing suddenly (new assay types adopted)
   - Changes in naming conventions (different lab member took over?)
   - Literature PDFs collected around the same time (reading phase before experiments)

6. **Cross-reference documents against raw data.** Compare what the abstracts/presentations claim vs what the raw data folders actually contain. Flag discrepancies:
   - Results described in abstracts but no matching raw data folder?
   - Raw data folders with no corresponding mention in any presentation?
   - Dates in presentations that don't match file timestamps?

## Phase 2: Documentation

7. **Generate README.md** at the project root containing:
   - Executive summary (current state of the project)
   - Chronological timeline with `[verified]` tags for dates confirmed against file metadata
   - Hypothesis evolution table (H1 → H2 → H3...)
   - Repository structure map with purpose annotations
   - Key sequences/parameters (if molecular biology project)
   - Critical notes and caveats (data integrity observations)
   - Methods and tools inventory

8. **Create `00.RawData/INDEX.csv`** — a machine-readable experiment registry:
   ```csv
   Folder,Date,Phase,Assay,Conditions,CellLine,Status,Notes
   ```

## Phase 3: Version Control Setup

9. **Check filesystem and available tools:**
   ```bash
   df -Th .          # filesystem type
   git --version     # git available?
   git lfs version   # git-lfs available?
   ```

10. **Initialize Git + Git LFS** (if on ext4/APFS with sufficient disk):
    ```bash
    git init
    git lfs install
    ```

11. **Create `.gitignore`** — exclude macOS/Windows junk and Office temp files.

12. **Create `.gitattributes`** — define LFS tracking for large binary files (*.tif, *.czi, *.pptx, *.pzfx, *.dna, etc.).

13. **Initial commit** — stage everything and commit as the historical baseline:
    ```bash
    git add .
    git commit -m "Initial snapshot: project as-found on [DATE]"
    ```

## Phase 5: Agentic Setup

14. **Seed the LLM-Wiki**. Use the `/wiki-ingest` workflow to process the project `README.md` and any critical "Executive Summary" or "Final Report" PDFs identified in Phase 1. This establishes the initial Knowledge Graph.

15. **Generate Project-Specific Rules**. **After** the LLM-Wiki is seeded, the agent shall automatically generate or update the `AGENTS.md` file at the root. 
    - The `AGENTS.md` must contain explicit trigger rules for *every* workflow found in `~/.gemini/antigravity/global_workflows/`.
    - Critically, ensure the `/wiki-research` workflow is registered to trigger when the AI detects gaps in the local `.wiki/` knowledge base, maintaining strict grounding.
    - Importantly, the `/manuscript-write` global workflow MUST be explicitly linked so that the user can ask the agent to automatically extract all experimental data, generate figures, and iteratively write the paper.
    - Enforce **Workspace Hygiene**: Instruct agents that diagnostic, ad-hoc, or one-off scratch scripts MUST NOT be generated in the root project directory, but instead strictly isolated to the designated IDE scratch directory (`~/.gemini/antigravity/brain/<id>/scratch/`).
    - Explicitly add an "LLM-Wiki Context Injection" section to the generated `AGENTS.md` that enforces:
      1. **Wiki-First Resolution**: Before answering domain-specific questions, agents MUST search the local `.wiki/` directory. External knowledge should only supplement, not replace, wiki-grounded answers.
      2. **Automatic Workflow Routing**: When the user's message matches a wiki workflow pattern, automatically suggest the relevant `/wiki-*` workflow (e.g., "Research X" → `/wiki-research`, "What does the wiki say about X" → `/wiki-query`).
    - The rule generation must be based on the established LLM-Wiki. (e.g., If the wiki defines "RNA-Seq" as a core methodology, create a trigger for RNA-Seq data commits).
    - Ensure it includes the "Self-Evolution" rules (`/science-project-onboarding`, etc.).

16. **Initialize the Lessons Learned Log**. Create `.wiki/system/lessons-learned.md` to track the evolution of project rules and operational logic.

17. **Obsidian Compatibility Verification**. Obsidian natively ignores dot-prefixed folders (like `.wiki`). To ensure researchers can access their knowledge base directly from Obsidian's graphical File Explorer, you MUST create a visible symbolic link at the project root pointing to the `.wiki` folder:
    ```bash
    # // turbo
    ln -sfn .wiki Wiki
    ```

## Phase 6: Ongoing Maintenance

17. From this point forward, use the `lab-commit` workflow for daily experiment commits.
18. Use `git mv` (via `lab-reorganize` workflow) for any file moves to preserve history.
19. Update `INDEX.csv` when adding new experiment folders.
20. **Compounding Knowledge**: Run `/wiki-update` weekly to resolve orphans and link new experiment results to established biological entities.
