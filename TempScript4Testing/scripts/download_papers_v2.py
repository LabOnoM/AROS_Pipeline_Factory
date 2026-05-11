
import os
import re
import time
import requests
import urllib3
import json
import glob
from bs4 import BeautifulSoup

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
INPUT_FILE = "Reference/list.md"
OUTPUT_DIR = "Reference/papers"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Timeout settings
TIMEOUT = 20

def setup_dirs():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def get_downloaded_ids():
    downloaded = set()
    if os.path.exists(OUTPUT_DIR):
        files = glob.glob(os.path.join(OUTPUT_DIR, "*.pdf"))
        
        for f in files:
            basename = os.path.basename(f)
            # Match {id}_{doi_slug}.pdf
            match = re.match(r'^(\d+)_', basename)
            if match:
                downloaded.add(match.group(1))
    return downloaded

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
                papers.append({"id": current_idx, "doi": raw_doi})
            else:
                 # TODO: Add title search if DOI is missing
                pass
    return papers

def download_file(url, filepath):
    headers = {"User-Agent": USER_AGENT}
    try:
        print(f"    Downloading from: {url[:60]}...")
        response = requests.get(url, headers=headers, stream=True, timeout=30, verify=False)
        content_type = response.headers.get('Content-Type', '').lower()
        
        # Accept text/html if we can verify it's a PDF later, but ideally application/pdf
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Validation
            size = os.path.getsize(filepath)
            if size > 1000:
                # Check magic bytes for PDF
                with open(filepath, 'rb') as f:
                    header = f.read(4)
                    if header == b'%PDF':
                        return True
                    else:
                        # Sometimes it might be HTML claiming strictly to be PDF?
                        # Or maybe we just downloaded a HTML page.
                        pass
                
                # If it's a reasonably large file, maybe it's valid?
                # But if header isn't %PDF, it's likely junk.
                # Let's keep strict check.
                if header != b'%PDF':
                    print("    File is not a valid PDF (header check failed).")
                    os.remove(filepath)
                    return False
                return True
            else:
                os.remove(filepath)
                return False
    except Exception as e:
        print(f"    Download error: {e}")
    return False

# --- STRATEGY C: Metadata Scraping (citation_pdf_url) ---
def try_landing_page_metadata(doi, filepath):
    url = f"https://doi.org/{doi}"
    headers = {"User-Agent": USER_AGENT}
    try:
        # Follow redirects to landing page
        response = requests.get(url, headers=headers, timeout=TIMEOUT, verify=False, allow_redirects=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # standard meta tag
            meta_pdf = soup.find('meta', attrs={'name': 'citation_pdf_url'})
            if meta_pdf and meta_pdf.get('content'):
                pdf_url = meta_pdf['content']
                print(f"    Found citation_pdf_url: {pdf_url}")
                return download_file(pdf_url, filepath)
                
            # sometimes: DC.identifier.URI or similar? Less reliable for direct PDF.
            
    except Exception as e:
        print(f"    Metadata scrape error: {e}")
    return False

# --- STRATEGY A: LibGen / SciMag ---
def try_libgen(doi, filepath):
    mirrors = [
        "https://libgen.is",
        "https://libgen.li",
        "https://libgen.rs"
    ]
    headers = {"User-Agent": USER_AGENT}
    
    for mirror in mirrors:
        try:
            # SciMag search pattern
            search_url = f"{mirror}/scimag/?q={doi}"
            resp = requests.get(search_url, headers=headers, timeout=TIMEOUT, verify=False)
            
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'html.parser')
                # LibGen scimag usually lists results. If direct hit, it might have 'get.php'
                
                # Look for links containing 'book/index.php' or 'scimag/get.php' assuming DOI match
                # Simple heuristic: Look for any link that looks like a detail page or download page
                links = soup.find_all('a', href=True)
                candidate_url = None
                
                for link in links:
                    href = link['href']
                    if 'sci-hub' in href: continue # Avoid sci-hub links if we want libgen specifically
                    
                    # Direct download link style
                    if 'get.php' in href or 'index.php?md5=' in href:
                         # Make absolute
                         if href.startswith('/'):
                             candidate_url = mirror + href
                             break
                         if href.startswith('http'):
                             candidate_url = href
                             break
                
                if candidate_url:
                     # Visit the download page to get the real PDF link
                     # Sometimes the candidate IS the download link (get.php)
                     print(f"    Found LibGen candidate: {candidate_url}")
                     if 'get.php' in candidate_url:
                         if download_file(candidate_url, filepath): return True
                     else:
                         # It's a detail page, visit it
                         d_resp = requests.get(candidate_url, headers=headers, timeout=TIMEOUT, verify=False)
                         d_soup = BeautifulSoup(d_resp.content, 'html.parser')
                         # Look for 'GET' or 'Cloudflare' links
                         dl_links = d_soup.find_all('a', href=True)
                         for dl in dl_links:
                             if dl.get_text().upper() == 'GET':
                                 dl_href = dl['href']
                                 if dl_href.startswith('/'): dl_href = mirror + dl_href
                                 if download_file(dl_href, filepath): return True
        except Exception:
            continue
    return False

