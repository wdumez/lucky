import random
import sys
from collections.abc import Generator
from pathlib import Path
from typing import Annotated

import emoji
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
    paths = search_paths(file, Path.home()) if recurse else singleton(file)
    for path in paths:
        try:
            winner = lucky_winner(path)
            print_winner(winner, art)
            sys.exit(0)
        except FileNotFoundError:
            if verbose:
                print(f"lucky could not read file: {path.absolute()}")
            continue
        except IndexError:
            if verbose:
                print(f"lucky found an empty file: {path.absolute()}")
            continue
    print(
        emoji.emojize(
            "lucky could not find a valid lucky file :downcast_face_with_sweat:"
        )
    )
    sys.exit(1)


def search_paths(path: Path, home: Path) -> Generator[Path]:
    """The different paths that lucky should try to read."""
    path = path.absolute()
    return (
        p / path.name
        for p in filter(lambda parent: parent.is_relative_to(home), path.parents)
    )


def lucky_winner(path: Path) -> str:
    """Read the file and randomly select one of the lines as the lucky winner."""
    with open(path, "r") as f:
        return random.choice([line.strip() for line in f])


def print_winner(winner: str, art: bool):
    """Print the winner, artsy if asked."""
    tprint(winner) if art else print(winner)


def singleton[T](x: T) -> Generator[T]:
    """Create a generator that yields the given element once."""
    yield x


app.__doc__ = f"""
:four_leaf_clover: Choose a lucky winner!

The winner is chosen by default from a file called {DEFAULT_LUCKY_FILE} in the current directory.
"""


def main():
    typer.run(app)
