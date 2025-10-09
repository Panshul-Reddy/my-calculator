"""
Command Line Interface for Calculator
Example: python src/cli.py add 5 3
"""
import sys
import click
from calculator import add, subtract, multiply, divide, power, square_root

@click.command()
@click.argument('operation')
@click.argument('num1', type=float)
@click.argument('num2', type=float, required=False)
def calculate(operation, num1, num2=None):
    """Simple calculator CLI"""

    try:
        if operation == 'add':
            if num2 is None:
                raise ValueError("add requires two numbers")
            result = add(num1, num2)
        elif operation == 'subtract':
            if num2 is None:
                raise ValueError("subtract requires two numbers")
            result = subtract(num1, num2)
        elif operation == 'multiply':
            if num2 is None:
                raise ValueError("multiply requires two numbers")
            result = multiply(num1, num2)
        elif operation == 'divide':
            if num2 is None:
                raise ValueError("divide requires two numbers")
            result = divide(num1, num2)
        elif operation == 'power':
            if num2 is None:
                raise ValueError("power requires two numbers")
            result = power(num1, num2)
        elif operation in ('sqrt', 'square_root'):
            result = square_root(num1)
        else:
            click.echo(f"Unknown operation: {operation}")
            sys.exit(1)

        # Format result nicely
        if isinstance(result, float) and result.is_integer():
            click.echo(int(result))
        else:
            if isinstance(result, float):
                click.echo(f"{result:.2f}")
            else:
                click.echo(str(result))

    except ValueError as e:
        click.echo(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    calculate()
