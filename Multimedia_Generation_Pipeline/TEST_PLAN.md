# Multimedia_Generation_Pipeline: Comprehensive Test Plan

## 1. Overview
This test plan outlines the validation steps for the `Multimedia_Generation_Pipeline` to ensure robust programmatic video generation across platforms, proper integration with AROS memory streams, and consistent CLI wrapper behavior.

## 2. Supported Platforms
- Ubuntu Linux (20.04+)
- macOS (Intel & Apple Silicon)
- Windows (via WSL2 / Node.js native)

## 3. Test Scenarios

### 3.1. Unit Testing (Component Level)
- **Environment Validation**:
  - `render_video.py` detects missing Node/npm/FFmpeg and exits gracefully.
  - `render_video.py` auto-installs `node_modules` if missing.
  - `render_video.py` successfully detects pre-installed browsers (`/usr/bin/google-chrome-stable`, etc.) for offline usage.
- **Composition Resolution**:
  - `render_video.py` correctly locates the React entry point (`src/index.ts`, `index.tsx`, etc.).
- **Props Passing**:
  - CLI properly forwards inline JSON strings to Remotion.
  - CLI properly forwards file-based JSON props to Remotion.

### 3.2. Integration Testing (Pipeline Level)
- **End-to-End Render (Default)**:
  - Run `python3 render_video.py --project-dir ../Templates/HelloWorld --composition HelloWorld --output out/test1.mp4`.
  - Validate that `test1.mp4` is generated and has duration > 0s.
- **End-to-End Render (Custom Props)**:
  - Run `python3 render_video.py --project-dir ../Templates/HelloWorld --composition HelloWorld --output out/test2.mp4 --props '{"titleText": "Test"}'`.
  - Validate video renders without failure.
- **Self-Healing Fallback**:
  - Simulate missing Puppeteer browser; ensure script triggers `npx remotion install browser` and retries successfully.

### 3.3. GUI / Visual Confirmation Workflows
- **Playback Verification**:
  - Play `out/video.mp4` in a standard video player (VLC/QuickTime).
  - Verify H264 codec and YUV420p pixel format (e.g., via `ffprobe`).
- **Visual Artifacts Check**:
  - Confirm opacity animation starts at 0 and fades to 1.
  - Confirm spring scale animation resolves smoothly.
  - Check that font colors and text shadow render identically across environments.

## 4. Automation Pipeline Integration
- Incorporate end-to-end tests into the AROS test harness.
- Ensure the pipeline can be invoked asynchronously via `/wiki-build` or `/manuscript-write`.
