# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import argparse
import pandas as pd
import base64, re, io, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from bs4 import BeautifulSoup

# ── library metadata ──────────────────────────────────────────────────────────
LIBRARIES = [
    ("GO: Biological Process", "GO Biological Process_2023"),
    ("GO: Molecular Function", "GO Molecular Function_2023"),
    ("GO: Cellular Component", "GO Cellular Component_2023"),
    ("KEGG Pathways",          "KEGG_2019_Mouse"),
    # Add backward compatibility names if they differ
    ("GO: Biological Process", "GO Biological Process"),
    ("GO: Molecular Function", "GO Molecular Function"),
    ("GO: Cellular Component", "GO Cellular Component"),
    ("KEGG Pathways",          "KEGG Pathways")
]

# ── helper: encode image to base64 ───────────────────────────────────────────
def img_b64(path):
    try:
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

# ── helper: build dot plot inline with matplotlib ────────────────────────────
def make_dot_plot_b64(sub_df, title, top_n=20):
    df = sub_df.copy().sort_values("FDR q-val", ascending=True).head(top_n)
    df = df[df["FDR q-val"] < 1.0]
    if df.empty:
        return ""

    def parse_pct(v):
        try:
            if isinstance(v, str) and "/" in v:
                a, b = v.split("/")
                return int(a) / int(b)
            return float(str(v).replace("%","")) / 100
        except:
            return 0.05

    df["TagRatio"] = df["Tag %"].apply(parse_pct)
    df["-log10FDR"] = -np.log10(df["FDR q-val"].replace(0, 1e-300))

    def shorten(t, n=55):
        t = re.sub(r"\s*\(GO:\d+\)", "", str(t))
        return t[:n] + "…" if len(t) > n else t

    df["Label"] = df["Term"].apply(shorten)
    df_plot = df.sort_values("-log10FDR")

    nes_vals = df_plot["NES"].values
    vmin, vmax = nes_vals.min(), nes_vals.max()
    if pd.isna(vmin) or pd.isna(vmax): return ""
    norm = mcolors.TwoSlopeNorm(vmin=min(vmin, -0.01), vcenter=0, vmax=max(vmax, 0.01))
    cmap = plt.cm.RdBu_r

    size_vals = df_plot["TagRatio"].values * 400 + 30

    fig, ax = plt.subplots(figsize=(10, max(5, len(df_plot) * 0.45)))
    sc = ax.scatter(
        df_plot["-log10FDR"], range(len(df_plot)),
        s=size_vals, c=nes_vals, cmap=cmap, norm=norm,
        alpha=0.85, edgecolors="k", linewidths=0.4, zorder=3
    )
    ax.set_yticks(range(len(df_plot)))
    ax.set_yticklabels(df_plot["Label"].tolist(), fontsize=8.5)
    ax.set_xlabel("-log₁₀(FDR q-value)", fontsize=10)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.axvline(x=-np.log10(0.05), color="grey", linestyle="--", linewidth=0.8, label="FDR=0.05")
    ax.grid(axis="x", alpha=0.3)

    cb = fig.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=norm), ax=ax, pad=0.01)
    cb.set_label("NES", fontsize=9)

    for size_ratio, label in [(0.1, "10%"), (0.3, "30%"), (0.6, "60%")]:
        ax.scatter([], [], s=size_ratio * 400 + 30, c="grey", alpha=0.6,
                   label=f"Tag%={label}", edgecolors="k", linewidths=0.4)
    ax.legend(loc="lower right", fontsize=8, framealpha=0.7)

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode()

# ── helper: build DataTables HTML table from dataframe ───────────────────────
def make_datatable(df, table_id):
    display_cols = ["Term", "NES", "NOM p-val", "FDR q-val", "FWER p-val", "Tag %", "Gene %", "Lead_genes"]
    display_cols = [c for c in display_cols if c in df.columns]
    ddf = df[display_cols].copy()

    for c in ["NES", "NOM p-val", "FDR q-val", "FWER p-val"]:
        if c in ddf.columns:
            ddf[c] = ddf[c].apply(lambda v: f"{v:.4e}" if isinstance(v, float) else v)

    header = "".join(f"<th>{c}</th>" for c in display_cols)
    rows = []
    for _, row in ddf.iterrows():
        cells = "".join(f"<td>{row[c]}</td>" for c in display_cols)
        rows.append(f"<tr>{cells}</tr>")

    return f"""
<div class="table-responsive" style="margin-top:12px;">
  <table id="{table_id}" class="display compact nowrap fea-table" style="width:100%">
    <thead><tr style="background:#2c3e50; color:#fff; font-weight:700;">{header}</tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>"""

