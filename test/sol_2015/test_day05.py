"""Examples and rule boundaries for both parts of 2015 Day 5.

Example input: examples/2015/day05.txt
Run: mise run test test/sol_2015/test_day05.py
"""

from pathlib import Path

import pytest

from src.sol_2015.day05 import solution

EXAMPLE = Path(__file__).resolve().parents[2] / "examples/2015/day05.txt"


def test_part1() -> None:
    assert solution.part1(solution.parse(EXAMPLE.read_text(encoding="utf-8"))) == 2


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("ugknbfddgicrmopn", 1),
        ("aaa", 1),
        ("jchzalrnumimnmhp", 0),
        ("haegwjzuvuyypxyu", 0),
        ("dvszwmarrgswjxmb", 0),
        ("", 0),
        ("a", 0),
        ("aa", 0),
        ("aei", 0),
    ],
)
def test_part1_rules(text: str, expected: int) -> None:
    assert solution.part1(solution.parse(text)) == expected


@pytest.mark.parametrize("pair", ["ab", "cd", "pq", "xy"])
def test_forbidden_pairs_override_other_rules(pair: str) -> None:
    assert solution.part1(solution.parse("aaa" + pair)) == 0


def test_empty_input() -> None:
    assert solution.part1(solution.parse("")) == 0
    assert solution.part2(solution.parse("")) == 0


def test_blank_lines_are_not_nice() -> None:
    assert solution.part1(solution.parse("aaa\n\nxxyxx\n")) == 1
    assert solution.part2(solution.parse("aaa\n\nxxyxx\n")) == 1


def test_part2() -> None:
    assert solution.part2(solution.parse(EXAMPLE.read_text(encoding="utf-8"))) == 2


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("qjhvhtzxzqqjkmpb", 1),
        ("xxyxx", 1),
        ("uurcxstgmygtbstg", 0),
        ("ieodomkazucvgmuy", 0),
        ("", 0),
        ("a", 0),
        ("aa", 0),
        ("aaa", 0),
        ("aaaa", 1),
        ("xyxy", 1),
        ("aabaa", 1),
        ("aabbaa", 0),
        ("abcdefe", 0),
    ],
)
def test_part2_rules(text: str, expected: int) -> None:
    assert solution.part2(solution.parse(text)) == expected


def test_parse_preserves_candidate_characters() -> None:
    assert list(solution.parse("aaa \r\nxxyxx\r\n")) == ["aaa ", "xxyxx"]
