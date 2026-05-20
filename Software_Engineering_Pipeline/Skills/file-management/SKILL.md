---
name: file-management
description: Organize, back up, compress, split, and merge files/folders using rule-driven plans; use when you need safe previews, conflict handling, and verification before executing file operations.
license: MIT
skill-author: AIPOCH
---

# File Management

## When to Use

- You need to **reorganize a directory** (move/copy/rename) based on include/exclude patterns and a target folder structure.
- You want a **repeatable backup workflow** (copy or archive) with optional retention rules and verification manifests.
- You need to **compress** a folder or a set of files to reduce size or package deliverables.
- You must **split very large files** into fixed-size parts for transfer/storage limits (binary-safe).
- You need to **merge previously split parts** back into the original file reliably (binary-safe).

## Key Features

- **Safety-first planning**: generate a preview/manifest of intended actions before writing changes.
- **Rule-driven scope control**: root path + include/exclude patterns + thresholds + target structure (see `references/rule-schema.md`).
- **Conflict handling**: default to skip/rename on collisions; overwrite only with explicit confirmation.
- **Non-destructive defaults**: avoid deletion unless explicitly requested.
- **Verification support**: compare counts/sizes and optionally generate hashes for critical backups.
- **Binary-safe split/merge**: split by fixed size and merge parts without corrupting binary data (`scripts/`).

### Error Prevention: Unsafe Path Validation

To prevent catastrophic errors from unsafe file operations, a path validation wrapper is now mandatory for any skill performing file system writes, moves, or deletions.

**Core Requirement:** Before executing any file operation, the skill MUST resolve the absolute path of the target and validate it against a list of protected system directories.

**Protected Directories:**
*   `/`
*   `/etc`
*   `/usr`
*   `/var`
*   `/root`

**Implementation:**
The wrapper function must:
1.  Take the intended file path as input.
2.  Resolve it to an absolute, canonical path (e.g., using `os.path.realpath` in Python or `realpath` in shell).
3.  Check if the resolved path or any of its parent directories match any of the protected directories.
4.  If a match is found, the operation MUST be blocked, and an error must be logged and raised.

This check MUST be performed before any call to functions like `write_local_file`, `os.remove`, `shutil.move`, `mv`, `rm`, etc. Bypassing this validation is a critical policy violation.

## Dependencies

- PowerShell 5.1+ (Windows PowerShell) or PowerShell 7+
  - Cmdlets used: `Get-ChildItem`, `Copy-Item`, `Move-Item`, `Compress-Archive`, `Get-FileHash`
- Python 3.8+ (for split/merge scripts)
  - `scripts/split_file.py`
  - `scripts/merge_parts.py`

## Example Usage

### 1) Organize files with a preview plan (PowerShell)

```powershell
# Inputs (adjust to your case)
$Root = "D:\Inbox"
$Target = "D:\Organized"
$Include = @("*.pdf","*.docx")
$ExcludeDirs = @("node_modules",".git")
$WhatIf = $true  # set to $false to execute

# Build a manifest (preview plan)
$files = Get-ChildItem -Path $Root -Recurse -File |
  Where-Object {
    ($Include | ForEach-Object { $_ }) -contains $_.Extension -eq $false
  }

# Practical include filter (simple example)
$files = Get-ChildItem -Path $Root -Recurse -File -Include $Include

# Exclude directories by path segment
$files = $files | Where-Object {
  $p = $_.FullName
  -not ($ExcludeDirs | Where-Object { $p -match [regex]::Escape("\$_\") })
}

$plan = foreach ($f in $files) {
  # Example target structure: by extension
  $ext = $f.Extension.TrimStart(".").ToLower()
  $destDir = Join-Path $Target $ext
  $destPath = Join-Path $destDir $f.Name

  [pscustomobject]@{
    Source = $f.FullName
    Destination = $destPath
    Action = "Copy"  # start with Copy; switch to Move after verification
  }
}

# Preview
$plan | Format-Table -AutoSize

# Execute (safe defaults: create dirs; do not overwrite unless you decide to)
foreach ($item in $pl
```