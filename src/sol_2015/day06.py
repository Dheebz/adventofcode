"""2015 Day 6: Probably a Fire Hazard."""

from collections.abc import Iterable

from src.solution import Solution

type Coordinate = tuple[int, int]
type Instruction = tuple[str, Coordinate, Coordinate]
type Data = Iterable[Instruction]
type LightGrid = list[list[bool]]
type BrightnessGrid = list[list[int]]
GRID_SIZE: tuple[int, int] = (1000, 1000)


class Puzzle(Solution[Data]):
    def parse(self, text: str) -> Data:
        """Yield validated light commands with inclusive rectangle corners."""
        for number, line in enumerate(text.splitlines(), start=1):
            parts = line.split()
            if len(parts) == 4 and parts[0] == "toggle":
                action = "toggle"
                start, separator, end = parts[1:]
            elif len(parts) == 5 and parts[0] == "turn" and parts[1] in ("on", "off"):
                action = parts[1]
                start, separator, end = parts[2:]
            else:
                raise ValueError(
                    f"line {number}: expected 'turn on', 'turn off', or 'toggle' "
                    "followed by two coordinates separated by 'through'"
                )
            if separator != "through":
                raise ValueError(
                    f"line {number}: expected 'through' between coordinates"
                )
            try:
                start_x, start_y = map(int, start.split(","))
                end_x, end_y = map(int, end.split(","))
            except ValueError as error:
                raise ValueError(
                    f"line {number}: expected coordinates containing two integers, "
                    "e.g. 0,0"
                ) from error
            if not (
                0 <= start_x <= end_x < GRID_SIZE[0]
                and 0 <= start_y <= end_y < GRID_SIZE[1]
            ):
                raise ValueError(
                    f"line {number}: coordinates must be within the grid "
                    "and start must not exceed end"
                )
            yield (action, (start_x, start_y), (end_x, end_y))

    def part1(self, data: Data) -> int:
        """Count lights left on after applying each inclusive rectangle command."""
        grid: LightGrid = []
        for _ in range(GRID_SIZE[0]):
            row: list[bool] = [False] * GRID_SIZE[1]
            grid.append(row)

        for action, (x1, y1), (x2, y2) in data:
            for x in range(x1, x2 + 1):
                row = grid[x]
                for y in range(y1, y2 + 1):
                    if action == "toggle":
                        row[y] = not row[y]
                    elif action == "on":
                        row[y] = True
                    elif action == "off":
                        row[y] = False
                    else:
                        raise ValueError(f"Unknown light action: {action!r}")
        return sum(sum(row) for row in grid)

    def part2(self, data: Data) -> int:
        """Return total brightness, keeping each light at or above zero."""
        grid: BrightnessGrid = []
        for _ in range(GRID_SIZE[0]):
            row: list[int] = [0] * GRID_SIZE[1]
            grid.append(row)
        for action, (x1, y1), (x2, y2) in data:
            for x in range(x1, x2 + 1):
                row = grid[x]
                for y in range(y1, y2 + 1):
                    if action == "toggle":
                        row[y] += 2
                    elif action == "on":
                        row[y] += 1
                    elif action == "off":
                        row[y] = max(0, row[y] - 1)
                    else:
                        raise ValueError(f"Unknown light action: {action!r}")
        return sum(sum(row) for row in grid)


solution = Puzzle(
    year=2015,
    day=6,
    title="Probably a Fire Hazard",
)
