"""
agent_package_builder.py
------------------------
This script orchestrates the automated synthesis of AI Agent Packages for the AROS Pipeline Factory.
It scans registered pipeline directories, safely excludes heavy build artifacts (like node_modules and package-lock.json),
and constructs context windows which are sent to the Gemini 3.1 Pro model. The LLM generates declarative
configurations including agent.yaml, system.md persona prompts, and input/output JSON schemas.

This enables a scalable, cross-platform mechanism for deploying AROS capabilities into the Cloud Federation.
"""

import os
import sys
import json
import time
import yaml
import argparse
import requests
from dotenv import load_dotenv

# Load API key from ~/.gemini/.env
load_dotenv(os.path.expanduser("~/.gemini/.env"))
API_KEY = os.getenv("GOOGLE_AI_API_KEY")

if not API_KEY:
    print("ERROR: GOOGLE_AI_API_KEY not found in ~/.gemini/.env")
    sys.exit(1)

def read_skill_summary(filepath):
    """Read only the frontmatter or name/description from a SKILL.md file to save token budget."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = []
            in_frontmatter = False
            frontmatter_lines = []
            for _ in range(30):  # limit to first 30 lines
                line = f.readline()
                if not line:
                    break
                lines.append(line)
                if line.strip() == '---':
                    if not in_frontmatter and not frontmatter_lines:
                        in_frontmatter = True
                    elif in_frontmatter:
                        in_frontmatter = False
                elif in_frontmatter:
                    frontmatter_lines.append(line)
            
            # If we found frontmatter, return it
            if frontmatter_lines:
                return "---\n" + "".join(frontmatter_lines) + "---\n"
            else:
                # Fallback to returning the first 10 lines
                return "".join(lines[:10])
    except Exception as e:
        return f"Error reading skill summary: {e}\n"

def scan_directory(pipeline_dir):
    """Recursively scan directory and return contents of relevant files, optimizing for large folders."""
    contents = ""
    ignore_dirs = {'.git', 'schemas', 'prompts', '__pycache__', 'assets', 'out', 'node_modules', 'dist', '.next', 'build'}
    valid_exts = {'.md', '.py', '.json', '.txt', '.sh'}
    
    for root, dirs, files in os.walk(pipeline_dir):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        # Check if we are inside a skill or KI subdirectory
        rel_root = os.path.relpath(root, pipeline_dir)
        path_parts = rel_root.split(os.sep)
        
        is_skill_sub = 'Skills' in path_parts and len(path_parts) > path_parts.index('Skills') + 1
        is_ki_sub = 'KIs' in path_parts and len(path_parts) > path_parts.index('KIs') + 1
        
        for file in files:
            if file == 'package-lock.json':
                continue
            ext = os.path.splitext(file)[1].lower()
            if ext in valid_exts:
                filepath = os.path.join(root, file)
                
                # If it's a file inside a specific skill folder
                if is_skill_sub:
                    if file == 'SKILL.md':
                        summary = read_skill_summary(filepath)
                        contents += f"\n\n--- SKILL SUMMARY: {os.path.relpath(filepath, pipeline_dir)} ---\n"
                        contents += summary
                    continue
                
                # If it's a file inside a specific KI folder
                if is_ki_sub:
                    if file == 'metadata.json' or (ext == '.md' and not file.startswith('.')):
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                lines = [f.readline() for _ in range(50)]
                                ki_content = "".join([l for l in lines if l])
                            contents += f"\n\n--- KI FILE SUMMARY: {os.path.relpath(filepath, pipeline_dir)} ---\n"
                            contents += ki_content
                            if len(lines) == 50:
                                contents += "... [TRUNCATED] ...\n"
                        except Exception as e:
                            print(f"Warning: Could not read KI file {filepath}: {e}")
                    continue
                
                # Default case for workflows and other root files
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        contents += f"\n\n--- FILE: {os.path.relpath(filepath, pipeline_dir)} ---\n"
                        contents += f.read()
                except Exception as e:
                    print(f"Warning: Could not read {filepath}: {e}")
    return contents

def generate_agent_package(pipeline_name, file_contents):
    """Call Gemini API to generate the agent package structure."""
    prompt = f"""
