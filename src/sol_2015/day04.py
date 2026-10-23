"""Fill in the title and puzzle methods; run with mise run solution YEAR DAY."""

import hashlib

from src.solution import Solution

# Change the item type to fit the puzzle: int, a dataclass, etc.
type Data = str


class Puzzle(Solution[Data]):
    def parse(self, text: str) -> Data:
        """Yield one item per input line. Convert or validate each item here."""
        key = text.strip("\r\n")
        return key

    def part1(self, data: Data) -> int | str:
        """Solve part one and return its answer."""
        number: int = 0
        while True:
            number += 1
            digest = hashlib.md5(f"{data}{number}".encode()).hexdigest()
            if digest.startswith("0" * 5):
                return number

    def part2(self, data: Data) -> int | str:
        """Solve part two and return its answer."""
        number: int = 0
        while True:
            number += 1
            digest = hashlib.md5(f"{data}{number}".encode()).hexdigest()
            if digest.startswith("0" * 6):
                return number


# The new command fills these in. You can also edit the title here later.
solution = Puzzle(
    year=2015,
    day=4,
    title="The Ideal Stocking Stuffer",
)
