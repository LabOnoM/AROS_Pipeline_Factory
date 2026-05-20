---
name: aros-dashboard-control
description: AROS Dashboard Control Skill
---

# AROS Dashboard Control Skill

Use this skill when you need to interact with the AROS Control Center dashboard programmatically — querying metrics, triggering cycles, managing the Brain Federation, or configuring MCP servers.

## Dashboard URL
`http://localhost:8000` (default)

Start with: `cd /mnt/Disk1/AntigravityInit/antigravity-dashboard && uv run uvicorn src.antigravity_dashboard.main:app --host 0.0.0.0 --port 8000`

## All REST Endpoints

### System Status & Monitoring
```bash
# System running state (dream/mutation running, next schedule)
GET  /api/status
# → {"dream_running": false, "mutation_running": false, "next_scheduled_run": "2026-04-14 03:00"}

# Live memory metrics
GET  /api/metrics
# → {"memory": {"world_facts": 1408, "experiences": 65, "mental_models": 0, "agent_archetypes": 8},
#    "swarm": {"active_nodes": 0, "completed_tasks": 4},
#    "evolution": {"failed_traces": 7, "mutated_skills": 2, ...}}

# System daemon logs (last 100 lines from journalctl)
GET  /api/logs

# Memory graph for vis.js rendering
GET  /api/memory_graph
# → {"nodes": [...], "edges": [...]}

# GEPA mutation traces (for dashboard trace panel)
GET  /api/mutations
```

### Process Triggers
```bash
# Trigger dream cycle (background, idempotent)
POST /api/dream

# Trigger full GEPA mutation sweep + Knowledge Distillation (background)
POST /api/mutate_all
```

### MCP Server Configuration
```bash
# Configure and install MCP servers (writes ~/.gemini/antigravity/mcp_config.json)
POST /api/mcp/setup
# Body: {"github_token": "ghp_...", "uniprot_enabled": true, "google_dev_enabled": true,
#        "kosmos_enabled": true, "claude_skills_enabled": true, "brain_enabled": true}

# Export current mcp_config.json + .env
GET  /api/mcp/export

# Import mcp_config.json + .env from another instance
POST /api/mcp/import
# Body: {"env_vars": {...}, "mcp_config": {...}}
```

### Brain Federation (New in v2.2)
```bash
# Export selective brain snapshot (unindexed facts, taxonomy, skills, KIs, workflows, policy)
GET  /api/brain/export
# → {"status": "success", "filename": "brain_export_HOSTNAME_20260413.json",
#    "stats": {"world_facts_count": 826, "skills_count": 534, ...}}

# Upload a brain export file from another PC (staging only — no merge yet)
POST /api/brain/import   (multipart/form-data, field: "file")
# → {"status": "success", "source_instance": "...", "preview": {...}, "import_path": "..."}

# Trigger LLM-reviewed merge of the staged import
POST /api/brain/merge
# Body: {"import_path": "/path/to/incoming_file.json"}
# → {"status": "success", "report": {"facts_merged": 42, "facts_skipped_duplicate": 18, ...}}

# Run Knowledge Distillation (cluster conversation facts, surface GEPA proposals)
POST /api/brain/distill
# → {"status": "success", "report": {"clusters_found": 547, "skill_ki_proposals": [...], ...}}
```