"""2016 Day 1: No Time for a Taxicab."""

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

from src.solution import Solution

type Direction = Literal["L", "R"]
type Coordinate = tuple[int, int]


@dataclass(frozen=True)
class Turn:
    direction: Direction
    distance: int


type Data = Iterable[Turn]

# North, east, south, west: a right turn moves forward through this tuple.
DIRECTIONS: tuple[Coordinate, ...] = ((0, 1), (1, 0), (0, -1), (-1, 0))


class Puzzle(Solution[Data]):
    def parse(self, text: str) -> Data:
        """Yield validated turns and distances from comma-separated instructions."""
        if not text.strip():
            return
        for number, piece in enumerate(text.strip().split(","), start=1):
            piece = piece.strip()
            if piece.startswith("R"):
                direction: Direction = "R"
            elif piece.startswith("L"):
                direction = "L"
            else:
                raise ValueError(
                    f"instruction {number}: expected a turn starting with L or R"
                )
            try:
                distance = int(piece[1:])
            except ValueError as error:
                raise ValueError(
                    f"instruction {number}: expected an integer distance after the turn"
                ) from error
            if distance < 0:
                raise ValueError(f"instruction {number}: distance must not be negative")
            yield Turn(direction, distance)

    def part1(self, data: Data) -> int:
        """Return the Manhattan distance after following every turn and move."""
        x, y = 0, 0
        facing = 0
        for turn in data:
            if turn.direction == "R":
                facing = (facing + 1) % 4
            else:
                facing = (facing - 1) % 4
            dx, dy = DIRECTIONS[facing]
            x += dx * turn.distance
            y += dy * turn.distance
        return abs(x) + abs(y)

    def part2(self, data: Data) -> int:
        """Return the first revisit's distance; raise if no location is revisited."""
        x, y = 0, 0
        facing = 0
        visited: set[Coordinate] = {(0, 0)}
        for turn in data:
            if turn.direction == "R":
                facing = (facing + 1) % 4
            else:
                facing = (facing - 1) % 4
            dx, dy = DIRECTIONS[facing]
            # A repeated location can occur before the instruction's endpoint.
            for _ in range(turn.distance):
                x += dx
                y += dy
                position = (x, y)
                if position in visited:
                    return abs(x) + abs(y)
                visited.add(position)
        raise ValueError("No location visited twice")


solution = Puzzle(
    year=2016,
    day=1,
    title="No Time for a Taxicab",
)
