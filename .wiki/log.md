# Wiki Change Log

## [2026-05-12] - Initialization & Philosophy Sync
- **Initialize Wiki Index**: Restructured `index.md` to categorize all entities and concepts.
- **Create Overview**: Added `overview.md` to articulate the project mission and "Embodiment & Co-Evolution" philosophy.
- **Sync Philosophy**: Grounded the wiki in the latest 2025 research on sensory perception and thermodynamic computation.
- **Audit**: Resolved 7 orphan pages by linking them from the central index.
## [2026-05-13] - Literature Ingestion & MTL Synthesis
- **Ingest Research**: Processed arXiv:2604.14004 (Memory Transfer Learning) via the hardened literature-ingestion pipeline.
- **Skill Hardening**: Remediated `pdf_converter.py` CLI arguments for `opendataloader-pdf` compatibility.
- **Philosophy Expansion**: Integrated the MTL hypothesis into the core project philosophy (READMEs and Wiki Overview).
- **CPCP Registry Update**: Documented infrastructure fixes in `SHARED_ASSET_REGISTRY.md`.
## [2026-05-13] - SkillOS Evaluation & Self-Evolution Roadmap
- **Ingest Research**: Processed arXiv:2605.06614 (SkillOS: RL-trained Skill Curation for Self-Evolving Agents) via CPCP pipeline.
- **Gap Analysis**: Completed comprehensive 8-dimension evaluation of AROS vs. MTL/SkillOS paradigms. Identified 3 critical gaps and 4 competitive advantages.
- **Roadmap Definition**: Established 5-phase integration roadmap (Insight Memory → Full Lifecycle → Curator Decoupling → RL Training → Agentic Retrieval).
- **Wiki Synthesis**: Updated `overview.md` with SkillOS philosophy pillar and Self-Evolution Roadmap section.
## [2026-05-13] - Wiki Audit & Maintenance
- **Structural Audit**: Verified zero orphan pages.
- **Agent Audit**: Confirmed re_gent integrity.
- **Policy Evolution**: Executed RL-informed evolution cycle (CURATION_POLICY v1.0.1 candidate generated).

## [2026-05-20] - Concurrency Locking & Rsync Fallback Integration
- **Locking Mechanism**: Added flock/mkdir cross-platform concurrency locking (`knowledge.lock`) to `sync_with_aros.sh` to prevent dual-write corruption.
- **rsync Fallback**: Implemented copy/remove fallback directory sync logic to allow script functionality on platforms lacking `rsync` (e.g. Windows Git Bash).
- **Cleanup**: Cleaned up the repository by deleting all staged files with literal backslashes in their names.

## [2026-05-21] - AROS Ecosystem Sync & Alignment
- **Ecosystem Alignment**: Executed bidirectional sync using `sync_with_aros.sh` to pull 17 GEPA-mutated skills from the live AROS runtime.
- **Factory Update Push**: Pushed the updated `agentic-data-scientist` skill from the factory repository back to the AROS runtime, achieving 100% in-sync status across 888 tracking nodes.
- **Documentation**: Documented changes and updated `SHARED_ASSET_REGISTRY.md` and `.wiki/log.md`.

## [2026-05-28] - Agent Package Builder Modernization & Batch Schema Generation
- **Model Upgrade**: Upgraded the AI Agent Package Builder script to utilize `gemini-3.1-pro-preview`.
- **JSON Schema Output Bug Fix**: Corrected Gemini API `response_schema` constraints that forced empty JSON structures, enabling rich dynamic output for `agent.yaml`, `input_schema.json`, and `output_schema.json`.
- **Batch Processing**: Regenerated full AI Agent configurations for all 15 pipelines in the `AROS_Pipeline_Factory` workspace successfully.
- **Documentation**: Updated `agent_package_builder.py` with rigorous file headers and integrated `SPEC.md` alignment.

## [2026-06-05] - Workspace Integrity Restoration & Concurrency Bug Fix
- **Restore Truncated Assets**: Detected and resolved a massive truncation anomaly affecting 149 files (skills and KIs) in both the factory working tree and the active AROS runtime. Restored all assets to their healthy Git HEAD versions.
- **Push Restore**: Executed bidirectional sync push to restore 111 healthy, complete assets back to the live AROS runtime (`~/.gemini/`), overwriting the corrupted files.
- **Concurrency Bug Fix**: Fixed a `set -e` exit bug in `sync_with_aros.sh` that caused status checks to crash when specific conditional filters returned false.
- **Clean Submodule**: Restored and cleaned the nested `agentic-data-scientist` submodule's working tree.

## [2026-06-08] - Dynamic Data Folder Detection
- **Onboarding Workflow**: Updated `/science-project-onboarding` workflow to dynamically detect and use existing data repositories (e.g., `data/`, `raw_data/`) instead of strictly creating `00.RawData/`.
- **Policy Adaptation**: Updated `AGENTS.md` LAW 3 to allow Canonical Storage of PDFs under the detected `<DATA_DIR>/Literature/` path.
- **Documentation**: Updated walkthroughs and the LLM-Wiki to reflect these workflow adjustments.

## [2026-06-15] - Mass External Skill Integration
- **Skill Ingestion**: Processed 457 external capabilities from 15 GitHub repositories (including nature-skills, claudedesignskills, scipilot).
- **CPCP Normalization**: Deployed `integrate_external_skills.py` to rename `README.md` to `SKILL.md`, inject compliant YAML frontmatter, and safely resolve namespace collisions (e.g., `claudedesign-skill-creator`).
- **Runtime Sync**: Successfully pushed 241 normalized unique skill directories to the live AROS runtime (`~/.gemini/skills/`) using the SAMS deployment protocol.
- **Documentation**: Updated `README.md`, `SPEC.md`, and `lessons-learned.md` to document the mass ingestion methodology.
