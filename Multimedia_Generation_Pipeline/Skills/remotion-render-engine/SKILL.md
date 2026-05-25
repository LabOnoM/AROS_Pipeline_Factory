---
name: remotion-render-engine
description: Executes programmatic video rendering using the Remotion framework. Validates environmental dependencies, triggers Puppeteer/Chromium setups if needed, bundles compositions, and renders high-fidelity MP4 files.
license: MIT
skill-author: AROS_System_Architect
metadata:
  version: 1.0.0
---

# Skill: Remotion Render Engine

This skill exposes programmatic access to the Remotion command-line renderer to compile video compositions using React/TypeScript.

## Usage

The skill is wrapped in a Python execution script that handles pre-flight tool verification (Node, npm, FFmpeg) and catches Puppeteer-specific Chromium download failures, offering self-healing options.

### Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--project-dir` | String | Yes | Path to the directory containing the Remotion project (`package.json`). |
| `--composition` | String | Yes | The ID of the React composition defined in `Root.tsx`. |
| `--output` | String | Yes | Path to write the output MP4 video file. |
| `--props` | String | No | JSON string or path to JSON file containing input props to customize composition rendering. |
| `--concurrency` | Integer | No | Max number of CPU threads to allocate for rendering. |

### Command Example

```bash
python3 scripts/render_video.py \
  --project-dir ./Templates/HelloWorld \
  --composition HelloWorld \
  --output ./out/hello_world.mp4
```
