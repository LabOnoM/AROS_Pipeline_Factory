# AROS Pipeline Factory Specification v2.0
**Author**: Antigravity AI  
**Status**: PRODUCTION  
**Last Updated**: 2026-05-20  


## 1. Executive Summary
The AROS Pipeline Factory is the canonical source-of-truth for the Antigravity Research OS (AROS) runtime environment. This specification defines the modular domain pipeline architecture, the Shared Asset Management System (SAMS), and the Cross-Pipeline Compatibility Protocol (CPCP).

## 2. System Architecture
The repository is organized into discrete domain pipelines, each containing specialized Skills, KIs, and Workflows.

### 2.1 Domain Pipelines
- **Bioinformatics_Pipeline**: Genomic and proteomic analysis.
- **Data_Analysis_Pipeline**: Statistical modeling and visualization.
- **Image_Processing_Pipeline**: CV and scientific imaging.
- **Writing_Publishing_Pipeline**: Academic manuscript and grant authoring.
- **[Full list in 00.RawData/PIPELINE_REGISTRY.md]**

### 2.2 Shared Assets (SAMS)
Assets located in \`01.Shared_Assets/\` are governed by SAMS. These are common utilities (e.g., \`pptx\`, \`word-read-write\`) used across multiple pipelines.

## 3. Governance Protocols
### 3.1 LAW 0: CPCP (Cross-Pipeline Compatibility Protocol)
Any modification to a shared asset REQUIRES:
1. Impact assessment across all consumer pipelines.
2. Logging in `00.RawData/SHARED_ASSET_REGISTRY.md`.
3. Forking if a breaking change is required for a specific pipeline.

### 3.2 LAW 1: Asset Deployment & Bidirectional Sync
All production deployments and synchronization operations MUST use `01.Shared_Assets/Scripts/sync_with_aros.sh`. Manual file movement between the Factory and `~/.gemini/` is prohibited. The `deploy_to_aros.sh` script is maintained as a legacy wrapper for `sync_with_aros.sh push`.

## 4. Systems Integration
### 4.4 Self-Healing Environment (SHE)
The repository implements a SHE pattern using shell-based audits (`audit_shared_assets.py`) to ensure metadata integrity and path consistency.

### 4.5 AROS Runtime Directory Mapping (Antigravity V2)
The canonical mapping between Factory structures and the live AROS runtime is:
- **Skills**: `~/.gemini/skills/<skill-name>/SKILL.md` (exposed via `antigravity-brain` MCP server)
- **Knowledge Items**: `~/.gemini/antigravity-ide/knowledge/<ki-name>/artifacts/` (primary V2 path) with dual-write synchronization to `~/.gemini/antigravity/knowledge/` (agent runtime path). Write operations to either directory MUST utilize cross-platform concurrency locks (`knowledge.lock`) to prevent concurrent write corruption.
- **Policies**: `~/.gemini/antigravity/policies/<policy-name>.md`
- **Workflows**: `~/.gemini/antigravity/global_workflows/<workflow-name>.md`
- **Scripts**: `~/.gemini/scripts/` (Global AROS scripts)
- **Environments**: `~/.gemini/environments/` (Global AROS Conda definitions)

#### 4.5.1 Concurrency Lock & Copy Fallbacks
To ensure cross-platform compatibility across Windows, macOS, and Linux:
- **Lock Fallback**: If POSIX `flock` is unavailable on the target environment, the sync tool MUST fallback to atomic directory creation (`mkdir` lock) on `/tmp/aros_knowledge.lock.dir`. Lock release must be guaranteed under EXIT/INT/TERM shell traps.
- **Copy Fallback**: If `rsync` is unavailable, the sync tool MUST fallback to a native directory cleaning and reproduction routine using `find` + `rm` + `cp -Rf`.

### 4.6 AROS V2 Plugin Integration
In V2, AROS resources are registered with the IDE agent prompt using a native V2 plugin located at `~/.gemini/config/plugins/aros/` containing a `GEMINI.md`-style skill document that teaches the agent how to invoke all 16 AROS MCP tools.

### 4.7 Cross-Platform Path Compatibility
The AROS Pipeline Factory strictly prohibits the use of literal backslashes (`\`) in filenames and path representations in the Git index, as they cause checkout failures on macOS/Linux and tooling desyncs. All paths MUST use standard forward-slash (`/`) formatting. Redundant backslash-containing duplicates must be immediately purged.

### 4.8 Unified Native CLI Sync (aros-sync)

The sync and audit procedures are unified into a single cross-platform compiled Rust CLI utility named `aros-sync`. This replaces shell and python script wrappers.

#### 4.8.1 CLI Interface
The CLI binary MUST support the following execution interface:
- `aros-sync push --target <path>`
  - Computes source file checksum hashes (SHA-256) inside the Factory and copies updated assets to the destination path.
- `aros-sync pull --source <path>`
  - Retrieves changes from local runtime directories back to the Factory structure.
- `aros-sync audit`
  - Validates SAMS asset lists, cross-references imports, and flags broken symlinks or missing files.

#### 4.8.2 Atomic Concurrency locks
- `aros-sync` MUST enforce lock checks. Before any directory writes, the tool MUST check for `knowledge.lock`. If a lock collision is detected, `aros-sync` MUST wait and retry up to 5 times (using exponential backoff 50ms, 100ms, 200ms, etc.) before aborting with exit code 1.

## 5. Global Context Hub Integration
The Pipeline Factory acts as the primary data source for the AROS Cloud Federation's **Global Context Hub**.

### 5.1 Skill Publishing to the Hub
All domain skills (e.g., `Bioinformatics_Pipeline`) are synchronized to the Cloud Federation via the `aros-sync` CLI tool. The Global Context Hub provides a Next.js-based frontend for users to browse these skills.

### 5.2 Autonomous Categorization (BDD/TDD Stub)
The `AROS-agent` deployed on the cloud automatically scans `SKILL.md` payloads and applies domain tags.
*See Cloud Federation's `skill_categorization.feature` for BDD specifications.*

### 5.3 Feedback Routing (BDD/TDD Stub)
User comments generated in the Global Context Hub UI are automatically triaged by the `AROS-agent` and routed to the corresponding GitHub Issue Tracker for the `AROS_Pipeline_Factory`.
*See Cloud Federation's `feedback_system.feature` for BDD specifications.*

### 5.4 AI Agent Package Synthesis
The `agent_package_builder.py` script automatically synthesizes structured agent definitions (`agent.yaml`, `input_schema.json`, `output_schema.json`, and `system.md`) for all pipelines using the `gemini-3.1-pro-preview` model. This process ensures scalable deployment to the AROS Cloud Federation with full cross-platform compatibility by safely generating and distributing agent context payloads without exposing raw scripts directly.
