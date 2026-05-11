#!/usr/bin/env python3
"""
e-Rad Character Counter — Calibrated Tool for JSPS KAKENHI Web Forms
=====================================================================

Counts characters exactly as the e-Rad electronic application system does.

Counting rules (calibrated 2026-05-11 against live e-Rad screenshots):
  - Each VISIBLE character counts as **1 文字** regardless of byte width
    (both full-width 全角 and half-width 半角 count as 1).
  - Line feeds (\\n) are **NOT** counted toward the character total,
    but each form field has a separate maximum number of allowed line feeds.
  - Carriage returns (\\r) are stripped and ignored.

NOTE: The e-Rad UI displays a "byte explanation" (全角=2bytes, 半角=1byte,
改行=2bytes) — this describes internal database storage, NOT the displayed
character count. The "入力文字数" displayed on screen equals the count of
visible characters as defined above.

JIS X0208 validation:
  The e-Rad system only accepts characters within the JIS X0208 standard.
  Characters outside this standard (e.g., em-dash U+2014, smart quotes)
  are silently converted to &#xxxx; HTML entities, triggering a warning.
  This tool validates and flags non-JIS characters with safe replacements.

Field limits (F-19-1 — visible character count):
  研究成果の概要（和文）:           max  300 chars, max 2 line feeds
  研究成果の概要（英文）:           max 1000 chars, max 2 line feeds
  研究成果の学術的意義や社会的意義: max  300 chars, max 2 line feeds

Field limits (F-7 — byte-based count):
  研究実績の概要 (F-7-1/F-7-2):   max  800 chars (1600 bytes), max 5 line feeds
                                    WARNING threshold: >=1200 bytes
  次年度使用額が生じた理由と使用計画: max  600 chars (1200 bytes), max 3 line feeds
  ホームページ等 タイトル:         max   50 chars per entry
  ホームページ等 備考:              max  200 chars (400 bytes), max 2 line feeds

Usage:
  python3 erad_char_count.py "your text here"
  python3 erad_char_count.py --file path/to/file.md --section "研究成果の学術的意義"
  python3 erad_char_count.py --file path/to/file.md --check-jis
  python3 erad_char_count.py --byte-mode "F-7 text"   # Use byte-based counting for F-7 fields
"""

import sys
import re
import argparse
import unicodedata


def erad_char_count(text: str) -> int:
    """Count visible characters in text using e-Rad rules.
    
    Each visible character = 1.
    Line feeds are excluded from the count.
    """
    clean = text.replace('\r\n', '\n').replace('\r', '')
    return len(clean.replace('\n', ''))


def erad_byte_count(text: str) -> int:
    """Count bytes in text using e-Rad F-7 rules.
    
    全角 (full-width) = 2 bytes, 半角 (half-width) = 1 byte, 改行 (LF) = 2 bytes.
    This is the counting method used by e-Rad for F-7 研究実績の概要 and
    次年度使用額 fields (as opposed to the visible-character count used for F-19-1).
    """
    clean = text.replace('\r\n', '\n').replace('\r', '')
    byte_count = 0
    for ch in clean:
        if ch == '\n':
            byte_count += 2
        elif ord(ch) < 128:
            byte_count += 1
        else:
            byte_count += 2
    return byte_count


def erad_line_feed_count(text: str) -> int:
    """Count line feeds in text."""
    clean = text.replace('\r\n', '\n').replace('\r', '')
    return clean.count('\n')


# ── Common non-JIS X0208 characters and their safe replacements ──
_JIS_REPLACEMENTS = {
    '\u2014': ' - ',   # EM DASH → spaced hyphen
    '\u2013': '-',     # EN DASH → hyphen
    '\u2012': '-',     # FIGURE DASH → hyphen
    '\u2010': '-',     # HYPHEN → ASCII hyphen
    '\u2011': '-',     # NON-BREAKING HYPHEN → ASCII hyphen
    '\u2018': "'",     # LEFT SINGLE QUOTATION MARK → apostrophe
    '\u2019': "'",     # RIGHT SINGLE QUOTATION MARK → apostrophe
    '\u201C': '"',     # LEFT DOUBLE QUOTATION MARK → ASCII double quote
    '\u201D': '"',     # RIGHT DOUBLE QUOTATION MARK → ASCII double quote
    '\u2026': '...',   # HORIZONTAL ELLIPSIS → three dots
    '\u00A0': ' ',     # NO-BREAK SPACE → regular space
    '\u2002': ' ',     # EN SPACE → regular space
    '\u2003': ' ',     # EM SPACE → regular space
    '\u200B': '',      # ZERO WIDTH SPACE → remove
    '\uFEFF': '',      # BOM → remove
}


def check_jis_x0208(text: str) -> list:
    """Check for characters NOT in JIS X0208.
    
    The e-Rad system only accepts JIS X0208 characters.
    Non-JIS chars get silently converted to &#xxxx; HTML entities.
    
    Uses Shift_JIS encoding as a proxy for JIS X0208 membership.
    
    Returns a list of (position, char, unicode_name, suggested_fix) tuples.
    """
    problems = []
    for i, ch in enumerate(text):
        if ch in ('\n', '\r'):
            continue
        try:
            ch.encode('shift_jis')
        except (UnicodeEncodeError, UnicodeDecodeError):
            name = unicodedata.name(ch, f'U+{ord(ch):04X}')
            fix = _JIS_REPLACEMENTS.get(ch, f'[remove or replace U+{ord(ch):04X}]')
            problems.append((i, ch, name, fix))
    return problems


