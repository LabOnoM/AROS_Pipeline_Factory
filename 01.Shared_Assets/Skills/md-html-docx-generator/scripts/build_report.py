#!/usr/bin/env python3
import os
import re
import sys
import base64
import argparse
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

try:
    import google.generativeai as genai
    from google.generativeai.types import GenerationConfig
except ImportError:
    print("Error: google-generativeai is not installed. Please install it with 'pip install google-generativeai'.")
    sys.exit(1)


@dataclass
class Section:
    index: int
    title: str
    markdown_body: str
    html_content: str = ""
    anchor: str = ""

def resolve_api_key(args_key: Optional[str] = None) -> str:
    """Portable 4-tier API key resolution chain."""
    if args_key:
        return args_key
    
    key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    try:
        from dotenv import load_dotenv
    except ImportError:
        def load_dotenv(*args, **kwargs): pass
        
    for start_dir in [Path.cwd(), Path(__file__).resolve().parent]:
        d = start_dir
        for _ in range(6):
            env_path = d / ".env"
            if env_path.exists():
                load_dotenv(dotenv_path=env_path, override=False)
                key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GEMINI_API_KEY")
                if key:
                    return key
            if d.parent == d:
                break
            d = d.parent
            
    aros_env = Path.home() / ".gemini" / ".env"
    if aros_env.exists():
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=aros_env, override=False)
        key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if key:
            return key
            
    raise EnvironmentError(
        "No API key found. Set GOOGLE_AI_API_KEY via:\n"
        "  1. CLI: --api-key YOUR_KEY\n"
        "  2. Environment: export GOOGLE_AI_API_KEY=YOUR_KEY\n"
        "  3. File: Add to ~/.gemini/.env"
    )

def encode_images_in_markdown(md_content: str, base_dir: Path) -> str:
    """Replaces local image paths in markdown with base64 data URIs."""
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    
    def replace_image(match):
        alt_text = match.group(1)
        img_path_str = match.group(2).strip()
        
        if img_path_str.startswith(("http://", "https://", "data:")):
            return match.group(0)
            
        img_path = base_dir / img_path_str
        if not img_path.is_absolute():
            img_path = (base_dir / img_path_str).resolve()
            
        if img_path.exists() and img_path.is_file():
            ext = img_path.suffix.lower().lstrip(".")
            mime_type = "image/png"
            if ext in ["jpg", "jpeg"]: mime_type = "image/jpeg"
            elif ext == "svg": mime_type = "image/svg+xml"
            elif ext == "gif": mime_type = "image/gif"
            
            try:
                with open(img_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                data_uri = f"data:{mime_type};base64,{encoded}"
                return f"![{alt_text}]({data_uri})"
            except Exception as e:
                print(f"Warning: Could not encode image {img_path}: {e}")
                
        return match.group(0)

    return img_pattern.sub(replace_image, md_content)


def parse_markdown(md_path: Path) -> tuple[dict, List[Section]]:
    """Parse markdown file into metadata and sections separated by ## headers."""
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    metadata = {
        "TITLE": md_path.stem.replace("_", " ").title(),
        "AUTHOR": "",
        "DATE": ""
    }
    
    # Very basic YAML frontmatter parsing
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            content = parts[2]
            for line in frontmatter.strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip().upper()
                    if k in metadata:
                        metadata[k] = v.strip().strip("'\"")
                        
    # Try to find an H1 title if not in metadata
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match and metadata["TITLE"] == md_path.stem.replace("_", " ").title():
        metadata["TITLE"] = h1_match.group(1).strip()
        
    # Pre-process local images to base64 so LLM doesn't have to invent paths
    content = encode_images_in_markdown(content, md_path.parent)

    sections = []
    # Split by ## (but not ###)
    # Using a lookahead to keep the delimiter
    parts = re.split(r'(^##\s+.*?$)', content, flags=re.MULTILINE)
    
    current_title = "Introduction"
    current_body = []
    section_idx = 0
    
    # Handle the case where the doc doesn't start with an H2
    if parts and parts[0].strip():
        # First part is intro
        sections.append(Section(
            index=section_idx,
            title="Introduction",
            markdown_body=parts[0].strip(),
            anchor="section-0"
        ))
        section_idx += 1
        
    for i in range(1, len(parts), 2):
        title_line = parts[i]
        body = parts[i+1] if i+1 < len(parts) else ""
        
        # Clean up title
        title = title_line.replace("##", "").strip()
        
        anchor = f"section-{section_idx}-{re.sub(r'[^a-z0-9]', '-', title.lower())}"
        
        sections.append(Section(
            index=section_idx,
            title=title,
            markdown_body=f"{title_line}\n{body}".strip(),
            anchor=anchor
        ))
        section_idx += 1
        
    # If no sections were found (no H2s), just make one big section
    if not sections:
        sections.append(Section(
            index=0,
            title="Content",
            markdown_body=content.strip(),
            anchor="section-0"
        ))
        
    return metadata, sections

def render_section_html(section: Section, model_name: str) -> str:
    """Uses LLM to convert a markdown section to styled HTML."""
    prompt = f"""You are an expert web developer and technical writer. 
Convert the following Markdown section into high-fidelity semantic HTML5.
    
DESIGN SYSTEM CSS CLASSES AVAILABLE (Use these generously!):
- .table-container (wrap all <table> elements in this)
- .alert, .alert-note, .alert-tip, .alert-warning, .alert-caution (Use for blockquotes or callouts. Format: <div class="alert alert-note"><div class="alert-title">Note</div><p>...</p></div>)
- <table>, <thead>, <tbody>, <th>, <td>, <tr> (Use standard semantic tags)
- <figure>, <figcaption> (Use for images)
- <pre>, <code> (Use for code blocks)

INSTRUCTIONS:
1. Return ONLY valid HTML. No markdown code blocks (```html). No <head> or <body> tags. Just the HTML content.
2. Ensure the top-level heading in this section is an <h2 id="{section.anchor}">{section.title}</h2>.
3. Convert all sub-headings correctly (### to <h3>, #### to <h4>).
4. If there are data tables, wrap them in <div class="table-container">.
5. If there are images, wrap them in <figure> and add a <figcaption> if text is provided. The images are already base64 encoded.
6. Make the output clean and professional.

MARKDOWN CONTENT TO CONVERT:
{section.markdown_body}
"""

    model = genai.GenerativeModel(model_name)
    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(temperature=0.1)
    )
    
    html = response.text.strip()
    if html.startswith("```html"):
        html = html[7:]
    if html.endswith("```"):
        html = html[:-3]
        
    return html.strip()

