"""2015 Day 3: Perfectly Spherical Houses in a Vacuum."""

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
type Data = Iterable[Coordinate]


class Puzzle(Solution[Data]):
    def parse(self, text: str) -> Data:
        """Yield a movement offset per character, allowing a trailing file newline."""
        instructions = text.rstrip("\r\n")
        for position, instruction in enumerate(instructions, start=1):
            if instruction not in DIRECTION_MAP:
                raise ValueError(
                    f"expected '^', 'v', '<', or '>' at position {position}, "
                    f"got {instruction!r}"
                )
            yield DIRECTION_MAP[instruction]

    def part1(self, data: Data) -> int:
        """Count unique houses visited by Santa, including the starting house."""
        position: Coordinate = Coordinate(0, 0)
        visited: set[Coordinate] = {position}
        for instruction in data:
            position = Coordinate(
                position.x + instruction.x, position.y + instruction.y
            )
            visited.add(position)
        return len(visited)

    def part2(self, data: Data) -> int:
        """Count unique houses visited by Santa and Robo-Santa taking turns."""
        positions: list[Coordinate] = [Coordinate(0, 0) for _ in range(2)]
        visited: set[Coordinate] = {Coordinate(0, 0)}
        for step, instruction in enumerate(data):
            idx = step % 2
            positions[idx] = Coordinate(
                positions[idx].x + instruction.x, positions[idx].y + instruction.y
            )
            visited.add(positions[idx])
        return len(visited)


solution = Puzzle(
    year=2015,
    day=3,
    title="Perfectly Spherical Houses in a Vacuum",
)