def sanitize_for_erad(text: str) -> str:
    """Replace known non-JIS X0208 characters with safe alternatives.
    
    Returns the sanitized text.
    """
    result = text
    for bad_char, replacement in _JIS_REPLACEMENTS.items():
        result = result.replace(bad_char, replacement)
    return result


def extract_section(filepath: str, section_header: str) -> str:
    """Extract the content of a markdown section from a file.
    
    Reads from the line matching `section_header` until the next
    section header (## ■) or end of file.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_section = False
    section_lines = []
    
    for line in lines:
        if section_header in line:
            in_section = True
            continue
        if in_section:
            # Stop at the next section header
            if line.strip().startswith('## ■') or line.strip() == '---':
                break
            section_lines.append(line)
    
    # Strip leading/trailing blank lines and HTML/markdown comments
    content = ''.join(section_lines).strip()
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL).strip()
    return content


def main():
    parser = argparse.ArgumentParser(
        description='e-Rad Character Counter (calibrated for JSPS KAKENHI)')
    parser.add_argument('text', nargs='?', default=None,
                        help='Text to count (inline)')
    parser.add_argument('--file', '-f', default=None,
                        help='Path to a markdown file')
    parser.add_argument('--section', '-s', default=None,
                        help='Section header to extract from the file')
    parser.add_argument('--limit', '-l', type=int, default=None,
                        help='Character limit to check against')
    parser.add_argument('--max-lf', type=int, default=None,
                        help='Maximum allowed line feeds')
    parser.add_argument('--check-jis', action='store_true',
                        help='Check for non-JIS X0208 characters')
    parser.add_argument('--sanitize', action='store_true',
                        help='Print sanitized text with non-JIS chars replaced')
    parser.add_argument('--byte-mode', action='store_true',
                        help='Use byte-based counting for F-7 fields (全角=2, 半角=1, 改行=2)')
    parser.add_argument('--byte-limit', type=int, default=None,
                        help='Byte limit for --byte-mode (e.g., 1600 for F-7, 1200 for carryover)')
    parser.add_argument('--byte-warn', type=int, default=None,
                        help='Byte warning threshold (e.g., 1200 for F-7 — below triggers e-Rad warning)')
    args = parser.parse_args()
    
    if args.file and args.section:
        text = extract_section(args.file, args.section)
        source = f'{args.file} → section "{args.section}"'
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        source = args.file
    elif args.text:
        text = args.text
        source = '(inline)'
    else:
        text = sys.stdin.read().strip()
        source = '(stdin)'
    
    char_count = erad_char_count(text)
    lf_count = erad_line_feed_count(text)
    
    print(f'Source:          {source}')
    print(f'Character count: {char_count} 文字')
    print(f'Line feeds:      {lf_count}')
    
    if args.limit:
        delta = char_count - args.limit
        if delta > 0:
            print(f'Limit:           {args.limit} 文字')
            print(f'⚠️  OVER BY:      {delta} chars — must shorten!')
        else:
            print(f'Limit:           {args.limit} 文字')
            print(f'✅ Within limit  ({abs(delta)} chars remaining)')
    
    if args.max_lf is not None:
        if lf_count > args.max_lf:
            print(f'⚠️  Too many line feeds: {lf_count} > {args.max_lf}')
        else:
            print(f'✅ Line feeds OK ({lf_count} ≤ {args.max_lf})')
    
    # JIS X0208 validation (always runs)
    jis_problems = check_jis_x0208(text)
    if jis_problems:
        print(f'⚠️  JIS X0208:    {len(jis_problems)} non-JIS character(s) found!')
        print(f'   These will be converted to &#xxxx; by e-Rad.')
        for pos, ch, name, fix in jis_problems:
            print(f'   Position {pos}: "{ch}" ({name}) → replace with: {fix}')
    else:
        print(f'✅ JIS X0208 OK  (all characters are e-Rad safe)')
    
    if args.sanitize:
        sanitized = sanitize_for_erad(text)
        print(f'\n--- Sanitized text ---')
        print(sanitized)
        print(f'--- End ---')
        new_count = erad_char_count(sanitized)
        print(f'Sanitized count: {new_count} 文字')
    
    # Byte-mode counting for F-7 fields
    if args.byte_mode:
        byte_count = erad_byte_count(text)
        print(f'\n--- Byte Mode (F-7 rules: 全角=2, 半角=1, 改行=2) ---')
        print(f'Byte count:      {byte_count} バイト')
        if args.byte_limit:
            delta = byte_count - args.byte_limit
            if delta > 0:
                print(f'Byte limit:      {args.byte_limit} バイト')
                print(f'\u26a0\ufe0f  OVER BY:      {delta} bytes \u2014 must shorten!')
            else:
                print(f'Byte limit:      {args.byte_limit} バイト')
                print(f'\u2705 Within limit  ({abs(delta)} bytes remaining)')
        if args.byte_warn:
            if byte_count < args.byte_warn:
                print(f'\u26a0\ufe0f  WARNING:     {byte_count} < {args.byte_warn} bytes \u2014 e-Rad will display a warning!')
                print(f'   Recommendation: expand text to \u2265{args.byte_warn} bytes.')
            else:
                print(f'\u2705 Warning OK   ({byte_count} \u2265 {args.byte_warn} bytes)')


if __name__ == '__main__':
    main()
