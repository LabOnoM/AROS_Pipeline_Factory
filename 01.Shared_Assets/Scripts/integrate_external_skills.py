#!/usr/bin/env python3
# =============================================================================
# integrate_external_skills.py — External Skill Ingestion & Categorization
# =============================================================================
#
# PURPOSE:
#   Ingests raw external skills from cloned GitHub repositories, categorizes them
#   into specific AROS Pipeline Factory directories, and normalizes their structure
#   (injecting CPCP-compliant YAML frontmatter and copying parent directories).
#
# USAGE:
#   python3 01.Shared_Assets/Scripts/integrate_external_skills.py
#
# PART OF: AROS Pipeline Factory (01.Shared_Assets/Scripts/)
# SPEC:    §4.5 AROS Runtime Directory Mapping
# =============================================================================

import os
import json
import shutil
import re
import argparse

# Pipeline mapping assigns imported repos to their respective Pipeline directories
PIPELINE_MAP = {
    "nature-skills": "Manuscript_Write_Pipeline/Skills",
    "Supervisor-Skills": "Manuscript_Write_Pipeline/Skills",
    "scipilot-cite-skill": "Manuscript_Write_Pipeline/Skills",
    "scipilot-figure-skill": "Manuscript_Write_Pipeline/Skills",
    "execplan-skill": "Software_Engineering_Pipeline/Skills",
    "web-project-builder-skill": "Software_Engineering_Pipeline/Skills",
    "archify": "Software_Engineering_Pipeline/Skills",
    "claudedesignskills": "UI_Development_Pipeline/Skills",
    "html-anything": "UI_Development_Pipeline/Skills",
    "garden-skills": "Multimedia_Generation_Pipeline/Skills",
    "hyperframes": "Multimedia_Generation_Pipeline/Skills",
    "guizang-social-card-skill": "Multimedia_Generation_Pipeline/Skills",
    "Horizon": "Data_Analysis_Pipeline/Skills",
    "serenity-skill": "Data_Analysis_Pipeline/Skills",
    "dbskill": "Data_Analysis_Pipeline/Skills"
}

def sanitize_description(desc):
    """
    Sanitize the description to satisfy CPCP constraints (max 250 characters).
    """
    if not desc:
        return "No description provided."
    # Remove newlines, compress spaces
    desc = re.sub(r'\s+', ' ', desc).strip()
    if len(desc) > 245:
        desc = desc[:245] + "..."
    # Escape quotes
    desc = desc.replace('"', "'")
    return desc

def main():
    parser = argparse.ArgumentParser(description="Ingest and categorize external AROS skills.")
    parser.add_argument("--data-file", required=True, help="Path to the JSON metadata file containing new skills.")
    parser.add_argument("--source-root", required=True, help="Root directory containing the cloned skill repositories.")
    parser.add_argument("--dest-root", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
                        help="Root directory of the AROS Pipeline Factory (defaults to repository root).")
    
    args = parser.parse_args()

    if not os.path.exists(args.data_file):
        print(f"Data file {args.data_file} not found. Skipping integration.")
        return

    with open(args.data_file, "r") as f:
        data = json.load(f)

    new_files = data.get("new_skills_files", {})
    processed_count = 0

    for filepath, meta in new_files.items():
        parts = filepath.split('/')
        repo = parts[0]
        
        # Path relative to scratch/skills_repos
        source_md_path = os.path.join(args.source_root, filepath)
        source_parent_dir = os.path.dirname(source_md_path)
        folder_name = os.path.basename(source_parent_dir)
        
        # If the skill is right at the repo root (e.g. garden-skills/README.md),
        # then source_parent_dir is the repo root.
        if folder_name == repo:
            skill_name = meta.get("name") or repo
        else:
            skill_name = meta.get("name") or folder_name
            
        # Collision resolution for known duplicates across pipelines
        if repo == "claudedesignskills" and skill_name == "skill-creator":
            skill_name = "claudedesign-skill-creator"
            folder_name = "claudedesign-skill-creator"
            
        # Determine the destination pipeline
        dest_pipeline = PIPELINE_MAP.get(repo, "Uncategorized_Orphan_Pipeline/Skills")
        dest_pipeline_path = os.path.join(args.dest_root, dest_pipeline)
        
        # Determine target folder name, sanitizing spaces/underscores
        target_folder_name = folder_name if folder_name != repo else skill_name
        target_folder_name = target_folder_name.replace(' ', '-').replace('_', '-')
        target_skill_dir = os.path.join(dest_pipeline_path, target_folder_name)
        
        # Copy the entire parent directory to preserve assets (LAW -1)
        # Using symlinks=True and ignore_dangling_symlinks=True to prevent crashes on node_modules
        if not os.path.exists(target_skill_dir):
            shutil.copytree(source_parent_dir, target_skill_dir, dirs_exist_ok=True, symlinks=True, ignore_dangling_symlinks=True)
        
        # Normalize the primary markdown file to SKILL.md
        target_md_path = os.path.join(target_skill_dir, os.path.basename(source_md_path))
        if os.path.basename(target_md_path).lower() == 'readme.md':
            new_target_md_path = os.path.join(target_skill_dir, 'SKILL.md')
            if os.path.exists(target_md_path):
                os.rename(target_md_path, new_target_md_path)
                target_md_path = new_target_md_path

        # Inject/Fix YAML frontmatter for CPCP compliance
        if os.path.exists(target_md_path):
            with open(target_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            desc = sanitize_description(meta.get("description") or meta.get("description_preview"))
            
            # Check if there is existing frontmatter
            match = re.search(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
            if match:
                # Overwrite frontmatter to ensure compliance (description <= 250 chars)
                rest_of_content = match.group(2)
                new_frontmatter = f"---\nname: {skill_name}\ndescription: \"{desc}\"\n---\n\n"
                new_content = new_frontmatter + rest_of_content
            else:
                new_frontmatter = f"---\nname: {skill_name}\ndescription: \"{desc}\"\n---\n\n"
                new_content = new_frontmatter + content
                
            with open(target_md_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            processed_count += 1

    print(f"Integration script finished. Processed {processed_count} files into Factory pipelines.")

if __name__ == "__main__":
    main()
