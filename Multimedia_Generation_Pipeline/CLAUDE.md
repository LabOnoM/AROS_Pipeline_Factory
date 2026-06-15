# Multimedia Generation Pipeline Context

## 🧭 Domain Context
This pipeline governs programmatic video rendering, animations, and multimedia generation using tools like Remotion.

## ⚖️ Component Rules
- **Remotion Render Engine**: The primary asset is the `remotion-render-engine` shared skill.
- **Hardware Restraints**: Video rendering can exhaust Docker container memory; ensure code includes streaming optimizations or chunking logic.
