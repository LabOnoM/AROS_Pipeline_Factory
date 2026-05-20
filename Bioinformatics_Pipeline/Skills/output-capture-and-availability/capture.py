# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import argparse
import json
import os
from pathlib import Path
import datetime
import uuid

def capture_output(task_id: str, agent_name: str, output_type: str, content: str):
    """
    Intercepts, logs, and stores an agent's output.

    Args:
        task_id: The unique identifier for the current task.
        agent_name: The name of the agent generating the output.
        output_type: The type of content being generated (e.g., 'python', 'markdown', 'json').
        content: The actual output content from the agent.

    Returns:
        The path to the directory where the output and metadata were stored.
    """
    # 1. Define the base storage directory
    storage_root = Path(os.path.expanduser("~/.gemini/antigravity/logs/output_captures"))

    # 2. Create a structured, time-based directory path
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    capture_uuid = str(uuid.uuid4())
    storage_path = storage_root / current_date / task_id / capture_uuid

    # 3. Create the directory structure
    os.makedirs(storage_path, exist_ok=True)

    # 4. Prepare metadata
    metadata = {
        "capture_timestamp_utc": datetime.datetime.utcnow().isoformat(),
        "task_id": task_id,
        "agent_name": agent_name,
        "output_type": output_type,
        "content_file": "output.content",
        "uuid": capture_uuid
    }

    # 5. Write the content and metadata to files
    content_file_path = storage_path / "output.content"
    metadata_file_path = storage_path / "metadata.json"

    with open(content_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    with open(metadata_file_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4)

    return str(storage_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AROS Output Capture and Availability Skill.")
    parser.add_argument("--task-id", required=True, help="The unique identifier for the current task.")
    parser.add_argument("--agent-name", required=True, help="The name of the agent generating the output.")
    parser.add_argument("--output-type", required=True, help="The type of content (e.g., 'python', 'markdown').")
    parser.add_argument("--content", required=True, help="The actual output content to be captured.")

    args = parser.parse_args()

    # Execute the capture function
    final_path = capture_output(
        task_id=args.task_id,
        agent_name=args.agent_name,
        output_type=args.output_type,
        content=args.content
    )

    # Print the final storage path to stdout for the calling agent
    print(final_path)
