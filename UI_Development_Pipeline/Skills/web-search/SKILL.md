---
name: web-search
description: Web search and content extraction via DuckDuckGo. Use when you need real-time web results, citations, or raw article content without a browser.
---

# Web Search

Headless web search and content extraction using `duckduckgo-search`. Built for LLM agents — returns clean results with optional raw article bodies. No browser required, and no API key required.

## When to use

- You need up-to-date web information (news, docs, pricing, facts)
- You want cited sources with URLs for a research/writing task
- You need the full readable body of a URL as markdown
- Brave/Google search is not available or rate-limited

## When NOT to use

- You already have the page in your context
- The answer is static and likely in the model's training data
- You need to interact with a page (login, click) — use a browser MCP instead

## Search

```bash
# Basic search — 5 results
uv run ~/.gemini/skills/web-search/scripts/search.py "your query"

# More results
uv run .../search.py "your query" --max-results 10

# Output as JSON
uv run .../search.py "your query" --json
```

### Flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--max-results N` | `5` | Number of results to return (1–20) |
| `--topic {general,news}` | `general` | News mode adds recency filtering |
| `--json` | off | Machine-readable JSON output |

## Extract a single URL

```bash
uv run .../search.py --extract https://example.com/article
```

Returns clean text of the page body (no nav, ads, or boilerplate).

## Output format (default, human-readable)

```
RESULTS:
[1] <title>
    <url>
    <snippet — 1–2 sentences>

[2] ...
```

## Examples

Research a library:

```bash
uv run .../search.py "Gemini 3 Flash Image API pricing"
```

Get the full article body of a blog post:

```bash
uv run .../search.py --extract https://blog.example.com/post --json > post.json
```

News sweep:

```bash
uv run .../search.py "OpenAI Codex release" --topic news --max-results 10
```

## Environment

- Default model: DuckDuckGo API wrapper
- No API Key required.

## Common failures

| Error | Fix |
|------|-----|
| `Extract failed` | Ensure the URL isn't protected by strong bot-protection (Cloudflare etc). |
| `Search failed` | Check internet connectivity or network limits. |
| `No results` | Broaden query. |

## Verification

- [ ] `uv run .../search.py "hello world"` returns results
