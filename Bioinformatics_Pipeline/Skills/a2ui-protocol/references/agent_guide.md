# A2UI Agent Implementation Guide

## Architecture Overview

An A2UI agent has three parts:
1. **Agent logic** — LLM that processes queries and generates A2UI JSON
2. **Tools** — Functions the LLM calls to retrieve data (e.g., query database, generate plots)
3. **A2A transport** — HTTP server exposing the agent via A2A protocol

## Python ADK Setup

### Prerequisites
```bash
pip install google-adk  # or use uv
```

### Agent Structure
```
my_agent/
├── __init__.py
├── __main__.py       # Entry point (HTTP server)
├── agent.py          # Agent class with LLM + A2UI handling
├── agent_executor.py # A2A ↔ A2UI bridge
├── tools.py          # Tool functions for data retrieval
├── prompt_builder.py # System prompt construction
└── generated_plots/  # Server-side plot storage
```

### Serving Static Files
Plots generated server-side need to be served via HTTP:
```python
from starlette.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="generated_plots"), name="static")
```

Image URLs in A2UI then reference `http://localhost:PORT/static/filename.png`.

## Prompt Engineering for A2UI

The LLM needs to generate valid A2UI JSON. Key strategies:

### 1. Use a delimiter
Split LLM output into text + JSON:
```
Your analysis text here...
---a2ui_JSON---
[{"surfaceId": "default", "surfaceUpdate": {...}}, ...]
```

### 2. Provide concrete examples in the system prompt
Show the EXACT JSON format you expect. LLMs follow examples better than descriptions.

### 3. Restrict to reliable components
Not all components are equally reliable for LLM generation:
- **Reliable**: Text, Image, Card, Column, Row, Divider
- **Moderate**: Button, TextField (need careful prompting)
- **Challenging**: MultipleChoice, Slider, Tabs, Modal (complex structure)

For challenging components, consider generating the JSON server-side instead of via LLM.

### 4. Auto-fix LLM output
Always post-process LLM JSON before sending to client:
```python
# Parse
data = json.loads(cleaned_json)
# Wrap dict in list
if isinstance(data, dict):
    data = [data]
# Inject surfaceId
for msg in data:
    if "surfaceId" not in msg:
        msg["surfaceId"] = "default"
```

## Server-Side Form Generation

For complex interactive forms (like the user's bioinformatics plot configurator), generate the A2UI JSON server-side in a Python function rather than relying on the LLM:

```python
def generate_config_form(plot_type: str, available_options: dict) -> list:
    """Generate A2UI JSON for a plot configuration form."""
    components = [
        {"id": "root", "component": {"Column": {
            "children": {"explicitList": ["title", "plotType", "colorScheme", "generate"]},
            "alignment": "stretch"
        }}},
        {"id": "title", "component": {"Text": {
            "text": {"literalString": f"Configure {plot_type} Plot"},
            "usageHint": "h2"
        }}},
        # ... more components
    ]
    return [
        {"surfaceId": "default", "surfaceUpdate": {"components": components}},
        {"surfaceId": "default", "beginRendering": {"root": "root"}}
    ]
```

The LLM calls a tool that returns this pre-built form. This is more reliable than having the LLM generate complex interactive JSON.

## Handling User Actions

When a Button action fires, the A2A client sends a `userAction` message. The agent executor must:

1. Detect the `userAction` in the incoming A2A message
2. Extract the `name` and `context`
3. Route to the appropriate handler
4. Return new A2UI messages

```python
# In agent_executor.py
if "userAction" in parts:
    action = parts["userAction"]
    if action["name"] == "generatePlot":
        config = action["context"]
        plot_url = generate_plot(**config)
        return build_plot_response(plot_url, config)
```

## Multi-Turn Conversations

For multi-turn chat, the client must preserve session context:
- Store `contextId` from A2A response
- Send `contextId` in subsequent messages
- The LLM then has full conversation history

## Local A2UI Repository

If you have the A2UI repo cloned locally, key files:
- `specification/v0_8/docs/a2ui_protocol.md` — Full protocol spec
- `specification/v0_8/json/standard_catalog_definition.json` — Component schema
- `specification/v0_8/json/server_to_client_with_standard_catalog.json` — Full resolved schema
- `samples/agent/adk/` — Example agents (contact_lookup, restaurant_finder)
- `samples/client/lit/shell/` — Shell client (generic A2UI renderer)
- `renderers/lit/` — Lit web component renderer
