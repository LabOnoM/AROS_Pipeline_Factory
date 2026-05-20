---
name: browse-cli
description: >
  Automate web browser interactions using the browse CLI with natural language commands.
  Use when the user asks to browse websites, navigate web pages, extract data, take screenshots,
  fill forms, click buttons, or interact with JavaScript-heavy web applications.
  Supports local Chrome and remote Browserbase sessions with anti-bot stealth, CAPTCHA solving,
  and residential proxies.
skill-author: Browserbase (adapted for AROS)
license: MIT
original-source: https://github.com/browserbase/skills
---

# Browser Automation via browse CLI

Automate browser interactions using the `browse` CLI. Supports both local Chrome and remote Browserbase cloud sessions.

## Prerequisites

```bash
which browse || npm install -g @browserbasehq/browse-cli
```

For remote Browserbase sessions: `export BROWSERBASE_API_KEY="your_api_key"` (get from https://browserbase.com/settings)

## Environment Selection

### Local mode (default for development/localhost)
- `browse env local` — clean isolated local browser (default)
- `browse env local --auto-connect` — reuse existing Chrome session with cookies/login
- `browse env local <port|url>` — attach to a specific CDP target

### Remote mode (Browserbase cloud)
- `browse env remote` — cloud session with stealth, CAPTCHA solving, proxies
- Use for: bot detection, CAPTCHAs, IP rate limiting, Cloudflare, geo-specific access

### Decision Guide

| Scenario | Mode |
|----------|------|
| Development/localhost/clean state | `browse env local` |
| Reuse existing login/cookies | `browse env local --auto-connect` |
| Simple browsing (docs, wikis, public APIs) | Local |
| Protected sites (login walls, CAPTCHAs) | Remote |
| Bot detection / access denied | Remote |

## Core Commands

### Navigation
```bash
browse open <url>                       # Navigate to URL
browse open <url> --context-id <id>     # Load Browserbase persistent context
browse reload                           # Reload page
browse back / browse forward            # History navigation
```

### Page State (prefer snapshot over screenshot)
```bash
browse snapshot                         # Accessibility tree with element refs (fast, structured)
browse screenshot [path]                # Visual screenshot (slow, uses vision tokens)
browse get url                          # Current URL
browse get title                        # Page title
browse get text <selector>              # Text content ("body" for all)
browse get html <selector>              # HTML content
browse get value <selector>             # Form field value
```

**Always use `browse snapshot` as default** — it returns the accessibility tree with element refs. Only use `browse screenshot` when you need visual context.

### Interaction
```bash
browse click <ref>                      # Click by ref from snapshot (e.g., @0-5)
browse type <text>                      # Type into focused element
browse fill <selector> <value>          # Fill input and press Enter
browse select <selector> <values...>    # Select dropdown option(s)
browse press <key>                      # Press key (Enter, Tab, Escape, Cmd+A)
browse drag <fromX> <fromY> <toX> <toY> # Drag and drop
browse scroll <x> <y> <deltaX> <deltaY> # Scroll at coordinates
browse wait <type> [arg]                # Wait for: load, selector, timeout
```

### Session Management
```bash
browse stop                             # Stop daemon + clear env override
browse status                           # Check daemon status
browse env                              # Show current environment
browse pages                            # List open tabs
browse tab_switch <index>               # Switch tab
browse tab_close [index]                # Close tab
```

## Typical Workflow

1. `browse env local` (or `remote`) — set environment
2. `browse open <url>` — navigate
3. `browse snapshot` — read accessibility tree, get element refs
4. `browse click <ref>` / `browse type <text>` / `browse fill <selector> <value>` — interact
5. `browse snapshot` — confirm action worked
6. Repeat 4-5 as needed
7. `browse stop` — cleanup

## Mode Comparison

| Feature | Local | Browserbase |
|---------|-------|-------------|
| Speed | Faster | Slightly slower |
| Setup | Chrome required | API key required |
| Stealth mode | No | Yes |
| CAPTCHA solving | No | Yes (automatic) |
| Residential proxies | No | Yes (201 countries) |
| Session persistence | No | Yes (via contexts) |

## Troubleshooting

- **"No active page"**: `browse stop`, then retry. For zombies: `pkill -f "browse.*daemon"`
- **Chrome not found**: `sudo apt install google-chrome-stable` (Linux)
- **Action fails**: `browse snapshot` to see available elements
- **Browserbase fails**: Verify API key is set
- **Switch to remote** when you detect: CAPTCHAs, bot detection pages, HTTP 403/429, empty pages on content sites

## AROS Integration Notes

This skill complements `aros-scrapling` (Python-based web scraping). Use this for:
- Interactive browser sessions requiring JavaScript execution
- Form filling, login flows, and multi-step workflows
- Anti-bot bypass with Browserbase cloud
- Visual debugging with screenshots and accessibility trees

Use `aros-scrapling` when you need: batch scraping, CSS selector extraction, headless HTML parsing without a full browser.
