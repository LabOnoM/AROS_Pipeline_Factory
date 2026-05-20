# KI-284: Self-Contained Web Application Bundling for Portable Scientific Visualizations

This Knowledge Item provides a robust pattern for bundling a client-side web application (HTML, CSS, JavaScript, and JSON data) into a single, portable HTML file. This is ideal for sharing interactive scientific visualizations or data dashboards that must work offline without a web server.

## 1. Use Case & Core Problem

**Goal:** You have a data-driven web visualization that you need to share as a single, double-clickable file (e.g., as an email attachment or a supplemental file in a publication).

**The Challenge (`file://` Protocol and CORS):** Modern web browsers enforce strict security policies. When you open an HTML file from your local filesystem (`file://`), any attempt by its JavaScript code to load other local files (like `data.json`) using the `fetch()` API will be blocked by a Cross-Origin Resource Sharing (CORS) error. This is because the browser treats the local file as a unique, "opaque" origin, preventing it from accessing other files, even in the same directory.

---

## 2. Applicability & Constraints (Guardrails)

This pattern is the correct choice only when specific conditions are met.

**✅ Use this pattern when:**
- Your application is **fully client-side** (HTML, CSS, JS).
- Your data is **static and pre-generated** in `.json` files.
- The total size of all data is reasonable for a single file (e.g., < 50MB).
- The primary goal is **portability and offline access** for viewing pre-computed results.
- **Example Use Cases:** An interactive chart from a Matplotlib export, a D3.js visualization of a simulation result, a data table browser.

**❌ DO NOT use this pattern when:**
- Your application requires a **server-side backend** (e.g., Python Flask, Node.js).
- Your application needs to query a **live database or API**.
- Your goal is to share an **executable analysis or script** (e.g., a Python model, an R script).
- **Alternative Solutions for these cases:**
    - For executable analysis: Share a Jupyter Notebook, a script with a `requirements.txt`, or package the environment with Docker.
    - For applications with a backend: Deploy to a web server or create a containerized version of the entire application stack.

---

## 3. The Robust Inlining Pattern

The solution is to create a new HTML file where all external assets are inlined. We will use a robust Python script with a proper HTML parser (`BeautifulSoup`) to avoid fragile string replacement.

### Project Structure Example

**Before Bundling:**
```
/my_visualization
├── data/
│   ├── experiment_1.json
│   └── experiment_2.json
├── index.html
├── style.css
├── app.js
└── bundle.py        # Our bundling script
```

**After Bundling:**
```
/my_visualization
├── ... (original files) ...
└── standalone_visualization.html  # The final, single-file output
```

### Robust Implementation (`bundle.py`)

This script uses `beautifulsoup4` for reliable HTML parsing and a clear placeholder strategy for patching the JavaScript.

**Prerequisites:** `pip install beautifulsoup4`

```python
import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

# --- Configuration ---
SRC_DIR = Path('.')
DATA_DIR = SRC_DIR / 'data'
HTML_FILE = SRC_DIR / 'index.html'
OUTPUT_FILE = SRC_DIR / 'standalone_visualization.html'

# A placeholder in your JS to indicate where the fetch logic is.
# This is more robust than matching the exact line of code.
# In your app.js, your fetch line might look like:
# const res = await fetch(`data/${name}.json`); //::FETCH_DATA::
JS_PATCH_TARGET = re.compile(r"fetch\(.*?\); //::FETCH_DATA::")

# --- Logic ---

print("Starting webapp bundling process...")

# 1. Aggregate all JSON data into a single Python dictionary
embedded_data = {}
if DATA_DIR.exists():
    for f in DATA_DIR.glob('*.json'):
        print(f"  - Embedding data from: {f.name}")
        embedded_data[f.stem] = json.loads(f.read_text(encoding='utf-8'))
else:
    print("  - Warning: Data directory not found. No data will be embedded.")

# 2. Prepare the new data-loading logic for JavaScript
# This logic checks for the embedded data object first, falling back to fetch.
# This ensures the original app remains functional with a dev server.
js_data_payload = f"const EMBEDDED_DATA = {json.dumps(embedded_data, indent=2)};"
new_fetch_logic = """
    if (typeof EMBEDDED_DATA !== 'undefined' && EMBEDDED_DATA[name]) {
        // Use embedded data if available
        return new Response(JSON.stringify(EMBEDDED_DATA[name]));
    }
    // Fallback to original fetch for development server
    return fetch(`data/${name}.json`); //::FETCH_DATA::
"""
# Note: We return a `Response` object to keep the API consistent with fetch.
# Your JS code that calls this function will still need to do `.json()`.
# e.g., const res = await fetchData(name); const data = await res.json();

# 3. Use BeautifulSoup to parse and modify the HTML robustly
soup = BeautifulSoup(HTML_FILE.read_text(encoding='utf-8'), 'html.parser')

# 4. Find, inline, and remove all <link rel="stylesheet"> tags
for tag in soup.find_all('link', {'rel': 'stylesheet'}):
    css_path = SRC_DIR / tag['href']
    if css_path.exists():
        print(f"  - Inlining stylesheet: {css_path.name}")
        style_tag = soup.new_tag('style')
        style_tag.string = css_path.read_text(encoding='utf-8')
        tag.replace_with(style_tag)
    else:
        print(f"  - Warning: Stylesheet not found: {css_path}")

# 5. Find, patch, inline, and remove all <script src="..."> tags
for tag in soup.find_all('script', src=True):
    js_path = SRC_DIR / tag['src']
    if js_path.exists():
        print(f"  - Inlining and patching script: {js_path.name}")
        original_js = js_path.read_text(encoding='utf-8')
        
        # Use regex with the placeholder to find and replace the fetch logic
        patched_js, count = JS_PATCH_TARGET.subn(new_fetch_logic, original_js)
        
        if count == 0:
            print(f"  - CRITICAL WARNING: JS patch target '//::FETCH_DATA::' not found in {js_path.name}. Data loading will likely fail.")

        # Remove the original src attribute and set the script content
        del tag['src']
        # Prepend the data payload to the patched script content
        tag.string = f"{js_data_payload}\n\n{patched_js}"
    else:
        print(f"  - Warning: Script not found: {js_path}")

# 6. Write the final, self-contained HTML file
OUTPUT_FILE.write_text(str(soup), encoding='utf-8')
print(f"\n✅ Success! Bundled application written to: {OUTPUT_FILE}")

```