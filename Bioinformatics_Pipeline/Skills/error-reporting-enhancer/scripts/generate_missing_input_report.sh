#!/bin/bash
#
# Name: generate_missing_input_report.sh
# Description: Intercepts missing input halts and generates a precise,
#              unambiguous JSON report detailing the missing input, its
#              expected source, and type.
#
# AROS-Integration: This script is a core component of the
#                   'error-reporting-enhancer' skill. It is invoked by other
#                   skills or the AROS runtime when input validation fails.

# --- Strict Mode & Error Handling ---
set -euo pipefail

# --- Input Validation ---
if [ "$#" -ne 3 ]; then
    echo "ERROR: Invalid number of arguments. Requires exactly 3." >&2
    echo "Usage: $0 <missing_input_name> <expected_source> <expected_type>" >&2
    echo "Example: $0 'API_KEY' 'environment_variable' 'string'" >&2
    exit 1
fi

MISSING_INPUT_NAME="$1"
EXPECTED_SOURCE="$2"
EXPECTED_TYPE="$3"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# --- Report Generation ---
# Generate a unique ID for the report
if command -v uuidgen &> /dev/null; then
    REPORT_ID=$(uuidgen)
else
    # Fallback for systems without uuidgen
    REPORT_ID=$(cat /proc/sys/kernel/random/uuid)
fi

# Define the output directory for error reports
OUTPUT_DIR="${HOME}/.gemini/antigravity/logs/error_reports"
mkdir -p "${OUTPUT_DIR}"
OUTPUT_FILE="${OUTPUT_DIR}/${REPORT_ID}.json"

# Construct the JSON report using a heredoc for clarity
# This avoids potential quoting issues with jq or complex echo statements.
cat << EOF > "${OUTPUT_FILE}"
{
  "error_type": "MissingInput",
  "report_id": "${REPORT_ID}",
  "timestamp": "${TIMESTAMP}",
  "severity": "High",
  "source_skill": "error-reporting-enhancer",
  "details": {
    "missing_input_name": "${MISSING_INPUT_NAME}",
    "expected_source": "${EXPECTED_SOURCE}",
    "expected_type": "${EXPECTED_TYPE}"
  },
  "message": "Execution halted due to a missing critical input. The input '${MISSING_INPUT_NAME}' (expected type: ${EXPECTED_TYPE}) was not found in the expected source: '${EXPECTED_SOURCE}'."
}
EOF

# --- Output & Confirmation ---
# Print the path to the report for logging and user feedback
echo "Generated missing input report: ${OUTPUT_FILE}"

# Optionally, print the report content to stdout for immediate visibility
# cat "${OUTPUT_FILE}"
