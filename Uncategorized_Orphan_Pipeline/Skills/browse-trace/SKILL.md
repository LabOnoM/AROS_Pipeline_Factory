---
name: browse-trace
description: >
  Capture a full DevTools-protocol trace (CDP firehose, screenshots, DOM dumps) alongside any
  browser automation, then bisect the stream into per-page searchable buckets. Use when debugging
  failed browser runs, auditing network/console/DOM activity, or feeding structured per-page
  summaries back into an agent loop.
skill-author: Browserbase (adapted for AROS)
license: MIT
original-source: https://github.com/browserbase/skills
---

# Browser Trace — CDP Debugging Skill

Attach a read-only CDP client to a browser session to record the full DevTools firehose. This skill **does not drive pages** — it only listens. Pair with browse-cli, Playwright, or any CDP-speaking automation.

## When to Use

- Debug a browser-automation run (failing form, missing element, hung navigation, JS exception)
- Attach a trace mid-flight without restarting the automation
- Split a CDP firehose into network / console / DOM / page buckets
- Capture timed screenshots + DOM snapshots joined to CDP events

## Prerequisites

```bash
node --version                    # Require Node 18+
which browse || npm install -g @browserbasehq/browse-cli
which jq || true                  # Optional for ad-hoc querying
```

## How It Works

Every Chrome DevTools target accepts multiple concurrent CDP clients. The tracer adds a second read-only client:

1. **Firehose**: streams every CDP event as NDJSON to `cdp/raw.ndjson`
2. **Sampler**: polls for screenshots and DOM dumps at intervals (default 2s)
3. **Bisector**: slices `raw.ndjson` into per-bucket JSONL files keyed by CDP method and per-page boundaries

## Filesystem Layout

```
.o11y/<run-id>/
  manifest.json                 # run metadata
  index.jsonl                   # one line per sample: {ts, screenshot, dom, url}
  cdp/
    raw.ndjson                  # full CDP firehose
    summary.json                # session overview with pages[] array
    network/{requests,responses,finished,failed}.jsonl
    console/{logs,exceptions}.jsonl
    page/{navigations,lifecycle,frames}.jsonl
    pages/                      # per-page slices
      000/                      # first page
        url.txt
        summary.json
        raw.jsonl
        network/, console/, page/   # same buckets, page-scoped
  screenshots/<iso-ts>.png
  dom/<iso-ts>.html
```

## Top Analysis Recipes

```bash
# All failed network requests
jq -c '.params' .o11y/<run>/cdp/network/failed.jsonl

# Find requests to specific host
jq -c 'select(.params.request.url | test("api\\.example\\.com"))' \
  .o11y/<run>/cdp/network/requests.jsonl

# 4xx/5xx responses
jq -c 'select(.params.response.status >= 400) | {status: .params.response.status, url: .params.response.url}' \
  .o11y/<run>/cdp/network/responses.jsonl

# Console errors only
jq -c 'select(.params.type == "error")' .o11y/<run>/cdp/console/logs.jsonl

# Sequence of URLs visited
jq -r '.params.frame.url' .o11y/<run>/cdp/page/navigations.jsonl
```

## Best Practices

1. Don't poll faster than ~1s (2s is good default)
2. Pick CDP domains deliberately — defaults (Network, Console, Runtime, Log, Page) cover most debugging
3. Add DOM domain only when needed (very noisy)
4. Always run stop-capture, even after crashes
5. Bisect once per run (idempotent)

## AROS Integration

This skill is useful for:
- Debugging AROS Dashboard UI issues with full network trace
- Capturing evidence during automated QA runs (pairs with browse-ui-test)
- Analyzing Shiny app (SCRIB) browser interactions
- Building training data for autobrowse strategy refinement
