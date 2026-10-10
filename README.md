# 🍀 lucky

Choose a lucky winner!

The lucky winner is selected randomly as one of the lines of a file. By default, it tries `.lucky`, starting from the current directory and trying parent directories until it reaches the home directory.

Lucky's behavior can be configured, use `--help` for detailed instructions!

## Installation

Lucky requires Python 3.12 or newer and is installed with [`uv`](https://docs.astral.sh/uv/). Clone the repository and install it as a tool:

```sh
git clone https://github.com/wdumez/lucky.git
cd lucky
uv tool install .
```

This puts the `lucky` command on your `PATH`. To uninstall it, run:

```sh
uv tool uninstall lucky
```

## Usage

Create a `.lucky` file with one candidate per line:

```
Alice
Bob
Carol
```

Then let fate decide:

```sh
lucky
```

By default, the winner is shown with fancy ASCII art. To read from a different file, pass it as an argument:

```sh
lucky path/to/candidates.txt
```

### Options

| Option                       | Description                                                   | Default        |
| ---------------------------- | ------------------------------------------------------------- | -------------- |
| `FILE`                       | The file to read the lucky winner from                        | `.lucky`       |
| `--art` / `--no-art`         | Whether to show the winner with fancy ASCII art               | `--art`        |
| `--recurse` / `--no-recurse` | Whether to recursively search parent directories for the file | `--recurse`    |
| `--verbose` / `--no-verbose` | Whether to print error messages during execution              | `--no-verbose` |

Run `lucky --help` for the full details.

### Exit status

Lucky exits with `0` when a winner was chosen and with `1` if it could not find a valid lucky file. Use `--verbose` to see which files it tried and why they were skipped.

## License

Lucky is released under the [MIT License](LICENSE).
