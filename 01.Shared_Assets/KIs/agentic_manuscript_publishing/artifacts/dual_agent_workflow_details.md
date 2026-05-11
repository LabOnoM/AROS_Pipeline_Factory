---
cpcp_asset: true
canonical_location: "01.Shared_Assets/KIs/agentic_manuscript_publishing"
consumers:
  - Grant_Write_Pipeline
  - Manuscript_Write_Pipeline
last_cpcp_review: "2026-05-11"
---
# Dual Agent Manuscript Pipeline - Technical Reference

This document contains the required code snippets, parser mappings, and State Header formats for the `/manuscript-write` global workflow.

## 1. Supported File Formats and Parsers

When extracting data from `00.RawData/`, use the following reference mapping. Do NOT use this as a mechanical script—adapt it to the actual file structure discovered.

| Extension | Typical Source | Reference Parser | Key Pitfalls |
|-----------|---------------|-----------------|--------------|
| `.pzfx` | GraphPad Prism (qPCR, WB, ALP) | `xml.etree.ElementTree` | Multiple tables per file; Title nodes may be null; inspect all tables before choosing table_index |
| `.xlsx` / `.xls` | Excel workbooks | `pandas.read_excel(engine='openpyxl')` | Inspect `.columns` and `.head()` first; unnamed columns and hidden header rows are common |
| `.csv` / `.txt` | Instrument exports | `pandas.read_csv()` | Auto-detect delimiter; check for instrument header rows requiring `skiprows=` |
| `.czi` / `.nd2` / `.lif` | Confocal microscopy | `aicsimageio` (universal) | Multi-channel, multi-Z stacks; extract pixel size and channel metadata |
| `.tif` / `.tiff` | Microscopy / CT slices | `tifffile` or `skimage.io` | BigTIFF (>4 GB) requires `tifffile.memmap()`; check bit depth |
| `.fcs` | Flow cytometry | `flowio` or `FlowCal` | Channel compensation may be required; gating decisions are scientific, not algorithmic |
| `.pdb` + `.dcd`/`.xtc` | Structural biology / MD | `MDAnalysis` | Pair topology with trajectory; choose metrics appropriate to the hypothesis |
| `.h5ad` | Single-cell RNA-seq | `scanpy` / `anndata` | Column names with `/` must be renamed |
| `.nii` / `.dcm` | Medical imaging | `nibabel` / `pydicom` | Always check voxel spacing and orientation |

### Example PZFX Parser
```python
import xml.etree.ElementTree as ET
def extract_pzfx(path, table_index=0):
    tree = ET.parse(path)
    groups = {}
    tables = tree.getroot().findall('.//Table')
    for i, t in enumerate(tables):
        te = t.find('Title')
        print(f"Table {i}: {te.text if te is not None else '(untitled)'}")
    table = tables[min(table_index, len(tables)-1)]
    for col in table.findall('.//YColumn'):
        t_elem = col.find('Title')
        label = t_elem.text if (t_elem is not None and t_elem.text) else f'Group_{len(groups)}'
        vals = [float(d.text) for d in col.findall('.//d') if d.text and d.text.strip()]
        if vals:
            groups[label] = vals
    return groups
```

## 2. Agentic State Header Block

> ⚠️ **AUTHORING RULE (April 2026):** The `.md` file is the source of truth. The `.tex` file is a Pandoc-derived artifact. 
> Agent A writes/edits `manuscript.md` → runs Pandoc pipeline → then embeds the state header in the resulting `.tex`.
> **Direct LaTeX authoring is PROHIBITED — proven to reduce scientific content by 93%.**

To reliably track manuscript resume state, Agent A MUST embed this specific LaTeX comment block at the very top of `<manuscript_name>.tex` (after Pandoc conversion).

```latex
% =======================================================================
% BGPT-AGENT-STATE-TRACKER
% WORKFLOW: /manuscript-write
% CURRENT_ITERATION: X / 5
% AGENT_B_LAST_SCORE: XX / 120
% VERDICT: [IN_PROGRESS / MAJOR_REVISIONS / MINOR_REVISIONS / PASSED]
% LAST_UPDATED: YYYY-MM-DD
% =======================================================================
```

## 3. Publication-Grade Matplotlib Defaults

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="white", font_scale=1.2)
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'axes.spines.top': False,
    'axes.spines.right': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

def annotate_stat(ax, x1, x2, y_top, pval):
    stars = '****' if pval < 0.0001 else '***' if pval < 0.001 else \
            '**' if pval < 0.01 else '*' if pval < 0.05 else 'ns'
    ylim = ax.get_ylim()
    h = (ylim[1] - ylim[0]) * 0.02
    ax.plot([x1, x1, x2, x2], [y_top, y_top+h, y_top+h, y_top], lw=1.2, c='k')
    ax.text((x1+x2)/2, y_top+h, f'{stars}\np={pval:.4f}', ha='center', va='bottom', fontsize=9)
```
