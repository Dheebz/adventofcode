"""The puzzle's published examples and a few input edge cases."""

from pathlib import Path

import pytest

from src.sol_2015.day01 import solution

EXAMPLE = Path(__file__).resolve().parents[2] / "examples/2015/day01.txt"


def test_example_file() -> None:
    text = EXAMPLE.read_text(encoding="utf-8")
    assert solution.part1(solution.parse(text)) == -1
    assert solution.part2(solution.parse(text)) == 5


@pytest.mark.parametrize(
    ("text", "floor"),
    [
        ("(())", 0),
        ("()()", 0),
        ("(((", 3),
        ("(()(()(", 3),
        ("))(((((", 3),
        ("())", -1),
        ("))(", -1),
        (")))", -3),
        (")())())", -3),
        ("", 0),
    ],
)
def test_part1(text: str, floor: int) -> None:
    assert solution.part1(solution.parse(text)) == floor


@pytest.mark.parametrize(("text", "position"), [(")", 1), ("()())", 5)])
def test_part2(text: str, position: int) -> None:
    assert solution.part2(solution.parse(text)) == position


@pytest.mark.parametrize("text", ["", "(())", "((("])
def test_never_enters_basement(text: str) -> None:
    assert solution.part2(solution.parse(text)) is None


@pytest.mark.parametrize("text", ["()())\n", "()())\r\n"])
def test_trailing_newline(text: str) -> None:
    assert list(solution.parse(text)) == list("()())")


@pytest.mark.parametrize("text", ["()x", "() ", "()\n()"])
def test_invalid_instruction(text: str) -> None:
    with pytest.raises(ValueError, match="position 3"):
        list(solution.parse(text))
