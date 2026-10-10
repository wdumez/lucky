import random
import sys
from dataclasses import dataclass
from typing import Annotated

import typer
from art import tprint  # type: ignore

DEFAULT_LUCKY_FILE = ".lucky"


@dataclass
class FileIsEmptyError(Exception):
    filename: str


def app(
    file: Annotated[
        str, typer.Argument(help="The file to read the lucky winner from")
    ] = DEFAULT_LUCKY_FILE,
    art: Annotated[
        bool, typer.Option(help="Whether to show the winner with fancy ASCII art")
    ] = True,
):
    try:
        with open(file, "r") as f:
            lines = [x.strip() for x in f]
        if len(lines) == 0:
            raise FileIsEmptyError(file)
        line = random.choice(lines)
        tprint(line) if art else print(line)
    except FileNotFoundError as e:
        print(f"lucky could not read file: {e.filename}")
        sys.exit(1)
    except FileIsEmptyError as e:
        print(f"lucky found an empty file: {e.filename}")
        sys.exit(1)


app.__doc__ = f"""
:four_leaf_clover: Choose a lucky winner!

The winner is chosen by default from a file called {DEFAULT_LUCKY_FILE} in the current directory.
"""


def main():
    typer.run(app)
