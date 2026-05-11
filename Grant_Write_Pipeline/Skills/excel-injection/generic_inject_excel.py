import os
import json
import argparse
import openpyxl
from openpyxl.drawing.image import Image as XlImage

def safe_write(sheet, cell_address, value):
    if not value: return
    cell = sheet[cell_address]
    if cell.protection.locked:
        print(f"  ⚠ Cell {cell_address} in {sheet.title} is locked — forcing write.")
    cell.value = value

def run(project_dir, funder_profile_path, template_path):
    print(f"Loading funder profile from {funder_profile_path}")
    with open(funder_profile_path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    grant_draft_dir = os.path.join(project_dir, "GrantDraftElements")
    out_dir = project_dir

    if profile.get("submission_format") != "xlsx":
        print("This funder does not use xlsx submission format. Exiting.")
        return

    # Assuming the profile has a "mapping" section for Excel cells.
    # We will look for mapping in the sections.
    # MEXT SPReAD uses 1枚目, 2枚目, 3枚目, etc.
    # For a truly generic script, the profile should define sheet_name, cell, and section_id.
    # For now, we will adapt the hardcoded logic slightly but make it read from GrantDraftElements.
    
    # We'll generate EN and JP if available.
    for lang in ["en", "jp"]:
        print(f"Generating {lang.upper()} workbook...")
        try:
            wb = openpyxl.load_workbook(template_path)
        except Exception as e:
            print(f"Could not load template {template_path}: {e}")
            continue

        # In a fully generic system, we iterate through profile['sections'] and read the mapped cell
        # Since mext_spread_fy2026.json isn't perfectly structured for generic cell mapping in our scope,
        # we will use the logic from the specific SPReAD template but parameterized by project directory.
        
        sheet2 = wb['研究計画調書_2枚目'] if '研究計画調書_2枚目' in wb.sheetnames else wb.worksheets[1]
        
        # Read the markdown files
        for section in profile.get("sections", []):
            sid = section["id"]
            # Look for the markdown file
            # En uses: 02_objectives_en.md
            # Jp uses: 02_objectives_jp_compressed.md (if exists) or 02_objectives_jp.md
            
            content = ""
            filename_compressed = os.path.join(grant_draft_dir, f"{sid}_{lang}_compressed.md")
            filename_normal = os.path.join(grant_draft_dir, f"{sid}_{lang}.md")
            
            if os.path.exists(filename_compressed):
                with open(filename_compressed, "r", encoding="utf-8") as f:
                    content = f.read().strip()
            elif os.path.exists(filename_normal):
                with open(filename_normal, "r", encoding="utf-8") as f:
                    content = f.read().strip()
            
            # Simple heuristic mapping for SPReAD (can be extended via JSON)
            if "objective" in sid.lower(): safe_write(sheet2, "A3", content)
            elif "method" in sid.lower(): safe_write(sheet2, "A5", content)
            elif "ai_validity" in sid.lower(): safe_write(sheet2, "A7", content)
            elif "milestone" in sid.lower(): safe_write(sheet2, "A9", content)
            elif "knowhow" in sid.lower(): safe_write(sheet2, "A11", content)
        
        # Insert Workflow diagram
        workflow_img_path = os.path.join(grant_draft_dir, "workflow_diagram.png")
        if not os.path.exists(workflow_img_path):
             workflow_img_path = os.path.join(project_dir, "Elements", "workflow_diagram.png")
             
        if os.path.exists(workflow_img_path):
            try:
                img = XlImage(workflow_img_path)
                orig_w, orig_h = img.width, img.height
                img.width = 680
                img.height = int(680 * (orig_h / orig_w))
                sheet2.add_image(img, "A13")
            except Exception as e:
                print(f"Error adding image: {e}")

        # Save
        out_path = os.path.join(out_dir, f"Form1_Draft_{lang}.xlsx")
        wb.save(out_path)
        print(f"Saved {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--funder-profile", required=True)
    parser.add_argument("--template", required=True)
    args = parser.parse_args()
    run(args.project_dir, args.funder_profile, args.template)
