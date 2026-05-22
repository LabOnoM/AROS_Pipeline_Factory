"""
VPEP (Video-to-Protocol Extraction Pipeline) - Master Orchestrator
==================================================================

Description:
    This script acts as the main entry point (orchestrator) for the VPEP workflow. It automatically
    detects if an input video has a compressed counterpart, performs compression if needed,
    and runs all subsequent processing, keyframe extraction, and reporting stages in sequence.

Key Capabilities:
    - Automatically checks for video compression and compresses raw video files via FFmpeg on the fly.
    - Sequentially executes 6 pipeline stages (processing, keyframe extraction, notebook, report, interactive HTML, and dashboard).
    - Accepts parameters from JSON configuration files and overrides them with CLI arguments.

Cross-Platform Compatibility:
    - Paths resolved using os.path.abspath and os.path.dirname for compatibility on Windows, macOS, and Linux.
    - Uses system-agnostic python execution (via sys.executable) for downstream stages.
"""

import os
import sys
import json
import argparse
import subprocess

def run_stage(script_name, args_list):
    """Executes a pipeline stage script as a subprocess."""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
    cmd = [sys.executable, script_path] + args_list
    print(f"\n========================================================")
    print(f"RUNNING STAGE: {script_name}")
    print(f"COMMAND: {' '.join(cmd)}")
    print(f"========================================================\n")
    
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Stage {script_name} failed with return code {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)
    print(f"Stage {script_name} completed successfully.\n")