You are an expert AI architect building a declarative Agent Package for the AROS Cloud Federation.
I will provide you with the raw source files (markdown workflows, scripts, etc.) for a pipeline named '{pipeline_name}'.

Your job is to read these files line-by-line, understand the pipeline's logic, and generate a JSON object containing the configurations for this agent.

If the pipeline requires reading from local file paths (like /home/ubuntu4) or executing local system binaries that wouldn't be available in a cloud environment, set execution_context to "local_only". Otherwise, set it to "cloud_native".
If you are unsure about a tool or input, add a "[TODO: MANUAL REVIEW]" comment in the description.

Extract the following:
1. 'agent_yaml': A dictionary representing the agent.yaml file. Must NOT be empty.
2. 'system_md': A string representing the system.md persona prompt.
3. 'input_schema': A dictionary representing the input_schema.json (JSON Schema). Must NOT be empty.
4. 'output_schema': A dictionary representing the output_schema.json (JSON Schema). Must NOT be empty.

CRITICAL: Do NOT return empty dictionaries. You MUST infer and construct the complete agent_yaml, input_schema, and output_schema structures.

Expected agent_yaml structure:
{{
  "kind": "PipelineAgent",
  "metadata": {{
    "name": "<name>",
    "version": "1.0.0",
    "trigger": "</command>",
    "description": "<desc>",
    "execution_context": "<cloud_native or local_only>"
  }},
  "persona": {{
    "role": "<role>",
    "mission": "<mission>",
    "tone": "<tone>"
  }},
  "capabilities": {{
    "model": "gemini-3.1-pro-preview",
    "allowed_tools": [ {{"name": "tool_1"}}, {{"name": "tool_2"}} ]
  }},
  "guardrails": {{
    "max_token_budget": 150000,
    "human_in_the_loop": true,
    "anti_goals": ["<rule 1>", "<rule 2>"]
  }},
  "io": {{
    "input_schema": "schemas/input_schema.json",
    "output_schema": "schemas/output_schema.json"
  }}
}}