# --- STRATEGY B: Anna's Archive ---
def try_annas_archive(doi, filepath):
    # Anna's archive search
    # https://annas-archive.org/search?q=DOI
    base_url = "https://annas-archive.org"
    search_url = f"{base_url}/search?q={doi}"
    headers = {"User-Agent": USER_AGENT}
    
    try:
        resp = requests.get(search_url, headers=headers, timeout=TIMEOUT, verify=False)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            # Find first result. Anna's structure changes, but usually main list items
            # Look for class potentially? Or just links to /md5/...
            
            # Heuristic: Find a link starting with /md5/ or /scidb/
            # Anna's usually has /md5/xxxxxxxx for books, /scidb/DOI for papers sometimes?
            # Let's look for result links.
            
            links = soup.find_all('a', href=True)
            detail_page = None
            for link in links:
                href = link['href']
                if href.startswith('/md5/') or href.startswith('/scidb/'):
                    detail_page = base_url + href
                    break
            
            if detail_page:
                # print(f"    Found Anna's detail page: {detail_page}")
                # Visit detail page
                d_resp = requests.get(detail_page, headers=headers, timeout=TIMEOUT, verify=False)
                d_soup = BeautifulSoup(d_resp.content, 'html.parser')
                
                # Look for download links. Usually robust list.
                # "Slow partner server #1", "Fast partner server #1" etc.
                # We can try to find 'douban' or 'libgen' external links, or the internal /slow_download/
                
                # Try finding any link that contains 'slow_download' (direct from Anna)
                # or external mirrors.
                
                down_links = d_soup.find_all('a', href=True)
                for dl in down_links:
                    dh = dl['href']
                    if '/slow_download/' in dh:
                         target = base_url + dh
                         if download_file(target, filepath): return True
                    # Check for external libgen links provided by Anna
                    if 'libgen' in dh and 'get.php' in dh:
                        if download_file(dh, filepath): return True
                        
    except Exception as e:
        # print(f"    Anna's Archive error: {e}")
        pass
    return False

def main():
    setup_dirs()
    papers = extract_metadata(INPUT_FILE)
    downloaded_ids = get_downloaded_ids()
    
    # Filter only missing
    missing_papers = [p for p in papers if p['id'] not in downloaded_ids]
    print(f"Total DOIs: {len(papers)}")
    print(f"Already downloaded: {len(downloaded_ids)}")
    print(f"To attempt: {len(missing_papers)}")
    
    success_count = 0
    
    for paper in missing_papers:
        pid = paper['id']
        doi = paper['doi']
        safe_doi = doi.replace('/', '_')
        filepath = os.path.join(OUTPUT_DIR, f"{pid}_{safe_doi}.pdf")
        
        print(f"[{pid}] Attempting DOI: {doi}")
        
        # 1. Strategy C (Metadata) - Cleanest, most legal-ish
        if try_landing_page_metadata(doi, filepath):
            print("  -> Success (Metadata)")
            success_count += 1
            continue
            
        # 2. Strategy A (LibGen)
        if try_libgen(doi, filepath):
            print("  -> Success (LibGen)")
            success_count += 1
            continue
            
        # 3. Strategy B (Anna's Archive)
        if try_annas_archive(doi, filepath):
            print("  -> Success (Anna's Archive)")
            success_count += 1
            continue
            
        print("  -> Failed all methods.")
        # Be polite between papers
        time.sleep(2)
        
    print(f"\nBatch complete. New successes: {success_count}")

if __name__ == "__main__":
    main()
