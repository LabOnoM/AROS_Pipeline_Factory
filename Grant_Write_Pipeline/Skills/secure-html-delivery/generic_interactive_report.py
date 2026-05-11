import os
import json
import argparse
import base64

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    ext = os.path.splitext(image_path)[1].lower()
    mime_type = "image/png"
    if ext in [".jpg", ".jpeg"]: mime_type = "image/jpeg"
    elif ext == ".svg": mime_type = "image/svg+xml"
    return f"data:{mime_type};base64,{encoded}"

def run(project_dir, funder_profile_path, output_path):
    print(f"Loading funder profile from {funder_profile_path}")
    with open(funder_profile_path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    grant_draft_dir = os.path.join(project_dir, "GrantDraftElements")
    
    sections_html = ""
    for section in profile.get("sections", []):
        sid = section["id"]
        title = section["name_en"]
        
        content = f"<p>File not found for section {sid}</p>"
        filename = os.path.join(grant_draft_dir, f"{sid}_en.md")
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                content_raw = f.read().strip()
                # Extremely naive markdown to HTML conversion for the template
                content = content_raw.replace("\n\n", "</p><p>").replace("\n", "<br>")
                content = f"<p>{content}</p>"

        sections_html += f"<h2>{title}</h2>\n{content}\n"

    # Try to embed workflow diagram
    workflow_img_path = os.path.join(grant_draft_dir, "workflow_diagram.png")
    if not os.path.exists(workflow_img_path):
         workflow_img_path = os.path.join(project_dir, "Elements", "workflow_diagram.png")
         
    workflow_html = ""
    if os.path.exists(workflow_img_path):
        b64 = get_base64_image(workflow_img_path)
        workflow_html = f'<h2>Workflow Diagram</h2><img src="{b64}" alt="Workflow" style="max-width:100%; border-radius: 8px;"/>'

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grant Application Report</title>
    <style>
        body {{ font-family: 'Inter', sans-serif; max-width: 900px; margin: 0 auto; padding: 2rem; background: #fafafa; color: #333; }}
        h1 {{ color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 0.5rem; }}
        h2 {{ color: #202124; margin-top: 2rem; }}
        .card {{ background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 2rem; }}
    </style>
</head>
<body>
    <h1>Grant Application Draft: {profile.get("funder", "Unknown")}</h1>
    <div class="card">
        {workflow_html}
        {sections_html}
    </div>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Generated generic interactive report at {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--funder-profile", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    run(args.project_dir, args.funder_profile, args.output)
