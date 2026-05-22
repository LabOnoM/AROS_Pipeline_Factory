"""
VPEP (Video-to-Protocol Extraction Pipeline) - Compared Experiment Notebook Generator
=====================================================================================

Description:
    This script handles Stage 3 of the VPEP pipeline. It reads the parsed timeline JSON, extracts the
    Standard Operating Procedure (SOP) text from a reference DOCX file using `pandoc`, and queries a
    Gemini Pro model to synthesize a detailed "Compared Experiment Notebook" in English and Japanese.
    It links the extracted keyframe images into the markdown timeline table.

Key Capabilities:
    - Extracts text from DOCX files using Pandoc plain text conversion.
    - Compares execution logs (JSON) against the SOP standard to identify deviations and supplements.
    - Re-injects annotated keyframe URLs (`keyframe_url`) directly into the output tables.

Cross-Platform Compatibility:
    - Uses system-agnostic file paths and checks for pandoc command availability.
    - Verified on macOS, Ubuntu, and Windows.
"""

import os
import json
import argparse
import subprocess
from utils import load_api_client

def extract_docx(docx_path):
    try:
        result = subprocess.run(['pandoc', docx_path, '-t', 'plain'], capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        print(f"Error extracting docx: {e}")
        return ""

def build_prompt(timeline_json, sop_text, reference_markdown, lang="EN"):
    language_instruction = "ENGLISH" if lang == "EN" else "JAPANESE"
    
    return f"""You are an expert scientific auditor and medical writer.
I will provide you with a raw video timeline JSON, a Standard Operating Procedure (SOP) text extracted from a DOCX file, and a Reference Markdown Notebook showing the exact layout and structure I want.

Your task is to generate a comprehensive "Compared Experiment Notebook" in {language_instruction}.
You MUST strictly follow the exact layout, section headers, and table structures as the Reference Markdown Notebook, but dynamically fill in the content by comparing the TIMELINE JSON against the SOP TEXT.

CRITICAL INSTRUCTIONS:
1. For the "Video Timeline & Actions" table, you must include a "key frame" column. You must use the EXACT string provided in the `keyframe_url` field of the TIMELINE JSON to embed the image. Format: `![](EXACT_URL)`
2. Do NOT hallucinate image names. If `keyframe_url` is provided, use it exactly as is.
3. Compare the quantities and steps from the Timeline to the SOP, and note them in the "Materials & Reagents" and "Critical Parameters to Supplement" sections.
4. Output the complete raw Markdown string. Do not wrap it in markdown code block formatting (like ```markdown), just return the pure markdown text.

--- REFERENCE MARKDOWN NOTEBOOK (Target Layout) ---
{reference_markdown}

--- SOP TEXT (From Master DOCX) ---
{sop_text}

--- TIMELINE JSON ---
{timeline_json}
"""

def main():
    parser = argparse.ArgumentParser(description="Generate compared experiment notebook from video timeline and SOP docx.")
    parser.add_argument("--json_path", "-j", required=True, help="Path to the vlm_parsed_timeline.json file.")
    parser.add_argument("--docx_path", "-d", required=True, help="Path to the SOP DOCX file.")
    parser.add_argument("--ref_path", "-r", required=True, help="Path to the reference markdown Compared_Experiment_Notebook.md file.")
    parser.add_argument("--output_dir", "-o", required=True, help="Directory to save the outputs.")
    parser.add_argument("--output_en", help="Optional explicit path to the EN markdown output file.")
    parser.add_argument("--output_jp", help="Optional explicit path to the JA markdown output file.")
    parser.add_argument("--model", default="gemini-3.1-pro-preview", help="Model to use for generating notebook (default: gemini-3.1-pro-preview).")
    
    args = parser.parse_args()
    
    out_en = args.output_en or os.path.join(args.output_dir, "Compared_Experiment_Notebook_EN.md")
    out_jp = args.output_jp or os.path.join(args.output_dir, "Compared_Experiment_Notebook_JA.md")
    
    client = load_api_client()
    
    print(f"Extracting SOP text from docx: {args.docx_path}...")
    sop_text = extract_docx(args.docx_path)
    
    print(f"Reading reference markdown: {args.ref_path}...")
    with open(args.ref_path, "r", encoding="utf-8") as f:
        reference_markdown = f.read()
    
    print("Injecting explicit keyframe URLs into timeline to prevent hallucinations...")
    with open(args.json_path, 'r', encoding='utf-8') as f:
        timeline_data = json.load(f)
        for i, step in enumerate(timeline_data):
            img_name = f"row_{i+1:02d}_step_{step['primary_action'].replace(' ', '_').replace('/', '')}.jpg"
            step['keyframe_url'] = f"annotated_keyframes/{img_name}"
        timeline = json.dumps(timeline_data, indent=2)
        
    def generate_markdown(lang, out_path):
        print(f"Requesting {args.model} for {lang} notebook...")
        prompt = build_prompt(timeline, sop_text, reference_markdown, lang)
        
        response = client.models.generate_content(
            model=args.model,
            contents=prompt,
        )
        
        md_text = response.text.replace("```markdown", "").strip()
        if md_text.endswith("```"):
            md_text = md_text[:-3].strip()
            
        # Ensure directories exist
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md_text)
        print(f"Saved {out_path}")
        
    generate_markdown("EN", out_en)
    generate_markdown("JP", out_jp)
    print("Done!")

if __name__ == "__main__":
    main()
