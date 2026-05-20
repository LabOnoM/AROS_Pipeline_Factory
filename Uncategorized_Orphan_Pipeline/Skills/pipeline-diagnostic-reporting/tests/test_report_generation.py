# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import unittest
import subprocess
import json
import os

class TestReportGeneration(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.script_path = os.path.expanduser("~/.gemini/skills/pipeline-diagnostic-reporting/scripts/generate_report.py")
        if not os.path.exists(self.script_path):
            self.fail(f"Script not found at: {self.script_path}")

    def test_script_executes_and_produces_valid_json(self):
        """
        Verify that the script runs without errors and its output is valid JSON.
        This serves as a basic smoke test.
        """
        try:
            result = subprocess.run(
                ["python", self.script_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            self.assertEqual(result.returncode, 0, "Script should exit with status code 0.")
            try:
                json.loads(result.stdout)
            except json.JSONDecodeError:
                self.fail("Script output is not valid JSON.")
        except subprocess.CalledProcessError as e:
            self.fail(f"Script execution failed with error: {e.stderr}")
        except subprocess.TimeoutExpired:
            self.fail("Script execution timed out.")

    def test_report_schema_enforcement(self):
        """
        Validate that the generated report structurally enforces the required keys.
        This directly addresses the objective criteria from the previous failed attempt.
        """
        result = subprocess.run(
            ["python", self.script_path, "--pipeline-name", "Test-Pipeline"],
            capture_output=True,
            text=True,
            check=True
        )
        report_data = json.loads(result.stdout)

        # Check for the presence of all mandatory top-level keys
        self.assertIn("pipeline_name", report_data)
        self.assertIn("run_id", report_data)
        self.assertIn("execution_status", report_data)
        self.assertIn("successes", report_data)
        self.assertIn("failures", report_data)
        self.assertIn("actionable_recommendations", report_data)

        # Check that the required keys have the correct types
        self.assertIsInstance(report_data["pipeline_name"], str)
        self.assertEqual(report_data["pipeline_name"], "Test-Pipeline")
        self.assertIsInstance(report_data["run_id"], str)
        self.assertIsInstance(report_data["execution_status"], str)
        self.assertIn(report_data["execution_status"], ["SUCCESS", "FAILURE", "SKIPPED"])
        self.assertIsInstance(report_data["successes"], list)
        self.assertIsInstance(report_data["failures"], list)
        self.assertIsInstance(report_data["actionable_recommendations"], list)

        # If there are successes, check the schema of the first one
        if report_data["successes"]:
            first_success = report_data["successes"][0]
            self.assertIn("step_name", first_success)
            self.assertIn("status", first_success)
            self.assertEqual(first_success["status"], "SUCCESS")
            self.assertIn("duration_seconds", first_success)

if __name__ == '__main__':
    unittest.main()
