"""Extend Solution[Data] with parse, part1, and part2 for each puzzle."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Solution[Data]:
    """Puzzle metadata and methods; the runner supplies file contents to parse."""

    year: int
    day: int
    title: str

    def __str__(self) -> str:
        return f"{self.year} · Day {self.day:02} · {self.title}"

    def parse(self, text: str) -> Data:
        """Convert input text into the data needed by each part."""
        raise NotImplementedError

    def part1(self, data: Data, /) -> int | str | None:
        """Return part one's answer, or leave unimplemented while solving."""
        raise NotImplementedError

    def part2(self, data: Data, /) -> int | str | None:
        """Return part two's answer, or leave unimplemented while solving."""
        raise NotImplementedError
