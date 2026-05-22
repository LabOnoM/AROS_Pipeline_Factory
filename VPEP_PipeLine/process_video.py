"""
VPEP (Video-to-Protocol Extraction Pipeline) - Video Processor & VLM Parser
===========================================================================

Description:
    This script is the first stage of the VPEP pipeline. It splits the input video into smaller segments,
    uploads them to Google GenAI for analysis, and prompts a VLM (Gemini 2.5/3.5) to parse the actions,
    hand kinematics, reagents, and consumable volumes. The outputs are synthesized into a consolidated
    markdown protocol audit and a structured timeline JSON file.

Key Capabilities:
    - Splits large video files into configurable temporal chunks using FFmpeg segmenter.
    - Uploads chunked files and calls Gemini models sequentially to maintain procedural context.
    - Synthesizes chunked analyses into a single cohesive Markdown summary and a structured timeline JSON.

Cross-Platform Compatibility:
    - Safe path resolution using standard `os.path` functions.
    - Subprocesses execute `ffmpeg` with cross-platform friendly argument list.
"""

import os
import time
import json
import argparse
import subprocess
from google.genai import types
from utils import load_api_client

def split_video(input_path, output_dir, segment_time=600):
    # Splits the video into chunks
    print(f"Splitting video into {segment_time}-second chunks...")
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_pattern = os.path.join(output_dir, f"{base_name}_part%03d.mp4")
    
    # Get list of generated files
    files = sorted([os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.startswith(base_name + "_part") and f.endswith(".mp4")])
    if files:
        print("Chunks already exist, skipping splitting.")
        return files

    # Run ffmpeg to split
    cmd = [
        "ffmpeg", "-i", input_path,
        "-c", "copy",
        "-map", "0",
        "-segment_time", str(segment_time),
        "-f", "segment",
        "-reset_timestamps", "1",
        output_pattern
    ]
    subprocess.run(cmd, check=True)
    
    # Get list of generated files
    files = sorted([os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.startswith(base_name + "_part") and f.endswith(".mp4")])
    return files

def upload_and_wait(client, file_path: str, max_wait_s: int = 600):
    print(f"Uploading {file_path}...")
    myfile = client.files.upload(file=file_path)
    waited = 0
    while myfile.state.name == "PROCESSING" and waited < max_wait_s:
        time.sleep(5)
        waited += 5
        myfile = client.files.get(name=myfile.name)

    if myfile.state.name == "FAILED":
        raise ValueError(f"Video processing failed: {myfile.state.name}")
    if myfile.state.name == "PROCESSING":
        raise TimeoutError(f"Processing timeout after {max_wait_s}s")
    
    print(f"Uploaded {file_path} as {myfile.name}")
    return myfile

