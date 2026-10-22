"""2015 Day 1: Not Quite Lisp."""

from collections.abc import Iterable

from src.solution import Solution

type Data = Iterable[str]


class Puzzle(Solution[Data]):
    def parse(self, text: str) -> Data:
        """Yield parentheses, allowing a trailing file newline."""
        instructions = text.rstrip("\r\n")
        for position, instruction in enumerate(instructions, start=1):
            if instruction not in "()":
                raise ValueError(
                    f"expected '(' or ')' at position {position}, got {instruction!r}"
                )
            yield instruction

    def part1(self, instructions: Data) -> int:
        """Find the final floor: each '(' goes up and each ')' goes down."""
        return sum(1 if instruction == "(" else -1 for instruction in instructions)

    def part2(self, instructions: Data) -> int | None:
        """Find the first basement position, or None if Santa never enters it."""
        floor = 0
        for position, instruction in enumerate(instructions, start=1):
            if instruction == "(":
                floor += 1
            else:
                floor -= 1
            if floor == -1:
                return position
        return None


solution = Puzzle(year=2015, day=1, title="Not Quite Lisp")
