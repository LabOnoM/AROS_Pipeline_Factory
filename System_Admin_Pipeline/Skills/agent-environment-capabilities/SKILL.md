---
name: agent-environment-capabilities
description: A policy mandating that agents confirm their operating environment provides all necessary tools, direct shell access, and specific libraries prior to initiating a task (GEPA Rule).
skill-author: AROS Internal Policy Board
license: Apache-2.0
allowed-tools: [Bash]
---

# Agent Environment Capabilities Policy

This document defines the 'Agent Environment Capabilities' policy. It is a mandatory skill that governs how all AROS agents must verify their execution environment *before* starting a task, as mandated by the General Environment Pre-flight Assessment (GEPA) Rule.

## 1. Overview

This policy establishes a mandatory pre-execution check for all agents operating within the AROS environment. To ensure task reliability, reproducibility, and robustness, agents MUST verify that all required dependencies are available in their operating environment *before* beginning substantive work. This verification process is known as the General Environment Pre-flight Assessment (GEPA) Rule.

The GEPA rule prevents common failure modes where a task fails midway due to a missing tool, a misconfigured library, or inaccessible data, thereby saving computational resources and reducing debugging time.

## 2. The General Environment Pre-flight Assessment (GEPA) Rule

**All autonomous agents must perform a pre-flight assessment of their execution environment to confirm the presence and accessibility of all required tools, libraries, and data resources before proceeding with task execution.**

If any required dependency is not found, the agent must:
1.  **Halt Execution**: Stop immediately before performing any core task logic.
2.  **Report Missing Dependencies**: Clearly report which specific requirements are not met, following the `agent-communication` policy.
3.  **Attempt Installation (If Permitted)**: If policies and permissions allow, attempt to install the missing dependency (e.g., via `pip`). If installation is not permitted or fails, the task must be terminated.

## 3. Core Implementation Steps

Agents must integrate the following checks into the beginning of their execution cycle.

### Step 1: Identify Dependencies
Before execution, parse the task goal and the associated skill documentation to build a list of all dependencies. This includes:
-   **Shell Commands/Executables**: e.g., `git`, `python`, `gcc`, `docker`
-   **Python Libraries**: e.g., `pandas`, `numpy`, `torch`
-   **File Paths / Data Resources**: e.g., `/mnt/Disk1/datasets/data.csv`, `~/.gemini/antigravity/brain.db`
-   **API Endpoints / Services**: e.g., `http://localhost:8000/api/status`

### Step 2: Perform Environment Checks
Execute checks for each identified dependency.

#### A. Verifying Shell Commands
Use `command -v` to check for the existence of a shell command. It is silent on success and provides a clear error on failure.

**Example:**
```bash
# Check for 'git' and 'make'
if ! command -v git &> /dev/null; then
    echo "GEPA FAIL: 'git' command not found. Aborting."
    exit 1
fi
if ! command -v make &> /dev/null; then
    echo "GEPA FAIL: 'make' command not found. Aborting."
    exit 1
fi
echo "GEPA PASS: All required shell commands are available."
```

#### B. Verifying Python Libraries
Use `python -c "import <library>"` to confirm a library is installed and importable.

**Example:**
```bash
# Check for 'pandas' and 'torch'
if ! python -c "import pandas" &> /dev/null; then
    echo "GEPA FAIL: Python library 'pandas' not found. Attempting installation."
    pip install pandas || (echo "Installation failed. Aborting." && exit 1)
fi
if ! python -c "import torch" &> /dev/null; then
    echo "GEPA FAIL: Python library 'torch' not found. Aborting."
    exit 1
fi
echo "GEPA PASS: All required Python libraries are available."
```

#### C. Verifying File/Directory Access
Use `test -r` (readable), `test -w` (writable), or `test -f` (is a file), `test -d` (is a directory) to check for file system resources.

**Example:**
```bash
# Check for a readable data file and a writable output directory
DATA_FILE="/mnt/Disk1/datasets/data.csv"
OUTPUT_DIR="/mnt/Disk1/results/"

if [ ! -r "$DATA_FILE" ]; then
    echo "GEPA FAIL: Cannot read data file at $DATA_FILE. Aborting."
    exit 1
fi

if [ ! -d "$OUTPUT_DIR" ] || [ ! -w "$OUTPUT_DIR" ]; then
    echo "GEPA FAIL: Output directory $OUTPUT_DIR does not exist or is not writable. Aborting."
    exit 1
fi
echo "GEPA PASS: All required file system resources are accessible."
```

#### D. Verifying Network Services
Use tools like `curl` or `nc` to check if a network service is reachable.

**Example:**
```bash
# Check if a local API server is responding
API_URL="http://localhost:8000/api/status"
if ! curl --output /dev/null --silent --head --fail "$API_URL"; then
    echo "GEPA FAIL: API endpoint at $API_URL is not reachable. Aborting."
    exit 1
fi
echo "GEPA PASS: All required network services are reachable."
```

## 4. Validation
This policy is validated by observing agent behavior. Agents that fail due to missing dependencies without performing a pre-flight check are in violation of this policy. A successful implementation will show the GEPA checks in the agent's execution trace before the core task logic begins.
