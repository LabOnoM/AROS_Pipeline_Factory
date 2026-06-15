---
name: web-project-builder
description: ">"
---

# Web Project Builder

Build full-stack web projects organized by four roles: Frontend, Backend, UI, Testing.

## Quick Start

Scaffold a new project using the bundled script:

```bash
python3 scripts/scaffold.py <project-name> --dir <parent-directory>
```

This generates a ready-to-run project with Flask backend, Bootstrap/ECharts frontend, and pytest tests.

## Tech Stack

- Frontend: Bootstrap 5.3.3 + ECharts 5.5.0 (all CDN)
- Backend: Python Flask + SQLite
- Testing: pytest
- See [references/tech-reference.md](references/tech-reference.md) for CDN URLs, API patterns, and chart types

## Workflow

### 1. Scaffold

Run `scripts/scaffold.py` to generate the project skeleton. Customize the project name and output directory.

### 2. Customize by Role

**Frontend**: Edit `templates/` and `static/js/main.js`. Add pages by creating new templates extending `base.html`. Add ECharts visualizations in JS files.

**Backend**: Edit `app.py`. Add new routes, database tables, and API endpoints. Follow the RESTful pattern: `GET /api/resource`, `POST /api/resource`, `DELETE /api/resource/<id>`.

**UI**: Edit `templates/` and `static/css/style.css`. Use Bootstrap grid (`row`/`col-*`), cards, tables, and form components. Keep responsive.

**Testing**: Edit `tests/test_app.py`. Use Flask `test_client` with a temporary SQLite database. Cover all API endpoints.

### 3. Run

```bash
cd <project-name>
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`.

### 4. Test

```bash
pytest tests/ -v
```

## Key Conventions

- All external libraries loaded via CDN in `base.html` (no npm/node)
- Templates use Jinja2 inheritance: all pages extend `base.html`
- API routes prefixed with `/api/`
- SQLite database auto-created on first run
- Chinese UI text by default (configurable)
