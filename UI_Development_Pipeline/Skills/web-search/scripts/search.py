# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "duckduckgo-search>=6.0.0",
#     "beautifulsoup4>=4.12.0",
#     "requests>=2.31.0"
# ]
# ///
import argparse
import json
import sys
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

def main():
    parser = argparse.ArgumentParser(description="Web Search / Extract CLI")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--extract", metavar="URL", help="Extract URL")
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--depth", default="basic")
    parser.add_argument("--topic", default="general")
    parser.add_argument("--days", type=int)
    parser.add_argument("--raw-content", action="store_true")
    parser.add_argument("--json", action="store_true")
    
    args, unknown = parser.parse_known_args()
    
    if args.extract:
        try:
            resp = requests.get(args.extract, timeout=15)
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            print(f"# {args.extract}\n\n{text[:10000]}")
        except Exception as e:
            print(f"Extract failed: {e}", file=sys.stderr)
            sys.exit(2)
        return
        
    if args.query:
        try:
            results = []
            with DDGS() as ddgs:
                if args.topic == "news":
                    for r in ddgs.news(args.query, max_results=args.max_results):
                        results.append(r)
                else:
                    for r in ddgs.text(args.query, max_results=args.max_results):
                        results.append(r)
                        
            out = {"results": []}
            for idx, r in enumerate(results, 1):
                title = r.get("title", "")
                url = r.get("url", r.get("href", ""))
                body = r.get("body", r.get("description", ""))
                out["results"].append({"title": title, "url": url, "content": body})
            
            if args.json:
                print(json.dumps(out, indent=2))
            else:
                lines = ["RESULTS:"]
                for i, r in enumerate(out["results"], 1):
                    lines.append(f"[{i}] {r['title']}\n    {r['url']}\n    {r['content']}\n")
                print("\n".join(lines))
        except Exception as e:
            print(f"Search failed: {e}", file=sys.stderr)
            sys.exit(2)
        
if __name__ == "__main__":
    main()