prompt = """# Role & Domain Expertise
You are an expert Computer Vision Protocol Parser and Laboratory Automation Analyst. Your objective is to audit first-person (egocentric) laboratory execution videos, decode the underlying scientific workflow, and generate a hyper-granular temporal map of physical actions alongside a precise material consumption log for inventory management.

# Objective
1. Identify the overarching mission, protocol name, or biological/chemical task being executed in the video.
2. Segment the video into distinct, continuous procedural steps based on shifts in actions or targets.
3. Construct a high-fidelity Markdown table mapping timeframes, hand kinematics, specific chemical reagents, laboratory consumables, and background instrumentation.
4. Quantify all materials, reagents, and disposable consumables used during the task to create an automated inventory depletion log.
5. If the video contains audio, transcribe any spoken dialogue, dictation, or relevant sound cues to facilitate the interpretation of the actions and purpose.

# Extraction Granularity Guidelines

When parsing the video, you must apply extreme precision to the following categories:
- **Primary Action / Task:** Define the exact technical sub-protocol occurring (e.g., "Enzymatic dissociation neutralization", "Aspiration of supernatant").
- **Active Hand(s) Kinematics:** Document bimanual coordination. Specify what the Left Hand (LH) and Right Hand (RH) are doing independently or collaboratively.
- **Interacted Objects, Reagents, & Consumables:** Capture explicit item identities (e.g., "15mL conical tube", "sterile serological pipette", "Accutase aliquot").
- **Quantity / Volume Consumed:** Record the exact numeric quantity or volume depleted during that specific step (e.g., "5 mL dispensed", "1 unit used", "10 microliters aspirated").
- **Background Equipment & Environment:** Identify stationary or background assets contextually linked to the step (e.g., "Class II Biosafety Cabinet", "Inverted Phase-Contrast Microscope").
- **Audio Transcription:** Document verbatim what is being spoken (if anything), mapping it to the timeline.

# Output Structure

Your final response must strictly adhere to this layout:

---
## Executive Summary of Protocol
- **Identified Main Mission/Task:** [Name of protocol]
- **Total Duration:** [MM:SS]

---
## Audio Transcription
- **[MM:SS - MM:SS]**: [Transcription text, dictation, or auditory cue]
(Repeat for all audible dialog/sounds in this chunk. If no audio, write "No relevant audio detected.")

---
## Detailed Video Timeline & Actions Table

| Timeline (MM:SS - MM:SS) | Primary Action / Task | Active Hand(s) & Detailed Movements | Interacted Objects & Reagents | Quantity / Volume Consumed | Background Equipment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **[Start] - [End]** | [Action] | **LH:** [Action] <br>**RH:** [Action] | [Item Name / Fluid Type] | [e.g., 5 mL / 1 unit] | [Equipment name] |

---
## Inventory & Material Consumption Ledger
Generate a consolidated list summarizing the total inventory depleted across the entire video for inventory system deduction.

| Material / Reagent / Consumable Name | Total Quantity Consumed | Unit Type (mL, Units, Tips) | Waste Status (Aspirated to Liquid Waste / Seeded in Dish) |
| :--- | :--- | :--- | :--- |
| [e.g., Sterile P1000 Pipette Tips] | [e.g., 3] | Units | Spent / Discarded |
| [e.g., Phosphate-Buffered Saline (PBS)] | [e.g., 10.0] | mL | Aspirated to Liquid Waste |
| [e.g., Accutase Enzyme Solution] | [e.g., 1.0] | mL | Aspirated to Liquid Waste |
| [e.g., 15mL Conical Tube] | [e.g., 1] | Units | Retained (Contains cell pellet) |
| [e.g., 60mm Cell Culture Dish] | [e.g., 1] | Units | Active (In incubator) |

---

# Chain-of-Thought Processing Rules
- **No Volumetric Gaps:** If a reagent bottle is opened and liquid is drawn, use visual cues (pipette graduation lines, micro-pipette dial settings, or verbal confirmation from the operator) to determine the exact volume. If the volume cannot be visually verified, estimate based on standard laboratory protocols for that vessel type and flag it with an asterisk (e.g., "5 mL*").
- **Consumable Unit Tracking:** Explicitly track the disposal of single-use items (e.g., counting each time a pipette tip is ejected or a new serological pipette is unwrapped).
- **Text Labels:** Monitor handwritten labels on tubes, bottles, and dishes, as well as digital UI readouts on centrifuges, timers, and automated cell counters to corroborate volume and inventory tracking.
- **Micro-movements:** Log the complete lifecycle of a consumable: touch/open packaging, load tip, execute transfer, discard/eject tip."""

