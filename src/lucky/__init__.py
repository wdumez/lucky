import random
import sys
from pathlib import Path
from typing import Annotated

import typer
from art import tprint  # type: ignore

DEFAULT_LUCKY_FILE = Path(".lucky")


def app(
    file: Annotated[
        Path, typer.Argument(help="The file to read the lucky winner from")
    ] = DEFAULT_LUCKY_FILE,
    art: Annotated[
        bool, typer.Option(help="Whether to show the winner with fancy ASCII art")
    ] = True,
):
    try:
        winner = lucky_winner(file)
        print_winner(winner, art)
    except FileNotFoundError:
        print(f"lucky could not read file: {file}")
        sys.exit(1)
    except IndexError:
        print(f"lucky found an empty file: {file}")
        sys.exit(1)


def lucky_winner(path: Path) -> str:
    """Select a random lucky winner."""
    with open(path, "r") as f:
        return random.choice([line.strip() for line in f])


def print_winner(winner: str, art: bool):
    """Print the winner, artfully if asked."""
    tprint(winner) if art else print(winner)


app.__doc__ = f"""
:four_leaf_clover: Choose a lucky winner!

The winner is chosen by default from a file called {DEFAULT_LUCKY_FILE} in the current directory.
"""


def main():
    typer.run(app)
