"""
VPEP (Video-to-Protocol Extraction Pipeline) - Master Dashboard Generator
========================================================================

Description:
    This script is Stage 6 (the final stage) of the VPEP pipeline. It aggregates all intermediate
    outputs (interactive reports, SOP protocols, and compared experiment notebooks) into a single,
    unified, premium bilingual HTML dashboard supporting instant language switching (JA/EN),
    interactive keyframe Lightbox modals, and automated table searching.

Key Capabilities:
    - Extracts individual report cards from generated HTML documents.
    - Automatically converts markdown files to HTML via pandoc.
    - Compiles a cohesive, beautiful bilingual dashboard matching modern design guidelines.

Cross-Platform Compatibility:
    - Cross-platform file path management using standard `os.path` operations.
    - Standardized UTF-8 encoding across all reads and writes to avoid encoding discrepancies.
"""

import os
import subprocess
import re
import argparse

def extract_cards(html_content):
    cards = []
    pos = 0
    while True:
        start_idx = html_content.find('<div class="card"', pos)
        if start_idx == -1:
            break
        
        div_open_end = html_content.find('>', start_idx)
        if div_open_end == -1:
            break
        
        count = 1
        pos = div_open_end + 1
        
        while count > 0 and pos < len(html_content):
            next_open = html_content.find('<div', pos)
            next_close = html_content.find('</div>', pos)
            
            if next_close == -1:
                break
                
            if next_open != -1 and next_open < next_close:
                count += 1
                pos = next_open + 4
            else:
                count -= 1
                pos = next_close + 6
                
        if count == 0:
            cards.append(html_content[start_idx:pos])
        else:
            break
    return cards

