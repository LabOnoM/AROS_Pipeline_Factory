# A2UI Agent Implementation Patterns

This document details best practices and advanced strategies for building reliable A2UI-compatible agents.

## 1. Prompt Engineering Strategies

*   **Delimiter Separation**: Use a clear delimiter like `---a2ui_JSON---` to strictly separate conversational text from UI-specific data. This prevents the LLM from mixing biological interpretation with JSON syntax.
*   **Concrete Examples**: Include one or two full A2UI JSON examples in the system prompt. LLMs are more accurate when emulating valid structures than when following abstract schemas.
*   **Component Whitelisting**: Explicitly whitelist reliable components (Text, Image, Card, Column, Row) and warn the LLM against using interactive components (Slider, MultipleChoice) unless specifically asked.

## 2. Server-Side vs. LLM-Generated UI

While LLMs can generate UI structure, complex interactive elements are more reliably generated **server-side** as Python or TypeScript functions.

*   **LLM Role**: Analyzes the query and decides *which* data or settings to show.
*   **Server Role**: Takes those decisions and generates formal A2UI JSON (e.g., `TextField`, `MultipleChoice`) with correct data binding paths.
*   **Decoupling**: This approach ensures the UI is technically valid even if the LLM's reasoning is slightly off.

## 3. Automated Response Upgrading (Injection)

A powerful pattern is to have the `AgentExecutor` automatically detect specific outputs (like a plot URL) and "upgrade" the response by injecting a pre-built configuration panel.

### The Injection Flow (`agent_executor.py`)
1.  **Scan**: The executor scans the LLM output for markers (e.g., `/static/pca_*.png`).
2.  **Intercept**: If a marker is found, the executor intercepts the message.
3.  **Build**: It calls a server-side `ui_builder.py` to generate the Plot + Interpretation + Config Panel.
4.  **Yield**: It yields the "upgraded" multi-part message (TextPart + A2UI DataParts) to the client.

### Benefits
- **Technical Reliability**: Configuration panels (sliders, dropdowns) are guaranteed to be valid and follow the protocol.
- **Consistency**: High-utility dashboards (like PCA or Volcano plots) look and behave identically across the application.
- **Expertise**: The `ui_builder` can inject hard-coded expert "AI Suggestions" (💡) alongside dynamic data.

## 4. Serving Assets and Caching

For scientific plots (PNGs), use a content-hash or parameter-hash caching system:
1.  Generate the plot based on parameters.
2.  Calculate a hash of those parameters.
3.  Store as `/static/plot_<hash>.png`.
4.  If a user requests the same plot in a future turn, the server returns the cached URL immediately, saving compute.

## 5. LLM-Powered Query Routing and Classification

Instead of simple keyword matching, use a high-order LLM (Gemini 2.0 Flash) to classify user intent and extract parameters.

### Routing Pattern
1.  **System Prompt**: Define available actions (e.g., `pca`, `volcano`, `custom_plot`) and their parameters.
2.  **Constraint**: Require the LLM to output a strict JSON structure representing the action.
3.  **Executor**: The `AgentExecutor` parses this JSON and calls the corresponding server-side analysis function.
4.  **Parameter Extraction**: The LLM extracts biological entities (gene names like `SOX9`) and mapping them to tool parameters.

## 6. Real-Data Grounding vs. Fabricated Data

A major risk in LLM-assisted scientific exploration is the hallucination of data or trends. 

- **The Grounding Rule**: The A2UI agent should **never** generate plot data based purely on the LLM's internal weights.
- **Pattern**: The agent always loads from a **verified primary source** (e.g., `[WORKSPACE_ROOT]/GSE261849/analysis/results/*.csv`). 
- **Verifiable Interpretation**: Even if the LLM generates the interpretation, it should be prompted to "read" the analysis results (e.g., top 10 genes from a CSV) to ensure the text matches the visual plot.

## 7. Dynamic Config Persistence (Action Context Injection)

To provide a seamless "re-analysis" experience, the client must preserve UI state across turns.

- **The Problem**: Clicking "Update Plot" refreshes the surface, losing current slider/text values.
- **The Solution**: The shell client (`app.ts`) should scrape its own data model for any user-modified values (typically under a `/config` path) and inject them into the `context` of the action event being sent to the agent.
- **Agent Handling**: The agent receives the user's previous settings in the action context and uses them to pre-populate the new surface, preventing an unexpected reset to defaults.

## 8. Session and Conversation Continuity

To enable multi-turn interaction:
1.  **Frontend**: Store the `context_id` and `task_id` returned from the A2A task response.
2.  **Frontend**: Persist these in local storage or state.
3.  **Message Metadata**: Include these IDs in the metadata of every subsequent request.
4.  **Backend**: Use an `InMemorySessionService` or database to retrieve the agent's memory and chat history associated with that `context_id`.
