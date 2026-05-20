---
name: a2ui-protocol
description: "A2UI (Agent to UI) protocol for building AI agent-driven interfaces. A JSONL-based streaming UI protocol that lets agents send declarative component descriptions to clients. Use this skill whenever working with A2UI protocol, building A2UI agents, generating A2UI JSON messages, debugging A2UI rendering issues, creating interactive forms, handling user actions/events, or integrating A2UI with A2A (Agent to Agent) transport. Also use when encountering surfaceUpdate, dataModelUpdate, beginRendering, components like TextField, MultipleChoice, Button, Slider, CheckBox, or any mention of A2UI, a2ui, or agent-driven UI."
---

# A2UI Protocol Skill

A2UI (Agent to UI) is a JSONL-based, streaming UI protocol created by Google. It enables AI agents to send platform-agnostic, declarative UI definitions to clients, which render them using native widgets.

**Official resources:**
- Website: https://a2ui.org/
- GitHub: https://github.com/google/A2UI
- Spec: https://a2ui.org/specification/v0.8-a2ui/
- Composer: https://a2ui-composer.ag-ui.com/

## Core Architecture

### Three Decoupled Elements
1. **Component Tree** (Structure) — What the UI looks like, defined via `surfaceUpdate`
2. **Data Model** (State) — Dynamic values, managed via `dataModelUpdate`
3. **Widget Catalog** — Client-defined mapping of component types to native widgets

### Message Types
Every message in the JSONL stream must include a `surfaceId` at the top level.

| Message | Purpose |
|---------|---------|
| `surfaceUpdate` | Define/update UI components |
| `dataModelUpdate` | Update application state |
| `beginRendering` | Signal client to render (must come LAST) |
| `deleteSurface` | Remove a UI surface |

### Message Format
```json
{"surfaceId": "default", "surfaceUpdate": {"components": [...]}}
{"surfaceId": "default", "dataModelUpdate": {"contents": [...]}}
{"surfaceId": "default", "beginRendering": {"root": "root"}}
```

## Component Model (Adjacency List)

Components are a **flat list** — NOT nested trees. Parent-child relationships use string ID references.

```json
{"surfaceId": "default", "surfaceUpdate": {"components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["title", "content"]}}}},
  {"id": "title", "component": {"Text": {"text": {"literalString": "Hello"}, "usageHint": "h1"}}},
  {"id": "content", "component": {"Text": {"text": {"literalString": "World"}}}}
]}}
```

## Standard Catalog Components

Read `references/standard_catalog.md` for the complete component reference with all properties.

### Layout
- **Row** — Horizontal layout. Props: `children`, `alignment`, `distribution`
- **Column** — Vertical layout. Props: `children`, `alignment`, `distribution`
- **List** — Scrollable list. Props: `children`

### Display
- **Text** — Text display. Props: `text` (BoundValue), `usageHint` (h1/h2/h3/body/caption)
- **Image** — Image display. Props: `url` (BoundValue)
- **Video** — Video player. Props: `url` (BoundValue)
- **Icon** — Material icon. Props: `icon` (string)
- **Divider** — Horizontal line. No required props.

### Interactive
- **Button** — Clickable. Props: `child` (ID), `action`, `primary` (bool)
- **TextField** — Text input. Props: `label` (BoundValue), `text` (BoundValue), `textFieldType`
- **MultipleChoice** — Selection. Props: `selections` (BoundValue), `options[]`, `maxAllowedSelections`
- **CheckBox** — Toggle. Props: `label` (BoundValue), `value` (BoundValue)
- **Slider** — Range input. Props: `value` (BoundValue), `min`, `max`, `step`
- **DateTimeInput** — Date/time picker. Props: `value` (BoundValue), `label` (BoundValue)

### Container
- **Card** — Elevated container. Props: `child` (ID)
- **Tabs** — Tabbed view. Props: `tabItems[]` (each: `title`, `child`)
- **Modal** — Overlay. Props: `entryPointChild` (ID), `contentChild` (ID)

## Data Binding (BoundValue)

Any property that accepts dynamic data uses a `BoundValue` object:

```json
// Static (fixed)
{"literalString": "Hello World"}

// Dynamic (from data model)
{"path": "/user/name"}

// Initialize + bind (sets default AND binds)
{"path": "/form/name", "literalString": "Default Name"}
```

Types: `literalString`, `literalNumber`, `literalBoolean`, `literalArray`

### dataModelUpdate Format
```json
{"surfaceId": "default", "dataModelUpdate": {
  "path": "form",
  "contents": [
    {"key": "name", "valueString": "Alice"},
    {"key": "age", "valueNumber": 30},
    {"key": "active", "valueBoolean": true}
  ]
}}
```

## Event Handling (User Actions)

When a user clicks a Button with an `action`, the client sends a `userAction`:

### Button Definition
```json
{"id": "submit-btn", "component": {"Button": {
  "child": "submit-text",
  "primary": true,
  "action": {
    "name": "submitForm",
    "context": [
      {"key": "plotType", "value": {"path": "/form/plotType"}},
      {"key": "colorScheme", "value": {"path": "/form/colorScheme"}}
    ]
  }
}}}
```

### Client sends userAction (A2A message)
```json
{"userAction": {
  "name": "submitForm",
  "surfaceId": "default",
  "sourceComponentId": "submit-btn",
  "timestamp": "2025-09-19T17:05:00Z",
  "context": {"plotType": "volcano", "colorScheme": "viridis"}
}}
```

The agent handles this action and responds with new `surfaceUpdate`/`dataModelUpdate`.

## Container Children

Containers use `children` with either `explicitList` or `template`:

```json
// Static children
{"children": {"explicitList": ["child1", "child2"]}}

// Dynamic from data
{"children": {"template": {"dataBinding": "/items", "componentId": "item-template"}}}
```

## Complete Interactive Form Example

See `references/form_example.md` for a full working form with TextField, MultipleChoice, CheckBox, Button, and action handling.

## Common Pitfalls & Troubleshooting

Read `references/troubleshooting.md` for:
- Missing `surfaceId` on messages
- Validation errors
- Components not rendering
- Data binding not resolving
- Multi-turn session issues

## Agent Implementation Guide

Read `references/agent_guide.md` for:
- Python ADK agent setup
- Prompt engineering for A2UI JSON generation
- Tool integration patterns
- Error handling and auto-fixing
