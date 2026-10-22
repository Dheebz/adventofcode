"""Exercise the framework without creating puzzle files in the repository."""

from pathlib import Path
from textwrap import indent

import pytest

from src import aoc


@pytest.fixture
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for name in ("src/template.py", "templates/test_day.py.txt"):
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            (aoc.ROOT / name).read_text(encoding="utf-8"), encoding="utf-8"
        )
    monkeypatch.setattr(aoc, "ROOT", tmp_path)
    return tmp_path


def write_puzzle(path: Path, methods: str) -> None:
    path.write_text(
        "from src.solution import Solution\n\nclass Puzzle(Solution):\n"
        + indent(methods, "    ")
        + '\nsolution = Puzzle(year=2024, day=1, title="Test puzzle")\n',
        encoding="utf-8",
    )


def test_new_day_preserves_existing_work(workspace: Path) -> None:
    paths = aoc.new_day(2024, 1)
    assert len(paths) == 4
    assert aoc.load_solution(2024, 1).title == "Untitled puzzle"
    solution = workspace / "src/sol_2024/day01.py"
    solution.write_text("# work in progress\n", encoding="utf-8")
    with pytest.raises(aoc.PuzzleError, match="Already exists"):
        aoc.new_day(2024, 1)
    assert solution.read_text(encoding="utf-8") == "# work in progress\n"
    assert "{{" not in (workspace / "test/sol_2024/test_day01.py").read_text()


def test_new_day_checks_all_targets_before_writing(workspace: Path) -> None:
    example = workspace / "examples/2024/day01.txt"
    example.parent.mkdir(parents=True)
    example.write_text("existing example", encoding="utf-8")
    with pytest.raises(aoc.PuzzleError, match="Already exists"):
        aoc.new_day(2024, 1)
    assert not (workspace / "src/sol_2024/day01.py").exists()


@pytest.mark.parametrize(("year", "day"), [(2014, 1), (2024, 0), (2024, 26)])
def test_invalid_dates(workspace: Path, year: int, day: int) -> None:
    with pytest.raises(aoc.PuzzleError):
        aoc.new_day(year, day)


@pytest.mark.parametrize("parse_body", ["return list(text)", "yield from text"])
def test_run_preserves_whitespace_and_isolates_parts(
    workspace: Path, capsys: pytest.CaptureFixture[str], parse_body: str
) -> None:
    aoc.new_day(2024, 1)
    write_puzzle(
        workspace / "src/sol_2024/day01.py",
        f"def parse(self, text):\n    {parse_body}\n"
        "def part1(self, data):\n    data.clear()\n    return 42\n"
        "def part2(self, data):\n    return len(data)\n",
    )
    (workspace / "inputs/2024/day01.txt").write_text(" a\n", encoding="utf-8")
    assert aoc.main(["run", "2024", "1"]) == 0
    output = capsys.readouterr().out
    assert "Part 1: 42" in output
    assert "Part 2: 3" in output


def test_example_custom_input_and_unfinished_part(
    workspace: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    aoc.new_day(2024, 1)
    assert aoc.main(["run", "2024", "1", "--example", "--part", "2"]) == 0
    output = capsys.readouterr().out
    assert "Part 2: not implemented" in output
    assert "Part 1:" not in output
    custom = workspace / "custom.txt"
    custom.write_text("test", encoding="utf-8")
    assert aoc.main(["run", "2024", "1", "--input", str(custom)]) == 0


@pytest.mark.parametrize(
    "title", ["Bridge Repair", 'Santa\'s "Workshop" \\ North Pole', "Étage\nDeux"]
)
def test_generated_solution_details(
    workspace: Path, capsys: pytest.CaptureFixture[str], title: str
) -> None:
    assert aoc.main(["new", "2024", "7", title]) == 0
    assert aoc.load_solution(2024, 7).title == title
    capsys.readouterr()
    assert aoc.main(["run", "2024", "7", "--example"]) == 0
    output = capsys.readouterr().out
    assert output.startswith(
        f"2024 · Day 07 · {title}\nInput: examples/2024/day07.txt\n"
    )


def test_solution_details_must_match_requested_day(
    workspace: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    aoc.new_day(2024, 1)
    path = workspace / "src/sol_2024/day01.py"
    path.write_text(
        path.read_text(encoding="utf-8").replace("year=2024", "year=2023"),
        encoding="utf-8",
    )
    assert aoc.main(["run", "2024", "1"]) == 1
    assert "solution year/day must match 2024/1" in capsys.readouterr().err


def test_missing_solution_and_input(
    workspace: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert aoc.main(["run", "2024", "1"]) == 1
    assert "No solution" in capsys.readouterr().err
    aoc.new_day(2024, 1)
    assert aoc.main(["run", "2024", "1", "--input", str(workspace / "absent")]) == 1
    assert "Cannot read input" in capsys.readouterr().err


def test_parse_errors_are_friendly_but_solver_bugs_propagate(
    workspace: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    aoc.new_day(2024, 1)
    solution = workspace / "src/sol_2024/day01.py"
    write_puzzle(
        solution,
        'def parse(self, text):\n    raise ValueError("expected a number")\n'
        "def part1(self, data):\n    return 0\n"
        "def part2(self, data):\n    return 0\n",
    )
    assert aoc.main(["run", "2024", "1"]) == 1
    assert "expected a number" in capsys.readouterr().err
    write_puzzle(
        solution,
        "def parse(self, text):\n    return text\n"
        'def part1(self, data):\n    raise ValueError("solver bug")\n'
        "def part2(self, data):\n    return 0\n",
    )
    with pytest.raises(ValueError, match="solver bug"):
        aoc.main(["run", "2024", "1"])


def test_lazy_parse_errors_are_reported_before_solving(
    workspace: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    aoc.new_day(2024, 1)
    write_puzzle(
        workspace / "src/sol_2024/day01.py",
        "def parse(self, text):\n    yield 1\n"
        '    raise ValueError("invalid second item")\n'
        "def part1(self, data):\n"
        '    raise AssertionError("must not solve invalid input")\n',
    )
    assert aoc.main(["run", "2024", "1", "--part", "1"]) == 1
    assert "invalid second item" in capsys.readouterr().err
