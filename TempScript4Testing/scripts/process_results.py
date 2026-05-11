
import json
import os
import requests
import time

def process_results(json_file):
    with open(json_file, 'r') as f:
        items = json.load(f)
        
    pdf_dir = "Reference/downloads/pdfs"
    abstract_dir = "Reference/downloads/abstracts"
    
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    if not os.path.exists(abstract_dir):
        os.makedirs(abstract_dir)
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
        
    for item in items:
        idx = item['id']
        title = item.get('title', 'Unknown Title')
        status = item.get('status')
        url = item.get('url')
        abstract = item.get('abstract')
        
        print(f"Processing Item {idx}: {title}")
        
        if status == 'pdf' and url:
            try:
                print(f"  Downloading PDF from {url}...")
                response = requests.get(url, headers=headers, timeout=30)
                if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', '').lower():
                    filename = os.path.join(pdf_dir, f"{idx}.pdf")
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"  Saved PDF to {filename}")
                else:
                    # sometimes content-type is binary or stream
                    if response.status_code == 200:
                         # heuristic: check magic bytes
                        if response.content.startswith(b'%PDF'):
                            filename = os.path.join(pdf_dir, f"{idx}.pdf")
                            with open(filename, 'wb') as f:
                                f.write(response.content)
                            print(f"  Saved PDF to {filename} (Magic bytes verified)")
                        else:
                            print(f"  Failed: Content-Type is {response.headers.get('Content-Type')}, not PDF.")
                    else:
                        print(f"  Failed to download PDF. Status Code: {response.status_code}")
            except Exception as e:
                print(f"  Error downloading PDF: {e}")
                
        elif status == 'abstract' and abstract:
            filename = os.path.join(abstract_dir, f"{idx}.txt")
            with open(filename, 'w') as f:
                f.write(f"Title: {title}\nURL: {url}\n\nAbstract:\n{abstract}")
            print(f"  Saved Abstract to {filename}")
        else:
            print("  No PDF or Abstract found.")
            
        time.sleep(1) # be nice

if __name__ == "__main__":
    process_results("Reference/batches/batch_01_results.json")
