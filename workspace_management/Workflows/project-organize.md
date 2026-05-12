---
description: Audit and reorganize the project structure — clean root clutter, enforce naming conventions, and maintain folder hierarchy
---

# Project Organization Workflow

// Note: All commands must execute from the active project root.

Use this workflow periodically (e.g., monthly or before a major presentation/submission) to audit the project structure and fix any organizational drift.

## Canonical Folder Structure

This is the **authoritative** layout. Every file in the project should live in one of these locations. If a file doesn't fit, create a new numbered folder under `00.RawData/` or discuss extending this standard.

```
2021_Weng_AS/
├── 00.RawData/                         # PRIMARY DATA — never rename internals, only add
│   ├── 01.PCR/                         #   RT-PCR gel images + Sanger sequencing
│   ├── 02.qPCR/                        #   Quantitative PCR raw output
│   ├── 03.wb/                          #   Western blot images + quantification
│   ├── 04.CLS/                         #   Confocal / fluorescence microscopy
│   ├── 05.FCS/                         #   Flow cytometry (FACS) data
│   ├── 07.differentiation/             #   Differentiation assays (ALP, Alizarin Red, etc.)
│   ├── 08.Prolifration/                #   Cell proliferation / counting
│   ├── 09.HisTAG/                      #   His-tag pull-down / IP experiments
│   ├── 10.CT_Results/                  #   Micro-CT bone analysis
│   ├── ComputionalBiology/             #   In-silico analysis (AlphaFold3, etc.)
│   ├── Pairs/                          #   mCherry reporter time-series (qPCR + WB)
│   ├── Zeiss_Aptome3/                  #   Structured illumination raw CZI files
│   └── INDEX.csv / PIPELINE_REGISTRY.md #   Project registry (ALWAYS update this)
│
├── 01.Materials/                       # CONSTRUCTS & CLONING
│   ├── PlanA_The_Cheapest/             #   Cloning strategy A
│   ├── PlanB_The_Fastest/              #   Cloning strategy B
│   ├── PlanC_The_Mild/                 #   Cloning strategy C
│   ├── PlanC_The_Mild BspDI/           #   PlanC variant
│   ├── Sequences/                      #   All nucleotide/protein sequence docs
│   ├── Primers/                        #   Master primer registries
│   └── backup/                         #   Legacy/backup materials
│
├── plasmid/                            # PLASMID MAPS (SnapGene .dna, VectorBuilder .pdf)
│
├── Articles/                           # LITERATURE
│   ├── 01.Review&Mechanism/            #   AS review papers
│   ├── 02.ImportantmentMarkersWithAS/  #   Bone marker + AS papers
│   ├── 03.O-GlcNAc&AS/                #   O-GlcNAcylation × splicing papers
│   └── 04.UTR_Function/               #   5'UTR / uORF function papers
│
├── ppt/                                # PRESENTATIONS (chronological)
│   └── conference/                     #   Conference posters + abstracts
│
├── Runx2 Transcripts/                  # SnapGene shared collection (Runx2 reference)
├── package/                            # SnapGene package files (Sp7 reference)
│
├── Manuscripts/                        # Paper drafts, figure plans, and abstracts


├── README.md                           # Project documentation
├── .gitignore                          # Git ignore rules
├── .gitattributes                      # Git LFS tracking rules
└── .agents/workflows/                  # Automation workflows
```

## Step 1: Audit — Find Misplaced Files

Run this diagnostic to find files that are in the wrong location:

```bash
echo "=== Root-level files that should be moved ==="
# PDFs at root (should be in Articles/ or ppt/)
ls -1 *.pdf 2>/dev/null

# Sequence .docx at root (should be in 01.Materials/Sequences/)
ls -1 SP7-sequence.docx Sp7_Sequence.docx TranscriptSeq.docx 2>/dev/null

echo ""
echo "=== macOS junk still tracked by git ==="
git ls-files '*.DS_Store' '._*' 2>/dev/null | head -20

echo ""
echo "=== Empty directories ==="
find . -type d -empty -not -path './.git/*' 2>/dev/null

echo ""
echo "=== Files with spaces or special chars that may cause issues ==="
find . -not -path './.git/*' -name '*[（）【】]*' -type f 2>/dev/null | head -10

echo ""
echo "=== New experiment folders not yet in Project Registry ==="
# Dynamic Registry Discovery — works with both INDEX.csv and PIPELINE_REGISTRY.md
if [ -f "00.RawData/INDEX.csv" ]; then
    REGISTRY_FILE="00.RawData/INDEX.csv"
elif [ -f "00.RawData/PIPELINE_REGISTRY.md" ]; then
    REGISTRY_FILE="00.RawData/PIPELINE_REGISTRY.md"
else
    REGISTRY_FILE=""
fi
if [ -n "$REGISTRY_FILE" ]; then
  for dir in 00.RawData/*/; do
    find "$dir" -maxdepth 1 -type d -name '20*' 2>/dev/null
  done | while read folder; do
    basename=$(echo "$folder" | sed 's|00.RawData/||')
    grep -q "$basename" "$REGISTRY_FILE" 2>/dev/null || echo "  NOT INDEXED: $folder"
  done
else
  echo "  (No registry file found in 00.RawData/)"
fi
```

