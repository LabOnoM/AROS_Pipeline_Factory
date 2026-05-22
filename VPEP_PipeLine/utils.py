"""
VPEP (Video-to-Protocol Extraction Pipeline) - Shared Utilities
==============================================================

Description:
    This module provides shared helper functions for the VPEP pipeline, including API client
    loading, time conversions, and video compression.

Key Capabilities:
    - load_api_client(): Retrieves Google GenAI client, reading key from env or standard paths.
    - time_to_seconds(): Converts timestamp strings (MM:SS, HH:MM:SS) to numerical seconds.
    - compress_video(): Compresses large raw videos using FFmpeg to 480p, 15fps, CRF 30.

Cross-Platform Compatibility:
    - Verified on Windows, macOS, and Linux (Ubuntu).
    - Utilizes system-agnostic paths (via `os.path`) and standard subprocessing.
"""

import os
from google import genai

def load_api_client():
    """Reads API key from environment variables or standard .env locations and returns Client.
    
    Includes a robust retry policy for all downstream pipeline stages to handle transient API issues.
    """
    from google.genai import types

    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key:
        env_path = os.path.expanduser("~/.gemini/.env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GOOGLE_AI_API_KEY="):
                        api_key = line.strip().split("=", 1)[1].strip("'\"")
                        break

    # Configure robust retry strategy for all pipeline stages (especially to handle transient 503/429)
    retry_options = types.HttpRetryOptions(
        initial_delay=2.0,         # Wait 2 seconds before first retry
        attempts=5,                # Try up to 5 times
        exp_base=2.0,              # Exponential backoff (2s, 4s, 8s, 16s)
        max_delay=30.0,            # Max delay 30s
        http_status_codes=[429, 500, 502, 503, 504]
    )
    http_options = types.HttpOptions(
        retry_options=retry_options,
        timeout=300 * 1000         # 5 minutes timeout in milliseconds for video/text generation
    )

    if api_key:
        return genai.Client(api_key=api_key, http_options=http_options)
    else:
        # Fallback to default client setup (which may use GEMINI_API_KEY or other mechanisms)
        return genai.Client(http_options=http_options)

def time_to_seconds(time_str):
    """Convert MM:SS or HH:MM:SS to seconds."""
    parts = list(map(int, time_str.split(':')))
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0

def is_video_already_compressed(video_path, target_height=480, target_fps=15, bitrate_threshold_kbps=800):
    """Detect whether a video is already sufficiently compressed for VPEP processing.

    Uses ffprobe to inspect the video's codec, resolution, frame rate, and bitrate.
    Returns True if the video meets or falls below the VPEP compression targets,
    meaning re-compression would be wasteful or quality-degrading.

    The VPEP compression target (from compress_video()) is:
        - Resolution: 480p (height <= 480)
        - Frame rate: <= 15 fps
        - Codec: H.264 (libx264)
        - CRF 30 (maps to roughly 300-800 kbps for 480p content)

    Args:
        video_path: Absolute path to the video file.
        target_height: Maximum pixel height to consider "compressed" (default: 480).
        target_fps: Maximum frames-per-second to consider "compressed" (default: 15).
        bitrate_threshold_kbps: Maximum video bitrate in kbps (default: 800).

    Returns:
        True if the video is already compressed, False if it needs compression.
    """
    import subprocess
    import json as _json

    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=codec_name,width,height,r_frame_rate,bit_rate",
            "-show_entries", "format=bit_rate",
            "-of", "json",
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"ffprobe failed (rc={result.returncode}). Assuming video needs compression.")
            return False  # Can't probe → assume not compressed → compress it

        data = _json.loads(result.stdout)
        stream = data.get("streams", [{}])[0]
        fmt = data.get("format", {})

        # 1. Check codec — must be a standard lossy codec
        codec = stream.get("codec_name", "")
        if codec not in ("h264", "hevc", "vp9", "av1", "mpeg4"):
            print(f"Codec '{codec}' is not a standard compressed codec. Compression needed.")
            return False

        # 2. Check resolution
        height = int(stream.get("height", 9999))
        if height > target_height:
            print(f"Video height {height}px exceeds target {target_height}px. Compression needed.")
            return False

        # 3. Check frame rate (r_frame_rate is a fraction like "30/1" or "30000/1001")
        fps_str = stream.get("r_frame_rate", "30/1")
        num, den = map(int, fps_str.split("/"))
        fps = num / den if den else 30
        if fps > target_fps + 1:  # +1 tolerance for rounding
            print(f"Video fps {fps:.1f} exceeds target {target_fps}fps. Compression needed.")
            return False

        # 4. Check bitrate (stream-level or format-level fallback)
        bitrate_str = stream.get("bit_rate") or fmt.get("bit_rate")
        if bitrate_str and bitrate_str != "N/A":
            bitrate_kbps = int(bitrate_str) / 1000
            if bitrate_kbps > bitrate_threshold_kbps:
                print(f"Video bitrate {bitrate_kbps:.0f}kbps exceeds threshold {bitrate_threshold_kbps}kbps. Compression needed.")
                return False
            print(f"Video bitrate {bitrate_kbps:.0f}kbps is within threshold.")
        else:
            print("Bitrate not available in metadata. Relying on resolution/fps checks only.")

        print(f"Video already compressed: codec={codec}, height={height}px, fps={fps:.1f}, bitrate={bitrate_str or 'N/A'}.")
        return True  # Passes all thresholds → already compressed

    except Exception as e:
        print(f"Compression detection error: {e}. Defaulting to compress.")
        return False  # On any error, default to compressing


def compress_video(input_path, output_path):
    """Compress video using ffmpeg to a standard low-bitrate format (480p, 15fps, CRF 30)."""
    import subprocess
    print(f"Compressing video: {input_path} -> {output_path}...")
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", "scale=-2:480",
        "-r", "15",
        "-vcodec", "libx264",
        "-preset", "ultrafast",
        "-crf", "30",
        "-c:a", "aac",
        "-b:a", "64k",
        output_path
    ]
    subprocess.run(cmd, check=True)
    print("Video compression complete!")

