# Interactive Scientific Enrichment Reporting Standard (Python Pattern)

This document specifies a Python-centric standard for generating high-quality, interactive, and portable (single-file) HTML reports for functional enrichment analysis (GSEA and ORA).

## 1. Architectural Philosophy
The goal is to move beyond static images and basic tables by embedding interactivity directly into a standalone HTML file. This avoids dependency on external servers or complex R-Markdown rendering environments when working in Python-heavy pipelines.

- **Responsive Tabs**: Uses Bootstrap 5 `nav-tabs` to organize results (e.g., Spreadsheets vs. Summary Plots).
- **Interactive Tables**: Uses `DataTables.js` via CDN for client-side filtering, sorting, and CSV exporting.
- **Drill-down Modals**: Allows users to click on term names in a table to instantly view the associated Enrichment Plot or Pathway Map in a modal window.
- **Portability**: All data and small assets are inlined or fetched via high-availability CDNs.

## 2. Technical Stack
- **Core Logic**: `pandas`, `gseapy`, `matplotlib`.
- **HTML DOM**: `BeautifulSoup4`.
- **Frontend UI**: Bootstrap 5 (CSS/JS), DataTables.js (JS), jQuery.

## 3. Implementation Workflow

### 3.1 Data Preparation
Results should be stored in a structured format (e.g., `.xlsx`) containing:
- `Term`, `NES`, `FDR q-val`, `Tag %`, `Lead_genes`, `Library`.

### 3.2 HTML Tabset Structure
Group the analysis into nested tiers using Bootstrap tabs:
1. **Spreadsheets** (Inner Tabs: GO:BP, GO:MF, GO:CC, KEGG)
2. **Summary Plots** (Inner Tabs: Dot Plots, Grouped Bar Charts)

### 3.3 Modal Drill-down Pattern
Each term in the table should be wrapped in a clickable span:
```html
<span class="term-link" data-termkey="term_id" data-plotvar="libraryPlotsVar">Term Name</span>
```
A central JavaScript handler listens for clicks and updates a hidden modal's `src` attribute with the pre-loaded Base64 image.

## 4. Critical Troubleshooting: GSEA Mapping Bug
A known issue exists in `gseapy.prerank` and `gseapy.gseaplot` where the Enrichment Score (`RES`) and the `ranking` array indices can drift by one element (`n+1` mismatch), causing plotting crashes.

### The Fix (Manual Plotting)
Always use the length of the `RES` array as the authoritative length and align other features to it.

```python
def draw_gsea_plot(term, r, ranking, nes, pval, fdr):
    RES  = np.array(r["RES"])
    hits = np.array(r["hits"])
    n    = len(RES)           # Authority length
    x    = np.arange(n)
    
    # Safely trim ranking series
    rm = np.array(ranking)[:n]
    
    # Filter hits that fall outside the trimmed range
    valid_hits = hits[hits < n]
    
    # ... Create Matplotlib plot manually ...
```

## 5. KEGG Pathway Enhancement
For KEGG, static GSEA plots are often less informative than colored pathway maps.
- **Standard**: Use the R `pathview` package (called via `subprocess`) to generate abundance-colored nodes.
- **Integration**: Map symbols to `pathway.id` and species (e.g., `mmu` for mouse) and embed the resulting `.png` as a Base64 string.

## 6. CSS/JS Boilerplate
Include these via CDN in the `<head>` or at the top of the injected section:
- `bootstrap.min.css` (v5.3+)
- `jquery.dataTables.min.css`
- `jquery-3.7.1.min.js`
- `jquery.dataTables.min.js`
- `bootstrap.bundle.min.js`
