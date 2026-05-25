# Specification: Multimedia Generation Pipeline (MGP)

This specification defines the directory structure, dependencies, design constraints, and contracts for the AROS Multimedia Generation Pipeline (MGP). The pipeline enables programmatic rendering of high-fidelity videos using the Remotion framework.

---

## 1.0 Pipeline Directory Structure

The canonical structure for the MGP is defined as follows:

```
Multimedia_Generation_Pipeline/
├── SPEC.md                      # This specification
├── README.md                    # Overview and onboarding guide
├── Skills/
│   └── remotion-render-engine/  # Node/Python wrapper skill
│       ├── SKILL.md             # Skill metadata & documentation
│       └── scripts/
│           └── render_video.py  # Execution script
└── Templates/
    └── HelloWorld/              # Test composition template
        ├── package.json         # Node dependencies
        ├── remotion.config.ts   # Remotion CLI configuration
        └── src/                 # React/TypeScript components
            ├── index.ts         # Entry point
            ├── Root.tsx         # Composition registry
            ├── HelloWorld.tsx   # Video components
            └── Logo.tsx         # Animated vector assets
```

---

## 2.0 Dependencies & Environment

To guarantee deterministic builds and cross-platform compatibility, the MGP mandates the following environmental constraints (adhering to the Self-Healing Environment Policy SPEC §4.4):

1. **Node.js**: Minimum version `v18.0.0`. Managed via the local environment path.
2. **NPM/NPX**: Used to run `create-video` and execute CLI commands.
3. **FFmpeg**: Required by Remotion for frame stitching. Must be available in the system PATH.
4. **Browser**: Puppeteer manages headless Chromium. If missing at runtime, the skill wrapper must execute `npx remotion install browser` automatically.

---

## 3.0 Composition & Render Standards

To prevent cross-platform video playback desyncs (especially inside HTML dashboards like VPEP), the MGP enforces the following standards:

| Parameter | Standard | Notes |
|-----------|----------|-------|
| **Resolution** | `1920x1080` (Landscape) / `1080x1080` (Square) | Custom sizes are permitted but must match preset aspect ratios. |
| **Frame Rate** | `30 FPS` | Default standard. Supports `60 FPS` if requested. |
| **Codec** | `h264` | Encoded via libx264 for universal HTML5 browser playback. |
| **Pixel Format** | `yuv420p` | Required for Safari and standard mobile/desktop browsers. |
| **Profile** | `high` / `level 4.0` | Default FFmpeg compression tuning. |

---

## 4.0 Skill Contract (remotion-render-engine)

The wrapper skill must support the following CLI interface:

```bash
python3 render_video.py \
  --project-dir <path> \
  --composition <id> \
  --output <path> \
  [--props <json-string-or-file>] \
  [--concurrency <threads>]
```

### Outputs
- **Video file**: Rendered MP4 at the designated `--output` path.
- **Log / Trace**: Log messages matching the standard AROS logging format.
