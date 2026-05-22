"""
VPEP (Video-to-Protocol Extraction Pipeline) - Test Keyframe Extractor
======================================================================

Description:
    This script is a variation of `extract_annotated_keyframes.py` customized for lower detection thresholds
    and tracking mode (`static_image_mode=False`). It extracts frames at 1fps using direct OpenCV seeks
    and uses MediaPipe Hands to capture hand landmarks at lower confidence, with Gemini predicting bounding boxes.

Key Capabilities:
    - Runs MediaPipe Hands in tracking mode (lower latency, handles multi-frame context).
    - Lower confidence detection threshold (0.1) for loose or difficult hand poses.
    - Annotates keyframes with Gemini bounding boxes and MediaPipe landmarks.

Cross-Platform Compatibility:
    - Full compatibility with Linux, macOS, and Windows. Headless execution compatible.
"""

import os
import json
import cv2
import base64
import argparse
import mediapipe as mp
from google.genai import types
from utils import load_api_client, time_to_seconds

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def extract_candidate_frames(video_path, start_sec, end_sec, max_candidates=10, 
                             static_image_mode=False, max_num_hands=2, 
                             min_detection_confidence=0.1, min_tracking_confidence=0.1):
     """Extract frames between start_sec and end_sec at ~1fps, and filter using MediaPipe Hands."""
     cap = cv2.VideoCapture(video_path)
     fps = cap.get(cv2.CAP_PROP_FPS)
     if fps <= 0: fps = 30
     
     candidates = []
     
     with mp_hands.Hands(
         static_image_mode=static_image_mode,
         model_complexity=1,
         max_num_hands=max_num_hands,
         min_detection_confidence=min_detection_confidence,
         min_tracking_confidence=min_tracking_confidence) as hands:
         
         for sec in range(int(start_sec), int(end_sec) + 1):
             frame_idx = int(sec * fps)
             cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
             ret, frame = cap.read()
             if not ret: break
             
             # Convert BGR to RGB for MediaPipe
             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
             results = hands.process(rgb_frame)
             
             # If hands detected, this is a candidate
             if results.multi_hand_landmarks:
                 candidates.append({
                     'image': frame,
                     'landmarks': results.multi_hand_landmarks,
                     'timestamp': sec
                 })
             
     # If no hands detected at all, take the middle frame to guarantee 1 candidate
     if not candidates:
         print("No hands detected by MediaPipe. Taking middle frame as candidate.")
         mid_sec = (start_sec + end_sec) / 2
         cap.set(cv2.CAP_PROP_POS_FRAMES, int(mid_sec * fps))
         ret, frame = cap.read()
         if ret:
             candidates.append({
                 'image': frame,
                 'landmarks': None,
                 'timestamp': mid_sec
             })
             
     cap.release()
     
     # Downsample evenly if we have too many candidates
     if len(candidates) > max_candidates:
         step = len(candidates) / max_candidates
         candidates = [candidates[int(i * step)] for i in range(max_candidates)]
         
     return candidates