def assemble_report(metadata: dict, sections: List[Section], templates_dir: Path, output_path: Path, template_path: Optional[Path] = None):
    """Combines CSS, Shell HTML, and generated sections into a single file."""
    css_path = templates_dir / "scientific_report.css"
    shell_path = template_path if template_path else templates_dir / "report_shell.html"
    
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
        
    with open(shell_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Generate TOC
    toc_html = []
    for s in sections:
        toc_html.append(f'<li><a href="#{s.anchor}">{s.title}</a></li>')
    toc_str = "\n".join(toc_html)
    
    # Generate Body
    body_str = "\n\n".join([s.html_content for s in sections])
    
    # Replace templates
    html = html.replace("{{TITLE}}", metadata["TITLE"])
    html = html.replace("{{AUTHOR}}", metadata.get("AUTHOR", ""))
    html = html.replace("{{DATE}}", metadata.get("DATE", ""))
    html = html.replace("{{CSS}}", css)
    html = html.replace("{{TOC}}", toc_str)
    
    # Handle Handlebars style conditional replacement for empty fields
    if not metadata.get("AUTHOR"):
        html = re.sub(r'\{\{#if AUTHOR\}\}.*?\{\{/if\}\}', '', html, flags=re.DOTALL)
    else:
        html = html.replace("{{#if AUTHOR}}", "").replace("{{/if}}", "")
        
    if not metadata.get("DATE"):
        html = re.sub(r'\{\{#if DATE\}\}.*?\{\{/if\}\}', '', html, flags=re.DOTALL)
    else:
        html = html.replace("{{#if DATE}}", "").replace("{{/if}}", "")

    html = html.replace("{{BODY}}", body_str)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"✅ Successfully wrote HTML report to: {output_path}")

def export_docx(input_html: Path):
    """Exports HTML to DOCX using Pandoc."""
    output_docx = input_html.with_suffix(".docx")
    try:
        print(f"Exporting to DOCX via Pandoc: {output_docx}")
        subprocess.run(
            ["pandoc", str(input_html), "-o", str(output_docx)],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ Successfully wrote DOCX report to: {output_docx}")
    except FileNotFoundError:
        print("❌ Error: Pandoc not found. Please install pandoc to enable --docx export.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Pandoc error: {e.stderr}")

def main():
    parser = argparse.ArgumentParser(description="Generate high-fidelity HTML/DOCX reports from Markdown.")
    parser.add_argument("input_md", type=str, help="Path to input Markdown file")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to output HTML file")
    parser.add_argument("--docx", action="store_true", help="Also export a DOCX version via Pandoc")
    parser.add_argument("--api-key", type=str, help="Explicit API key (overrides env vars)")
    parser.add_argument("--model", type=str, default="gemini-2.5-flash", help="Gemini model to use")
    parser.add_argument("--template", type=str, help="Optional path to a custom HTML template shell")
    
    args = parser.parse_args()
    
    input_path = Path(args.input_md)
    output_path = Path(args.output)
    templates_dir = Path(__file__).resolve().parent.parent / "templates"
    
    if not input_path.exists():
        print(f"❌ Error: Input file {input_path} not found.")
        sys.exit(1)
        
    # 1. Setup API
    try:
        api_key = resolve_api_key(args.api_key)
        genai.configure(api_key=api_key)
    except EnvironmentError as e:
        print(f"❌ {e}")
        sys.exit(1)
        
    # 2. Parse Markdown
    print(f"Parsing markdown from {input_path}...")
    metadata, sections = parse_markdown(input_path)
    print(f"Found {len(sections)} sections.")
    
    # 3. Render Sections (Iterative LLM calls)
    print(f"Rendering sections via {args.model}...")
    for i, section in enumerate(sections):
        print(f"  [{i+1}/{len(sections)}] Rendering section: '{section.title}'...")
        try:
            section.html_content = render_section_html(section, args.model)
        except Exception as e:
            print(f"❌ Error rendering section '{section.title}': {e}")
            sys.exit(1)
            
    # 4. Assemble HTML
    template_path = Path(args.template) if args.template else None
    assemble_report(metadata, sections, templates_dir, output_path, template_path=template_path)
    
    # 5. Optional DOCX Export
    if args.docx:
        export_docx(output_path)

if __name__ == "__main__":
    main()
