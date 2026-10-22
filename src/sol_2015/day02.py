"""2015 Day 2: I Was Told There Would Be No Math."""

from collections.abc import Iterable
from dataclasses import dataclass

from src.solution import Solution


@dataclass(frozen=True)
class Box:
    length: int
    width: int
    height: int


type Data = Iterable[Box]


class Puzzle(Solution[Data]):
    def parse(self, text: str) -> Data:
        """Yield boxes from lines of positive dimensions, e.g. 2x3x4."""
        for number, line in enumerate(text.splitlines(), start=1):
            try:
                length, width, height = map(int, line.split("x"))
            except ValueError as error:
                raise ValueError(
                    f"line {number}: expected three integers, e.g. 2x3x4"
                ) from error
            if min(length, width, height) <= 0:
                raise ValueError(f"line {number}: box dimensions must be positive")
            yield Box(length, width, height)

    def part1(self, data: Data) -> int:
        """Total wrapping paper: surface area plus the smallest face for slack."""
        total: int = 0
        for box in data:
            a: int = box.length * box.width
            b: int = box.width * box.height
            c: int = box.height * box.length
            slack: int = min(a, b, c)
            total += (2 * a) + (2 * b) + (2 * c) + slack
        return total

    def part2(self, data: Data) -> int:
        """Total ribbon: the smallest perimeter plus the volume for the bow."""
        total: int = 0
        for box in data:
            a, b, c = sorted((box.length, box.width, box.height))
            bow = a * b * c
            wrap = 2 * (a + b)
            total += bow + wrap
        return total


solution = Puzzle(
    year=2015,
    day=2,
    title="I Was Told There Would Be No Math",
)
