---
name: markitdown
description: "Convert files and Office documents into clean Markdown when you need LLM-friendly, token-efficient text (e.g., for summarization, search, RAG ingestion, or dataset preparation). Supports PDF, DOCX, PPTX, XLSX, images (with OCR), audio (with transcription), HTML, CSV, JSON, XML, ZIP, YouTube URLs, EPubs and more."
allowed-tools: [Read, Write, Edit, Bash]
license: MIT
skill-author: AIPOCH
source: https://github.com/microsoft/markitdown
---
```

## Overview

MarkItDown is a tool for converting various file formats into Markdown. It's particularly useful for preparing documents for LLMs, where token efficiency and structured text are important.

## When to Use

- Converting research papers or reports (PDF/DOCX/EPUB/HTML) into Markdown for LLM summarization, Q&A, or RAG indexing.
- Extracting tables and structured content from spreadsheets (XLSX/CSV) into Markdown for analysis or documentation.
- Turning slide decks (PPTX) into Markdown notes, including speaker notes and (optionally) AI-generated image descriptions.
- Processing images or scanned documents with OCR to obtain searchable, editable Markdown text.
- Transcribing audio (WAV/MP3) or pulling YouTube transcripts into Markdown for meeting notes, content analysis, or knowledge bases.

## Key Features

- Converts many formats to structured Markdown (PDF, DOCX, PPTX, XLSX, images, audio, HTML, CSV, JSON, XML, ZIP, EPUB, YouTube URLs, etc.).
- Produces token-efficient output suitable for LLM pipelines (summarization, chunking, embedding).
- OCR support for images/scans (when OCR dependencies are installed).
- Audio transcription support (when transcription dependencies are installed).
- Optional AI-enhanced image/slide descriptions via an OpenAI-compatible client (e.g., OpenRouter).
- Plugin system to extend format support and custom behaviors.
- Stream-based conversion API for large files.

## Supported Formats

| Format | Description | Notes |
|---|---|---|
| **PDF** | Portable Document Format | Full text extraction |
| **DOCX** | Microsoft Word | Tables, formatting preserved |
| **PPTX** | PowerPoint | Slides with notes |
| **XLSX** | Excel spreadsheets | Tables and data |
| **Images** | JPEG, PNG, GIF, WebP | EXIF metadata + OCR |
| **Audio** | WAV, MP3 | Metadata + transcription |
| **HTML** | Web pages | Clean conversion |
| **CSV** | Comma-separated values | Table format |
| **JSON** | JSON data | Structured representation |
| **XML** | XML documents | Structured format |
| **ZIP** | Archive files | Iterates contents |
| **EPUB** | E-books | Full text extraction |
| **YouTube** | Video URLs | Fetch transcriptions |

## Dependencies

- Python: `>=3.9` (recommended)
- Package: `markitdown[all]` (installs all optional format handlers)

Optional system dependencies (feature-dependent):
- Tesseract OCR: `tesseract-ocr` (for image/scanned-text OCR)

Optional external services (feature-dependent):
- Azure Document Intelligence endpoint (for enhanced PDF extraction)
- OpenAI-compatible LLM endpoint (e.g., OpenRouter) for AI image descriptions

## Installation

```bash
pip install 'markitdown[all]'
```

Control which file formats you support:

```bash
# Install specific formats
pip install 'markitdown[pdf, docx, pptx]'

# All available options:
# [all]                  - All optional dependencies
# [pptx]                 - PowerPoint files
# [docx]                 - Word documents
# [xlsx]                 - Excel spreadsheets
# [xls]                  - Older Excel files
# [pdf]                  - PDF documents
# [outlook]              - Outlook messages
# [az-doc-intel]         - Azure Document Intelligence
# [audio-transcription]  - WAV and MP3 transcription
# [youtube-transcription] - YouTube video transcription
```

## Example Usage

### CLI: Convert a PDF to Markdown

```bash
markitdown document.pdf -o output.md
```

### Python: Convert multiple formats (PDF/XLSX/PPTX/DOCX) and save outputs

```python
from pathlib import Path
from markitdown import MarkItDown

md = MarkItDown()

files = [
    "document.pdf",
    "spreadsheet.xlsx",
    "presentation.pptx",
    "notes.docx",
]

for path in files:
    result = md.convert(path)
    out = Path(path).with_suffix(".md")
    out.write_text(result.text_content, encoding="utf-8")
    print(f"Converted {path} -> {out}")