def main():
    parser = argparse.ArgumentParser(description="Master orchestrator for the VPEP pipeline.")
    parser.add_argument("--config", "-c", help="Path to the JSON configuration file.")
    parser.add_argument("--video_path", "-v", help="Path to the input video file.")
    parser.add_argument("--output_dir", "-o", help="Directory where all outputs should be written.")
    parser.add_argument("--materials_dir", help="Directory containing standard SOP/reference materials.")
    parser.add_argument("--sop_docx_path", help="Path to the SOP DOCX file.")
    parser.add_argument("--sop_template_path", help="Path to the SOP/notebook markdown template.")
    parser.add_argument("--reference_notebook_path", help="Path to reference Compared_Experiment_Notebook.md.")
    parser.add_argument("--reference_html_path", help="Path to reference VPEP_Audit_Report.html.")
    parser.add_argument("--segment_time", type=int, help="Video segment time in seconds (default: 600).")
    parser.add_argument("--model_flash", help="Gemini model for analysis and JSON parsing (default: gemini-3.5-flash).")
    parser.add_argument("--model_pro", help="Gemini model for report synthesis (default: gemini-3.1-pro-preview).")
    parser.add_argument("--use_test_extract", action="store_true", help="If set, uses test_extract.py instead of extract_annotated_keyframes.py.")
    
    args = parser.parse_args()
    
    config = {}
    
    # 1. Load config JSON if provided
    if args.config:
        if os.path.exists(args.config):
            print(f"Loading configuration from {args.config}...")
            with open(args.config, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            print(f"Warning: Configuration file {args.config} not found. Using defaults/CLI args.", file=sys.stderr)
            
    # 2. Merge configuration with CLI arguments taking precedence
    video_path = args.video_path or config.get("video_path")
    output_dir = args.output_dir or config.get("output_dir")
    materials_dir = args.materials_dir or config.get("materials_dir")
    
    if not video_path:
        print("Error: video_path must be specified either in config or CLI args.", file=sys.stderr)
        sys.exit(1)
    if not output_dir:
        print("Error: output_dir must be specified either in config or CLI args.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # 3. Intelligent video compression detection using ffprobe metadata
    from utils import compress_video, is_video_already_compressed
    basename = os.path.basename(video_path)

    # Fast-path: if the file is already named with our convention, skip detection
    if basename.startswith("compressed_"):
        print(f"Input video '{basename}' is already marked as compressed (prefix). Proceeding.")
    elif is_video_already_compressed(video_path):
        # ffprobe analysis shows video is already at or below VPEP targets
        print(f"Input video '{basename}' is already compressed (ffprobe metadata check). Skipping re-compression.")
    else:
        # Video needs compression — check for existing compressed file first (backward compat)
        dir_name = os.path.dirname(os.path.abspath(video_path))
        base_no_ext, ext = os.path.splitext(basename)
        compressed_name = f"compressed_{base_no_ext}.mp4"
        candidate_compressed_path = os.path.join(dir_name, compressed_name)
        
        if os.path.exists(candidate_compressed_path):
            print(f"Found existing compressed video at: {candidate_compressed_path}")
            video_path = candidate_compressed_path
        else:
            # Compress the video. Write to output_dir if input dir is not writable.
            if os.access(dir_name, os.W_OK):
                compressed_output_path = os.path.join(dir_name, compressed_name)
            else:
                compressed_output_path = os.path.join(output_dir, compressed_name)
            
            print(f"Video requires compression (high resolution/bitrate/fps detected).")
            try:
                compress_video(video_path, compressed_output_path)
                video_path = compressed_output_path
            except Exception as e:
                print(f"Error compressing video: {e}. Falling back to original video.", file=sys.stderr)
        
    # Resolve materials directory fallback if needed
    if not materials_dir:
        materials_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "01.Materials")
        
    sop_docx_path = args.sop_docx_path or config.get("sop_docx_path") or os.path.join(materials_dir, "Cell_Passage_Protocol_Trypsin.docx")
    sop_template_path = args.sop_template_path or config.get("sop_template_path") or os.path.join(os.path.dirname(output_dir), "NewData", "Compared_Experiment_Notebook.md")
    # If the default sop_template_path doesn't exist, we can fallback to standard NewData directory or a known template
    if not os.path.exists(sop_template_path):
        # Fallback search or fallback to a known location
        new_data_template = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "02.Outputs", "NewData", "Compared_Experiment_Notebook.md")
        if os.path.exists(new_data_template):
            sop_template_path = new_data_template
            
    reference_notebook_path = args.reference_notebook_path or config.get("reference_notebook_path") or os.path.join(os.path.dirname(output_dir), "archive", "Compared_Experiment_Notebook.md")
    if not os.path.exists(reference_notebook_path):
        archive_ref_notebook = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "02.Outputs", "SAM3_LabClaw_Analysis", "archive", "Compared_Experiment_Notebook.md")
        if os.path.exists(archive_ref_notebook):
            reference_notebook_path = archive_ref_notebook

    # Fallback to reference_notebook_path if sop_template_path does not exist
    if not os.path.exists(sop_template_path) and os.path.exists(reference_notebook_path):
        sop_template_path = reference_notebook_path

    reference_html_path = args.reference_html_path or config.get("reference_html_path") or os.path.join(os.path.dirname(output_dir), "archive", "VPEP_Audit_Report.html")
    if not os.path.exists(reference_html_path):
        archive_ref_html = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "02.Outputs", "SAM3_LabClaw_Analysis", "archive", "VPEP_Audit_Report.html")
        if os.path.exists(archive_ref_html):
            reference_html_path = archive_ref_html
            
    segment_time = args.segment_time or config.get("segment_time", 600)
    model_flash = args.model_flash or config.get("model_flash", "gemini-3.5-flash")
    model_pro = args.model_pro or config.get("model_pro", "gemini-3.1-pro-preview")
    use_test_extract = args.use_test_extract or config.get("use_test_extract", False)
    
    # Print resolved configuration
    print("\nResolved Pipeline Parameters:")
    print(f"  video_path:               {video_path}")
    print(f"  output_dir:               {output_dir}")
    print(f"  materials_dir:            {materials_dir}")
    print(f"  sop_docx_path:            {sop_docx_path}")
    print(f"  sop_template_path:        {sop_template_path}")
    print(f"  reference_notebook_path:  {reference_notebook_path}")
    print(f"  reference_html_path:      {reference_html_path}")
    print(f"  segment_time:             {segment_time}")
    print(f"  model_flash:              {model_flash}")
    print(f"  model_pro:                {model_pro}")
    print(f"  use_test_extract:         {use_test_extract}")
    print("--------------------------------------------------------\n")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Defined outputs used downstream
    json_path = os.path.join(output_dir, "vlm_parsed_timeline.json")
    summary_path = os.path.join(output_dir, "vlm_video_summary.md")
    keyframes_dir = os.path.join(output_dir, "annotated_keyframes")
    
    # ----------------------------------------------------
    # Stage 1: process_video.py
    # ----------------------------------------------------
    stage1_args = [
        "-v", video_path,
        "-o", output_dir,
        "--segment_time", str(segment_time),
        "--model_analysis", model_flash,
        "--model_synthesis", model_pro
    ]
    run_stage("process_video.py", stage1_args)
    
    # ----------------------------------------------------
    # Stage 2: Keyframe extraction
    # ----------------------------------------------------
    keyframe_script = "test_extract.py" if use_test_extract else "extract_annotated_keyframes.py"
    stage2_args = [
        "-v", video_path,
        "-j", json_path,
        "-o", keyframes_dir,
        "--model", model_flash
    ]
    run_stage(keyframe_script, stage2_args)
    
    # ----------------------------------------------------
    # Stage 2.5: generate_tracking_video.py
    # ----------------------------------------------------
    stage2_5_args = [
        "-o", output_dir
    ]
    run_stage("generate_tracking_video.py", stage2_5_args)
    
    # ----------------------------------------------------
    # Stage 3: generate_compared_notebook.py
    # ----------------------------------------------------
    stage3_args = [
        "-j", json_path,
        "-d", sop_docx_path,
        "-r", reference_notebook_path,
        "-o", output_dir,
        "--model", model_pro
    ]
    run_stage("generate_compared_notebook.py", stage3_args)
    
    # ----------------------------------------------------
    # Stage 4: generate_bilingual_report.py
    # ----------------------------------------------------
    stage4_args = [
        "-j", json_path,
        "-s", summary_path,
        "-t", sop_template_path,
        "-o", output_dir,
        "--model", model_pro
    ]
    run_stage("generate_bilingual_report.py", stage4_args)
    
    # ----------------------------------------------------
    # Stage 5: generate_interactive_html.py
    # ----------------------------------------------------
    # We use the generated Compared_Experiment_Notebook_EN.md as the SOP comparison text
    generated_sop_path = os.path.join(output_dir, "Compared_Experiment_Notebook_EN.md")
    stage5_args = [
        "-j", json_path,
        "-s", generated_sop_path,
        "-r", reference_html_path,
        "-o", output_dir,
        "--model", model_pro
    ]
    run_stage("generate_interactive_html.py", stage5_args)
    
    # ----------------------------------------------------
    # Stage 6: generate_master_dashboard.py
    # ----------------------------------------------------
    stage6_args = [
        "-o", output_dir
    ]
    run_stage("generate_master_dashboard.py", stage6_args)
    
    print("VPEP Pipeline Completed Successfully!")
    print(f"Master interactive report is available at: {os.path.join(output_dir, 'Interactive_Report.html')}")

if __name__ == "__main__":
    main()
