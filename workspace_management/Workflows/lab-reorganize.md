---
description: Safely reorganize project files and folders while preserving git history
---

# Lab Directory Reorganize Workflow

// Note: All commands must execute from the active project root.

Run this procedure whenever experimental folders need to be merged, renamed, or moved within `00.RawData/` to keep history intact. **Always use `git mv` instead of regular `mv`** so that git preserves the file's history across the rename.

## Steps

1. **Check Git Status**
   ```bash
   git status
   ```

2. Move / rename files using `git mv`:
   ```bash
   # Move a file:
   git mv "old/path/to/file.xlsx" "new/path/to/file.xlsx"

   # Rename a folder:
   git mv "old_folder_name" "new_folder_name"

   # Move scattered root-level files to proper homes:
   git mv "Background free imaging...pdf" "Articles/04.UTR_Function/"
   git mv "CRISPR 101 2nd Ed Final May 2018_2.pdf" "Articles/01.Review&Mechanism/"
   ```

3. **Execution via Bash Script (Agent automation)**
   Use your `run_command` tool to execute the moves using bash wildcards or loops if there are many files.
   Example:
   ```bash
   for f in *.pdf; do
       echo "Moving $f to Articles/"
       git mv "$f" Articles/
   done
   ```

4. **Auto-Commit:** Delegate to the canonical `/lab-commit` workflow. Do NOT write inline `git add` / `git commit` commands here — the lab-commit workflow handles staging, Obsidian symlink verification, INDEX.csv updates, and commit message formatting automatically.

5. Verify files are still tracked:
   ```bash
   git log --follow --oneline "new/path/to/file.xlsx"
   ```

## Rules

- **Never use plain `mv` or drag-and-drop in a file manager** — git will see this as a delete + create, losing history.
- **Never reorganize and edit in the same commit** — do the move first, commit, then edit content separately. This keeps `git log --follow` clean.
- **Update INDEX.csv** if experiment folders were moved.
- **Update README.md** repository structure section if the folder map changed.

## Common Reorganization Tasks for This Project

### Move scattered root-level files
```bash
# Literature PDFs misplaced at root
git mv "Background free imaging of single mRNAs in live cells using split fluorescent proteins.pdf" "Articles/04.UTR_Function/"
git mv "CRISPR 101 2nd Ed Final May 2018_2.pdf" "Articles/01.Review&Mechanism/"
git mv "Li et al. - 2016 - Gene replacements and insertions in rice by intron targeting using CRISPR-Cas9.pdf" "Articles/01.Review&Mechanism/"

# Sequence docs to Materials
mkdir -p "01.Materials/Sequences"
git mv "SP7-sequence.docx" "01.Materials/Sequences/"
git mv "Sp7_Sequence.docx" "01.Materials/Sequences/"
git mv "TranscriptSeq.docx" "01.Materials/Sequences/"

# Meeting materials to ppt/
git mv "伊藤先生meeting 20220516資料.pdf" "ppt/"

git commit -m "REORG: Move scattered root-level files to proper directories"
```

### Clean macOS junk (after .gitignore is set up)
```bash
find . -name '.DS_Store' -o -name '._*' | xargs git rm --cached 2>/dev/null
git commit -m "CLEAN: Remove macOS metadata from tracking"
```
