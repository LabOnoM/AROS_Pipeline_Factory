# Antigravity SDK Agentic Rulebook

This directory is an AI-Native execution space. All external agents (OpenClaw, Claude Code, Cline, etc.) MUST obey the following trigger rules and routing policies to ensure continuous OS stability, valid LLM memory contexts, and proper version control.

## Global Workflow Triggers
Always rely on the built-in `global_workflows` to execute complex tasks rather than writing ad-hoc Bash scripts.

1. **/lab-commit:** Trigger this when the user completes a coding or SDK development session. It evaluates `git diff`, validates stability, and builds concise commit messages.
2. **/lab-reorganize:** Trigger this when the user wants to refactor the folder structure or clean up temp_repos securely.
3. **/project-organize:** Trigger this to enforce codebase standards, root naming conventions, and linting.
4. **/research-discovery:** Trigger this when exploring new architectural components, API integrations, or OS evolutions before jumping into code.
5. **/science-project-onboarding:** (Currently completed for this environment). Used to initialize a blank workspace with proper Git, LFS, and Agent rules.
6. **/wiki-research:** **CRITICAL:** Trigger this when the AI detects gaps in the local `.wiki/` or `brain.db` knowledge base. It uses web-grounding to fetch docs and expands the `.wiki`.
7. **/wiki-ingest:** Trigger this to pipe newly structured OS documentation or external PDFs into the knowledge graph.
8. **/wiki-update:** Trigger this weekly to clean up orphan nodes, prune deprecated SDK documentation, and re-embed.
9. **/wiki-query:** Trigger this to answer user questions purely based on the established `.wiki` and `~/.gemini/antigravity/knowledge/`.
10. **/wiki-build:** Compile OS manuals, READMEs, or architectural release notes purely from indexed documents.
11. **/manuscript-write:** Trigger this if the user wants to synthesize a formal Whitepaper, Technical Spec, or Manuscript utilizing all execution traces.
12. **/visualize-data:** Trigger this when the user requests "fancy diagrams, plots, or workflows". It routes dynamically between `markdown-scientific-viz` (for Markdown IDE rendering) and `fireworks-tech-graph` (for SVG/PNG exports).

## Execution Directives
- **Self-Evolution (`antigravity-evolution`):** Agents must never blindly edit the `evolver.py` pipeline without mapping changes in the `implementation_plan.md` first.
- **Memory Priority:** Whenever asked to write a new OS function, agents must query `~/.gemini/antigravity/knowledge/` to ensure they don't break existing OS semantics.
- **Dashboard Telemetry Maintenance:** When modifying UI scripts (`app.js` or `main.py` in `antigravity-dashboard`), agents MUST review the `aros_telemetry_debugging` Knowledge Item. All updates must forcefully increment cache-busters in HTML headers and rigorously map to `.db` telemetry schemas.
- **Workspace Hygiene:** Diagnostic, ad-hoc, or one-off scratch scripts (e.g., `test_usage.py`) MUST NOT be generated in the root project directory. Agents must strictly isolate these sandbox files to their designated IDE scratch directory (`~/.gemini/antigravity/brain/<id>/scratch/`).
- **IDE Workspace Delegation:** The AROS Swarm operates in a strict per-job sandbox by default. However, when the IDE AI delegates the `ide_workspace` scope during agent creation, Swarm bots are permitted to read/write to the active project folder and will automatically ingest `AGENTS.md` and `.cursorrules` from that directory to inherit the localized intent.
