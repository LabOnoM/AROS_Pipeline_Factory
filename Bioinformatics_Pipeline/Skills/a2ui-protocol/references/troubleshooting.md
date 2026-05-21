# A2UI Troubleshooting Guide

## Common Issues

### 1. Missing `surfaceId`
**Error**: `'surfaceId' is a required property`

**Cause**: Every A2UI message must include `surfaceId` at the top level.

**Fix**: Ensure every message has `surfaceId`:
```json
{"surfaceId": "default", "surfaceUpdate": {"components": [...]}}
{"surfaceId": "default", "beginRendering": {"root": "root"}}
```

**Auto-fix pattern** (Python):
```python
if isinstance(parsed_json, list):
    for msg in parsed_json:
        if isinstance(msg, dict) and "surfaceId" not in msg:
            msg["surfaceId"] = "default"
```

### 2. Blank Page After Query
**Possible causes**:
- Schema validation rejecting valid JSON — disable or relax validation
- `beginRendering` message missing — it MUST be the last message
- Components referencing non-existent child IDs
- Empty response from LLM (no `---a2ui_JSON---` delimiter)

**Debug**: Log the raw JSON the LLM generates before validation.

### 3. Data Binding Shows Empty
**Cause**: Using `{"path": "/some/path"}` without sending a corresponding `dataModelUpdate`

**Fix options**:
- Use `literalString` for static content
- Use both path and literal for initialization: `{"path": "/form/name", "literalString": "Default"}`
- Send `dataModelUpdate` before `beginRendering`

### 4. Multi-Turn Chat Doesn't Remember Context
**Cause**: Each message creates a new session with no conversation history.

**Fix**: Persist `contextId` and `taskId` from the A2A response across messages:
```typescript
// After first response
if (result.contextId) this.contextId = result.contextId;
if (result.id) this.taskId = result.id;
// In subsequent requests
sendParams.message.contextId = this.contextId;
sendParams.message.taskId = this.taskId;
```

### 5. Chat Input Disappears After Error
**Cause**: UI clears surfaces on every response, including errors.

**Fix**: Only clear surfaces when there are valid new messages:
```typescript
if (messages && messages.length > 0) {
    this.processor.clearSurfaces();
    this.processor.processMessages(messages);
}
```

### 6. LLM Generates Invalid JSON
**Common LLM mistakes**:
- Wrapping JSON in markdown code fences
- Generating a single object instead of array
- Missing `surfaceId`
- Using nested trees instead of flat adjacency lists
- Referencing IDs that don't exist in components

**Auto-fix pattern**:
```python
# Strip markdown fences
cleaned = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()

# Parse
data = json.loads(cleaned)

# Wrap single object in list
if isinstance(data, dict):
    data = [data]

# Inject surfaceId
for msg in data:
    if "surfaceId" not in msg:
        msg["surfaceId"] = "default"
```

### 7. Port Already in Use
```bash
lsof -ti :10003 | xargs kill -9
```

## Official Resources for Troubleshooting
- GitHub Issues: https://github.com/google/A2UI/issues
- A2UI Docs: https://a2ui.org/
- Component Gallery: Run the component_gallery demo locally
- A2UI Composer: https://a2ui-composer.ag-ui.com/ (interactive builder)
