"""2015 Day 5: Doesn't He Have Intern-Elves For This?"""

from collections.abc import Iterable
from itertools import pairwise

from src.solution import Solution

type Data = Iterable[str]

VOWELS: set[str] = set("aeiou")
FORBIDDEN: set[str] = {"ab", "cd", "pq", "xy"}


class Puzzle(Solution[Data]):
    def parse(self, text: str) -> Data:
        """Yield each candidate string without changing its characters."""
        yield from text.splitlines()

    def part1(self, data: Data) -> int:
        """Count strings with at least three vowels, a double, and no forbidden pair."""
        nice_count: int = 0
        for text in data:
            vowel_count = sum(1 for character in text if character in VOWELS)
            has_double = any(left == right for left, right in pairwise(text))
            has_forbidden = any(pair in text for pair in FORBIDDEN)
            if not has_forbidden and has_double and vowel_count >= 3:
                nice_count += 1
        return nice_count

    def part2(self, data: Data) -> int:
        """Count strings with a non-overlapping repeated pair and a gapped repeat."""
        nice_count: int = 0
        for text in data:
            pair_twice: bool = False
            for index in range(len(text) - 1):
                pair = text[index : index + 2]
                # Search after both characters: "aaa" overlaps, "aaaa" does not.
                if pair in text[index + 2 :]:
                    pair_twice = True
                    break
            # Only the outer characters must match; the middle can match too.
            repeat_with_gap = any(
                text[index] == text[index + 2] for index in range(len(text) - 2)
            )
            if pair_twice and repeat_with_gap:
                nice_count += 1
        return nice_count


solution = Puzzle(
    year=2015,
    day=5,
    title="Doesn't He Have Intern-Elves For This?",
)
