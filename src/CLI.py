"""Deprecated file left for compatibility on case-insensitive filesystems.

The real implementation is in :mod:`src.cli`. This module is intentionally
left as a no-op placeholder to avoid import conflicts during local edits on
case-insensitive filesystems. Remove when the filesystem and tooling allow.
"""

"""
Command Line Interface for Calculator
Example: python src/cli.py add 5 3
"""
"""Command Line Interface for Calculator (lowercase module for linting)

This module intentionally accepts a few pragmatic pylint suppressions
because CLI entrypoints frequently look irregular to static analyzers
(decorated callables, branching by operation, etc.).
"""
# pylint: disable=invalid-name,too-many-branches,broad-except

import sys
import click

# Make imports robust for both running as a script (python src/cli.py)
# and as a package (import src.CLI). Pylint runs from the repo root and
# prefers the package-style import, so try that first.
try:
    from src.calculator import add, subtract, multiply, divide, power, square_root
except Exception:
    # Fallback for script-style execution where `src` is not a package
    from calculator import add, subtract, multiply, divide, power, square_root


class UserInputError(Exception):
    """Raised when the user provides invalid input to the CLI."""

    pass


@click.command()
@click.argument("operation")
@click.argument("num1", type=float)
@click.argument("num2", type=float, required=False)
def calculate(operation, num1, num2=None):
    """Simple calculator CLI"""

    try:
        if operation == "add":
            if num2 is None:
                raise UserInputError("add requires two numbers")
            result = add(num1, num2)
        elif operation == "subtract":
            if num2 is None:
                raise UserInputError("subtract requires two numbers")
            result = subtract(num1, num2)
        elif operation == "multiply":
            if num2 is None:
                raise UserInputError("multiply requires two numbers")
            result = multiply(num1, num2)
        elif operation == "divide":
            if num2 is None:
                raise UserInputError("divide requires two numbers")
            result = divide(num1, num2)
        elif operation == "power":
            if num2 is None:
                raise UserInputError("power requires two numbers")
            result = power(num1, num2)
        elif operation in ("sqrt", "square_root"):
            result = square_root(num1)
        else:
            raise UserInputError(f"Unknown operation: {operation}")

        # Format result nicely
        if isinstance(result, float) and result.is_integer():
            click.echo(int(result))
        else:
            if isinstance(result, float):
                click.echo(f"{result:.2f}")
            else:
                click.echo(str(result))

    except UserInputError as e:
        # Clear, expected user error
        click.echo(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}")
        sys.exit(1)
    except Exception as e:  # pylint: disable=broad-except
        # Unexpected exceptions — keep this generic but intentionally
        # allow a broad except here to ensure the CLI always exits with
        # a helpful message; pylint is told to ignore the broad-except
        # warning at this site.
        click.echo(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Click-decorated functions appear to take parameters to static
    # analysis tools like pylint, which causes false positives.
    # Disable the "no-value-for-parameter" check here.
    calculate()  # pylint: disable=no-value-for-parameter
