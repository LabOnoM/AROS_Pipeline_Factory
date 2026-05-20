# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import json
import argparse
import os
import shutil

def check_skills(skill_names):
    """Checks for the existence of skill directories."""
    results = {}
    skills_dir = os.path.expanduser("~/.gemini/skills")
    for skill in skill_names:
        skill_path = os.path.join(skills_dir, skill)
        results[skill] = {"found": os.path.isdir(skill_path), "path": skill_path}
    return results

def check_dependencies(dep_names):
    """Checks for the existence of system dependencies (executables)."""
    results = {}
    for dep in dep_names:
        found_path = shutil.which(dep)
        results[dep] = {"found": found_path is not None, "path": found_path or "Not found in PATH"}
    return results

def main():
    """Main function to parse arguments and run checks."""
    parser = argparse.ArgumentParser(description="Check for skill and dependency availability.")
    parser.add_argument("--skills", type=str, help="Comma-separated list of skill names to check.")
    parser.add_argument("--dependencies", type=str, help="Comma-separated list of system dependencies to check.")
    args = parser.parse_args()

    report = {
        "skills": {},
        "dependencies": {}
    }

    if args.skills:
        skill_names = [s.strip() for s in args.skills.split(',')]
        report["skills"] = check_skills(skill_names)

    if args.dependencies:
        dep_names = [d.strip() for d in args.dependencies.split(',')]
        report["dependencies"] = check_dependencies(dep_names)

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