def main():
    parser = argparse.ArgumentParser(description="Process video for protocol extraction using Gemini models.")
    parser.add_argument("--video_path", "-v", required=True, help="Path to the input video file.")
    parser.add_argument("--output_dir", "-o", required=True, help="Directory to save the outputs.")
    parser.add_argument("--segment_time", type=int, default=600, help="Video segment time in seconds (default: 600).")
    parser.add_argument("--model_analysis", default="gemini-3.5-flash", help="Model name for video analysis.")
    parser.add_argument("--model_synthesis", default="gemini-3.1-pro-preview", help="Model name for synthesis.")
    
    args = parser.parse_args()
    
    client = load_api_client()
    
    temp_dir = os.path.join(args.output_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    chunk_files = split_video(args.video_path, temp_dir, segment_time=args.segment_time)
    
    all_responses = []
    
    for i, chunk in enumerate(chunk_files):
        print(f"Processing chunk {i+1}/{len(chunk_files)}: {chunk}")
        chunk_output_path = os.path.join(temp_dir, f"chunk_{i:03d}_output.md")
        
        if os.path.exists(chunk_output_path):
            print(f"Chunk output {chunk_output_path} already exists. Skipping upload and API call.")
            with open(chunk_output_path, "r", encoding="utf-8") as f:
                chunk_output = f.read()
        else:
            uploaded_file = upload_and_wait(client, chunk)
            
            current_contents = [prompt]
            if i > 0 and all_responses:
                prev_chunk_output = all_responses[-1]
                continuation_prompt = f"For context, here is your parsed output from the preceding video chunk. Please continue parsing this current video chunk, maintaining temporal continuity and the state of the inventory ledger:\n\n{prev_chunk_output}\n\nNow, parse the attached video chunk."
                current_contents.append(continuation_prompt)
                
            current_contents.append(uploaded_file)
            
            response = client.models.generate_content(
                model=args.model_analysis,
                contents=current_contents,
            )
            
            chunk_output = response.text
            with open(chunk_output_path, "w", encoding="utf-8") as f:
                f.write(chunk_output)
                
        all_responses.append(chunk_output)
        
    print("Combining responses...")
    
    final_md_path = os.path.join(args.output_dir, "vlm_video_summary.md")
    final_json_path = os.path.join(args.output_dir, "vlm_parsed_timeline.json")
    
    combined_content = "# Combined VLM Parsing Output\n\n"
    for i, res in enumerate(all_responses):
        combined_content += f"## Chunk {i+1}\n\n{res}\n\n---\n"
        
    # Ask Gemini to synthesize the final MD and JSON based on the combined responses.
    synthesis_prompt = f"""You are an expert Laboratory Automation Analyst. I have processed a long video in chunks and received the following chunked outputs. 
Please synthesize them into a single, cohesive document following the EXACT structure requested originally, with the following sections:
## Executive Summary of Protocol
## Audio Transcription
## Detailed Video Timeline & Actions Table
## Inventory & Material Consumption Ledger

For the timeline, please adjust the timestamps to reflect the continuous timeline (e.g. if Chunk 1 is 0-10m, Chunk 2 is 10-20m, Chunk 3 is 20-30m, etc. So add 10 mins to Chunk 2's timestamps, 20 mins to Chunk 3's, etc. if they restarted from 0 in each chunk's output).
Also generate a unified Inventory Ledger.

Here are the chunked responses:
{combined_content}
"""

    synth_response = client.models.generate_content(
        model=args.model_synthesis,
        contents=[synthesis_prompt]
    )
    
    with open(final_md_path, "w", encoding="utf-8") as f:
        f.write(synth_response.text)
        
    json_prompt = """Based on the final markdown output, please provide a structured JSON representation of the timeline. The JSON should be an array of objects, where each object has:
- start_time: string (MM:SS)
- end_time: string (MM:SS)
- primary_action: string
- active_hands: string
- objects_reagents: string
- quantity_consumed: string
- background_equipment: string

Markdown to parse:
""" + synth_response.text

    json_response = client.models.generate_content(
        model=args.model_analysis,
        contents=[json_prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    with open(final_json_path, "w", encoding="utf-8") as f:
        f.write(json_response.text)
        
    print(f"Done. Final files saved to {args.output_dir}")

if __name__ == "__main__":
    main()
