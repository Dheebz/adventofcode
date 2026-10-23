"""Fill in the title and puzzle methods; run with mise run solution YEAR DAY."""

from collections.abc import Iterable
from dataclasses import dataclass

from src.solution import Solution


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


DIRECTION_MAP: dict[str, Coordinate] = {
    "^": Coordinate(0, 1),
    "v": Coordinate(0, -1),
    "<": Coordinate(-1, 0),
    ">": Coordinate(1, 0),
}
# Change the item type to fit the puzzle: int, a dataclass, etc.
type Data = Iterable[Coordinate]


class Puzzle(Solution[Data]):
    def parse(self, text: str) -> Data:
        """Yield one item per input line. Convert or validate each item here."""
        instructions = text.strip("\r\n")
        for position, instruction in enumerate(instructions, start=1):
            if instruction not in ("v^<>"):
                raise ValueError(
                    f"expected '(' or ')' at position {position}, got {instruction!r}"
                )
            yield DIRECTION_MAP[instruction]

    def part1(self, data: Data) -> int:
        """Solve part one and return its answer."""
        position: Coordinate = Coordinate(0, 0)
        visited: set[Coordinate] = {position}
        for instruction in data:
            position = Coordinate(
                position.x + instruction.x, position.y + instruction.y
            )
            visited.add(position)
        return len(visited)

    def part2(self, data: Data) -> int:
        """Solve part two and return its answer."""
        position: list[Coordinate] = [Coordinate(0, 0) for _ in range(2)]
        visited: set[Coordinate] = {Coordinate(0, 0)}
        for step, instruction in enumerate(data):
            idx = step % 2
            position[idx] = Coordinate(
                position[idx].x + instruction.x, position[idx].y + instruction.y
            )
            visited.add(position[idx])
        return len(visited)


# The new command fills these in. You can also edit the title here later.
solution = Puzzle(
    year=2015,
    day=3,
    title="Perfectly Spherical Houses in a Vacuum",
)
