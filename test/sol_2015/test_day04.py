"""Day 4 answers and bounded-search validation.

Example input: examples/2015/day04.txt
Run: mise run test test/sol_2015/test_day04.py
"""

from pathlib import Path

import pytest

from src.sol_2015.day04 import cracker, solution

EXAMPLE = Path(__file__).resolve().parents[2] / "examples/2015/day04.txt"


def test_part1() -> None:
    assert solution.part1(solution.parse(EXAMPLE.read_text(encoding="utf-8"))) == 609043


def test_part2() -> None:
    assert (
        solution.part2(solution.parse(EXAMPLE.read_text(encoding="utf-8"))) == 6742839
    )


def test_first_candidate_is_included() -> None:
    assert cracker("abcdef", "5f8b62a2dced0cd28946a9c891ff3e5e", max_attempts=2) == 1


def test_last_allowed_candidate_is_included() -> None:
    assert cracker("abcdef", "cba0", max_attempts=2) == 2


def test_search_budget_exhausted() -> None:
    with pytest.raises(
        RuntimeError, match="No hash starting with '3db9' found after 2 attempts"
    ):
        cracker("abcdef", "3db9", max_attempts=2)


@pytest.mark.parametrize("max_attempts", [0, -1])
def test_invalid_budget(max_attempts: int) -> None:
    with pytest.raises(ValueError, match="max_attempts must be positive"):
        cracker("abcdef", "00000", max_attempts=max_attempts)


@pytest.mark.parametrize("prefix", ["", "xyz", "ABC", "0" * 33, "0 0", "0\n"])
def test_invalid_prefix(prefix: str) -> None:
    with pytest.raises(ValueError, match="1 to 32 lowercase hexadecimal characters"):
        cracker("abcdef", prefix)
