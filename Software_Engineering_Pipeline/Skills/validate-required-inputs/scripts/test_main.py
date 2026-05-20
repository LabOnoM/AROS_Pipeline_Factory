# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import unittest
import tempfile
import os
import subprocess
import json

SCRIPT_PATH = "/home/owner03/.gemini/skills/validate-required-inputs/scripts/main.py"

class TestValidateRequiredInputs(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to hold our test files
        self.test_dir = tempfile.mkdtemp()
        
        # 1. Create a valid file
        self.valid_file = os.path.join(self.test_dir, "valid.txt")
        with open(self.valid_file, 'w') as f:
            f.write("test")
            
        # 2. Non-existent file path
        self.missing_file = os.path.join(self.test_dir, "missing.txt")
        
        # 3. Create a file without read permissions
        self.no_read_file = os.path.join(self.test_dir, "no_read.txt")
        with open(self.no_read_file, 'w') as f:
            f.write("secret")
        # remove read permissions
        os.chmod(self.no_read_file, 0o000)

    def tearDown(self):
        # Restore permissions to allow deletion
        if os.path.exists(self.no_read_file):
            os.chmod(self.no_read_file, 0o666)
            os.remove(self.no_read_file)
        if os.path.exists(self.valid_file):
            os.remove(self.valid_file)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def run_script(self, args):
        cmd = ["python", SCRIPT_PATH] + args
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def test_all_valid_files(self):
        result = self.run_script([self.valid_file])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Valid Paths:", result.stdout)
        self.assertIn(self.valid_file, result.stdout)
        self.assertNotIn(self.missing_file, result.stdout)

    def test_nonexistent_file(self):
        result = self.run_script([self.missing_file])
        self.assertEqual(result.returncode, 1)
        self.assertIn("Invalid Paths:", result.stdout)
        self.assertIn("Path does not exist", result.stdout)

    def test_inaccessible_file(self):
        result = self.run_script([self.no_read_file])
        self.assertEqual(result.returncode, 1)
        self.assertIn("Path is not readable (check permissions)", result.stdout)

    def test_mixed_files_with_json(self):
        result = self.run_script(["--json", self.valid_file, self.missing_file, self.no_read_file])
        self.assertEqual(result.returncode, 1)
        try:
            output_data = json.loads(result.stdout)
        except json.JSONDecodeError:
            self.fail(f"Could not parse JSON from stdout: {result.stdout}")
        
        self.assertIn(self.valid_file, output_data["valid"])
        self.assertEqual(len(output_data["invalid"]), 2)
        
        reasons = {item["path"]: item["reason"] for item in output_data["invalid"]}
        self.assertEqual(reasons[self.missing_file], "Path does not exist.")
        self.assertEqual(reasons[self.no_read_file], "Path is not readable (check permissions).")

if __name__ == '__main__':
    unittest.main()
