
import os
import re
import time
import requests
import urllib3
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
INPUT_FILE = "Reference/list.md"
OUTPUT_DIR = "Reference/papers"
SCIHUB_BASE = "https://sci-hub.se" # For generating links for user

def setup_dirs():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def extract_metadata(file_path):
    papers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_idx = None
    doi_pattern = re.compile(r'(10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+)')

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        match_idx = re.match(r'^(\d+)\.', line)
        if match_idx:
            current_idx = match_idx.group(1)
            match_doi = doi_pattern.search(line)
            if match_doi:
                raw_doi = match_doi.group(1)
                if raw_doi.endswith('.'):
                    raw_doi = raw_doi[:-1]
                
                papers.append({
                    "id": current_idx,
                    "doi": raw_doi,
                    "original_line": line
                })
    return papers

def get_semantic_scholar_data(doi):
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
    params = {
        "fields": "title,openAccessPdf,url,externalIds"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 429:
            print("    Rate limited by Semantic Scholar. Waiting 60s...")
            time.sleep(60)
            return get_semantic_scholar_data(doi)
    except Exception as e:
        print(f"    Error querying Semantic Scholar: {e}")
    return None

def download_file(url, filepath):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    try:
        # Some PDF URLs might need redirects, etc.
        response = requests.get(url, headers=headers, stream=True, timeout=30, verify=False)
        content_type = response.headers.get('Content-Type', '').lower()
        
        if response.status_code == 200:
            # Check content type if possible, but some don't report correctly.
            # Start writing
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            if os.path.getsize(filepath) > 1000:
                return True
            else:
                os.remove(filepath)
                return False
    except Exception as e:
        print(f"    Error downloading PDF: {e}")
    return False

def main():
    setup_dirs()
    papers = extract_metadata(INPUT_FILE)
    print(f"Found {len(papers)} papers with DOIs.")
    
    report = []
    
    for paper in papers:
        paper_id = paper['id']
        doi = paper['doi']
        safe_doi = doi.replace('/', '_')
        filename = f"{paper_id}_{safe_doi}.pdf"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(filepath):
            print(f"[{paper_id}] Already exists: {doi}")
            report.append({"id": paper_id, "doi": doi, "status": "exists", "filepath": filepath})
            continue
            
        print(f"[{paper_id}] Checking DOI: {doi}")
        success = False
        
        # 1. Semantic Scholar
        data = get_semantic_scholar_data(doi)
        if data and data.get('openAccessPdf'):
            oa_url = data['openAccessPdf'].get('url')
            if oa_url:
                print(f"  -> Found OA PDF: {oa_url}")
                if download_file(oa_url, filepath):
                    print(f"  -> Downloaded!")
                    success = True
                    report.append({"id": paper_id, "doi": doi, "status": "downloaded_oa", "url": oa_url})
        
        if not success:
            print(f"  -> No OA link found or download failed.")
            report.append({"id": paper_id, "doi": doi, "status": "missing_oa"})
            
        time.sleep(3) # Rate limit protection
        
    # Generate backup script for missed papers
    missing = [p for p in report if p['status'] == 'missing_oa']
    if missing:
        print(f"\nGenerating manual download script for {len(missing)} papers...")
        with open("download_missing.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("# Script to download missing papers via Sci-Hub (requires User interaction or working connection)\n\n")
            for item in missing:
                doi = item['doi']
                pid = item['id']
                # Just open the browser or echo the link
                # Using 'open' on Mac
                url = f"{SCIHUB_BASE}/{doi}"
                f.write(f"echo 'Opening {pid}: {url}'\n")
                f.write(f"open '{url}'\n")
                f.write("sleep 2\n")
        
        # Also JSON report
        with open("download_report.json", "w") as f:
            json.dump(report, f, indent=2)

if __name__ == "__main__":
    main()
