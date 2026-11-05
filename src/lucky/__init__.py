import random
import sys
import time
from collections.abc import Generator
from pathlib import Path
from typing import Annotated

import emoji
import typer
from art import DEFAULT_FONT, FONT_NAMES, tprint  # type: ignore

DEFAULT_LUCKY_FILE = Path(".lucky")
STDIN = Path("-")
RANDOM_FONTS = ["random", "rnd-small", "rnd-medium", "rnd-large", "rnd-xlarge"]


def validate_font(font: str) -> str:
    """Reject unknown fonts, which art would otherwise render as garbage."""
    if font not in FONT_NAMES and font not in RANDOM_FONTS:
        raise typer.BadParameter(
            f"unknown font '{font}', use --list-fonts to see the available fonts"
        )
    return font


def list_fonts(value: bool):
    """Print the available ASCII art fonts and exit."""
    if value:
        print("\n".join([*RANDOM_FONTS, *FONT_NAMES]))
        raise typer.Exit()


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
    font: Annotated[
        str,
        typer.Option(
            help="The ASCII art font to show the winner with, use --list-fonts to see them all",
            callback=validate_font,
        ),
    ] = DEFAULT_FONT,
    _list_fonts: Annotated[
        bool,
        typer.Option(
            "--list-fonts",
            help="List the available ASCII art fonts and exit",
            callback=list_fonts,
            is_eager=True,
        ),
    ] = False,
    recurse: Annotated[
        bool,
        typer.Option(
            help="Whether to recursively search parent directories for the file"
        ),
    ] = True,
    verbose: Annotated[
        bool, typer.Option(help="Whether to print error messages during execution")
    ] = False,
    spin: Annotated[
        bool,
        typer.Option(
            help="Whether to build suspense by spinning through the candidates first, only in a terminal"
        ),
    ] = True,
):
    paths = search_paths(file) if recurse and file != STDIN else singleton(file)
    for path in paths:
        try:
            candidates = read_candidates(path)
            winner = random.choice(candidates)
        except FileNotFoundError:
            if verbose:
                print(f"lucky could not read file: {describe(path)}")
            continue
        except IndexError:
            if verbose:
                print(f"lucky found an empty file: {describe(path)}")
            continue
        if spin and sys.stdout.isatty() and len(set(candidates)) > 1:
            spin_through(candidates)
        print_winner(winner, art, font)
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


def spin_through(candidates: list[str], duration: float = 2.0):
    """Flash random candidates on one line, slowing down like a wheel of fortune."""
    delay, elapsed = 0.03, 0.0
    try:
        while elapsed < duration:
            sys.stdout.write(f"\r\033[K{random.choice(candidates)}")
            sys.stdout.flush()
            time.sleep(delay)
            elapsed += delay
            delay *= 1.15
    finally:
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()


def print_winner(winner: str, art: bool, font: str):
    """Print the winner, artsy if asked."""
    tprint(winner, font=font) if art else print(winner)


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