def interpret_lib(lib_name, top_rows):
    top = top_rows.head(5)
    terms_pos = top[top["NES"] > 0]["Term"].str.replace(r"\s*\(GO:\w+\)", "", regex=True).tolist()
    terms_neg = top[top["NES"] < 0]["Term"].str.replace(r"\s*\(GO:\w+\)", "", regex=True).tolist()

    pos_str = "; ".join([f"<em>{t}</em>" for t in terms_pos[:3]]) if terms_pos else "none"
    neg_str = "; ".join([f"<em>{t}</em>" for t in terms_neg[:3]]) if terms_neg else "none"

    if top.empty:
         return f'<div class="interp-box"><strong>🔬 LLM Interpretation:</strong> No significant enrichment terms.</div>'

    fdr_min = top["FDR q-val"].min()
    n_sig = (top_rows["FDR q-val"] < 0.05).sum()

    return f"""
<div class="interp-box">
  <strong>🔬 LLM Interpretation:</strong>
  The <em>{lib_name}</em> analysis identified <strong>{n_sig}</strong> significantly
  enriched gene sets (FDR &lt; 0.05). The minimum FDR reached <strong>{fdr_min:.2e}</strong>.
  Positively enriched terms: {pos_str}.
  Negatively enriched terms: {neg_str}.
</div>"""

