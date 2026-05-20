# A2UI Troubleshooting and Rendering Fixes

During the development of A2UI agents, several critical rendering issues were identified and resolved.

## 1. The "surfaceId" Required Property Error

**Problem**: The LLM often generates A2UI messages without the `surfaceId` property, or places it incorrectly, leading to validation failures and blank pages.

**Fix**: Implement auto-fix logic in the agent's response processing.

```python
# Strip markdown fences and parse JSON
json_string_cleaned = json_string.strip().lstrip("```json").rstrip("```").strip()
parsed_json_data = json.loads(json_string_cleaned)

# Wrap single object in list
if isinstance(parsed_json_data, dict):
    parsed_json_data = [parsed_json_data]

# Inject missing surfaceId
if isinstance(parsed_json_data, list):
    for msg in parsed_json_data:
        if isinstance(msg, dict) and "surfaceId" not in msg:
            msg["surfaceId"] = "default"
```

## 2. Strict Schema Validation Stalls

**Problem**: Even with `surfaceId` injected, strict `jsonschema` validation (e.g., using `jsonschema.validate` against the standard catalog) may fail due to complex nested requirements, protocol version mismatches, or minor LLM formatting errors. If this validation is blocking, the agent returns an error message instead of the UI, even if the UI is mostly correct.

**Strategy**: Relax or remove blocking validation. 
1.  **Non-Blocking Debugging**: Perform validation and log errors to the console for debugging, but do NOT let validation errors stop the message from being sent to the client.
2.  **Best-Effort Auto-Fix**: Run the auto-fix logic (surfaceId injection, wrapping dicts in lists) and pass the result through. The client-side renderer is often more resilient than the formal schema validator.
3.  **Removal of Dependencies**: If validation is consistently problematic, consider removing the `jsonschema` dependency from the agent's runtime to streamline response processing.

## 3. Blank Screens on Client Errors

**Problem**: In some client implementations (like Lit shells), any error or empty response clears the current UI "surfaces", leaving the user with a blank screen.

**Fix**:
1.  **Keep Form Visible**: Use a `hasInteracted` flag on the client side so that the initial input form/bar remains visible even after a failed agent response.
2.  **Conditional Clearing**: Only call `clearSurfaces()` and `processMessages()` if the agent returns a valid, non-empty set of A2UI messages. This preserves the previous state (e.g., a plot) while the user retries a query.

## 4. Multi-Turn Session Loss

**Problem**: Each turn of chat starts a new agent session, losing conversation context.

**Fix**: Persist the `contextId` (and `taskId`) from the agent's TASK results in the client state. Include these in the metadata of every subsequent `sendMessage` request to the A2A server.

## 5. Delimiter Misses

**Problem**: The LLM might fail to include the `---a2ui_JSON---` delimiter or place text after it.

**Strategy**: The splitting logic should handle whitespace and optional markdown code blocks. Always provide clear examples in the system prompt of how to separate biological interpretation from the UI JSON.
## 6. UI Verification with Browser Subagents

**Challenge**: Testing A2UI rendering manually is slow and prone to overlooking layout issues (e.g., "Invalid label" warnings or hidden elements).

**Solution**: Use a browser subagent (like `browser_subagent` or `playwright`) to:
1.  **Interact**: Automatically type queries (e.g., "Show me the PCA plot") and click send.
2.  **Screenshot**: Capture multiple screenshots at different scroll positions to verify the entire UI (plot, suggestions, config panel).
3.  **Inspect**: Check the DOM and console logs for `net::ERR_CONNECTION_REFUSED` or JS errors that indicate agent server crashes.
4.  **Wait**: Ensure sufficient `wait` time (e.g., 60 seconds) for the LLM to finish streaming and the client to buffer the `beginRendering` signal.

## 7. Missing Dependencies for Skills
**Problem**: The `search_skills` tool fails when parsing YAML frontmatter if the environment lacks `PyYAML`.
**Fix**: Add `"pyyaml>=6.0"` to the `dependencies` list in `pyproject.toml`.

## 8. Server Crashes on Complex Rendering
**Problem**: The `AgentExecutor` or backend server might crash (e.g., `net::ERR_CONNECTION_REFUSED`) if an LLM request takes too long to stream or if there's a timeout during complex plot generation.
**Fix**: Increase server timeouts or implement a heartbeat mechanism in the A2A stream. Ensure the server is restarted with `uv run .` if it's found down.

## 9. Blank Responses on Malformed LLM JSON

