# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import os
import shutil
import importlib
import sys

class EnvironmentValidator:
    """
    Verifies access to necessary data paths, shell commands, and libraries before running generated code.
    """

    def __init__(self):
        self.errors = []

    def check_read_paths(self, paths):
        """
        Checks if paths exist and are readable.
        """
        for path in paths:
            if not os.path.exists(path):
                self.errors.append(f"Required read path does not exist: {path}")
            elif not os.access(path, os.R_OK):
                self.errors.append(f"Required read path is not readable: {path}")

    def check_write_paths(self, paths):
        """
        Checks if the parent directories for the given paths exist and are writable.
        """
        for path in paths:
            parent_dir = os.path.dirname(path)
            if not os.path.isdir(parent_dir):
                self.errors.append(f"Parent directory for required write path does not exist: {parent_dir}")
            elif not os.access(parent_dir, os.W_OK):
                self.errors.append(f"Parent directory for required write path is not writable: {parent_dir}")

    def check_shell_commands(self, commands):
        """
        Checks if shell commands are available in the system's PATH.
        """
        for command in commands:
            if not shutil.which(command):
                self.errors.append(f"Required shell command is not in PATH: {command}")

    def check_python_libraries(self, libraries):
        """
        Checks if Python libraries can be imported.
        """
        for library in libraries:
            try:
                importlib.import_module(library)
            except ImportError:
                self.errors.append(f"Required Python library is not installed: {library}")

    def verify(self, read_paths=None, write_paths=None, shell_commands=None, python_libraries=None):
        """
        Runs all verification checks.
        Returns True if all checks pass, False otherwise.
        """
        self.errors = []
        if read_paths:
            self.check_read_paths(read_paths)
        if write_paths:
            self.check_write_paths(write_paths)
        if shell_commands:
            self.check_shell_commands(shell_commands)
        if python_libraries:
            self.check_python_libraries(python_libraries)

        return not self.errors

    def get_errors(self):
        """
        Returns the list of verification errors.
        """
        return self.errors

if __name__ == '__main__':
    # Example Usage and self-test
    validator = EnvironmentValidator()

    # --- Test Cases ---
    print("Running Environment Validator Self-Test...")

    # 1. Successful validation
    print("\n--- Running Test Case 1: Successful Validation ---")
    success_validator = EnvironmentValidator()
    test_dir = "/tmp/sec_code_exec_test"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    test_file = os.path.join(test_dir, "readable.txt")
    with open(test_file, "w") as f:
        f.write("test")

    success = success_validator.verify(
        read_paths=[test_file],
        write_paths=[os.path.join(test_dir, "writable.txt")],
        shell_commands=["ls", "echo"],
        python_libraries=["os", "sys"]
    )
    if success:
        print("✅ PASSED: Successful validation completed as expected.")
    else:
        print(f"❌ FAILED: Expected success, but got errors: {success_validator.get_errors()}")
    shutil.rmtree(test_dir)


    # 2. Failing validation
    print("\n--- Running Test Case 2: Failing Validation ---")
    failure_validator = EnvironmentValidator()
    # Define requirements that are expected to fail
    required_read_files = ['/does/not/exist/file.txt']
    required_write_files = ['/root/no_access/output.log']
    required_commands = ['non_existent_command_xyz']
    required_libraries = ['non_existent_library_abc']

    # Run verification
    success = failure_validator.verify(
        read_paths=required_read_files,
        write_paths=required_write_files,
        shell_commands=required_commands,
        python_libraries=required_libraries
    )

    if not success:
        print("✅ PASSED: Failing validation caught errors as expected.")
        errors = failure_validator.get_errors()
        print("Reported Errors:")
        for error in errors:
            print(f"  - {error}")

        # Assert specific errors are present
        assert "Required read path does not exist: /does/not/exist/file.txt" in errors
        assert "Parent directory for required write path is not writable: /root/no_access" in errors or "Parent directory for required write path does not exist: /root/no_access" in errors
        assert "Required shell command is not in PATH: non_existent_command_xyz" in errors
        assert "Required Python library is not installed: non_existent_library_abc" in errors
    else:
        print("❌ FAILED: Expected failure, but validation succeeded.")

    print("\nSelf-Test Complete.")
