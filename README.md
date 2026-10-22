# Advent of Code

A small Python scaffold for solving puzzles: create a day, save the input, fill in
three methods, and run it. Typed solutions, repeatable tests, and no runtime dependencies.

## Get started

Install [mise](https://mise.jdx.dev/getting-started.html) and
[uv](https://docs.astral.sh/uv/getting-started/installation/).
Python 3.14 is selected by `.python-version`; uv can install it when missing.

```sh
mise run setup
mise run new 2015 1 "Not Quite Lisp"
```

The initial scaffold contains no puzzle solutions, tests, or input files.
`new` creates these locally:

```text
src/sol_2015/day01.py        # Puzzle class and metadata
inputs/2015/day01.txt        # Personal input; ignored by Git
examples/2015/day01.txt      # Example from the puzzle
test/sol_2015/test_day01.py  # Example tests
```

1. Save your puzzle input in the input file.
2. Fill in `parse`, `part1`, and `part2` in the solution.
3. Paste a puzzle example in the example file.
4. Replace the expected test answers and remove skip markers as you finish each part.

```sh
mise run example 2015 1
mise run solution 2015 1
mise run solution 2015 1 -- --part 1
mise run solution 2015 1 -- --input "path/to/input.txt"
mise run test test/sol_2015/test_day01.py -- -v
mise run check
```

The title is optional: `mise run new 2015 1` uses `Untitled puzzle`.
Quote titles containing spaces. Existing day files are never overwritten.
Unfinished parts print `not implemented`.

## Solution pattern

Each day extends `Solution` and exports an instance named `solution`:

```python
from collections.abc import Iterable

from src.solution import Solution

type Data = Iterable[int]


class Puzzle(Solution[Data]):
    def parse(self, text: str) -> Data:
        for line in text.splitlines():
            yield int(line)

    def part1(self, data: Data) -> int:
        return sum(data)

    def part2(self, data: Data) -> int:
        return max(data)


solution = Puzzle(year=2015, day=1, title="Puzzle title")
```

This illustrates the structure using numbers; it is not a solution to Day 1.
`Data` describes what the parser returns and the parts accept. The template uses
`Iterable[str]`; change the item type to suit the puzzle, such as `int` or a `Box`
dataclass. Other data structures, such as grids, are also supported.

`yield` produces items one at a time. The runner collects generator output before
solving so malformed input is reported even when a part would stop early. Each
part is parsed independently. In direct tests, call `parse(text)` separately for
each part; a generator can only be consumed once. Use `list(solution.parse(text))`
to inspect parsed items or exercise validation.

The base class supplies the constructor and the heading. Puzzle methods contain
the calculations and return an integer, string, or `None` when no answer exists.
The runner handles file reading and printing.

## Input and output

| Task | Input |
| --- | --- |
| `mise run solution YEAR DAY` | `inputs/YEAR/dayDD.txt` |
| `mise run example YEAR DAY` | `examples/YEAR/dayDD.txt` |
| `mise run solution YEAR DAY -- --input custom.txt` | `custom.txt` |

Mise tasks run from the repository root. Relative custom paths are relative to
that root. `--example` and `--input` cannot be combined.

After implementing Day 1, its `()())` example would print:

```text
2015 · Day 01 · Not Quite Lisp
Input: examples/2015/day01.txt
Part 1: -1
Part 2: 5
```

Text reaches `parse` unchanged. Choose `splitlines()`, `split()`, or `split("\n\n")`
to match the puzzle; only remove whitespace when the puzzle permits it.
Raise `ValueError` with a useful message for invalid input. The runner displays
short input errors; unexpected calculation errors retain their tracebacks.

Personal inputs stay local and are ignored by Git. Commit examples alongside the
solution and tests so checks can run without your personal input or AoC credentials.

## Tests and checks

The generated tests are skipped placeholders. Replace `0` with the expected
answer and remove each `@pytest.mark.skip(...)` line as you implement that part.
Keep the names `test_part1` and `test_part2`; CI checks that both are collected.
For multiple examples, use parametrization:

```python
import pytest

from src.sol_2015.day01 import solution


@pytest.mark.parametrize(
    ("text", "floor"),
    [("(())", 0), ("(((", 3), ("())", -1)],
)
def test_part1(text: str, floor: int) -> None:
    assert solution.part1(solution.parse(text)) == floor
```

During development, local tests allow skipped unfinished parts. An empty scaffold
also passes with an explicit message that no solutions or tests exist yet.
CI requires example files and tests for both parts of every committed solution,
rejects skipped/expected-failure tests, and fails if solutions have no tests.
Day-only changes run the affected days' tests. Shared framework, configuration,
or dependency changes run the full suite. Lint, formatting, and types always
cover the whole project.


## Commands

| Task | Purpose |
| --- | --- |
| `mise run setup` | Install development dependencies using `uv.lock` |
| `mise run new YEAR DAY ["Title"]` | Create a solution, input, example, and tests |
| `mise run solution YEAR DAY` | Run with personal input |
| `mise run example YEAR DAY` | Run with example input |
| `mise run test` | Run all tests; append a path to select a day |
| `mise run lint` | Check code with Ruff |
| `mise run format` | Format Python files in place |
| `mise run format-check` | Check formatting without changing files |
| `mise run types` | Check types with ty |
| `mise run check` | Run tests, lint, formatting checks, and type checks |

`mise tasks` lists the commands. Use `--` before forwarded options such as `-v`
or `--part`. Mise is a thin wrapper; equivalent uv commands work directly:

```sh
uv sync
uv run python -B main.py new 2015 1 "Not Quite Lisp"
uv run python -B main.py run 2015 1 --example
uv run python -B scripts/check_tests.py
uv run ruff check --no-cache .
uv run ruff format --no-cache --check .
uv run ty check
```

For runner help, use `uv run python -B main.py --help`.
Normal uv commands use the lockfile and update it if dependency settings change.
CI uses `--locked` to reject unexpected lockfile changes.

Mise disables Python bytecode and Ruff caches. Pytest's disk cache is disabled
in `pyproject.toml`. When running outside mise, use `python -B` and Ruff's
`--no-cache` as shown above to keep generated cache folders out of the project.

## Layout

```text
.github/workflows/ci.yml     # Required quality check
.github/main-protection.json # Settings to apply to GitHub's main branch
main.py                     # CLI entry point
mise.toml                   # Task shortcuts
pyproject.toml              # Version, dependencies, and tool settings
uv.lock                     # Resolved development dependencies
scripts/check_tests.py      # Local tests and strict CI validation
src/aoc.py                  # Day generation, input loading, and execution
src/solution.py             # Base class and puzzle metadata
src/template.py             # Solution template
templates/test_day.py.txt   # Test template
```

