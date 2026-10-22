"""Dimension validation and wrapping paper/ribbon examples for 2015 Day 2.

Example input: examples/2015/day02.txt
Run: mise run test test/sol_2015/test_day02.py
"""

from pathlib import Path

import pytest

from src.sol_2015.day02 import Box, solution

EXAMPLE = Path(__file__).resolve().parents[2] / "examples/2015/day02.txt"


def test_parse_boxes() -> None:
    assert list(solution.parse("2x3x4\n1x1x10\n")) == [Box(2, 3, 4), Box(1, 1, 10)]


def test_empty_input() -> None:
    assert list(solution.parse("")) == []


@pytest.mark.parametrize("line", ["2x3", "2x3x4x5", "2xnopex4", ""])
def test_invalid_dimensions_report_line(line: str) -> None:
    with pytest.raises(ValueError, match="line 2: expected three integers"):
        list(solution.parse(f"2x3x4\n{line}\n"))


@pytest.mark.parametrize("line", ["0x3x4", "2x-3x4"])
def test_dimensions_must_be_positive(line: str) -> None:
    with pytest.raises(ValueError, match="line 1: box dimensions must be positive"):
        list(solution.parse(line))


def test_part1() -> None:
    assert solution.part1(solution.parse(EXAMPLE.read_text(encoding="utf-8"))) == 58


def test_part2() -> None:
    assert solution.part2(solution.parse(EXAMPLE.read_text(encoding="utf-8"))) == 34


@pytest.mark.parametrize(
    ("text", "paper", "ribbon"),
    [
        ("1x1x10", 43, 14),
        ("2x3x4\n1x1x10", 101, 48),
        ("4x2x3", 58, 34),
        ("", 0, 0),
    ],
)
def test_totals(text: str, paper: int, ribbon: int) -> None:
    assert solution.part1(solution.parse(text)) == paper
    assert solution.part2(solution.parse(text)) == ribbon
