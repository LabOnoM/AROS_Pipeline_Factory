
import re

def extract_titles(file_path):
    titles = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Simple heuristic: Split by ". "
        # Expected format: Index. Authors. Title. Journal...
        parts = line.split('. ')
        
        if len(parts) >= 3:
            # Check if part 0 is a number (the index)
            try:
                int(parts[0])
                # Authors are parts[1]
                # Title is likely parts[2]
                # specific handling if title itself has ". " or if authors have middlenames with dots?
                # Usually abbreviations don't have spaces after them in this list? like "Yar FGM." no space? 
                # Let's look at "Bushar TS."
                
                title = parts[2]
                
                # Sanity check: if title is very short, maybe it was split incorrectly
                if len(title) < 5 and len(parts) > 3:
                     # Maybe title continued?
                     pass
                
                titles.append(title)
            except ValueError:
                # Line didn't start with a number, maybe continuation or different format
                pass
        else:
            # Handle edge cases
            pass
            
    return titles

if __name__ == "__main__":
    titles = extract_titles("Reference/list.md")
    for i, title in enumerate(titles):
        print(f"{i+1}: {title}")
