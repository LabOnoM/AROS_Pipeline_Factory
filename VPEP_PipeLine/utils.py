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