def markdown_to_html(md_path):
    print(f"Converting {os.path.basename(md_path)} to HTML using pandoc...")
    result = subprocess.run(
        ["pandoc", md_path, "-t", "html"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="Generate the master bilingual VPEP dashboard.")
    parser.add_argument("--output_dir", "-o", required=True, help="Directory where intermediate outputs exist and master dashboard will be saved.")
    parser.add_argument("--en_report_path", help="Path to EN HTML report.")
    parser.add_argument("--ja_report_path", help="Path to JA HTML report.")
    parser.add_argument("--en_sop_path", help="Path to EN SOP markdown report.")
    parser.add_argument("--jp_sop_path", help="Path to JA/JP SOP markdown report.")
    parser.add_argument("--en_notebook_path", help="Path to EN Compared Experiment Notebook markdown.")
    parser.add_argument("--ja_notebook_path", help="Path to JA Compared Experiment Notebook markdown.")
    parser.add_argument("--output_html_path", help="Path where the final master dashboard HTML should be written.")
    parser.add_argument("--video_filename", default="masked_tracking_video.mp4", help="Name of the video file in the dashboard.")
    
    args = parser.parse_args()
    
    # Resolve paths
    en_report_path = args.en_report_path or os.path.join(args.output_dir, "Interactive_Report_EN.html")
    ja_report_path = args.ja_report_path or os.path.join(args.output_dir, "Interactive_Report_JA.html")
    
    en_sop_path = args.en_sop_path or os.path.join(args.output_dir, "Cell_Passage_Protocol_EN.md")
    jp_sop_path = args.jp_sop_path or os.path.join(args.output_dir, "Cell_Passage_Protocol_JP.md")
    
    en_notebook_path = args.en_notebook_path or os.path.join(args.output_dir, "Compared_Experiment_Notebook_EN.md")
    ja_notebook_path = args.ja_notebook_path or os.path.join(args.output_dir, "Compared_Experiment_Notebook_JA.md")
    
    output_html_path = args.output_html_path or os.path.join(args.output_dir, "Interactive_Report.html")
    
    # Get basenames for the downloads section
    en_sop_base = os.path.splitext(os.path.basename(en_sop_path))[0]
    jp_sop_base = os.path.splitext(os.path.basename(jp_sop_path))[0]
    en_notebook_base = os.path.splitext(os.path.basename(en_notebook_path))[0]
    ja_notebook_base = os.path.splitext(os.path.basename(ja_notebook_path))[0]
    
    # Read HTML reports
    with open(en_report_path, "r", encoding="utf-8") as f:
        en_html = f.read()
    with open(ja_report_path, "r", encoding="utf-8") as f:
        ja_html = f.read()
        
    # Extract style block and script block from original EN report
    style_match = re.search(r"<style>(.*?)</style>", en_html, re.DOTALL)
    style_block = style_match.group(1) if style_match else ""
    
    # Extract cards
    en_cards = extract_cards(en_html)
    ja_cards = extract_cards(ja_html)
    
    print(f"Extracted {len(en_cards)} cards from EN report and {len(ja_cards)} cards from JA report.")
    
    # Convert Markdown documents to HTML
    en_sop_html = markdown_to_html(en_sop_path)
    jp_sop_html = markdown_to_html(jp_sop_path)
    
    en_notebook_html = markdown_to_html(en_notebook_path)
    ja_notebook_html = markdown_to_html(ja_notebook_path)
    
    # Define master template using double curly brace placeholders
    template = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <title>VPEP インタラクティブ分析ダッシュボード</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Space+Grotesk:wght@400;500;700&family=Noto+Sans+JP:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        __STYLE_BLOCK__
        
        /* Premium Dashboard UI Overrides & Improvements */
        body {
            font-family: 'Outfit', 'Noto Sans JP', sans-serif;
            transition: background-color 0.3s ease;
        }
        
        .title-gradient {
            font-family: 'Space Grotesk', 'Noto Sans JP', sans-serif;
            font-size: 2.8rem;
            background: linear-gradient(135deg, #6366f1 0%, #a5b4fc 50%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 5px;
            font-weight: 700;
        }
        
        /* Language Toggle and Control Panel */
        .control-panel {
            position: sticky;
            top: 20px;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(11, 15, 25, 0.85) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 15px 25px;
            margin-bottom: 30px;
            gap: 20px;
            flex-wrap: wrap;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
        }
        
        /* Smooth Lightbox overrides */
        .lightbox-modal {
            display: flex !important;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: fixed;
            z-index: 9999;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(11, 15, 25, 0.95);
            backdrop-filter: blur(10px);
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
 
        .lightbox-modal.show {
            opacity: 1;
            pointer-events: auto;
        }
 
        .lightbox-content {
            margin: 0;
            max-width: 90%;
            max-height: 80vh;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
            transform: scale(0.95);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
 
        .lightbox-modal.show .lightbox-content {
            transform: scale(1);
        }
        
        .lightbox-close {
            position: absolute;
            top: 20px;
            right: 35px;
            color: #f3f4f6;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.2s;
        }
 
        .lightbox-close:hover {
            color: #6366f1;
        }
 
        .lightbox-caption {
            margin: 15px auto 0 auto;
            text-align: center;
            color: #cbd5e1;
            font-family: 'Space Grotesk', 'Noto Sans JP', sans-serif;
            font-size: 1.1rem;
        }
        
        .lang-switch-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .switch-label {
            font-family: 'Space Grotesk', 'Noto Sans JP', sans-serif;
            font-weight: 500;
            color: var(--text-muted);
            font-size: 0.95rem;
        }
        
        .lang-toggle-btn {
            display: flex;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 2px;
            cursor: pointer;
            user-select: none;
        }
        
        .toggle-option {
            padding: 6px 16px;
            border-radius: 18px;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.3s ease;
            color: var(--text-muted);
        }
        
        .toggle-option.active {
            background: var(--primary);
            color: #ffffff;
            box-shadow: 0 2px 8px var(--primary-glow);
        }
        
        /* Downloads Section */
        .downloads-container {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .downloads-label {
            font-family: 'Space Grotesk', 'Noto Sans JP', sans-serif;
            font-weight: 500;
            color: var(--text-muted);
            font-size: 0.95rem;
        }
        
        .download-buttons {
            display: flex;
            gap: 20px;
        }
        
        .download-group {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 4px 12px;
            border-radius: 8px;
        }
        
        .group-title {
            font-family: 'Space Grotesk', 'Noto Sans JP', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            color: #a5b4fc;
        }
        
        .download-btn {
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 4px;
            color: #c7d2fe;
            padding: 3px 8px;
            font-size: 0.8rem;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .download-btn:hover {
            background: var(--primary);
            color: #ffffff;
            border-color: transparent;
            box-shadow: 0 0 8px var(--primary-glow);
        }
        
        /* Navigation Tabs */
        .tabs-nav {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 15px;
        }
        
        .tab-btn {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 30px;
            color: var(--text-muted);
            padding: 12px 28px;
            font-family: 'Space Grotesk', 'Noto Sans JP', sans-serif;
            font-size: 1.05rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            outline: none;
        }
        
        .tab-btn:hover {
            background: rgba(255, 255, 255, 0.06);
            color: var(--text-color);
            border-color: var(--primary);
        }
        
        .tab-btn.active {
            background: linear-gradient(135deg, var(--primary) 0%, #6366f1 100%);
            color: #ffffff;
            border-color: transparent;
            box-shadow: 0 4px 15px var(--primary-glow);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
            animation: fadeIn 0.4s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Tab Document Rendering Layouts */
        .doc-view {
            background: rgba(17, 25, 40, 0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        
        .doc-view h2, .doc-view h3, .doc-view h4 {
            font-family: 'Space Grotesk', 'Noto Sans JP', sans-serif;
            color: #a5b4fc;
        }
        
        .doc-view h2 {
            font-size: 1.8rem;
            border-left: 4px solid var(--primary);
            padding-left: 12px;
            margin-top: 0;
            margin-bottom: 25px;
        }
        
        .doc-view h3 {
            font-size: 1.4rem;
            color: #c7d2fe;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 8px;
        }
        
        .doc-view h4 {
            font-size: 1.15rem;
            color: #e0e7ff;
            margin-top: 20px;
        }
        
        .doc-view table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            overflow: hidden;
        }
        
        .doc-view th, .doc-view td {
            padding: 12px 16px;
            border: 1px solid var(--border-color);
            text-align: left;
        }
        
        .doc-view th {
            background-color: rgba(99, 102, 241, 0.1);
            color: #a5b4fc;
            font-weight: 600;
        }
        
        .doc-view tr:nth-child(even) {
            background-color: rgba(255, 255, 255, 0.01);
        }
        
        .doc-view tr:hover {
            background-color: rgba(255, 255, 255, 0.04);
        }
        
        .doc-view ul, .doc-view ol {
            padding-left: 24px;
            margin-bottom: 20px;
        }
        
        .doc-view li {
            margin-bottom: 8px;
            line-height: 1.6;
        }
        
        /* Language Switching Engine Styling */
        body.lang-mode-ja .lang-en {
            display: none !important;
        }
        
        body.lang-mode-en .lang-ja {
            display: none !important;
        }
        
        /* Fixes for markdown-rendered images */
        .doc-view img {
            max-width: 100%;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            margin: 10px 0;
        }
        
        .doc-view .table-img {
            width: 120px;
            height: auto;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            display: block;
            margin: 0 auto;
        }
        
        .doc-view .table-img:hover {
            transform: translateY(-2px) scale(1.05);
            border-color: var(--primary);
            box-shadow: 0 0 10px var(--primary-glow);
        }
        
        /* Search container within active tabs */
        .tab-search-container {
            margin-bottom: 20px;
        }
    </style>
</head>
<body class="lang-mode-ja">
    <div class="container">
        
        <!-- Premium Bilingual Title Block -->
        <h1 class="title-gradient lang-ja">VPEP インタラクティブ分析ダッシュボード</h1>
        <h1 class="title-gradient lang-en">VPEP Interactive Analysis Dashboard</h1>
        <p class="subtitle lang-ja" style="text-align:center; margin-bottom: 30px;">ビデオ分析監査レポート、実験プロトコール、および比較実験ノートの統合</p>
        <p class="subtitle lang-en" style="text-align:center; margin-bottom: 30px;">Consolidation of Video Audit, SOP Protocol, and Compared Notebooks</p>
        
        <!-- Sticky Control Panel -->
        <div class="control-panel">
            <div class="lang-switch-container">
                <span class="switch-label">Language / 言語:</span>
                <div class="lang-toggle-btn" id="langToggle">
                    <span class="toggle-option active" data-lang="ja">日本語</span>
                    <span class="toggle-option" data-lang="en">EN</span>
                </div>
            </div>
            
            <div class="downloads-container">
                <span class="downloads-label">
                    <span class="lang-en">Downloads:</span>
                    <span class="lang-ja">ダウンロード:</span>
                </span>
                <div class="download-buttons">
                    <div class="download-group">
                        <span class="group-title">SOP:</span>
                        <a href="__JP_SOP_BASE__.pdf" class="download-btn lang-ja" download>PDF</a>
                        <a href="__JP_SOP_BASE__.docx" class="download-btn lang-ja" download>Word</a>
                        <a href="__EN_SOP_BASE__.pdf" class="download-btn lang-en" download>PDF</a>
                        <a href="__EN_SOP_BASE__.docx" class="download-btn lang-en" download>Word</a>
                    </div>
                    <div class="download-group">
                        <span class="group-title">
                            <span class="lang-en">Notebook:</span>
                            <span class="lang-ja">実験ノート:</span>
                        </span>
                        <a href="__JA_NOTEBOOK_BASE__.pdf" class="download-btn lang-ja" download>PDF</a>
                        <a href="__JA_NOTEBOOK_BASE__.docx" class="download-btn lang-ja" download>Word</a>
                        <a href="__EN_NOTEBOOK_BASE__.pdf" class="download-btn lang-en" download>PDF</a>
                        <a href="__EN_NOTEBOOK_BASE__.docx" class="download-btn lang-en" download>Word</a>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tabs Navigation -->
        <div class="tabs-nav">
            <button class="tab-btn active" data-tab="audit">
                <span class="lang-ja">監査レポート</span>
                <span class="lang-en">Audit Report</span>
            </button>
            <button class="tab-btn" data-tab="sop">
                <span class="lang-ja">SOPプロトコール</span>
                <span class="lang-en">SOP Protocol</span>
            </button>
            <button class="tab-btn" data-tab="notebook">
                <span class="lang-ja">実験ノート比較</span>
                <span class="lang-en">Compared Notebook</span>
            </button>
        </div>
        
        <!-- Tab: Audit Report -->
        <div id="audit" class="tab-content active">
            <div class="tab-search-container">
                <input type="text" class="search-input" placeholder="Search tables..." onkeyup="filterTable(this)">
            </div>
            
            <div class="lang-ja">
                __JA_CARDS__
            </div>
            
            <div class="lang-en">
                __EN_CARDS__
            </div>
            
        </div>
        
        <!-- Tab: SOP Protocol -->
        <div id="sop" class="tab-content">
            <div class="tab-search-container">
                <input type="text" class="search-input" placeholder="Search tables..." onkeyup="filterTable(this)">
            </div>
            
            <div class="doc-view lang-ja">
                __JP_SOP_HTML__
            </div>
            
            <div class="doc-view lang-en">
                __EN_SOP_HTML__
            </div>
        </div>
        
        <!-- Tab: Compared Notebook -->
        <div id="notebook" class="tab-content">
            <div class="tab-search-container">
                <input type="text" class="search-input" placeholder="Search tables..." onkeyup="filterTable(this)">
            </div>
            
            <div class="doc-view lang-ja">
                __JA_NOTEBOOK_HTML__
            </div>
            
            <div class="doc-view lang-en">
                __EN_NOTEBOOK_HTML__
            </div>
        </div>
 
    </div>
    
    <script>
        // Tab switching logic
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                btn.classList.add('active');
                const targetTab = btn.getAttribute('data-tab');
                document.getElementById(targetTab).classList.add('active');
            });
        });
        
        // Language switching logic
        const langToggle = document.getElementById('langToggle');
        const toggleOptions = langToggle.querySelectorAll('.toggle-option');
        
        function switchLanguage(lang) {
            document.body.className = ''; // clear all classes
            document.body.classList.add('lang-mode-' + lang);
            
            toggleOptions.forEach(opt => {
                if (opt.getAttribute('data-lang') === lang) {
                    opt.classList.add('active');
                } else {
                    opt.classList.remove('active');
                }
            });
            
            // Update document title
            if (lang === 'ja') {
                document.title = 'VPEP インタラクティブ analysis ダッシュボード';
            } else {
                document.title = 'VPEP Interactive Analysis Dashboard';
            }
 
            // Update placeholders
            const searchPlaceholders = {
                ja: "テーブル内の検索...",
                en: "Search tables..."
            };
            document.querySelectorAll('.search-input').forEach(input => {
                input.placeholder = searchPlaceholders[lang];
            });
        }
        
        toggleOptions.forEach(opt => {
            opt.addEventListener('click', () => {
                const targetLang = opt.getAttribute('data-lang');
                switchLanguage(targetLang);
            });
        });
        
        // Lightbox modal setup
        document.addEventListener('DOMContentLoaded', () => {
            const modal = document.createElement('div');
            modal.className = 'lightbox-modal';
            modal.innerHTML = `
                <span class="lightbox-close">&times;</span>
                <img class="lightbox-content" id="img-lightbox-src">
                <div class="lightbox-caption" id="img-lightbox-caption"></div>
            `;
            document.body.appendChild(modal);
 
            const modalImg = document.getElementById('img-lightbox-src');
            const captionText = document.getElementById('img-lightbox-caption');
            const closeBtn = modal.querySelector('.lightbox-close');
 
            // Attach listener to all table images dynamically (including the converted markdown ones)
            function setupLightboxListeners() {
                document.querySelectorAll('.table-img, .doc-view img').forEach(img => {
                    // Apply thumbnail style to markdown images pointing to keyframes
                    if (img.src.includes('annotated_keyframes') && !img.classList.contains('table-img')) {
                        img.classList.add('table-img');
                        if (!img.alt) {
                            const parts = img.src.split('/');
                            const filename = parts[parts.length - 1].replace('.jpg', '').replace(/_/g, ' ');
                            img.alt = filename;
                        }
                    }
                    
                    // Click listener for lightbox
                    img.addEventListener('click', () => {
                        modal.classList.add('show');
                        modalImg.src = img.src;
                        captionText.innerText = img.alt || "Keyframe View";
                    });
                });
            }
 
            setupLightboxListeners();
            
            closeBtn.addEventListener('click', () => {
                modal.classList.remove('show');
            });
 
            modal.addEventListener('click', (e) => {
                if (e.target === modal || e.target === closeBtn) {
                    modal.classList.remove('show');
                }
            });
 
            // Initialize default language (Japanese)
            switchLanguage('ja');
        });
        
        // Search filter logic for active tab
        function filterTable(inputElement) {
            const filter = inputElement.value.toLowerCase();
            const activeTab = document.querySelector('.tab-content.active');
            
            // Filter card elements or table rows
            const tables = activeTab.getElementsByTagName('table');
            for (let table of tables) {
                const tbody = table.getElementsByTagName('tbody')[0];
                if (!tbody) continue;
                const trs = tbody.getElementsByTagName('tr');
                for (let tr of trs) {
                    let found = false;
                    const tds = tr.getElementsByTagName('td');
                    for (let td of tds) {
                        if (td.innerText.toLowerCase().includes(filter)) {
                            found = true;
                            break;
                        }
                    }
                    tr.style.display = found ? "" : "none";
                }
            }
            
            // Also filter lists if any inside cards
            const lists = activeTab.getElementsByTagName('ul');
            for (let list of lists) {
                const lis = list.getElementsByTagName('li');
                for (let li of lis) {
                    if (li.innerText.toLowerCase().includes(filter)) {
                        li.style.display = "";
                    } else {
                        li.style.display = "none";
                    }
                }
            }
        }
    </script>
</body>
</html>
"""
    
    # Perform substitutions
    output_html = template.replace("__STYLE_BLOCK__", style_block)
    output_html = output_html.replace("__EN_CARDS__", "".join(en_cards))
    output_html = output_html.replace("__JA_CARDS__", "".join(ja_cards))
    output_html = output_html.replace("__EN_SOP_HTML__", en_sop_html)
    output_html = output_html.replace("__JP_SOP_HTML__", jp_sop_html)
    output_html = output_html.replace("__EN_NOTEBOOK_HTML__", en_notebook_html)
    output_html = output_html.replace("__JA_NOTEBOOK_HTML__", ja_notebook_html)
    
    # Replace basenames
    output_html = output_html.replace("__JP_SOP_BASE__", jp_sop_base)
    output_html = output_html.replace("__EN_SOP_BASE__", en_sop_base)
    output_html = output_html.replace("__JA_NOTEBOOK_BASE__", ja_notebook_base)
    output_html = output_html.replace("__EN_NOTEBOOK_BASE__", en_notebook_base)
    
    # Replace video filename
    output_html = output_html.replace("masked_tracking_video.mp4", args.video_filename)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_html_path)), exist_ok=True)
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(output_html)
    print(f"Unified Interactive Dashboard generated successfully: {output_html_path}")

if __name__ == "__main__":
    main()
