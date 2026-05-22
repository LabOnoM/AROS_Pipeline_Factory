"""
VPEP (Video-to-Protocol Extraction Pipeline) - Bilingual Report Generator
========================================================================

Description:
    This script is Stage 4 of the VPEP pipeline. It reads the parsed timeline JSON, the VLM
    video summary, and the template SOP notebook. It queries a Gemini Pro model to synthesize
    pristine, highly detailed Standard Operating Procedures (SOPs) in English and Japanese.
    It embeds the extracted keyframes dynamically into the timeline table.

Key Capabilities:
    - Generates separate English and Japanese SOP documents.
    - Synchronizes the section structures with the input reference template.
    - Resolves and formats dynamic markdown keyframe image links using absolute/relative paths.

Cross-Platform Compatibility:
    - Paths resolved using os.path.abspath and os.path.dirname for compatibility on Windows, macOS, and Linux.
    - Encodes and reads files with UTF-8 to prevent character encoding issues on Windows.
"""

import os
import json
import argparse
from utils import load_api_client

def main():
    parser = argparse.ArgumentParser(description="Generate bilingual reports from parsed timeline, summary, and template.")
    parser.add_argument("--json_path", "-j", required=True, help="Path to the timeline JSON file.")
    parser.add_argument("--summary_path", "-s", required=True, help="Path to the video summary markdown file.")
    parser.add_argument("--template_path", "-t", required=True, help="Path to the template notebook markdown file.")
    parser.add_argument("--output_dir", "-o", required=True, help="Directory to save generated bilingual reports.")
    parser.add_argument("--output_en", help="Optional explicit path to the EN markdown report.")
    parser.add_argument("--output_jp", help="Optional explicit path to the JP markdown report.")
    parser.add_argument("--model", default="gemini-3.1-pro-preview", help="Model to use for generating reports (default: gemini-3.1-pro-preview).")
    
    args = parser.parse_args()
    
    # Read inputs
    print(f"Reading timeline from {args.json_path}...")
    with open(args.json_path, 'r', encoding='utf-8') as f:
        timeline = json.dumps(json.load(f), indent=2)

    print(f"Reading summary from {args.summary_path}...")
    with open(args.summary_path, 'r', encoding='utf-8') as f:
        summary = f.read()

    print(f"Reading template from {args.template_path}...")
    with open(args.template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    client = load_api_client()
    
    prompt_en = f"""You are an expert scientific medical writer and biological researcher.
I will provide you with a raw video timeline and a summarized text of a cell passage protocol.
I will also provide you with a template document showing the exact required structure and sections.

Your task is to synthesize the raw timeline and summary into a pristine, highly-detailed Standard Operating Procedure (SOP) in ENGLISH only.

CRITICAL REQUIREMENTS:
1. **Keyframes**: In the "Video Timeline & Actions" table, you MUST include the markdown image links.
   The keyframe image paths should follow this exact format:
   `![](./annotated_keyframes/row_XX_step_ACTION.jpg)`
   (Where XX is the 1-indexed row number like 01, 02, etc. and ACTION is the primary_action with spaces and slashes replaced by underscores).
2. **Structure**: Strictly follow the sections outlined in the Reference Template, but translate everything to English.

---
### Reference Template Structure:
{template}

---
### Input 1: Raw Parsed Timeline JSON
{timeline}

---
### Input 2: VLM Video Summary
{summary}

---
Please write the final English Markdown report below.
"""

    prompt_jp = f"""You are an expert scientific medical writer and biological researcher.
I will provide you with a raw video timeline and a summarized text of a cell passage protocol.
I will also provide you with a template document showing the exact required structure and sections.

Your task is to synthesize the raw timeline and summary into a pristine, highly-detailed Standard Operating Procedure (SOP) in JAPANESE only.

CRITICAL REQUIREMENTS:
1. **Keyframes**: In the "Video Timeline & Actions" table, you MUST include the markdown image links.
   The keyframe image paths should follow this exact format:
   `![](./annotated_keyframes/row_XX_step_ACTION.jpg)`
   (Where XX is the 1-indexed row number like 01, 02, etc. and ACTION is the primary_action with spaces and slashes replaced by underscores).
2. **Structure**: Strictly follow the sections outlined in the Reference Template, keeping all content natively in Japanese.

---
### Reference Template Structure:
{template}

---
### Input 1: Raw Parsed Timeline JSON
{timeline}

---
### Input 2: VLM Video Summary
{summary}

---
Please write the final Japanese Markdown report below.
"""

    output_en = args.output_en or os.path.join(args.output_dir, "Cell_Passage_Protocol_EN.md")
    output_jp = args.output_jp or os.path.join(args.output_dir, "Cell_Passage_Protocol_JP.md")

    # Make sure output directories exist
    os.makedirs(os.path.dirname(os.path.abspath(output_en)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(output_jp)), exist_ok=True)

    print(f"Requesting {args.model} to synthesize English report...")
    response_en = client.models.generate_content(
        model=args.model,
        contents=prompt_en,
    )
    with open(output_en, 'w', encoding='utf-8') as f:
        f.write(response_en.text)
    print(f"Saved English report to {output_en}")

    print(f"Requesting {args.model} to synthesize Japanese report...")
    response_jp = client.models.generate_content(
        model=args.model,
        contents=prompt_jp,
    )
    with open(output_jp, 'w', encoding='utf-8') as f:
        f.write(response_jp.text)
    print(f"Saved Japanese report to {output_jp}")
        
    print("Done!")

if __name__ == "__main__":
    main()
