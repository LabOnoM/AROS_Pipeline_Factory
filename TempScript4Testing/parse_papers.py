import re
import json

def parse_list(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Lines look like: 1. Author. Title. Journal...
    # We'll split by double newline or matching the number pattern.
    
    entries = []
    lines = content.split('\n')
    current_entry = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line starts with a number and a dot (e.g., "1. ")
        if re.match(r'^\d+\.', line):
            if current_entry:
                entries.append(current_entry)
            current_entry = line
        else:
            current_entry += " " + line
            
    if current_entry:
        entries.append(current_entry)
        
    papers = []
    for entry in entries:
        # Simple extraction
        # Try to split by the first dot to get index
        parts = entry.split('. ', 1)
        if len(parts) < 2:
            continue
            
        index = parts[0]
        rest = parts[1]
        
        # Heuristic: Title often ends with a dot, usually after authors. 
        # Authors are usually at the start.
        # But the format varies.  "Yar FGM, ZAHID S... . Title. Journal..."
        # Let's just save the full string and a cleaned query string for now.
        
        papers.append({
            "id": index,
            "full_text": entry,
            "query": rest # Text without the index
        })
        
    return papers

papers = parse_list('Reference/list.md')
with open('Reference/papers_to_download.json', 'w') as f:
    json.dump(papers, f, indent=2)

print(f"Parsed {len(papers)} papers.")
