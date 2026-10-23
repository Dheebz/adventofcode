"""2015 Day 4: The Ideal Stocking Stuffer."""

import hashlib

from src.solution import Solution

type Data = str


def cracker(data: Data, prefix: str, *, max_attempts: int = 10_000_000) -> int:
    """Find the first matching suffix from 1 through max_attempts, inclusive."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    if not 1 <= len(prefix) <= 32 or any(
        character not in "0123456789abcdef" for character in prefix
    ):
        raise ValueError("prefix must contain 1 to 32 lowercase hexadecimal characters")

    for number in range(1, max_attempts + 1):
        digest = hashlib.md5(f"{data}{number}".encode()).hexdigest()
        if digest.startswith(prefix):
            return number
    raise RuntimeError(
        f"No hash starting with {prefix!r} found after {max_attempts:,} attempts"
    )


class Puzzle(Solution[Data]):
    def parse(self, text: str) -> Data:
        """Read the secret key without surrounding file newlines."""
        key = text.strip("\r\n")
        return key

    def part1(self, data: Data) -> int:
        """Find the first suffix producing five leading zeroes."""
        return cracker(data, "00000")

    def part2(self, data: Data) -> int:
        """Find the first suffix producing six leading zeroes."""
        return cracker(data, "000000")


solution = Puzzle(
    year=2015,
    day=4,
    title="The Ideal Stocking Stuffer",
)
