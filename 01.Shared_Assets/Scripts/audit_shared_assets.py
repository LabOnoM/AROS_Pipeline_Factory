#!/usr/bin/env python3
"""
audit_shared_assets.py — SAMS Audit Script (Cross-Platform)

Validates Cross-Pipeline Compatibility Protocol (CPCP) compliance for the
AROS Pipeline Factory.  Since SAMS v1.1 this repository supports Windows,
macOS, and Linux by eliminating POSIX symlinks.  This script enforces that
architecture by checking:

  1. No duplicate physical assets exist across pipeline directories.
     Pipelines MUST reference 01.Shared_Assets directly (no copies).
  2. All Markdown assets in 01.Shared_Assets contain the CPCP YAML
     frontmatter key  ``cpcp_asset: true``.
  3. .git/hooks/pre-commit exists and is executable (Linux/macOS only).

Duplicate Detection Logic
~~~~~~~~~~~~~~~~~~~~~~~~~
For KIs  — the *directory name* (e.g. ``agentic_manuscript_publishing``)
           is the canonical identifier.  If the same directory name appears
           under a pipeline's ``KIs/`` folder, it is a violation.
For Skills — the *skill directory name* (e.g. ``literature-ingestion``)
             is the canonical identifier.  A pipeline may legitimately have
             its *own* ``SKILL.md`` inside a *different* skill directory.
For Policies/Workflows — the *filename* is the identifier (e.g.
                         ``gepa_protocol.md``).  Same filename in a
                         pipeline is a violation.

Usage:
    python3 01.Shared_Assets/Scripts/audit_shared_assets.py
"""

import os
import sys
import yaml
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration — paths are relative to the project root
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
SHARED_ASSETS_DIR = PROJECT_ROOT / "01.Shared_Assets"
PIPELINES = ["Grant_Write_Pipeline", "KAKENHI_Pipeline", "Manuscript_Write_Pipeline"]
ASSET_TYPES = ["KIs", "Policies", "Skills", "Workflows"]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def check_git_hook() -> tuple[bool, str]:
    """Verify that .git/hooks/pre-commit exists and is executable."""
    hook_path = PROJECT_ROOT / ".git" / "hooks" / "pre-commit"
    if not hook_path.exists():
        return False, "pre-commit hook missing"
    # On Windows os.access(X_OK) always returns True, so this check is a
    # Linux/macOS best-effort only.
    if not os.access(hook_path, os.X_OK):
        return False, "pre-commit hook is not executable"
    return True, ""


def extract_frontmatter(filepath: Path) -> dict | None:
    """Parse YAML frontmatter from a Markdown file.  Returns None on failure."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if content.startswith("---"):
            end_idx = content.find("---", 3)
            if end_idx != -1:
                return yaml.safe_load(content[3:end_idx])
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Main audit logic
# ---------------------------------------------------------------------------
def audit() -> None:
    errors: list[str] = []

    # -- 1. Check Git pre-commit hook ------------------------------------
    hook_ok, hook_msg = check_git_hook()
    if not hook_ok:
        errors.append(f"Git Hook Error: {hook_msg}")

    # -- 2. Gather canonical shared assets & build identity sets ---------
    # We maintain *separate* identity sets per asset type so that, for
    # example, a KI directory named ``peer-review`` does not collide with
    # a Skill directory named ``peer-review``.
    canonical_assets: dict[str, Path] = {}       # rel_path -> full_path
    canonical_ki_dirs: set[str] = set()           # KI directory names
    canonical_skill_dirs: set[str] = set()        # Skill directory names
    canonical_policy_files: set[str] = set()      # Policy filenames
    canonical_workflow_files: set[str] = set()    # Workflow filenames (future)

    if SHARED_ASSETS_DIR.exists():
        for asset_type in ASSET_TYPES:
            type_dir = SHARED_ASSETS_DIR / asset_type
            if not type_dir.exists():
                continue

            for root, dirs, files in os.walk(type_dir):
                root_path = Path(root)

                if asset_type == "KIs":
                    # The KI identity is its *top-level directory name*
                    # directly under ``KIs/``.
                    for d in dirs:
                        if root_path == type_dir:
                            canonical_ki_dirs.add(d)

                elif asset_type == "Skills":
                    # The Skill identity is its *top-level directory name*
                    # directly under ``Skills/``.
                    for d in dirs:
                        if root_path == type_dir:
                            canonical_skill_dirs.add(d)

                elif asset_type == "Policies":
                    for f in files:
                        if f.endswith(".md"):
                            canonical_policy_files.add(f)

                elif asset_type == "Workflows":
                    for f in files:
                        if f.endswith(".md"):
                            canonical_workflow_files.add(f)

                # Collect every .md for frontmatter checks
                for f in files:
                    if f.endswith(".md"):
                        full_path = root_path / f
                        rel_path = full_path.relative_to(SHARED_ASSETS_DIR)
                        canonical_assets[str(rel_path)] = full_path

    # -- 3. Check CPCP frontmatter on canonical assets -------------------
    for rel_path, full_path in canonical_assets.items():
        fm = extract_frontmatter(full_path)
        if not fm or not fm.get("cpcp_asset"):
            errors.append(
                f"Missing/Invalid CPCP frontmatter: "
                f"{full_path.relative_to(PROJECT_ROOT)}"
            )

    # -- 4. Check pipelines for duplicate assets -------------------------
    for pipeline in PIPELINES:
        pipeline_dir = PROJECT_ROOT / pipeline
        if not pipeline_dir.exists():
            continue

        for asset_type in ASSET_TYPES:
            type_dir = pipeline_dir / asset_type
            if not type_dir.exists():
                continue

            for root, dirs, files in os.walk(type_dir):
                root_path = Path(root)

                if asset_type == "KIs":
                    # Flag if a pipeline has a KI directory whose name
                    # matches a canonical KI directory in Shared Assets.
                    if root_path == type_dir:
                        for d in dirs:
                            if d in canonical_ki_dirs:
                                errors.append(
                                    f"Illegal duplicate KI directory "
                                    f"(must reference 01.Shared_Assets): "
                                    f"{Path(root, d).relative_to(PROJECT_ROOT)}"
                                )

                elif asset_type == "Skills":
                    # Flag if a pipeline has a Skill directory whose name
                    # matches a canonical Skill directory in Shared Assets.
                    if root_path == type_dir:
                        for d in dirs:
                            if d in canonical_skill_dirs:
                                errors.append(
                                    f"Illegal duplicate Skill directory "
                                    f"(must reference 01.Shared_Assets): "
                                    f"{Path(root, d).relative_to(PROJECT_ROOT)}"
                                )

                elif asset_type == "Policies":
                    for f in files:
                        if f.endswith(".md") and f in canonical_policy_files:
                            errors.append(
                                f"Illegal duplicate Policy file "
                                f"(must reference 01.Shared_Assets): "
                                f"{Path(root, f).relative_to(PROJECT_ROOT)}"
                            )

                elif asset_type == "Workflows":
                    for f in files:
                        if f.endswith(".md") and f in canonical_workflow_files:
                            errors.append(
                                f"Illegal duplicate Workflow file "
                                f"(must reference 01.Shared_Assets): "
                                f"{Path(root, f).relative_to(PROJECT_ROOT)}"
                            )

    # -- 5. Report results -----------------------------------------------
    if errors:
        print("❌ SAMS Audit Failed!")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("✅ SAMS Audit Passed! All CPCP constraints verified (Cross-Platform).")
        sys.exit(0)


if __name__ == "__main__":
    audit()