**Problem**: If the LLM generates valid biological text but breaks the A2UI JSON part (e.g., missing a closing brace or bracket), a strict `json.loads` will raise an exception. If the agent merely returns a generic "error generating interface" message, the user loses the valuable text content.

**Fix: Robust Text Fallback**: Modify the `agent.py` or executor logic to extract the text part *before* the JSON delimiter if a parse error occurs.

```python
try:
    text_part, json_string = content.split("---a2ui_JSON---", 1)
    # ... attempt json parse ...
except (ValueError, json.JSONDecodeError):
    # Fallback: send the text part even if the UI part is broken
    logger.warning("JSON parse failed. Falling back to text-only.")
    yield {
        "is_task_complete": True,
        "content": text_part.strip(),
    }
```

This ensures the conversation can continue even if the UI rendering fails momentarily.

## 11. JSON Auto-Repair Strategies

To resolve persistent `Expecting ',' delimiter` or formatting errors (e.g., unescaped quotes in strings), implement a progressive repair function (`_try_parse_json`) in the agent's response processing:

| Strategy | Repair Action |
| :--- | :--- |
| **Strategy 1** | Standard `json.loads(s)` |
| **Strategy 2** | Remove trailing commas: `re.sub(r',\s*([}\]])', r'\1', s)` |
| **Strategy 3** | Fix unescaped quotes specifically within `"literalString":"..."` values. |
| **Strategy 4** | Wrap in `[]` if the string starts with `{` (bare object fix). |
| **Strategy 5** | Escape raw newlines (`\n`) within string values. |

This repair layer prevents common LLM hallucinations from breaking the entire A2UI experience, allowing the agent to "self-correct" its JSON structure.

## 12. AttributeError: 'NoneType' has no attribute 'get_selected_catalog'

**Problem**: Occurs during testing when the agent is called without A2UI extension headers (e.g., via a plain `curl` or when `use_ui=False`). The `self._schema_manager` is not initialized, causing a crash in `stream()`.

**Fix**: Always check `if self.use_ui and self._schema_manager` before accessing schema internal methods. Ensure the agent has a safe text-only fallback path.

## 13. Auto-Init Handshake Failure

**Problem**: The welcome screen doesn't appear on page load.
**Fix**: Verify the client (`app.ts`) sends a `__init__` message on `connectedCallback`. Ensure the server-side executor handles `__init__` by serving the welcome screen instead of forwarding the "message" to the LLM.

## 14. Invisible Slider Tracks in Light Mode

**Problem**: The slider track (background bar) is invisible or extremely faint in light mode (e.g., `rgba(255,255,255,0.2)`). Users only see the blue thumb floating.

**Fix**: Modify the slider component's CSS in the renderer (e.g., `components/slider.ts`). Use a solid, visible color for the track background:
```css
/* Change from invisible white to light gray */
.track {
  background: #ccc; 
}
```

## 15. The "sendSend" Icon-Label Bug

**Problem**: In some Lit client templates, including a Material Icon `<span>` inside a `<button>` with a text label (e.g., `<button><span class="g-icon"></span> Send</button>`) results in the icon name being incorrectly concatenated as text (e.g., "sendSend").

**Fix**: Remove the decorative span if it's causing layout or text extraction issues. Use a clean text label or a purely CSS-based icon.

## 16. Markdown Tables Not Rendering in Text Component

**Problem**: A2UI `Text` components do not reliably parse complex markdown tables (`| Column 1 | Column 2 |`). They may render as raw pipe-separated strings.

**Fix**: Pre-format tabular data as clean plain text with bullet points or numbered lists on the server-side (`plot_generator.py`):
```text
• **Comparison A**: Tested: 2000 | ↑ Up: 45 | ↓ Down: 12
• **Comparison B**: Tested: 1800 | ↑ Up: 30 | ↓ Down: 8
```

## 17. Configuration Values Reset on Plot Update

**Problem**: When a user clicks "Update Plot", the configuration panel resets all values (sliders, text fields) to their defaults, even if the user just changed them.

**Fix: Action Context Injection**: Modify the shell client's action handler (`app.ts`) to read the current state from the UI's data model and merge it into the action event's context before sending it to the agent.
```typescript
// Read state from surface data model
const configData = surface.dataModel.get('/config');
const message = {
  action: {
    name: action.name,
    context: { ...configData, ...(action.context || {}) },
  },
};
```
The agent should then detect these `current_values` and use them as the initial state when rebuilding the UI surface.
