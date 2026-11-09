import random
from collections.abc import Generator
from pathlib import Path
from typing import Annotated

import typer
from art import tprint  # type: ignore
from rich import print

DEFAULT_LUCKY_FILE = Path(".lucky")
VERSION = "0.2.0"


def version_callback(value: bool):
    """Print the version number and exit."""
    if value:
        print(f"lucky {VERSION}")
        raise typer.Exit()


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
    add: Annotated[
        list[str] | None,
        typer.Option(
            "--add",
            "-a",
            help="Add a candidate for this run only (can be repeated)",
        ),
    ] = None,
    remove: Annotated[
        list[str] | None,
        typer.Option(
            "--remove",
            "-r",
            help="Exclude a candidate for this run only (can be repeated)",
        ),
    ] = None,
    count: Annotated[
        int,
        typer.Option(
            "--count",
            "-c",
            help="The number of winners to select (must be positive)",
            min=1,
        ),
    ] = 1,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Print the version of lucky and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
):
    paths = search_paths(file) if recurse else singleton(file)
    for path in paths:
        try:
            candidates = read_candidates(path)
        except FileNotFoundError:
            if verbose:
                print(f"lucky could not read file: {path.absolute()}")
            continue
        candidates = adjust_candidates(candidates, add or [], remove or [])
        if not candidates:
            if verbose:
                print(f"lucky found no candidates in file: {path.absolute()}")
            continue
        if verbose and count > len(candidates):
            print(
                f"lucky found only {len(candidates)} candidates, "
                f"selecting all of them instead of {count}"
            )
        winners = random.sample(candidates, k=min(count, len(candidates)))
        for winner in winners:
            print_winner(winner, art)
        raise typer.Exit(0)
    print("lucky could not find a valid lucky file :downcast_face_with_sweat:")
    raise typer.Exit(1)


def search_paths(path: Path) -> Generator[Path]:
    """The different paths that lucky should try to read."""
    home = Path.home()
    return (p / path.name for p in path.absolute().parents if p.is_relative_to(home))


def read_candidates(path: Path) -> list[str]:
    """Read the file and return its filtered lines as the list of candidates."""
    with open(path, "r") as f:
        return list(filter(None, map(str.strip, f)))


def adjust_candidates(
    candidates: list[str], add: list[str], remove: list[str]
) -> list[str]:
    """Add and remove candidates for this run, without touching the file."""
    excluded = {name.strip() for name in remove}
    added = [name.strip() for name in add]
    return [c for c in candidates + added if c not in excluded]


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
