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

3. **Extract document contents.** Read every `.docx` (via Python `zipfile` XML extraction or `python-docx`), text file, and small spreadsheet. Never trust file names alone — read the actual content. (Note: PDF extraction is strictly handled in Phase 1.5 per LAW 3).

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

## Phase 1.5: PDF Indexing & Parsing (MANDATORY)

> **LAW 3 Enforcement**: All PDFs must be routed through the `literature-ingestion` pipeline before their content is consumed.

7. **Index and Parse all PDFs**:
   1. Scan the entire workspace for all `.pdf` files.
   2. For each PDF, check if a corresponding `.md` exists in `00.RawData/Literature/03_Parsed_Markdown/`. If not, copy the raw PDF to `02_Raw_PDFs/`.
   3. Run the conversion script (which handles its own dependency installation and self-healing):
      ```bash
      # // turbo
      python3 ~/.gemini/skills/literature-ingestion/scripts/pdf_converter.py
      ```

## Phase 2: Documentation

7. **Generate README.md** at the project root containing:
   - Executive summary (current state of the project)
   - Chronological timeline with `[verified]` tags for dates confirmed against file metadata
   - Hypothesis evolution table (H1 → H2 → H3...)
   - Repository structure map with purpose annotations
   - Key sequences/parameters (if molecular biology project)
   - Critical notes and caveats (data integrity observations)
   - Methods and tools inventory

8. **Create a Project Registry** — a machine-readable tracking mechanism in `00.RawData/`. 
   - For standard laboratory projects, create `00.RawData/INDEX.csv`:
     ```csv
     Folder,Date,Phase,Assay,Conditions,CellLine,Status,Notes
     ```
   - For computational or factory-level projects, create `00.RawData/PIPELINE_REGISTRY.md` with appropriate Markdown table headers (e.g., Pipeline, Description, Target Workflows).

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

## Phase 4: Agent Version Control (re_gent)

14. **Check and Initialize re_gent**. Ensure all AI agent activity is auditable via the `re_gent` version control system. This step implements the **Conda-Gated Self-Healing Pattern** (L0→L1→L2) per SPEC §4.4.
    ```bash
    # // turbo

    # --- L0: Ensure Conda ---
    if ! command -v conda &> /dev/null; then
        if [ -f "$HOME/miniconda3/bin/conda" ]; then
            eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
        elif [ -f "$HOME/anaconda3/bin/conda" ]; then
            eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
        else
            echo "  [WARN] Conda not found. Bootstrapping Miniconda3..."
            curl -fsSL --max-time 120 "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-$(uname -m).sh" \
                -o /tmp/miniconda.sh && bash /tmp/miniconda.sh -b -u -p "$HOME/miniconda3" && \
                eval "$($HOME/miniconda3/bin/conda shell.bash hook)" && rm -f /tmp/miniconda.sh
        fi
    fi

    # --- L1: Activate aros-base ---
    if command -v conda &> /dev/null; then
        eval "$(conda shell.bash hook)"
        if ! conda activate aros-base 2>/dev/null; then
            CMD=$(command -v mamba &>/dev/null && echo "mamba" || echo "conda")
            AROS_YML="$HOME/.gemini/environments/aros-base.yml"
            [ ! -f "$AROS_YML" ] && AROS_YML="01.Shared_Assets/Environments/aros-base.yml"
            [ ! -f "$AROS_YML" ] && AROS_YML="$(find ~ -maxdepth 4 -name 'aros-base.yml' -print -quit 2>/dev/null)"
            if [ -n "$AROS_YML" ]; then
                $CMD env create -f "$AROS_YML" -y && conda activate aros-base
            else
                $CMD create -n aros-base python=3.11 git pandoc go -c conda-forge -y && conda activate aros-base
            fi
        fi
    fi

    # --- L2: re_gent deployment ---
    RGT_BIN=""
    command -v rgt &> /dev/null && RGT_BIN="$(command -v rgt)"
    [ -z "$RGT_BIN" ] && [ -x "$HOME/go/bin/rgt" ] && RGT_BIN="$HOME/go/bin/rgt"

    if [ -z "$RGT_BIN" ] && command -v go &> /dev/null; then
        GOBIN="${CONDA_PREFIX:-$HOME/.local}/bin" go install github.com/regent-vcs/regent/cmd/rgt@latest 2>/dev/null && \
            RGT_BIN="${CONDA_PREFIX:-$HOME/.local}/bin/rgt" || \
            echo "  [WARN] rgt compilation failed. Skipping re_gent."
    fi

    if [ -n "$RGT_BIN" ]; then
        "$RGT_BIN" init --skip-hook 2>/dev/null && \
            echo "✅ re_gent initialized." || \
            echo "  [WARN] rgt init failed. Continuing without re_gent."
    fi
    ```

15. **Generate `.regentignore` and update `.gitignore`**. Use the `regent-governance` skill to generate the `.regentignore` file (excludes scientific data, OS junk, and build artifacts from the audit layer). Then add `.regent/` to `.gitignore`.
    ```bash
    # // turbo
    [ ! -f .regentignore ] && echo "node_modules/
.git/
.regent/
__pycache__/
*.pyc
*.tif
*.tiff
*.czi
*.nd2
*.bam
*.fastq.gz
*.raw
*.mzML
*.h5
*.hdf5
*.pptx
*.xlsx
*.docx
.DS_Store
Thumbs.db
._*
~\$*" > .regentignore
    grep -qxF ".regent/" .gitignore 2>/dev/null || echo ".regent/" >> .gitignore
    ```

## Phase 5: Agentic Setup

17. **Seed the LLM-Wiki**. Use the `/wiki-ingest` workflow to process the project `README.md` and ALL parsed PDFs generated from Phase 1.5. This establishes the initial Knowledge Graph.

18. **Generate Project-Specific Rules**. **After** the LLM-Wiki is seeded, generate/update the `AGENTS.md` file at the project root.
    - Register all global workflows from `~/.gemini/antigravity/global_workflows/`
    - Link `/wiki-research` for gap detection, `/manuscript-write` for paper generation
    - Enforce **Workspace Hygiene**: scratch scripts → `~/.gemini/antigravity/brain/<id>/scratch/`
    - Add **Wiki-First Resolution** and **Automatic Workflow Routing** rules
    - Include Self-Evolution rules (`/science-project-onboarding`, etc.)
    - **Enforce Large Artifact Generation Rules**: Explicitly state that generating massive markdown files, HTML reports, or documents exceeding 3000 words must use a programmatic intermediary (e.g. Python scripts) rather than direct LLM generation.

19. **Initialize the Lessons Learned Log**. Create `.wiki/system/lessons-learned.md` to track the evolution of project rules and operational logic.

20. **Obsidian Compatibility Verification**. Obsidian natively ignores dot-prefixed folders (like `.wiki`). To ensure researchers can access their knowledge base directly from Obsidian's graphical File Explorer, you MUST create a visible symbolic link at the project root pointing to the `.wiki` folder:
    ```bash
    # // turbo
    ln -sfn .wiki Wiki
    ```

## Phase 6: Ongoing Maintenance

21. From this point forward, use the `lab-commit` workflow for daily experiment commits.
22. Use `git mv` (via `lab-reorganize` workflow) for any file moves to preserve history.
23. Update the Project Registry (e.g., `INDEX.csv` or `PIPELINE_REGISTRY.md`) when adding new folders.
24. **Compounding Knowledge**: Run `/wiki-update` weekly to resolve orphans and link new experiment results to established biological entities.
