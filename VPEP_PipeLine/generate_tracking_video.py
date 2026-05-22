"""
VPEP (Video-to-Protocol Extraction Pipeline) - Stage 2.5: Tracking Video Generator
================================================================================

Description:
    This script stitches the chronologically sorted annotated keyframes (extracted in Stage 2)
    into a continuous slideshow video at a standard framerate (e.g., 30 FPS).
    It then transcodes the output to H.264 (yuv420p) via FFmpeg to guarantee cross-platform 
    HTML5 browser compatibility. This restores the video playback functionality inside the
    final interactive dashboard.

Key Capabilities:
    - Automatically discovers and sorts `.jpg` keyframes from the `annotated_keyframes` directory.
    - Compiles a cohesive H.264 tracking video (`masked_tracking_video.mp4`).
    - Implements resume logic: skips generation if the video already exists to save compute.

Cross-Platform Compatibility:
    - Path resolution utilizes `os.path` for robust Windows, macOS, and Linux compatibility.
    - Utilizes standard OpenCV capabilities and defensively falls back if FFmpeg H.264 re-encoding fails.
"""

import os
import cv2
import glob
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("GenerateTrackingVideo")

def generate_video(output_dir, fps=30, hold_seconds=2):
    keyframes_dir = os.path.join(output_dir, "annotated_keyframes")
    output_path = os.path.join(output_dir, "masked_tracking_video.mp4")

    if os.path.exists(output_path):
        logger.info(f"Tracking video already exists at {output_path}. Skipping generation to resume pipeline efficiently.")
        return

    image_files = glob.glob(os.path.join(keyframes_dir, "*.jpg"))
    # Sort files to maintain chronological order based on VLM extraction
    image_files.sort()

    if not image_files:
        logger.error(f"No keyframes found in {keyframes_dir}")
        return

    logger.info(f"Found {len(image_files)} keyframes. Generating slideshow video...")

    # Read first image to get dimensions
    first_image = cv2.imread(image_files[0])
    if first_image is None:
        logger.error(f"Failed to read first image: {image_files[0]}")
        return
        
    height, width, layers = first_image.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_video = cv2.VideoWriter(output_path, fourcc, float(fps), (width, height))

    frames_per_image = int(fps * hold_seconds)

    try:
        for img_path in image_files:
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, (width, height))
                for _ in range(frames_per_image):
                    out_video.write(img)
            else:
                logger.warning(f"Could not read image: {img_path}")
    finally:
        out_video.release()
        logger.info(f"Initial MP4 video generated at {output_path}")

    logger.info("Re-encoding video to H.264 for HTML5 browser compatibility...")
    temp_video_path = output_path.replace(".mp4", "_temp.mp4")
    
    if os.path.exists(output_path):
        try:
            import subprocess
            os.rename(output_path, temp_video_path)
            subprocess.run([
                "ffmpeg", "-y", "-i", temp_video_path, "-vcodec", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.0", output_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info("H.264 re-encoding completed successfully.")
            if os.path.exists(temp_video_path): 
                os.remove(temp_video_path)
        except Exception as e:
            logger.error(f"Failed to re-encode video to H.264 using ffmpeg: {str(e)}")
            if os.path.exists(temp_video_path):
                if os.path.exists(output_path): 
                    os.remove(output_path)
                os.rename(temp_video_path, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a tracking video from annotated keyframes.")
    parser.add_argument("-o", "--output_dir", required=True, help="Output directory containing 'annotated_keyframes' folder.")
    args = parser.parse_args()
    
    generate_video(args.output_dir)
