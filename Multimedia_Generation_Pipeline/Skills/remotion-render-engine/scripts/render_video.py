#!/usr/bin/env python3
# =============================================================================
# render_video.py — Wrapper Script for Remotion Programmatic Rendering
# =============================================================================
#
# PURPOSE:
#   Validates environment (Node, npm, FFmpeg), manages NPM dependencies, and
#   executes the Remotion CLI to render React video compositions.
#
# USAGE:
#   python3 render_video.py --project-dir <path> --composition <id> --output <path>
#
# PART OF: Multimedia_Generation_Pipeline (Skills/remotion-render-engine/scripts/)
# =============================================================================

import os
import sys
import shutil
import subprocess
import argparse
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RemotionRenderEngine")

def check_executable(cmd):
    """Check if an executable exists in the system PATH."""
    return shutil.which(cmd) is not None

def run_cmd(cmd, cwd=None, capture_output=False):
    """Run a shell command and handle exceptions."""
    logger.info(f"Executing: {' '.join(cmd)}")
    try:
        res = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            text=True
        )
        return res
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        if capture_output:
            logger.error(f"STDOUT: {e.stdout}")
            logger.error(f"STDERR: {e.stderr}")
        raise e

def validate_environment(project_dir):
    """Perform pre-flight environmental checks."""
    logger.info("Performing pre-flight environment validation...")
    
    # 1. Check Node.js
    if not check_executable("node"):
        logger.error("Node.js is not installed or not in PATH. Please install Node.js v18+.")
        sys.exit(1)
        
    # 2. Check npm
    if not check_executable("npm"):
        logger.error("npm is not installed or not in PATH.")
        sys.exit(1)
        
    # 3. Check FFmpeg
    if not check_executable("ffmpeg"):
        logger.error("FFmpeg is not installed or not in PATH. Remotion requires FFmpeg to compile frames.")
        sys.exit(1)
        
    # 4. Check dependencies in project directory
    node_modules_path = os.path.join(project_dir, "node_modules")
    if not os.path.exists(node_modules_path):
        logger.info(f"node_modules not found in {project_dir}. Running 'npm install'...")
        run_cmd(["npm", "install"], cwd=project_dir)
    else:
        logger.info("node_modules found. Skipping npm install.")

def find_entry_point(project_dir):
    """Locate the Remotion entry file."""
    candidates = [
        "src/index.ts",
        "src/index.tsx",
        "src/index.js",
        "src/index.jsx",
        "index.ts",
        "index.tsx"
    ]
    for c in candidates:
        full_path = os.path.join(project_dir, c)
        if os.path.exists(full_path):
            return c
    return None

def find_browser_executable():
    """Detect pre-installed browser to run offline without fetching Headless Shell."""
    candidates = [
        "/usr/bin/google-chrome-stable",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/opt/google/chrome/chrome"
    ]
    for c in candidates:
        if shutil.which(c):
            return c
    return None

def render_video(project_dir, composition, output_path, props=None, concurrency=None):
    """Execute the Remotion render CLI command."""
    validate_environment(project_dir)
    
    entry_point = find_entry_point(project_dir)
    if not entry_point:
        logger.error(f"Could not locate Remotion entry file in {project_dir}.")
        sys.exit(1)
        
    logger.info(f"Using entry point: {entry_point}")
    
    output_path = os.path.abspath(output_path)
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Build CLI command
    # npx remotion render <entry-point> <composition-id> <output-location>
    cmd = [
        "npx", "remotion", "render",
        entry_point,
        composition,
        output_path,
        "--codec=h264",
        "--pixel-format=yuv420p"
    ]
    
    browser_exe = find_browser_executable()
    if browser_exe:
        cmd.append(f"--browser-executable={browser_exe}")
        logger.info(f"Using auto-detected system browser path: {browser_exe}")

    
    if props:
        # Check if props is a JSON file path or a raw JSON string
        if os.path.exists(props):
            cmd.append(f"--props={props}")
        else:
            try:
                # Validate JSON string format
                json.loads(props)
                cmd.append(f"--props={props}")
            except json.JSONDecodeError:
                logger.error("Provided --props is neither a valid file path nor a valid JSON string.")
                sys.exit(1)
                
    if concurrency:
        cmd.append(f"--concurrency={concurrency}")
        
    try:
        run_cmd(cmd, cwd=project_dir)
        logger.info(f"Video rendered successfully to {output_path}")
    except subprocess.CalledProcessError as e:
        # Check if the error is a Puppeteer browser missing issue
        # and try to self-heal
        logger.warning("Render failed. Attempting self-healing by installing browser...")
        try:
            run_cmd(["npx", "remotion", "install", "browser"], cwd=project_dir)
            logger.info("Browser installed. Retrying render...")
            run_cmd(cmd, cwd=project_dir)
            logger.info(f"Video rendered successfully after self-healing to {output_path}")
        except Exception as retry_err:
            logger.error(f"Self-healing or retry failed: {str(retry_err)}")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wrapper script for rendering Remotion compositions.")
    parser.add_argument("--project-dir", required=True, help="Path to Remotion project directory.")
    parser.add_argument("--composition", required=True, help="Composition ID to render.")
    parser.add_argument("--output", required=True, help="Path to output video file.")
    parser.add_argument("--props", help="JSON string or path to JSON file containing input props.")
    parser.add_argument("--concurrency", type=int, help="Max concurrency threads.")
    
    args = parser.parse_args()
    
    render_video(
        project_dir=args.project_dir,
        composition=args.composition,
        output_path=args.output,
        props=args.props,
        concurrency=args.concurrency
    )
