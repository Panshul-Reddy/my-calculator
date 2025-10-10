"""Unit tests for the CLI module using Click's CliRunner.

These run the CLI in-process so coverage tools can measure `src/CLI.py`.
"""

import os
import sys
from click.testing import CliRunner

# Ensure the `src` directory is on sys.path so `src/CLI.py` can import
# the module `calculator` using the original script-style import
# (i.e. `from calculator import ...`). This mirrors how the CLI is
# executed via subprocess in integration tests.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from importlib.machinery import SourceFileLoader

CLI_PATH = os.path.join(ROOT, "src", "cli.py")
calculate = SourceFileLoader("cli", CLI_PATH).load_module().calculate


def test_cli_add_in_process():
    runner = CliRunner()
    result = runner.invoke(calculate, ["add", "5", "3"])
    assert result.exit_code == 0
    assert result.output.strip() == "8"


def test_cli_subtract_in_process():
    runner = CliRunner()
    result = runner.invoke(calculate, ["subtract", "5", "3"])
    assert result.exit_code == 0
    assert result.output.strip() == "2"


def test_cli_subtract_missing_operand_in_process():
    runner = CliRunner()
    result = runner.invoke(calculate, ["subtract", "5"])
    # CLI should exit non-zero for missing operand
    assert result.exit_code != 0
    # CLI now reports user input errors as 'Error: ...'
    assert result.output.strip().startswith("Error:")


def test_cli_multiply_and_divide_formatting():
    runner = CliRunner()
    mult = runner.invoke(calculate, ["multiply", "5", "3"])
    assert mult.exit_code == 0
    assert mult.output.strip() == "15"

    div = runner.invoke(calculate, ["divide", "5", "3"])
    assert div.exit_code == 0
    # division result is formatted to 2 decimal places
    assert div.output.strip() == "1.67"


def test_cli_power_and_sqrt():
    runner = CliRunner()
    p = runner.invoke(calculate, ["power", "2", "3"])
    assert p.exit_code == 0
    assert p.output.strip() == "8"

    s = runner.invoke(calculate, ["sqrt", "9"])
    assert s.exit_code == 0
    assert s.output.strip() == "3"


def test_cli_unknown_operation():
    runner = CliRunner()
    r = runner.invoke(calculate, ["foobar", "1", "2"])
    assert r.exit_code == 1
    assert r.output.strip().startswith("Error: Unknown operation:")
