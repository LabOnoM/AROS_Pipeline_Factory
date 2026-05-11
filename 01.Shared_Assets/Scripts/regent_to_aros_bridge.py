#!/usr/bin/env python3
import json
import subprocess
import sys
import os
import argparse

def extract_regent_session():
    """Extracts the latest session from re_gent."""
    try:
        # rgt log --limit 1 --conversation-only --json
        result = subprocess.run(
            ["rgt", "log", "--limit", "1", "--conversation-only", "--json"], 
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute rgt log: {e.stderr}")
        return None
    except json.JSONDecodeError:
        print("Failed to parse rgt JSON output.")
        return None
    except FileNotFoundError:
        print("rgt binary not found in PATH.")
        return None

def ingest_to_aros(session_data):
    """Ingests the extracted session data into AROS brain."""
    if not session_data or not isinstance(session_data, list) or len(session_data) == 0:
        print("No valid session data found to ingest.")
        return False
    
    latest_step = session_data[0]
    step_hash = latest_step.get("hash", "unknown")
    
    # Inject AROS root into path
    AROS_ROOT = os.environ.get("AROS_ROOT", "/home/ubuntu4/GitHub/AROS")
    sys.path.insert(0, os.path.join(AROS_ROOT, "antigravity-brain", "src"))
    
    try:
        from antigravity_brain.dreamer import process_log_chunk
    except ImportError:
        print(f"Error: Could not import antigravity_brain from {AROS_ROOT}")
        return False

    chunk = json.dumps(latest_step, indent=2)
    
    # Prevent chunk from exceeding typical LLM context limits by keeping the end
    if len(chunk) > 15000:
        chunk = chunk[-15000:]
        
    context_id = f"regent://{step_hash}"
    
    print(f"Processing re_gent session {step_hash[:8]} via AROS Dreamer...")
    
    # This will store the raw chunk as an experience and extract world_facts + mental_models using LLM
    success = process_log_chunk(chunk, context_id)
    if success:
        print(f"Successfully ingested regent session {step_hash[:8]} into AROS Brain.")
        return True
    else:
        print("Failed to process session chunk via AROS Dreamer.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bridge re_gent session transcripts to AROS Brain.")
    parser.add_argument("--dry-run", action="store_true", help="Extract but do not insert into DB.")
    args = parser.parse_args()

    print("Extracting latest re_gent session...")
    data = extract_regent_session()
    
    if args.dry_run:
        print("Dry run enabled. Session data snippet:")
        print(str(data)[:1000] + ("..." if data and len(str(data)) > 1000 else ""))
    else:
        ingest_to_aros(data)
