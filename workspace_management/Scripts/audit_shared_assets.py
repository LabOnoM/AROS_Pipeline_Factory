#!/usr/bin/env python3
"""
SAMS Audit Script (Cross-Platform)

Validates Cross-Pipeline Compatibility Protocol (CPCP) compliance.
Since SAMS v1.1, this repository supports Windows, macOS, and Linux by 
eliminating POSIX symlinks. This script enforces that architecture by checking:

1. No duplicate physical files exist across pipelines (pipelines must reference 01.Shared_Assets natively).
2. All shared assets contain CPCP YAML frontmatter.
3. .git/hooks/pre-commit exists and is executable.
"""

import os
import sys
import yaml
import glob
from pathlib import Path

PROJECT_ROOT = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
SHARED_ASSETS_DIR = PROJECT_ROOT / "01.Shared_Assets"
PIPELINES = ["Grant_Write_Pipeline", "KAKENHI_Pipeline", "Manuscript_Write_Pipeline"]
ASSET_TYPES = ["KIs", "Policies", "Skills", "Workflows"]

def check_git_hook():
    hook_path = PROJECT_ROOT / ".git" / "hooks" / "pre-commit"
    if not hook_path.exists():
        return False, "pre-commit hook missing"
    if not os.access(hook_path, os.X_OK):
        return False, "pre-commit hook is not executable"
    return True, ""

def extract_frontmatter(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.startswith('---'):
            end_idx = content.find('---', 3)
            if end_idx != -1:
                return yaml.safe_load(content[3:end_idx])
    except Exception as e:
        pass
    return None

def audit():
    errors = []
    
    # 1. Check Git Hook
    hook_ok, hook_msg = check_git_hook()
    if not hook_ok:
        errors.append(f"Git Hook Error: {hook_msg}")

    # Gather all canonical assets and their basenames
    canonical_assets = {}
    canonical_basenames = set()
    if SHARED_ASSETS_DIR.exists():
        for asset_type in ASSET_TYPES:
            type_dir = SHARED_ASSETS_DIR / asset_type
            if type_dir.exists():
                for root, _, files in os.walk(type_dir):
                    for file in files:
                        if file.endswith('.md'):
                            full_path = Path(root) / file
                            rel_path = full_path.relative_to(SHARED_ASSETS_DIR)
                            canonical_assets[str(rel_path)] = full_path
                            canonical_basenames.add(file)
                            # Also add the parent directory name if it's inside an artifacts folder
                            if "artifacts" in str(full_path):
                                parent_ki_dir = full_path.parent.parent.name
                                canonical_basenames.add(parent_ki_dir)

    # 2. Check frontmatter on canonical assets
    for rel_path, full_path in canonical_assets.items():
        fm = extract_frontmatter(full_path)
        if not fm or not fm.get('cpcp_asset'):
            errors.append(f"Missing/Invalid CPCP frontmatter: {full_path.relative_to(PROJECT_ROOT)}")

    # 3. Check pipelines for duplicates
    # Since symlinks are banned, if any pipeline folder contains an asset 
    # with the same name as a canonical asset, it's a violation.
    for pipeline in PIPELINES:
        pipeline_dir = PROJECT_ROOT / pipeline
        if not pipeline_dir.exists():
            continue
            
        for asset_type in ASSET_TYPES:
            type_dir = pipeline_dir / asset_type
            if not type_dir.exists():
                continue
                
            for root, dirs, files in os.walk(type_dir):
                # Check directory names (for KIs)
                for d in dirs:
                    if d in canonical_basenames:
                        errors.append(f"Illegal duplicate directory found (must reference 01.Shared_Assets): {Path(root, d).relative_to(PROJECT_ROOT)}")
                        
                # Check file names (for Policies, Workflows, Skills)
                for file in files:
                    if file.endswith('.md') and file in canonical_basenames:
                        full_path = Path(root) / file
                        errors.append(f"Illegal duplicate file found (must reference 01.Shared_Assets): {full_path.relative_to(PROJECT_ROOT)}")

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