RAW FILES FOR '{pipeline_name}':
{file_contents}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "response_mime_type": "application/json",
            "temperature": 0.2
        }
    }

    print("Calling Gemini 2.5 Pro to synthesize agent package...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        sys.exit(1)
        
    try:
        response_data = response.json()
        result_text = response_data['candidates'][0]['content']['parts'][0]['text']
        parsed = json.loads(result_text)
        if isinstance(parsed, list):
            print("Warning: LLM returned a list, attempting to extract the first dictionary...")
            for item in parsed:
                if isinstance(item, dict):
                    return item
            raise ValueError("No dictionary found in list response.")
        return parsed
    except Exception as e:
        print(f"Failed to parse Gemini response: {e}")
        print("Raw response:", response.text)
        sys.exit(1)

def get_registered_pipelines(repo_root):
    """Parse PIPELINE_REGISTRY.md to get the list of registered pipeline directories."""
    registry_path = os.path.join(repo_root, "00.RawData", "PIPELINE_REGISTRY.md")
    if not os.path.exists(registry_path):
        print(f"ERROR: Registry file not found at {registry_path}")
        sys.exit(1)
        
    pipelines = []
    with open(registry_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('|'):
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 2:
                continue
            col1 = parts[1]
            if col1.startswith('`') and col1.endswith('`'):
                pipeline_name = col1.strip('`')
                if pipeline_name != "Pipeline Directory":
                    pipelines.append(pipeline_name)
    return pipelines

def process_pipeline(pipeline_dir):
    """Process a single pipeline directory and build its Agent Package."""
    pipeline_dir = os.path.abspath(pipeline_dir)
    pipeline_name = os.path.basename(pipeline_dir)

    if not os.path.isdir(pipeline_dir):
        print(f"ERROR: Directory {pipeline_dir} does not exist.")
        return False

    print(f"\n--- Processing pipeline: {pipeline_name} ---")
    print(f"Scanning directory: {pipeline_dir}")
    file_contents = scan_directory(pipeline_dir)
    
    if not file_contents.strip():
        print(f"Warning: No valid source files found in {pipeline_dir}. Skipping...")
        return False
        
    print(f"Extracted {len(file_contents)} bytes of context. Sending to LLM...")
    try:
        package_data = generate_agent_package(pipeline_name, file_contents)
    except Exception as e:
        print(f"Error calling Gemini for {pipeline_name}: {e}")
        return False
    
    # Create directories
    schemas_dir = os.path.join(pipeline_dir, "schemas")
    prompts_dir = os.path.join(pipeline_dir, "prompts")
    os.makedirs(schemas_dir, exist_ok=True)
    os.makedirs(prompts_dir, exist_ok=True)
    
    # Write files
    agent_yaml_path = os.path.join(pipeline_dir, "agent.yaml")
    with open(agent_yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(package_data.get('agent_yaml', {}), f, sort_keys=False, default_flow_style=False)
        
    with open(os.path.join(schemas_dir, "input_schema.json"), 'w', encoding='utf-8') as f:
        json.dump(package_data.get('input_schema', {}), f, indent=2)
        
    with open(os.path.join(schemas_dir, "output_schema.json"), 'w', encoding='utf-8') as f:
        json.dump(package_data.get('output_schema', {}), f, indent=2)
        
    with open(os.path.join(prompts_dir, "system.md"), 'w', encoding='utf-8') as f:
        f.write(package_data.get('system_md', '# System Persona\n'))
        
    print(f"✅ Successfully generated Agent Package for {pipeline_name}!")
    print(f" - {agent_yaml_path}")
    print(f" - {os.path.join(schemas_dir, 'input_schema.json')}")
    print(f" - {os.path.join(schemas_dir, 'output_schema.json')}")
    print(f" - {os.path.join(prompts_dir, 'system.md')}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Automated Agent Package Builder")
    parser.add_argument("--pipeline_dir", help="Path to the pipeline directory")
    parser.add_argument("--all", action="store_true", help="Scan and process all registered pipelines in PIPELINE_REGISTRY.md")
    args = parser.parse_args()

    # Determine repository root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    if not args.pipeline_dir and not args.all:
        parser.print_help()
        sys.exit(1)

    if args.all:
        registered_pipelines = get_registered_pipelines(repo_root)
        if not registered_pipelines:
            print("No registered pipelines found in registry.")
            sys.exit(1)
        
        print(f"Found {len(registered_pipelines)} registered pipelines in PIPELINE_REGISTRY.md: {', '.join(registered_pipelines)}")
        success_count = 0
        skipped_count = 0
        failed_count = 0
        
        for i, pipeline_name in enumerate(registered_pipelines):
            pipeline_dir = os.path.join(repo_root, pipeline_name)
            if not os.path.exists(pipeline_dir):
                print(f"Warning: Registered pipeline directory {pipeline_dir} does not exist. Skipping.")
                skipped_count += 1
                continue
            
            # Check if there are valid files to scan before calling the api to avoid wasted calls
            file_contents = scan_directory(pipeline_dir)
            if not file_contents.strip():
                print(f"Skipping {pipeline_name}: No valid source files (.md, .py, .json, .txt, .sh) found.")
                skipped_count += 1
                continue
            
            # Introduce a small sleep between API calls to respect rate limits if we are processing multiple pipelines
            if i > 0:
                print("Sleeping for 5 seconds to respect Gemini API rate limits...")
                time.sleep(5)
                
            success = process_pipeline(pipeline_dir)
            if success:
                success_count += 1
            else:
                failed_count += 1
                
        print(f"\nBatch processing complete: {success_count} succeeded, {skipped_count} skipped, {failed_count} failed.")
        
    else:
        success = process_pipeline(args.pipeline_dir)
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()
