
import requests
import json
import time
import os
import re

def search_paper(query):
    # API key is not strictly required for low volume, but let's be careful.
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": 1,
        "fields": "title,abstract,url,openAccessPdf"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        # print(f"DEBUG: Searching '{query}' -> {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data['total'] > 0 and data['data']:
                return data['data'][0]
    except Exception as e:
        print(f"Error searching for {query[:20]}...: {e}")
    return None

def process_batch(batch_file):
    results = []
    with open(batch_file, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        print(f"Processing: {line[:60]}...")
        
        # Extract ID
        match = re.match(r'^(\d+)\.', line)
        paper_id = int(match.group(1)) if match else 0
        
        # Heuristics to find the title
        # Remove index
        cleaned_line = re.sub(r'^\d+\.\s*', '', line)
        
        # Split by ". "
        parts = cleaned_line.split('. ')
        
        candidates = []
        
        # Candidate 1: 2nd part (Index removed -> Part 0 is Authors, Part 1 is Title)
        # "Allchin R... . The Archaeology..." -> ["Allchin...", "The Archaeology...", "Edinburgh..."]
        if len(parts) > 1:
            candidates.append(parts[1])
            
        # Candidate 2: Full line (sometimes works)
        candidates.append(cleaned_line)

        # Candidate 3: Part 0 (Maybe no authors?)
        candidates.append(parts[0])
        
        paper_data = None
        for query in candidates:
            query = query.strip()
            # Remove trailing dot or colon
            query = query.rstrip('.:')
                
            if len(query) < 5: 
                continue
                
            # print(f"  Trying query: {query}")
            paper_data = search_paper(query)
            if paper_data:
                # Basic validation: check if title similarity is plausible?
                # For now, if we get a hit, we assume it's good.
                break
        
        if paper_data:
            print(f"  Found: {paper_data['title']}")
            results.append({
                "id": paper_id,
                "title": paper_data['title'],
                "status": "found",
                "abstract": paper_data.get('abstract'),
                "url": paper_data.get('url'),
                "pdf_url": paper_data.get('openAccessPdf', {}).get('url') if paper_data.get('openAccessPdf') else None,
                "found": True
            })
        else:
            print("  Not found.")
            results.append({
                "id": paper_id,
                "title": parts[1] if len(parts)>1 else cleaned_line,
                "status": "not_found",
                "abstract": None,
                "url": None,
                "pdf_url": None,
                "found": False
            })
            
        time.sleep(1) 
        
    return results

if __name__ == "__main__":
    batch_file = "Reference/batches/batch_02.txt"
    json_output = "Reference/batches/batch_02_api_results.json"
    
    results = process_batch(batch_file)
    
    with open(json_output, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Saved results to {json_output}")
