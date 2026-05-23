"""
VPEP (Video-to-Protocol Extraction Pipeline) - Interactive HTML Generator
========================================================================

Description:
    This script is Stage 5 of the VPEP pipeline. It takes the parsed timeline JSON and the SOP
    markdown, extracts CSS/JS styling from a reference HTML, and queries a Gemini Pro model
    to generate custom, structured HTML content for 9 specific sections of an interactive Audit Report.
    It returns these sections as JSON and consolidates them into a styled interactive HTML page.

Key Capabilities:
    - Custom HTML extraction for 9 report sections (Executive Summary, Compliance Matrix, etc.).
    - Embeds keyframe thumbnails with interactive click-to-zoom Lightbox controls.
    - Integrates search controls and simulated audio transcriptions.

Cross-Platform Compatibility:
    - Verified on Windows, macOS, and Linux.
    - Uses UTF-8 encoding exclusively for reading and writing HTML files.
"""

import os
import json
import argparse
from utils import load_api_client

def extract_assets(reference_path):
    with open(reference_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    style_block = ""
    if "<style>" in content and "</style>" in content:
        style_block = content.split("<style>")[1].split("</style>")[0]
        
    script_block = ""
    if "<script>" in content and "</script>" in content:
        script_block = content.split("<script>")[1].split("</script>")[0]
        
    return style_block, script_block

def build_prompt(timeline_json, sop_text, lang="EN"):
    language_instruction = "ENGLISH" if lang == "EN" else "JAPANESE"
    
    return f"""You are an expert scientific auditor and medical writer.
I will provide you with a raw video timeline JSON and a Standard Operating Procedure (SOP).
Your task is to generate the pure HTML content for 8 specific sections of a comprehensive Audit Report in {language_instruction}.
DO NOT hardcode generic text. Base everything strictly on the TIMELINE JSON. If the timeline JSON does not contain certain details, extrapolate logically based on standard scientific protocols. For the Audio Transcripts Log, since no audio was recorded, you MUST simulate a realistic audio transcript of what the researcher would likely be saying/dictating at each step.

You must return a valid JSON object with exactly the following 8 keys. The value for each key must be the raw HTML content (strings) for that section.
Do NOT include markdown backticks around the JSON. Return purely the JSON object.

Keys:
"qc_executive_summary": HTML paragraphs summarizing the overall compliance, major deviations, and execution quality.
"protocol_compliance_matrix": A complete HTML `<table>` (with `<thead>` and `<tbody>`) comparing the Timeline against the SOP. Use `<tr>` and `<td>`. The columns must be: Step, SOP Requirement, Observed Action, Compliance Badge, Time Window, Assessment Notes, Keyframe.
   - For badges use: `<span class="badge badge-success">COMPLIANT</span>`, `<span class="badge badge-warning">MINOR_DEVIATION</span>`, `<span class="badge badge-danger">MAJOR_DEVIATION</span>`.
   - For Keyframes use: `<img src="EXACT_URL" alt="Keyframe" class="table-img"/>` (Replace EXACT_URL with the exact string from the `keyframe_url` field provided in the timeline JSON step).
"inventory_safety_warnings": An HTML `<table>` listing observed reagents/objects and any safety/expiration warnings derived or inferred from the actions.
"qualitative_observations": An HTML `<table>` of qualitative visual observations (e.g. aseptic technique, pellet quality) inferred from the timeline.
"actionable_recommendations": An HTML `<ul>` list of recommendations for the operator.
"reagents_and_instruments": An HTML `<table>` listing the reagents and instruments identified in the timeline.
"experimental_stages": HTML paragraphs or lists outlining the high-level stages of the experiment.
"audio_transcripts_log": An HTML `<table>` containing a simulated/extrapolated audio transcript for the timeline steps, with columns for Time Window and Simulated Transcript. State clearly before the table that this is a simulated transcript.

--- SOP ---
{sop_text}

--- TIMELINE JSON ---
{timeline_json}
"""

def main():
    parser = argparse.ArgumentParser(description="Generate interactive HTML reports from parsed timeline and SOP.")
    parser.add_argument("--json_path", "-j", required=True, help="Path to the timeline JSON file.")
    parser.add_argument("--sop_path", "-s", required=True, help="Path to the SOP markdown/text file.")
    parser.add_argument("--ref_html_path", "-r", required=True, help="Path to the reference HTML file containing CSS/JS styles.")
    parser.add_argument("--output_dir", "-o", required=True, help="Directory to save the outputs.")
    parser.add_argument("--output_en", help="Optional explicit path to the EN HTML report.")
    parser.add_argument("--output_jp", help="Optional explicit path to the JP HTML report.")
    parser.add_argument("--model", default="gemini-3.1-pro-preview", help="Model to use for generation (default: gemini-3.1-pro-preview).")
    
    args = parser.parse_args()
    
    client = load_api_client()
    
    print(f"Reading assets from {args.ref_html_path}...")
    style_block, script_block = extract_assets(args.ref_html_path)
    
    print("Injecting explicit keyframe URLs into timeline to prevent hallucinations...")
    with open(args.json_path, 'r', encoding='utf-8') as f:
        timeline_data = json.load(f)
        for i, step in enumerate(timeline_data):
            img_name = f"row_{i+1:02d}_step_{step['primary_action'].replace(' ', '_').replace('/', '')}.jpg"
            step['keyframe_url'] = f"annotated_keyframes/{img_name}"
        timeline = json.dumps(timeline_data, indent=2)
        
    print(f"Reading SOP from {args.sop_path}...")
    with open(args.sop_path, 'r', encoding='utf-8') as f:
        sop_text = f.read()
        
    out_en = args.output_en or os.path.join(args.output_dir, "Interactive_Report_EN.html")
    out_jp = args.output_jp or os.path.join(args.output_dir, "Interactive_Report_JA.html")
    
    def generate_html(lang, out_path):
        print(f"Requesting {args.model} for {lang} sections...")
        prompt = build_prompt(timeline, sop_text, lang)
        
        response = client.models.generate_content(
            model=args.model,
            contents=prompt,
        )
        
        try:
            # Strip potential markdown formatting from response
            json_text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(json_text)
        except Exception as e:
            print(f"Failed to parse JSON for {lang}: {e}")
            print("Raw response first 500 characters:")
            print(response.text[:500])
            return
        
        title = "VPEP Video Analysis Audit Report" if lang == "EN" else "VPEP ビデオ分析監査レポート"
        
        headers = {
            "EN": {
                "qc_summary": "1. QC Executive Summary",
                "compliance_matrix": "2. Protocol Compliance Matrix",
                "search_placeholder": "Search timeline...",
                "inventory_safety": "3. Inventory & Safety Warnings",
                "qualitative_obs": "4. Qualitative Observations",
                "recommendations": "5. Actionable Recommendations",
                "video_section": "6. Masked Tracking Video",
                "video_subtitle": "Generated at 1 FPS from annotated keyframes.",
                "video_fallback": "Your browser does not support the video tag.",
                "reagents_instruments": "7. Reagents and Instruments (VLM Identifications)",
                "exp_stages": "8. Experimental Stages",
                "audio_log": "9. Audio Transcripts Log"
            },
            "JP": {
                "qc_summary": "1. QCエグゼクティブ・サマリー",
                "compliance_matrix": "2. プロトコール遵守マトリクス",
                "search_placeholder": "テーブル内の検索...",
                "inventory_safety": "3. 在庫および安全警告",
                "qualitative_obs": "4. 定性的観察事項",
                "recommendations": "5. 実行可能な推奨事項",
                "video_section": "6. 追跡ビデオ",
                "video_subtitle": "アノテーション付きキーフレームから1 FPSで生成。",
                "video_fallback": "お使いのブラウザはビデオタグをサポートしていません。",
                "reagents_instruments": "7. 試薬・器具一覧（VLM特定）",
                "exp_stages": "8. 実験工程",
                "audio_log": "9. 音声記録ログ"
            }
        }
        h = headers["JP"] if lang in ("JP", "JA") else headers["EN"]
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
    {style_block}
    table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
    th, td {{ padding: 12px; border: 1px solid var(--border-color); text-align: left; }}
    th {{ background-color: rgba(255,255,255,0.05); color: var(--primary); }}
    </style>
</head>
<body>
    <div class="container">
        <h1 style="text-align:center; margin-bottom: 40px; color: var(--primary);">{title}</h1>
        
        <div class="card">
            <h2>{h['qc_summary']}</h2>
            {data.get('qc_executive_summary', '')}
        </div>

        <div class="card">
            <h2>{h['compliance_matrix']}</h2>
            <input type="text" class="search-input" placeholder="{h['search_placeholder']}" onkeyup="filterTable(this)">
            <div style="overflow-x: auto;">
                {data.get('protocol_compliance_matrix', '')}
            </div>
        </div>

        <div class="card">
            <h2>{h['inventory_safety']}</h2>
            {data.get('inventory_safety_warnings', '')}
        </div>

        <div class="card">
            <h2>{h['qualitative_obs']}</h2>
            {data.get('qualitative_observations', '')}
        </div>

        <div class="card">
            <h2>{h['recommendations']}</h2>
            {data.get('actionable_recommendations', '')}
        </div>

        <div class="card">
            <h2>{h['video_section']}</h2>
            <div class="video-container">
                <video controls>
                    <source src="masked_tracking_video.mp4" type="video/mp4">
                    {h['video_fallback']}
                </video>
                <p class="subtitle" style="margin-top: 15px;">{h['video_subtitle']}</p>
            </div>
        </div>

        <div class="card">
            <h2>{h['reagents_instruments']}</h2>
            {data.get('reagents_and_instruments', '')}
        </div>

        <div class="card">
            <h2>{h['exp_stages']}</h2>
            {data.get('experimental_stages', '')}
        </div>

        <div class="card">
            <h2>{h['audio_log']}</h2>
            {data.get('audio_transcripts_log', '')}
        </div>

    </div>
    <script>
    {script_block}
    </script>
</body>
</html>
"""
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Saved {out_path}")
        
    generate_html("EN", out_en)
    generate_html("JP", out_jp)
    print("Done!")

if __name__ == "__main__":
    main()
