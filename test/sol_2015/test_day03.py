"""Set expected answers and remove skip markers as each part is implemented.

Example input: examples/2015/day03.txt
Run: mise run test test/sol_2015/test_day03.py
"""

from pathlib import Path

from src.sol_2015.day03 import solution

EXAMPLE = Path(__file__).resolve().parents[2] / "examples/2015/day03.txt"


def test_part1() -> None:
    assert solution.part1(solution.parse(EXAMPLE.read_text(encoding="utf-8"))) == 4


def test_part2() -> None:
    assert solution.part2(solution.parse(EXAMPLE.read_text(encoding="utf-8"))) == 3
