"""Fill in the title and puzzle methods; run with mise run solution YEAR DAY."""

from collections.abc import Iterable

from src.solution import Solution

# Change the item type to fit the puzzle: int, a dataclass, etc.
type Data = Iterable[str]


class Puzzle(Solution[Data]):
    def parse(self, text: str) -> Data:
        """Yield one item per input line. Convert or validate each item here."""
        yield from text.splitlines()

    def part1(self, data: Data) -> int | str:
        """Solve part one and return its answer."""
        raise NotImplementedError

    def part2(self, data: Data) -> int | str:
        """Solve part two and return its answer."""
        raise NotImplementedError


# The new command fills these in. You can also edit the title here later.
solution = Puzzle(
    year=0,
    day=0,
    title="Untitled puzzle",
)
