# LLM Timeout Workaround for google.genai

## Issue Description
The `google.genai` SDK (e.g. v1.72.0) has a design behavior where the `http_options={"timeout": X}` parameter provided during `genai.Client` instantiation is completely ignored by the underlying `httpx` HTTP transport layer. Instead, it applies a hard-coded default 5.0s timeout to all network requests.

This results in persistent `httpx.ReadTimeout` errors during long-running tasks, such as generating semantic embeddings of large log chunks or evaluating complex instructions via the LLM API. The AROS dreamer daemon is especially vulnerable as it relies on `process_log_chunk` running in the background, which frequently exceeds the 5-second boundary.

## The Workaround
To bypass this limitation without modifying the external library code or risking an uncontrolled SDK upgrade, AROS monkey-patches the instantiated client immediately.

The fix involves explicitly applying `httpx.Timeout(120.0)` to the private `_httpx_client` and `_async_httpx_client` attributes of the client object.

### Implementation Location
The patch is centrally implemented in `src/antigravity_brain/llm_client.py`:

```python
def _apply_timeout_patch(client):
    """Monkey-patch google.genai.Client to enforce a 120s httpx timeout."""
    import httpx
    timeout_val = httpx.Timeout(120.0)
    try:
        if hasattr(client, '_api_client'):
            if hasattr(client._api_client, '_httpx_client'):
                client._api_client._httpx_client.timeout = timeout_val
            if hasattr(client._api_client, '_async_httpx_client'):
                client._api_client._async_httpx_client.timeout = timeout_val
    except Exception as e:
        logger.warning(f"[llm_client] Failed to apply httpx timeout patch: {e}")
    return client
```

This ensures that both the direct offline connection and the cloud proxy connection are protected from premature disconnection.

## Diagnostic Verification
If `httpx.ReadTimeout` errors re-emerge in the future (e.g. after a `google.genai` library update that changes its internal structure), developers should check `llm_client.py` to ensure `_api_client._httpx_client` is still the correct path to the transport layer. A unit test `test_llm_timeout.py` is used to periodically verify that the timeout value overrides successfully.