```

### Python: Stream conversion (useful for large files)

```python
from markitdown import MarkItDown

md = MarkItDown()

with open("large_file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")

with open("large_file.md", "w", encoding="utf-8") as out:
    out.write(result.text_content)
```

### Python: AI-enhanced image/slide descriptions (OpenAI-compatible, e.g., OpenRouter)

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_OPENROUTER_API_KEY",
    base_url="https://openrouter.ai/api/v1",
)

md = MarkItDown(
    llm_client=client,
    llm_model="anthropic/claude-opus-4.5",
    llm_prompt="Describe this image in detail for scientific documentation.",
)

result = md.convert("presentation.pptx")
print(result.text_content)
```

## Implementation Details

- **Conversion entry points**
  - `MarkItDown().convert(path)` converts a file by path/URL and returns an object whose primary payload is `result.text_content` (Markdown).
  - `MarkItDown().convert_stream(stream, file_extension=".pdf")` converts from a binary stream; use this for large files or when data is not on disk.

- **Format handling**
  - Format support is provided by optional extras (e.g., `pdf`, `docx`, `pptx`, `xlsx`, `audio-transcription`, `youtube-transcription`) or `all`.
  - ZIP inputs are typically processed by iterating through contained files and converting each supported entry.

- **OCR**
  - For images/scanned documents, OCR is enabled when OCR tooling is available (commonly Tesseract). Ensure the OS-level OCR binary is installed and accessible in `PATH`.

- **AI image descriptions**
  - When `llm_client`, `llm_model`, and `llm_prompt` are provided, MarkItDown can request model-generated descriptions for images (including slide images), then inject those descriptions into the Markdown output.
  - Any OpenAI-compatible client can be used (e.g., OpenRouter) by setting `base_url` and `api_key`.

- **Enhanced PDF extraction (Azure Document Intelligence)**
  - When configured with a Document Intelligence endpoint, PDF extraction can be improved for complex layouts (tables, multi-column text, scanned PDFs), producing more faithful Markdown structure.

- **Plugins**
  - Plugins can be listed and enabled from the CLI (e.g., `--list-plugins`, `--use-plugins`) to extend conversion behavior or add new format handlers.

## Best Practices

### 1. Choose the Right Conversion Method

- **Simple documents**: Use basic `MarkItDown()`
- **Complex PDFs**: Use Azure Document Intelligence
- **Visual content**: Enable AI image descriptions
- **Scanned documents**: Ensure OCR dependencies are installed

### 2. Handle Errors Gracefully

```python
from markitdown import MarkItDown

md = MarkItDown()

try:
    result = md.convert("document.pdf")
    print(result.text_content)
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Conversion error: {e}")
```

### 3. Process Large Files Efficiently

```python
from markitdown import MarkItDown

md = MarkItDown()

# For large files, use streaming
with open("large_file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
    
    # Process in chunks or save directly
    with open("output.md", "w") as out:
        out.write(result.text_content)
```

### 4. Optimize for Token Efficiency

Markdown output is already token-efficient, but you can:
- Remove excessive whitespace
- Consolidate similar sections
- Strip metadata if not needed

```python
from markitdown import MarkItDown
import re

md = MarkItDown()
result = md.convert("document.pdf")

# Clean up extra whitespace
clean_text = re.sub(r'\n{3,}', '\n\n', result.text_content)
clean_text = clean_text.strip()

print(clean_text)
```

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Install feature-specific packages
   ```bash
   pip install 'markitdown[pdf]'  # For PDF support
   ```

2. **Binary file errors**: Ensure files are opened in binary mode
   ```python
   with open("file.pdf", "rb") as f:  # Note the "rb"
       result = md.convert_stream(f, file_extension=".pdf")
   ```

3. **OCR not working**: Install tesseract
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu
   sudo apt-get install tesseract-ocr
   ```

## Performance Considerations

- **PDF files**: Large PDFs may take time; consider page ranges if supported
- **Image OCR**: OCR processing is CPU-intensive
- **Audio transcription**: Requires additional compute resources
- **AI image descriptions**: Requires API calls (costs may apply)

## Resources

- **MarkItDown GitHub**: https://github.com/microsoft/markitdown
- **PyPI**: https://pypi.org/project/markitdown/
- **OpenRouter**: https://openrouter.ai (for AI-enhanced conversions)
- **OpenRouter API Keys**: https://openrouter.ai/keys
- **OpenRouter Models**: https://openrouter.ai/models
- **Plugin Development**: See `packages/markitdown-sample-plugin`