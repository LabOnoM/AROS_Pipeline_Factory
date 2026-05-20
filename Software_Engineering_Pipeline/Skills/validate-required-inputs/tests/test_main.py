# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import unittest
import os
import sys
import tempfile
import stat
from unittest.mock import patch

# Add scripts directory to path to import main
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import main

class TestValidateRequiredInputs(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.TemporaryDirectory()
        self.dir_path = self.test_dir.name
        
        # Create a valid test file
        self.valid_file_path = os.path.join(self.dir_path, "valid_file.txt")
        with open(self.valid_file_path, 'w') as f:
            f.write("test data")
            
        # Create an inaccessible file
        self.inaccessible_file_path = os.path.join(self.dir_path, "inaccessible_file.txt")
        with open(self.inaccessible_file_path, 'w') as f:
            f.write("secret data")
        os.chmod(self.inaccessible_file_path, 0o000) # Remove all permissions
        
        # Path that does not exist
        self.non_existent_path = os.path.join(self.dir_path, "does_not_exist.txt")

    def tearDown(self):
        # Restore permissions so temporary directory can be deleted
        os.chmod(self.inaccessible_file_path, 0o644)
        self.test_dir.cleanup()

    def test_valid_file(self):
        valid, invalid = main.validate_paths([self.valid_file_path])
        self.assertEqual(len(valid), 1)
        self.assertEqual(len(invalid), 0)
        self.assertEqual(valid[0], self.valid_file_path)

    def test_non_existent_file(self):
        valid, invalid = main.validate_paths([self.non_existent_path])
        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)
        self.assertEqual(invalid[0]["path"], self.non_existent_path)
        self.assertEqual(invalid[0]["reason"], "Path does not exist.")

    def test_inaccessible_file(self):
        # Only run this test if not running as root, since root can read 000 files
        if os.geteuid() == 0:
            self.skipTest("Cannot test inaccessible file as root user.")

        valid, invalid = main.validate_paths([self.inaccessible_file_path])
        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)
        self.assertEqual(invalid[0]["path"], self.inaccessible_file_path)
        self.assertEqual(invalid[0]["reason"], "Path is not readable (check permissions).")

    def test_mixed_files(self):
        paths = [self.valid_file_path, self.non_existent_path, self.inaccessible_file_path]
        valid, invalid = main.validate_paths(paths)
        
        # Adjust assertions based on euid
        if os.geteuid() == 0:
            self.assertEqual(len(valid), 2)
            self.assertEqual(len(invalid), 1)
            reasons = {item["path"]: item["reason"] for item in invalid}
            self.assertEqual(reasons[self.non_existent_path], "Path does not exist.")
        else:
            self.assertEqual(len(valid), 1)
            self.assertEqual(valid[0], self.valid_file_path)
            self.assertEqual(len(invalid), 2)
            reasons = {item["path"]: item["reason"] for item in invalid}
            self.assertEqual(reasons[self.non_existent_path], "Path does not exist.")
            self.assertEqual(reasons[self.inaccessible_file_path], "Path is not readable (check permissions).")

    @patch('sys.exit')
    @patch('sys.stderr', new_callable=list) # stub
    def test_main_no_args(self, mock_stderr, mock_exit):
        # We need to simulate sys.argv without any path args
        with patch('sys.argv', ['main.py']):
            # redirect stderr to devnull to avoid noise
            with patch('sys.stderr', open(os.devnull, 'w')):
                try:
                    main.main()
                except SystemExit:
                    pass
        mock_exit.assert_called_with(1)
        
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_valid_args(self, mock_print, mock_exit):
        with patch('sys.argv', ['main.py', self.valid_file_path]):
            try:
                main.main()
            except SystemExit:
                pass
        mock_exit.assert_called_with(0)
        
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_invalid_args(self, mock_print, mock_exit):
        with patch('sys.argv', ['main.py', self.non_existent_path]):
            try:
                main.main()
            except SystemExit:
                pass
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
