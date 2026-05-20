---
name: aros-swarm-orchestration
description: AROS Swarm Orchestration Skill
---

# AROS Swarm Orchestration Skill

Use this skill when you need to programmatically invoke the AROS Swarm Orchestrator to execute multi-agent scientific research goals.

## When to Use
- A goal requires decomposition into parallel sub-tasks (literature review + analysis + writing)
- You want to leverage specialized agent archetypes (bioinformatics_analyst, manuscript_writer, etc.)
- A research objective benefits from DAG-structured execution with memory-augmented context

## Architecture
```
Goal → Coordinator (gemini-2.5-pro)
     → DAG of TaskNodes
     → Skill Router (vec_world_facts)
     → Specialized Worker Agents
     → Trace Writer → brain.db
```

## Quick Invocation (Python)
```python
import asyncio
import sys
sys.path.insert(0, "/mnt/Disk1/AntigravityInit/antigravity-swarm/src")

from antigravity_swarm.orchestrator import SwarmOrchestrator

orchestrator = SwarmOrchestrator()
result = asyncio.run(orchestrator.execute_task(
    goal="Analyze the role of WNT signaling in osteoblast differentiation and suggest 3 testable hypotheses.",
    context_id="my-research-session"
))
print(result)
```

## Available Agent Archetypes (agent_taxonomy)
| agent_type | model_tier | specialty |
|---|---|---|
| literature_miner | analysis | PubMed/Semantic Scholar searches |
| bioinformatics_analyst | analysis | scRNA-seq, spatial TX, proteomics |
| data_visualizer | utility | matplotlib, seaborn, plotly |
| code_generator | analysis | Python/R scripts |
| manuscript_writer | orchestration | Drafting, reviewer responses |
| quality_reviewer | orchestration | Peer review simulation |
| pipeline_engineer | utility | Space Ranger, GEPA pipelines |
| proteomics_analyst | analysis | MS data, protein interactions |

## Key Data Classes
```python
class TaskNode(BaseModel):
    task_id: str            # Unique identifier
    description: str        # What this agent should do
    agent_persona: str      # One of the 8 archetypes above
    depends_on: List[str]   # task_ids this node waits for
    zero_shot_context: str  # Auto-populated from brain.db via vec similarity

class ExecutionPlan(BaseModel):
    tasks: List[TaskNode]   # The full DAG
```

## Environment Variables
- `BRAIN_DB_PATH`: Path to brain.db (default: `~/.gemini/antigravity/brain.db`)
- `GOOGLE_AI_API_KEY` or `GEMINI_API_KEY`: Required for LLM calls

## Telemetry — What Gets Updated in brain.db
- `system_telemetry.swarm_active_nodes` — increments per active TaskNode
- `system_telemetry.swarm_completed_tasks` — increments on completion
- Execution trace saved as `experience` in `experiences` table

## Triggering via Dashboard
```bash
# The GEPA mutation sweep also runs the swarm
curl -X POST http://localhost:8000/api/mutate_all
```

## Key Rules
- Always provide `context_id` as a UUID or session identifier for memory linkage
- The Coordinator auto-selects agent archetypes based on task description embedding similarity
- `zero_shot_context` is automatically injected from brain.db — do NOT pre-populate manually
- On failure, traces are written to `~/.gemini/antigravity/brain/*/walkthrough.md` for GEPA pickup
