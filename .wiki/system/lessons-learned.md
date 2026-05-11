# AROS Factory Post-Mortems & Operational Wisdom

This page serves as a historical repository of significant bugs, architectural missteps, and the resulting operational wisdom (now codified in `AGENTS.md` and `SPEC.md`).

## 1. The SAMS Basename Bug (May 2026)
**Context**: The `audit_shared_assets.py` script was originally designed to detect duplicate files by comparing base filenames.
**The Bug**: Because AROS Skills use a standard directory format (e.g., `literature-ingestion/SKILL.md`), every skill naturally contains a file named `SKILL.md`. The audit script falsely flagged every single skill as a duplicate, blocking commits.
**The Fix**: SAMS audits now use **per-asset-type identity sets**. Skills are identified by their parent directory name, KIs by their directory name, and Policies/Workflows by their filenames.

## 2. Cross-Platform Symlink Breakage (CPCP Origin)
**Context**: To share policies between `Grant_Write_Pipeline` and `KAKENHI_Pipeline`, agents initially used POSIX symlinks (`ln -s`).
**The Bug**: AROS is deployed across Ubuntu, macOS, and Windows. Symlinks break completely on Windows, causing catastrophic pipeline failures for Windows-based researchers.
**The Fix**: POSIX symlinks are strictly banned. The **Cross-Pipeline Compatibility Protocol (CPCP)** was established, mandating direct path referencing to `01.Shared_Assets/`.

## 3. LaTeX Truncation Disaster (April 2026)
**Context**: An agent was tasked with writing a Spatial Transcriptomics Probe portability manuscript.
**The Bug**: The agent attempted to write the manuscript directly in `.tex` format. Due to token management issues and complex LaTeX syntax, the 5800-word manuscript was truncated to 93 lines.
**The Fix**: The Markdown-first policy. Agents must write all text in `.md`. Pandoc handles the conversion.

## 4. Workflow Slash Command Registration Failures
**Context**: New workflows were created but didn't appear in the IDE UI.
**The Bug**: Agents were omitting the YAML frontmatter or providing invalid `description` strings.
**The Fix**: Every workflow `.md` file must start with YAML frontmatter containing a `description` field (under 250 characters).

## 5. The 10KB Workflow Limit (KI-Companion Pattern)
**Context**: Agents embedded massive lookup tables and logic scripts directly into workflow markdown files.
**The Bug**: The workflows exceeded the IDE's ~10KB file size limit, causing loading errors and slow UI rendering.
**The Fix**: The **KI-Companion Pattern**. Heavy assets must be extracted into Knowledge Items (`KIs/`) and loaded dynamically at runtime via `mcp_antigravity-brain_read_ki_document`.
