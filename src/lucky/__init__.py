import random
import sys
from collections.abc import Generator
from pathlib import Path
from typing import Annotated

import emoji
import typer
from art import tprint  # type: ignore

DEFAULT_LUCKY_FILE = Path(".lucky")
STDIN = Path("-")


def app(
    file: Annotated[
        Path,
        typer.Argument(
            help="The file to read the lucky winner from, use '-' to read from standard input"
        ),
    ] = DEFAULT_LUCKY_FILE,
    art: Annotated[
        bool, typer.Option(help="Whether to show the winner with fancy ASCII art")
    ] = True,
    recurse: Annotated[
        bool,
        typer.Option(
            help="Whether to recursively search parent directories for the file"
        ),
    ] = True,
    verbose: Annotated[
        bool, typer.Option(help="Whether to print error messages during execution")
    ] = False,
):
    paths = search_paths(file) if recurse and file != STDIN else singleton(file)
    for path in paths:
        try:
            winner = random.choice(read_candidates(path))
        except FileNotFoundError:
            if verbose:
                print(f"lucky could not read file: {describe(path)}")
            continue
        except IndexError:
            if verbose:
                print(f"lucky found an empty file: {describe(path)}")
            continue
        print_winner(winner, art)
        sys.exit(0)
    print(
        emoji.emojize(
            "lucky could not find a valid lucky file :downcast_face_with_sweat:"
        )
    )
    sys.exit(1)


def search_paths(path: Path) -> Generator[Path]:
    """The different paths that lucky should try to read."""
    home = Path.home()
    return (p / path.name for p in path.absolute().parents if p.is_relative_to(home))


def read_candidates(path: Path) -> list[str]:
    """Read the candidates from the file, or from standard input if the path is '-'."""
    if path == STDIN:
        lines = sys.stdin.read().splitlines()
    else:
        with open(path, "r") as f:
            lines = f.read().splitlines()
    return [line.strip() for line in lines]


def describe(path: Path) -> str:
    """A human-readable description of where the candidates are read from."""
    return "standard input" if path == STDIN else str(path.absolute())


def print_winner(winner: str, art: bool):
    """Print the winner, artsy if asked."""
    tprint(winner) if art else print(winner)


def singleton[T](x: T) -> Generator[T]:
    """Create a generator that yields the given element once."""
    yield x


app.__doc__ = f"""
:four_leaf_clover: Choose a lucky winner!

The lucky winner is selected randomly as one of the lines of a file. By default, it tries '{DEFAULT_LUCKY_FILE}', starting from the current directory and trying parent directories until it reaches the home directory.

Lucky's behavior can be configured, use `--help` for detailed instructions!
"""


def main():
    typer.run(app)
