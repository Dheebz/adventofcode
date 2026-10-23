"""Movement parsing, route examples, and alternating delivery for 2015 Day 3.

Example input: examples/2015/day03.txt
Run: mise run test test/sol_2015/test_day03.py
"""

from pathlib import Path

import pytest

from src.sol_2015.day03 import Coordinate, solution

EXAMPLE = Path(__file__).resolve().parents[2] / "examples/2015/day03.txt"


def test_part1() -> None:
    assert solution.part1(solution.parse(EXAMPLE.read_text(encoding="utf-8"))) == 4


def test_part2() -> None:
    assert solution.part2(solution.parse(EXAMPLE.read_text(encoding="utf-8"))) == 3


def test_parse_direction_offsets() -> None:
    assert list(solution.parse("^v<>")) == [
        Coordinate(0, 1),
        Coordinate(0, -1),
        Coordinate(-1, 0),
        Coordinate(1, 0),
    ]


@pytest.mark.parametrize(
    ("text", "santa_houses", "shared_houses"),
    [
        ("", 1, 1),
        (">", 2, 2),
        ("^v", 2, 3),
        ("^>v<", 4, 3),
        ("^v^v^v^v^v", 2, 11),
        (">>>", 4, 3),
        ("^^>>vv<<", 8, 4),
    ],
)
def test_routes(text: str, santa_houses: int, shared_houses: int) -> None:
    assert solution.part1(solution.parse(text)) == santa_houses
    assert solution.part2(solution.parse(text)) == shared_houses


@pytest.mark.parametrize("ending", ["\n", "\r\n"])
def test_trailing_newline(ending: str) -> None:
    assert list(solution.parse(">" + ending)) == [Coordinate(1, 0)]


@pytest.mark.parametrize("text", ["^x", "^ ", "^\n>"])
def test_invalid_direction_reports_position(text: str) -> None:
    with pytest.raises(ValueError, match="expected.*at position 2"):
        list(solution.parse(text))


def test_leading_newline_is_not_an_instruction() -> None:
    with pytest.raises(ValueError, match="at position 1"):
        list(solution.parse("\n>"))
