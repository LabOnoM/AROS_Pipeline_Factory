# A2UI Protocol and Architecture

A2UI (Agent to UI) is a declarative, streaming UI protocol that allows AI agents to send user interface definitions to clients. The client renders these using native widgets, ensuring platform independence.

## Core Philosophical Principles

1.  **Declarative, Not Imperative**: Agents describe *what* the UI looks like (components and their data), not *how* to build it.
2.  **Flat Component List (Adjacency List)**: Components are defined in a flat list with unique IDs. Relationships (parent-child) are established by referencing these IDs. This simplifies LLM generation by avoiding deep nesting.
3.  **Separation of Concerns**:
    *   **Structure**: Managed via `surfaceUpdate` (component definitions).
    *   **State (Data Model)**: Managed via `dataModelUpdate` (JSON data pointers).
    *   **Logic (Catalog)**: The client defines the set of available components (Catalog).
4.  **Streaming via JSONL**: Each line in the stream is a self-contained JSON message, allowing for progressive rendering.

## Message Types

Every message must include a `surfaceId` at the top level to identify which UI area is being targeted.

| Message Type | Description |
| :--- | :--- |
| `surfaceUpdate` | Adds or updates component definitions on a surface. |
| `dataModelUpdate` | Updates the JSON data model for a specific surface. |
| `beginRendering` | Signals the client that enough content is buffered to perform the initial render. This must be the **last** message in the initial sequence. |
| `deleteSurface` | Removes a surface and its contents. |

## The Adjacency List Model

Instead of a nested tree, A2UI uses a flat map of components.

```json
{"surfaceId": "default", "surfaceUpdate": {"components": [
  {"id": "root", "component": "Column", "children": {"explicitList": ["title", "description"]}},
  {"id": "title", "component": "Text", "text": "A2UI Example", "textStyle": "h1"},
  {"id": "description", "component": "Text", "text": "This is a flat list."}
]}}
{"surfaceId": "default", "beginRendering": {"rootId": "root"}}
```

## Data Binding

Properties can be static (`literalString`) or dynamic (`path`).

-   **Path Only**: `{"path": "/user/name"}` (resolves from data model).
-   **Path and Literal**: `{"path": "/user/name", "literalString": "Guest"}` (initializes data model and binds).

## Event Handling

User actions (like button clicks) are sent from client to agent via `userAction` messages. These include a `context` object containing resolved data from the UI's state at the moment of the action.