## Step 2: Clean macOS Metadata

// turbo
```bash
# Remove macOS junk from git tracking (files stay on disk but .gitignore handles them)
git rm -r --cached '*.DS_Store' 2>/dev/null
find . -name '._*' -not -path './.git/*' -exec git rm --cached {} \; 2>/dev/null

git commit -m "CLEAN: Remove macOS metadata files from git tracking"
```

## Step 3: Move Scattered Root Files

For each misplaced file found in Step 1, use `git mv` to relocate it. **Always use git mv to preserve history.** Example pattern:

```bash
# --- Literature PDFs misplaced at root → Articles/ ---
git mv "misplaced_paper.pdf" "Articles/appropriate_subfolder/"

# --- Sequence documents → 01.Materials/Sequences/ ---
mkdir -p "01.Materials/Sequences"
git mv "sequence_file.docx" "01.Materials/Sequences/"

# --- Meeting/presentation materials → ppt/ ---
git mv "meeting_materials.pdf" "ppt/"

git commit -m "REORG: Move scattered root-level files to proper directories"
```

## Step 4: Populate Empty Subfolders

Check for empty directories that should contain categorized files. Move relevant files from parent directories into the appropriate subfolders:

```bash
# Example: Move topically-related papers into empty subcategories
git mv "Articles/relevant_paper.pdf" "Articles/03.Subcategory/"
git commit -m "REORG: Categorize papers into appropriate subdirectories"
```

## Step 5: Update Project Registry

After any reorganization, check for new experiment folders:

```bash
# Dynamic Registry Discovery
if [ -f "00.RawData/INDEX.csv" ]; then
    REGISTRY_FILE="00.RawData/INDEX.csv"
elif [ -f "00.RawData/PIPELINE_REGISTRY.md" ]; then
    REGISTRY_FILE="00.RawData/PIPELINE_REGISTRY.md"
else
    REGISTRY_FILE=""
fi

echo "=== Experiment folders NOT in Project Registry ==="
if [ -n "$REGISTRY_FILE" ]; then
  for dir in 00.RawData/*/; do
    find "$dir" -maxdepth 1 -type d -name '20*' 2>/dev/null
  done | while read folder; do
    basename=$(echo "$folder" | sed 's|00.RawData/||')
    grep -q "$basename" "$REGISTRY_FILE" 2>/dev/null || echo "MISSING: $folder"
  done
else
  echo "  (No registry file found in 00.RawData/)"
fi
```

For each missing folder, add a row to the Project Registry (`00.RawData/INDEX.csv` or `00.RawData/PIPELINE_REGISTRY.md`).

## Step 6: Update README.md

After reorganization, update the repository structure section in `README.md` to match the new layout.

## Step 7: Auto-Commit

Delegate to the canonical `/lab-commit` workflow. Do NOT write inline `git add` / `git commit` commands here — the lab-commit workflow handles staging, Obsidian symlink verification, project registry updates (e.g., INDEX.csv or PIPELINE_REGISTRY.md), and commit message formatting automatically.

## Step 8: Verify

Run the audit from Step 1 again. The output should show:
- No experiment folders missing from Project Registry
- `Articles/03.O-GlcNAc&AS/` is no longer empty

## Step 9: Update Wiki Knowledge Base
Run the `/wiki-update` workflow to ensure the LLM-Wiki accurately reflects the newly reorganized folders and that the system recognizes the canonical paths.

---

## Rules for Adding New Data

When new experimental data is generated, follow these rules:

### New raw data
1. Create a folder under the appropriate `00.RawData/XX.*/` category
2. Use the naming convention: `YYYYMMDD description`
3. Add a row to the Project Registry (e.g., `00.RawData/INDEX.csv` or `PIPELINE_REGISTRY.md`)
4. Commit via the `/lab-commit` workflow

### New literature
1. Place in the appropriate `Articles/0X.*/` subcategory
2. Never leave PDFs at the project root

### New presentations
1. Place in `ppt/` with date prefix: `YYYYMMDD title.pptx`
2. Conference materials go in `ppt/conference/`

### New plasmid constructs
1. `.dna` files go in `plasmid/`
2. VectorBuilder order PDFs go alongside their `.dna` files in `plasmid/`

### New sequences
1. Sequence `.docx` or `.txt` files go in `01.Materials/Sequences/`

### New assay type (no existing folder)
1. Create a new numbered folder: `00.RawData/11.NewAssay/`
2. Continue the numbering (skip gaps like `06.` — don't backfill)
3. Add to the Project Registry
4. Update `README.md` repository structure section