def main():
    parser = argparse.ArgumentParser(description="Test keyframe extraction with lower MediaPipe thresholds.")
    parser.add_argument("--video_path", "-v", required=True, help="Path to the input video file.")
    parser.add_argument("--json_path", "-j", required=True, help="Path to the input timeline JSON file.")
    parser.add_argument("--output_dir", "-o", required=True, help="Directory to save annotated keyframes.")
    parser.add_argument("--model", default="gemini-3.5-flash", help="Gemini model name.")
    parser.add_argument("--static_image_mode", type=lambda x: (str(x).lower() == 'true'), default=False, help="MediaPipe static image mode.")
    parser.add_argument("--max_num_hands", type=int, default=2, help="MediaPipe max num hands.")
    parser.add_argument("--min_detection_confidence", type=float, default=0.1, help="MediaPipe min detection confidence.")
    parser.add_argument("--min_tracking_confidence", type=float, default=0.1, help="MediaPipe min tracking confidence.")
    parser.add_argument("--title_position", default="upper_right", choices=["lower_left", "upper_right"], help="Position to draw the title text.")
    
    args = parser.parse_args()
    
    client = load_api_client()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load Timeline
    with open(args.json_path, 'r', encoding='utf-8') as f:
        timeline = json.load(f)
        
    for i, step in enumerate(timeline):
        print(f"\nProcessing Step {i+1}/{len(timeline)}: {step['primary_action']}")
        
        # Parse times
        start_sec = time_to_seconds(step['start_time'])
        end_sec = time_to_seconds(step['end_time'])
        
        print(f"Extracting candidates between {step['start_time']} and {step['end_time']}...")
        candidates = extract_candidate_frames(
            args.video_path, start_sec, end_sec,
            static_image_mode=args.static_image_mode,
            max_num_hands=args.max_num_hands,
            min_detection_confidence=args.min_detection_confidence,
            min_tracking_confidence=args.min_tracking_confidence
        )
        
        if not candidates:
            print("Failed to extract any candidate frames (video end?). Skipping.")
            continue
            
        print(f"Found {len(candidates)} candidate frames.")
        
        # Prepare parts for Gemini
        prompt_text = f"""You are an expert Laboratory Automation Vision Analyst.
Attached are {len(candidates)} candidate frames extracted from a laboratory video during a specific protocol step.

Protocol Step Details:
- Primary Action: {step['primary_action']}
- Active Hands: {step['active_hands']}
- Interacted Objects & Reagents: {step['objects_reagents']}

Task:
1. Examine all candidate frames. Select the single best frame index (0 to {len(candidates)-1}) that most clearly demonstrates the hands interacting with the primary object.
2. Provide bounding boxes for the primary interacted object(s). If there are multiple key objects (up to 2) necessary to support the description, you may include them. Provide the coordinates strictly in the format [ymin, xmin, ymax, xmax] scaled from 0 to 1000.
3. Provide a short, precise label for each object (e.g., "15mL Conical Tube", "Pipette").

Respond strictly in JSON format matching this schema:
{{
    "selected_index": int,
    "objects": [
        {{
            "object_bounding_box": [int, int, int, int],
            "object_label": "string"
        }}
    ]
}}
"""
        parts = [prompt_text]
        for idx, cand in enumerate(candidates):
            success, encoded_image = cv2.imencode('.jpg', cand['image'])
            if success:
                parts.append(f"Frame Index: {idx}")
                parts.append(types.Part.from_bytes(data=encoded_image.tobytes(), mime_type='image/jpeg'))
                
        print(f"Asking Gemini to select keyframe and object boundary using {args.model}...")
        try:
            response = client.models.generate_content(
                model=args.model,
                contents=parts,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            sel_idx = result.get('selected_index', 0)
            objects = result.get('objects', [])
            
            if sel_idx < 0 or sel_idx >= len(candidates):
                sel_idx = 0
                
            print(f"Gemini selected frame {sel_idx}. Found {len(objects)} objects.")
            
            best_cand = candidates[sel_idx]
            frame_to_draw = best_cand['image'].copy()
            tracked_landmarks = best_cand['landmarks']
            
            # Draw MediaPipe Hands Skeleton
            if tracked_landmarks:
                for hand_landmarks in tracked_landmarks:
                    mp_drawing.draw_landmarks(
                        frame_to_draw,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
            
            h, w, _ = frame_to_draw.shape
            
            # Draw Gemini Bounding Boxes
            for obj in objects:
                bbox = obj.get('object_bounding_box', [0,0,0,0])
                label = obj.get('object_label', 'Object')
                
                ymin, xmin, ymax, xmax = bbox
                # Convert from [0, 1000] scale to pixel coordinates
                px_ymin = int((ymin / 1000.0) * h)
                px_xmin = int((xmin / 1000.0) * w)
                px_ymax = int((ymax / 1000.0) * h)
                px_xmax = int((xmax / 1000.0) * w)
                
                # Draw Box
                cv2.rectangle(frame_to_draw, (px_xmin, px_ymin), (px_xmax, px_ymax), (0, 255, 0), 3)
                
                # Draw Label
                label_text = f"{label} (Gemini)"
                font_scale = 1.0
                thickness = 2
                (text_w, text_h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                
                # Default position: above the top-left corner
                rect_y1 = px_ymin - text_h - 10
                rect_y2 = px_ymin
                label_y = px_ymin - 5
                
                rect_x1 = px_xmin
                rect_x2 = px_xmin + text_w
                label_x = px_xmin
                
                # If out of bounds on top, move below the top edge (inside box)
                if rect_y1 < 0:
                    rect_y1 = px_ymin
                    rect_y2 = px_ymin + text_h + 10
                    label_y = px_ymin + text_h + 5
                
                # If out of bounds on left or right, center it horizontally within the box
                if rect_x1 < 0 or rect_x2 > w:
                    box_center_x = px_xmin + (px_xmax - px_xmin) // 2
                    label_x = box_center_x - text_w // 2
                    rect_x1 = label_x
                    rect_x2 = label_x + text_w
                    
                    # Clamp to absolute screen boundaries just in case
                    if rect_x1 < 0:
                        rect_x1 = 0
                        rect_x2 = text_w
                        label_x = 0
                    if rect_x2 > w:
                        rect_x2 = w
                        rect_x1 = w - text_w
                        label_x = w - text_w
                
                cv2.rectangle(frame_to_draw, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 255, 0), -1)
                cv2.putText(frame_to_draw, label_text, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness)
            
            # Draw Title and Timestamp
            title_text = f"[{step['start_time']} - {step['end_time']}] {step['primary_action']}"
            title_font_scale = 1.2
            title_thick = 3
            (tw, th), _ = cv2.getTextSize(title_text, cv2.FONT_HERSHEY_SIMPLEX, title_font_scale, title_thick)
            
            if args.title_position == "lower_left":
                title_x = 20
                title_y = h - 20
                rect_y_start = title_y - th - 10
                rect_y_end = title_y + 10
            else:
                # upper_right
                title_x = w - tw - 20
                title_y = th + 20
                rect_y_start = title_y - th - 10
                rect_y_end = title_y + 10
                
            # Draw black background rectangle for title
            cv2.rectangle(frame_to_draw, (title_x - 10, rect_y_start), (title_x + tw + 10, rect_y_end), (0, 0, 0), -1)
            # Draw yellow text
            cv2.putText(frame_to_draw, title_text, (title_x, title_y), cv2.FONT_HERSHEY_SIMPLEX, title_font_scale, (0, 255, 255), title_thick)
            
            # Save Image
            out_filename = f"row_{i+1:02d}_step_{step['primary_action'].replace(' ', '_').replace('/', '')}.jpg"
            out_filepath = os.path.join(args.output_dir, out_filename)
            cv2.imwrite(out_filepath, frame_to_draw)
            print(f"Saved annotated keyframe to {out_filepath}")
            
        except Exception as e:
            print(f"Error processing step {i+1}: {e}")

if __name__ == "__main__":
    main()
