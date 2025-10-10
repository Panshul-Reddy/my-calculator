"""
Integration Tests - CLI + Calculator Working Together
"""

import subprocess
import sys
import os
import pytest


class TestCLIIntegration:
    """Test CLI application integrating with
    calculator module"""

    def run_cli(self, *args):
        """Helper method to run CLI and capture
        output"""
        # Try running the CLI as a module first (python -m src.cli). This
        # avoids issues on case-sensitive filesystems where the filename
        # might be `CLI.py` vs `cli.py`.
        module_cmd = [sys.executable, '-m', 'src.cli'] + list(args)
        try:
            result = subprocess.run(module_cmd, capture_output=True, text=True, cwd='.')
            # If the module invocation succeeded, return it.
            if result.returncode == 0:
                return result

            # If the invocation failed because the module/file wasn't
            # found, fall through to the file-based invocation.
            stderr = (result.stderr or '').lower()
            if ('no module named src.cli' in stderr) or ("can't open file" in stderr) or ('no module named src' in stderr):
                # try file-based fallback
                pass
            else:
                # some other error occurred when running the module; return
                # that result so the test can observe it.
                return result
        except Exception:
            # Fall back to file-based invocation below
            pass

        # Fallback: try explicit script file paths (case-insensitive
        # environments may use different casing).
        possible = ['src/cli.py', 'src/CLI.py']
        for p in possible:
            if os.path.exists(p):
                cmd = [sys.executable, p] + list(args)
                return subprocess.run(cmd, capture_output=True, text=True, cwd='.')

        # If neither approach worked, return a CompletedProcess-like
        # object indicating failure.
        return subprocess.CompletedProcess([sys.executable, *module_cmd], 2, stdout='', stderr='CLI not found')

    def test_cli_add_integration(self):
        """Test CLI can perform addition"""
        result = self.run_cli("add", "5", "3")
        assert result.returncode == 0
        assert result.stdout.strip() == "8"

    def test_cli_subtract_integration(self):
        """Test CLI can perform subtraction"""
        result = self.run_cli("subtract", "5", "3")
        assert result.returncode == 0
        assert result.stdout.strip() == "2"

    def test_cli_subtract_missing_operand_error(self):
        """Test CLI handles missing operand for
        subtraction gracefully"""
        # call subtract with only one operand; CLI
        # should exit with non-zero and print an error
        result = self.run_cli("subtract", "5")
        assert result.returncode == 1
        # CLI now prints a user-facing error message for this case
        assert result.stdout.strip().startswith("Error:")

    def test_cli_multiply_integration(self):
        """Test CLI can perform multiplication"""
        result = self.run_cli("multiply", "5", "3")
        assert result.returncode == 0
        assert result.stdout.strip() == "15"

    def test_cli_divide_integration(self):
        """Test CLI can perform division"""
        result = self.run_cli("divide", "5", "3")
        assert result.returncode == 0
        assert result.stdout.strip() == "1.67"
