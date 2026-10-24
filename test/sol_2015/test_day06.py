"""Day 6 examples: inclusive rectangles, on/off state, and brightness.

Each parametrized case starts with a fresh grid. The example file combines the
three part-one commands in order. Part two remains skipped until implemented.
Run: mise run test test/sol_2015/test_day06.py
"""

from pathlib import Path

import pytest

from src.sol_2015.day06 import solution

EXAMPLE = Path(__file__).resolve().parents[2] / "examples/2015/day06.txt"


def test_part1() -> None:
    # All on, first row toggled off, then the central four turned off.
    text = EXAMPLE.read_text(encoding="utf-8")
    assert solution.part1(solution.parse(text)) == 998_996


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("turn on 0,0 through 999,999", 1_000_000),
        ("toggle 0,0 through 999,0", 1_000),
        ("turn off 499,499 through 500,500", 0),
        ("turn on 0,0 through 2,2", 9),
        ("turn on 999,999 through 999,999", 1),
        ("turn on 0,0 through 0,0\nturn on 0,0 through 0,0", 1),
        ("toggle 0,0 through 0,0\ntoggle 0,0 through 0,0", 0),
        ("", 0),
    ],
)
def test_part1_examples(text: str, expected: int) -> None:
    assert solution.part1(solution.parse(text)) == expected


@pytest.mark.parametrize(
    ("command", "action"),
    [("turn on", "on"), ("turn off", "off"), ("toggle", "toggle")],
)
def test_parse_commands(command: str, action: str) -> None:
    assert list(solution.parse(f"{command} 0,1 through 998,999\n")) == [
        (action, (0, 1), (998, 999))
    ]


@pytest.mark.parametrize(
    "line",
    [
        "dance on 0,0 through 1,1",
        "turn blink 0,0 through 1,1",
        "toggle 0,0 instead 1,1",
        "toggle",
        "toggle 0,0 through 1,1 extra",
        "",
    ],
)
def test_invalid_command_reports_line(line: str) -> None:
    with pytest.raises(ValueError, match="line 2:"):
        list(solution.parse(f"turn on 0,0 through 0,0\n{line}\n"))


@pytest.mark.parametrize(
    "text",
    [
        "toggle a,0 through 1,1",
        "toggle 0 through 1,1",
        "toggle 0,0,0 through 1,1",
        "toggle 0,0 through 1",
    ],
)
def test_invalid_coordinate_format(text: str) -> None:
    with pytest.raises(ValueError, match="line 1: expected coordinates"):
        list(solution.parse(text))


@pytest.mark.parametrize(
    "text",
    [
        "toggle -1,0 through 1,1",
        "toggle 0,0 through 1000,1",
        "toggle 0,0 through 1,1000",
        "toggle 2,0 through 1,1",
        "toggle 0,2 through 1,1",
    ],
)
def test_coordinates_must_be_in_bounds_and_ordered(text: str) -> None:
    with pytest.raises(ValueError, match="line 1: coordinates must be within the grid"):
        list(solution.parse(text))


def test_part2() -> None:
    # On adds 1 per light; toggle adds 2; off subtracts 1 with a floor of zero.
    text = EXAMPLE.read_text(encoding="utf-8")
    assert solution.part2(solution.parse(text)) == 1_001_996


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("turn on 0,0 through 0,0", 1),
        ("toggle 0,0 through 999,999", 2_000_000),
        ("turn off 0,0 through 999,999", 0),
        ("turn on 0,0 through 2,2", 9),
        ("turn on 999,999 through 999,999", 1),
        ("turn on 0,0 through 0,0\nturn on 0,0 through 0,0", 2),
        ("toggle 0,0 through 0,0\ntoggle 0,0 through 0,0", 4),
        (
            "turn on 0,0 through 0,0\n"
            "turn off 0,0 through 0,0\n"
            "turn off 0,0 through 0,0",
            0,
        ),
        ("", 0),
    ],
)
def test_part2_examples(text: str, expected: int) -> None:
    assert solution.part2(solution.parse(text)) == expected
