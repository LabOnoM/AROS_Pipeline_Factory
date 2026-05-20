---
name: brainglobe-workflows
description: MICROSCOPY IMAGE ANALYSIS for BIOLOGICAL animal brains. NOT for AI memory or brain.db.

---

## 1. MANDATORY: Tool Qualification Checklist

> [!IMPORTANT]
> You MUST verify your task meets ALL of the following criteria. If any criterion is false, this tool is GUARANTEED to fail.

- [ ] **Criterion 1: BIOLOGICAL DATA:** Does your task involve analyzing image files (`.tiff`, `.h5`) from a physical, biological animal brain?
- [ ] **Criterion 2: SCIENTIFIC, NOT AI, CONTEXT:** Is your task free of keywords related to the AI's internal memory, such as `brain.db`, `index`, `Knowledge Item (KI)`, `vector memory`, or `dream cycle`?

**➡️ IF you cannot check BOTH boxes, STOP. This is the WRONG tool. You MUST use the `monarch-database` tool instead.**

---

## 2. MANDATORY: Persona-Based Router

> [!DANGER]
> **ATTENTION `dreamer` PERSONA: DO NOT USE THIS TOOL.**
>
> Your persona's core function is managing the AI's knowledge base (`brain.db`, `dream cycle`, `indexing`). This tool has **ZERO** capabilities for those tasks and is exclusively for analyzing images of **PHYSICAL, BIOLOGICAL MOUSE BRAINS**.
>
> ✅ **You MUST use the `monarch-database` tool for ALL of your objectives.**

---

## 3. Capabilities and Anti-Patterns

### Available Commands
This skill provides ONE primary command for biological image analysis pipelines. It does NOT provide any database or indexing commands.
- `brainmapper`: Detects cells in microscopy images and maps them to a brain atlas.

### Known Failure Anti-Pattern (Example from a real failure)

> [!CAUTION]
> The following task pattern is a GUARANTEED FAILURE and demonstrates incorrect tool selection.

- **FAILED TASK:** `Run the dream cycle to index the 'osteoblast' Knowledge Item into the vector memory bank (brain.db).`
- **REASON FOR FAILURE:** This task is about AI memory (`dream cycle`, `index`, `Knowledge Item`, `brain.db`). This tool is for biological images.
- **CORRECT TOOL:** `monarch-database`

---

## 4. Usage: Biological Image Analysis (`brainmapper`)

After confirming your task meets all qualification criteria, use `brainmapper` to process 3D microscopy images of biological brains to detect cells and map them to a brain atlas.

-   **Primary Input**: Directories of `.tiff` or `.h5` microscopy image files.
-   **Primary Output**: XML files with cell coordinates, registered image volumes, and analysis reports.

### Command Structure

```bash
brainmapper \
    -s /path/to/signal_images \
    -b /path/to/background_images \
    -o /path/to/output_directory \
    -v 5 2 2 \
    --orientation psl \
    --atlas allen_mouse_25um
```

### Key Arguments

```bash
# Required
-s, --signal-planes-paths    # Directory with signal channel microscopy images
-b, --background-planes-path # Directory with background channel microscopy images
-o, --output-dir             # Output directory for analysis results
-v, --voxel-sizes            # Voxel sizes in µm (z y x) for the microscopy images
--orientation                # Anatomical orientation of the brain images (e.g., "psl")

# Registration options
--atlas                      # Atlas name for brain registration (default: allen_mouse_25um)

# Cell detection options
--soma-diameter              # Expected cell size in µm (default: 16)
--n-free-cpus                # CPUs to leave free (default: 2)
--no-detection               # Skip cell detection (registration only)
--no-register                # Skip registration
```