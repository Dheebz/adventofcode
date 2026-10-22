"""Small command-line runner and day generator. No runtime dependencies."""

import argparse
import importlib.util
import json
import sys
from collections.abc import Iterator
from pathlib import Path

from src.solution import Solution

ROOT = Path(__file__).resolve().parent.parent


class PuzzleError(Exception):
    """An expected setup or input error that can be shown without a traceback."""


def validate_date(year: int, day: int) -> None:
    if year < 2015:
        raise PuzzleError("Year must be 2015 or later.")
    if not 1 <= day <= 25:
        raise PuzzleError("Day must be between 1 and 25.")


def new_day(year: int, day: int, title: str = "Untitled puzzle") -> list[Path]:
    """Create a solution, example, tests, and private input without overwriting."""
    validate_date(year, day)
    name = f"day{day:02}"
    test_template = (ROOT / "templates/test_day.py.txt").read_text(encoding="utf-8")
    files = {
        ROOT / f"src/sol_{year}/{name}.py": (ROOT / "src/template.py")
        .read_text(encoding="utf-8")
        .replace("year=0", f"year={year}")
        .replace("day=0", f"day={day}")
        .replace('"Untitled puzzle"', json.dumps(title, ensure_ascii=False)),
        ROOT / f"test/sol_{year}/test_{name}.py": test_template.replace(
            "{{YEAR}}", str(year)
        ).replace("{{DAY}}", f"{day:02}"),
        ROOT / f"examples/{year}/{name}.txt": "",
        ROOT / f"inputs/{year}/{name}.txt": "",
    }
    for path in files:
        if path.exists():
            raise PuzzleError(
                f"Already exists: {path.relative_to(ROOT)}. Nothing changed."
            )
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as file:
            file.write(content)
    return list(files)


def load_solution(year: int, day: int) -> Solution:
    path = ROOT / f"src/sol_{year}/day{day:02}.py"
    if not path.is_file():
        raise PuzzleError(
            f"No solution for {year} day {day}. "
            f"Create it: python main.py new {year} {day}"
        )
    name = f"src.sol_{year}.day{day:02}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise PuzzleError(f"Cannot load solution: {path}")
    module = importlib.util.module_from_spec(spec)
    # Dataclasses and other decorators look up their module during import.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    solution = getattr(module, "solution", None)
    if not isinstance(solution, Solution):
        raise PuzzleError(f"{path.name} must define a solution = Puzzle(...) instance.")
    if (solution.year, solution.day) != (year, day):
        raise PuzzleError(f"{path.name}: solution year/day must match {year}/{day}.")
    return solution


def run_day(
    year: int,
    day: int,
    *,
    example: bool = False,
    input_path: Path | None = None,
    part: int | None = None,
) -> None:
    validate_date(year, day)
    solution = load_solution(year, day)
    folder = "examples" if example else "inputs"
    path = (
        input_path
        if input_path is not None
        else ROOT / f"{folder}/{year}/day{day:02}.txt"
    )
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise PuzzleError(f"Cannot read input: {path}. {error}") from error
    print(solution)
    display_path = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    print(f"Input: {display_path}")
    for number in (1, 2) if part is None else (part,):
        try:
            # Parse separately so mutations in part one cannot affect part two.
            data = solution.parse(text)
            # Consume lazy parsers here so input errors are reported before solving.
            if isinstance(data, Iterator):
                data = list(data)
        except ValueError as error:
            raise PuzzleError(f"Invalid input in {path}: {error}") from error
        solve = solution.part1 if number == 1 else solution.part2
        try:
            answer = solve(data)
        except NotImplementedError:
            print(f"Part {number}: not implemented")
        else:
            print(f"Part {number}: {answer}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create and run Advent of Code solutions."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("new", help="create a day from the templates")
    run = commands.add_parser("run", help="run a solution against a saved input")
    for command in (new, run):
        command.add_argument("year", type=int)
        command.add_argument("day", type=int)
    new.add_argument(
        "title", nargs="?", default="Untitled puzzle", help="optional puzzle title"
    )
    inputs = run.add_mutually_exclusive_group()
    inputs.add_argument("--example", action="store_true", help="use the example input")
    inputs.add_argument("--input", type=Path, help="use a specific input file")
    run.add_argument("--part", type=int, choices=(1, 2), help="run just one part")
    args = parser.parse_args(argv)
    try:
        if args.command == "new":
            for path in new_day(args.year, args.day, args.title):
                print(f"Created {path.relative_to(ROOT)}")
        else:
            run_day(
                args.year,
                args.day,
                example=args.example,
                input_path=args.input,
                part=args.part,
            )
    except (PuzzleError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0
