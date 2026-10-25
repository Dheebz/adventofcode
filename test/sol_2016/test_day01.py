"""Turn parsing, Manhattan distances, and first revisits for 2016 Day 1.

Example input: examples/2016/day01.txt
Run: mise run test test/sol_2016/test_day01.py
"""

from pathlib import Path

import pytest

from src.sol_2016.day01 import Turn, solution

EXAMPLE = Path(__file__).resolve().parents[2] / "examples/2016/day01.txt"


def test_part1() -> None:
    text = EXAMPLE.read_text(encoding="utf-8")
    assert solution.part1(solution.parse(text)) == 8


def test_part2() -> None:
    text = EXAMPLE.read_text(encoding="utf-8")
    assert solution.part2(solution.parse(text)) == 4


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("R2, L3", 5),
        ("R2, R2, R2", 2),
        ("R5, L5, R5, R3", 12),
        ("L2, L2, L2", 2),
        ("L1, L1, L1, L1", 0),
        ("R0, R2", 2),
        ("", 0),
    ],
)
def test_part1_routes(text: str, expected: int) -> None:
    assert solution.part1(solution.parse(text)) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("R8, R4, R4, R8", 4),
        ("R1, R1, R1, R1", 0),
        ("L1, L1, L1, L1", 0),
        ("R1, R1, R1, R1, R5", 0),
    ],
)
def test_first_revisit(text: str, expected: int) -> None:
    assert solution.part2(solution.parse(text)) == expected


@pytest.mark.parametrize("text", ["", "R2, L3", "R0, R0, R0, R0"])
def test_no_location_revisited(text: str) -> None:
    with pytest.raises(ValueError, match="No location visited twice"):
        solution.part2(solution.parse(text))


def test_parse_turns() -> None:
    assert list(solution.parse(" R2,\n L3, R0\n")) == [
        Turn("R", 2),
        Turn("L", 3),
        Turn("R", 0),
    ]


def test_empty_input() -> None:
    assert list(solution.parse("\n ")) == []


@pytest.mark.parametrize("text", ["X2", "R", "Lnope", "L-1", ",R2", "R2,,L3", "R2,"])
def test_invalid_instruction(text: str) -> None:
    with pytest.raises(ValueError, match="instruction [123]:"):
        list(solution.parse(text))


def test_invalid_instruction_reports_position() -> None:
    with pytest.raises(ValueError, match="instruction 2:"):
        list(solution.parse("R2, X3"))