def build_fea_section(df_all, viz_dir):
    # Unique libraries from mapping
    libs_found = []
    for nice_name, search_key in LIBRARIES:
        if search_key in df_all["Library"].values and nice_name not in [x[0] for x in libs_found]:
            libs_found.append((nice_name, search_key))

    if not libs_found:
       return "<div>No Libraries Found.</div>"

    head_deps = """
<!-- FEA Section dependencies: Bootstrap 5 tabs + DataTables -->
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.8/css/jquery.dataTables.min.css">
<link rel="stylesheet" href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.datatables.net/1.13.8/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js"></script>
<style>
.fea-tabset { margin-top: 20px; }
.fea-tabset .nav-tabs { border-bottom: 2px solid #2c3e50; }
.fea-tabset .nav-tabs .nav-link { color: #2c3e50; font-weight: 600; font-size: 0.9rem; }
.fea-tabset .nav-tabs .nav-link.active { background: #2c3e50; color: #fff; border-radius: 4px 4px 0 0; }
.fea-tabset .tab-content { border: 1px solid #dee2e6; border-top: none; padding: 16px; border-radius: 0 0 6px 6px; background:#fff; margin-bottom: 40px;}
.inner-tabs .nav-link { font-size: 0.82rem; color: #555; }
.inner-tabs .nav-link.active { background: #3498db; color: #fff; border-radius: 4px; }
.inner-tabs .tab-content { padding: 12px 0 0 0; border: none; background: transparent; }
.interp-box { background: #eaf4fb; border-left: 4px solid #3498db; padding: 12px 16px; border-radius: 4px; margin-bottom: 14px; font-size: 0.9rem; line-height: 1.6; }
.fea-table thead th { white-space: nowrap; }
table.dataTable { font-size: 0.82rem; }
</style>"""

    dt_ids_spread = [f"dt_{re.sub(r'[^a-z]','_', ln.lower())}" for ln, _ in libs_found]
    js_init = """<script>
$(document).ready(function() {
  function initDT(id) {
    if (!$.fn.DataTable.isDataTable('#' + id)) {
      $('#' + id).DataTable({
        pageLength: 10,
        lengthMenu: [[10, 25, 50, 100, -1],["10","25","50","100","All"]],
        scrollX: true,
        dom: 'Blfrtip',
        buttons: ['copy','csv'],
        columnDefs: [{ targets: -1, render: function(d){ return d.length > 80 ? d.substr(0,80)+'…' : d; } }]
      });
    }
  }
  $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function(e){
    var targetId = $(e.target).attr('data-bs-target').replace('#','');
    var table = $('#' + targetId).find('table.fea-table');
    if (table.length) initDT(table.attr('id'));
  });
""" + "\n".join([f"  initDT('{tid}');" for tid in dt_ids_spread[:1]]) + """
});
</script>"""

    # Spreadsheets
    spread_nav, spread_panes = [], []
    for i, (label, lib_key) in enumerate(libs_found):
        tab_id = f"spread_{re.sub('[^a-z]','_',label.lower())}"
        active, show = ("active", "show active") if i == 0 else ("", "")
        
        sub = df_all[df_all["Library"] == lib_key].sort_values("FDR q-val")
        if not sub.empty:
            table_html = make_datatable(sub, dt_ids_spread[i])
            interp_html = interpret_lib(label, sub)
            spread_nav.append(f'<li class="nav-item"><button class="nav-link {active}" data-bs-toggle="tab" data-bs-target="#{tab_id}" type="button" role="tab">{label}</button></li>')
            spread_panes.append(f'<div class="tab-pane fade {show}" id="{tab_id}" role="tabpanel">{interp_html}{table_html}</div>')

    # Plots
    plot_nav, plot_panes = [], []
    for i, (label, lib_key) in enumerate(libs_found):
        tab_id = f"plot_{re.sub('[^a-z]','_',label.lower())}"
        active, show = ("active", "show active") if i == 0 else ("", "")

        sub = df_all[df_all["Library"] == lib_key].sort_values("FDR q-val")
        b64 = make_dot_plot_b64(sub, f"Dot Plot — {label}")
        img_html = f'<img src="{b64}" style="max-width:100%;" alt="Dot plot">' if b64 else "<p><em>No significant results.</em></p>"

        # Find static gseaplot for KEGG or GO if it exists in viz_dir
        if viz_dir and os.path.exists(f"{viz_dir}/{lib_key}.png"):
            extra_b64 = img_b64(f"{viz_dir}/{lib_key}.png")
            if extra_b64:
                 img_html += f'<hr><img src="{extra_b64}" style="max-width:100%;">'

        plot_nav.append(f'<li class="nav-item"><button class="nav-link {active}" data-bs-toggle="tab" data-bs-target="#{tab_id}" type="button" role="tab">{label}</button></li>')
        plot_panes.append(f'<div class="tab-pane fade {show}" id="{tab_id}" role="tabpanel">{img_html}</div>')

    spreadsheet_section = f'<div class="fea-tabset inner-tabs"><ul class="nav nav-tabs">{"".join(spread_nav)}</ul><div class="tab-content">{"".join(spread_panes)}</div></div>'
    plots_section = f'<div class="fea-tabset inner-tabs"><ul class="nav nav-tabs">{"".join(plot_nav)}</ul><div class="tab-content">{"".join(plot_panes)}</div></div>'

    fea_section = f"""{head_deps}
<div class="card" id="fea-section" style="margin-top:30px; padding:24px; background:#f9f9fc; border-radius:10px; border-left:5px solid #3498db;">
  <h2 style="color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;">✦ Interactive Functional Enrichment Analysis</h2>
  <div class="fea-tabset" style="margin-top:16px;">
    <ul class="nav nav-tabs" id="feaOuterTabs" role="tablist">
      <li class="nav-item"><button class="nav-link active" data-bs-toggle="tab" data-bs-target="#fea-spreadsheets" type="button" role="tab">📊 Spreadsheets</button></li>
      <li class="nav-item"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#fea-plots" type="button" role="tab">🔵 Summary Plots</button></li>
    </ul>
    <div class="tab-content">
      <div class="tab-pane fade show active" id="fea-spreadsheets" role="tabpanel">{spreadsheet_section}</div>
      <div class="tab-pane fade" id="fea-plots" role="tabpanel">{plots_section}</div>
    </div>
  </div>
</div>{js_init}"""
    return fea_section

def inject_into_html(fea_html, html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    for old in soup.find_all("div", id="fea-section"): old.decompose()
    for old in soup.find_all("div", class_="card"):
        h2 = old.find("h2")
        if h2 and ("GSEA" in h2.get_text() or "Enrichment" in h2.get_text()):
            old.decompose()

    new_section = BeautifulSoup(fea_html, "html.parser")
    if soup.body: soup.body.append(new_section)
    else: soup.append(new_section)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"✓ Injected GSEA interactive tables into {html_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert GSEA XLSX into interactive DataTables HTML")
    parser.add_argument("--xlsx", required=True, help="Path to gsea_results_full.xlsx")
    parser.add_argument("--html", required=True, help="Path to analysis_report.html to inject into")
    parser.add_argument("--viz_dir", required=False, help="Path to folder containing pre-rendered gseaplots or dotplots")
    args = parser.parse_args()

    df_all = pd.read_excel(args.xlsx)
    fea_html = build_fea_section(df_all, args.viz_dir)
    inject_into_html(fea_html, args.html)
