# Antigravity IDE Architecture & Execution Parameters

Based on direct OS extraction of the `~/.gemini` directories (as opposed to the outdated web documentation), the actual topology of the Google Antigravity AI IDE configuration requires explicit mapping strategies.

## Core Topology Principles

### True Filesystem Paths vs Legacy Routes

1. **Global Skills**: Located strictly at `~/.gemini/skills/<skill-name>/SKILL.md`. (Do not use `~/.gemini/skills/*.md` or `~/.gemini/antigravity/skills/`).
2. **Global Workflows**: Located at `~/.gemini/antigravity/global_workflows/*.md`.
3. **Session Database**: Raw conversations exist as native protobufs at `~/.gemini/antigravity/conversations/*.pb`.
4. **Knowledge Items (KIs)**: Located at `~/.gemini/antigravity/knowledge/<ki-name>/metadata.json`.
5. **Global Policies**: The system maintains a decoupled architecture: `~/.gemini/GEMINI.md` governs the local IDE developer agent, while `~/.gemini/antigravity/AROS_POLICY.md` governs all background autonomous swarm/Kosmos workers.

### Native MCP Architecture 
The IDE manages all native Model Context Protocol (MCP) servers (including UniProt, Kosmos, GitHub, and custom binaries) through a centralized state file.
- **ACTIVE TARGET PATH:** `~/.gemini/antigravity/mcp_config.json`
- **DEPRECATED PATHS:** `~/.gemini/mcp_config.json` or `%USERPROFILE%/.mcp_config.json` MUST NOT BE USED. 

### Local Workspace Integrations
When an IDE handles a local workspace (e.g. `[WORKSPACE_ROOT]`), A.R.O.S must adapt dynamically to parse:
- **Local Rules:** `<workspace>/.agents/rules/`
- **Local Skills:** `<workspace>/.agents/skills/`
- **Local Workflows:** `<workspace>/.agents/workflows/`

### Debugging Ideological Collisions
If an agentic integration drops context or fails to evolve:
1. Verify `~/.gemini/antigravity/mcp_config.json` target path formatting.
2. Ensure you are parsing the nested `<skill-name>/SKILL.md` boundaries.
3. Ensure no parallel web-dashboards are attempting to configure the IDE's MCP list manually.
