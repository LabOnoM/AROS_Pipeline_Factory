# Global Navigation & Operations Context (Root)

## 🧭 Navigation Pointers
- **STOP AND READ `CODE_MAP.md` FIRST**. 
- You are at the root of the **AROS Pipeline Factory**. 
- Navigate to the specific domain pipeline you need to work on (e.g., `Grant_Write_Pipeline/`), and read the local `CLAUDE.md` inside that directory for localized context. Do NOT perform global searches across pipelines without identifying your target first.

## ⚖️ Global Constraints & Standards
1. **SUPREME LAW (CPCP)**: Any modifications to `01.Shared_Assets/` MUST be registered in `00.RawData/SHARED_ASSET_REGISTRY.md` (LAW 0 in `AGENTS.md`).
2. **Strict Prohibitions**: Do NOT create scratch files, temporary logs, or testing scripts in the root directory. Use your designated agent scratch workspace.
3. **Commit Gateway**: Use the `/lab-commit` workflow for committing file changes safely.
4. **Symlink Ban**: POSIX symlinks are strictly banned for cross-pipeline asset sharing. Use direct absolute or relative paths.

## 📚 Wiki Grounding (Phase 4)
- This project utilizes a strict LLM-Wiki for grounded truth (`.wiki/`).
- **Drift Prevention**: Whenever you modify core architecture, you MUST update the corresponding section in `.wiki/system/` or `.wiki/concepts/` to prevent knowledge rot.
- Run `/wiki-update` to synthesize new information into the Wiki after major changes.

## Design Grounding

If any pipeline produces user-facing UI or styled HTML output: Before writing or changing anything a person sees, read the **LabOnoM Design Guide** (private repository `LabOnoM/design`, pinned here as version `2026.10.0` in `DESIGN_VERSION`): `DESIGN.md` at this repository's root is its family file "AROS Deep Space", verified by `scripts/design-pin-check.sh`; the family file itself is this product's profile (web and AROS surfaces); the guide's `GLOSSARY.md` holds every word on screen in English and Japanese, `STATES.md` every state a surface can be in, and `CONFORMANCE.md` the measured tests this repository keeps green. Design the change with the `ux-foundations` skill's P1 brief, audit the result with P2 and P3 in both themes, and record findings as clauses with tests. Tokens come from the guide, never pasted hex; status hues are reserved; no state is colour alone; words come from the glossary; every string ships in English and Japanese. Do not invent palettes; the "Modern Web Guidance" of the UI pipeline yields to the guide where they differ. Details: `.wiki/design-guide.md`.

## CI/CD is manual: no GitHub Actions (owner's decision, 2026-10-13)

LabOnoM does not use GitHub Actions: there is no budget for it. Never add a file under `.github/workflows/`, never
rely on or wait for a GitHub status check, and never describe a change as "green on CI". Instead:

- **Before every merge**, run this repository's checks locally (the commands in the "Checks and deploys" section of
  the README) and write the pass, fail and skip counts in the pull request.
- **Deploys and releases** are run by hand from a machine that holds the owner's credentials, with the scripts in
  `scripts/` (or the documented commands), never by a hosted runner; record what ran and its result (revision,
  version, digest) in the pull request or the session receipt.
- Steps that need a platform this machine is not (macOS or Windows builds, signing) are run on such a machine by
  the owner, or are recorded as not run; they are never claimed.
