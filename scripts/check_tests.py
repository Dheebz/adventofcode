"""Run pytest, allowing an empty scaffold and enforcing complete puzzle tests in CI."""

import argparse
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def affected_tests(base: str | None) -> list[Path] | None:
    """Select isolated day tests; None means shared changes require the full suite."""
    if not base or not re.fullmatch(r"[0-9a-f]{40}", base) or base == "0" * 40:
        return None
    exists = subprocess.run(
        ["git", "cat-file", "-e", f"{base}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
    )
    if exists.returncode:
        return None
    diff = subprocess.run(
        ["git", "diff", "--name-only", base, "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    selected: set[Path] = set()
    patterns = (
        r"src/sol_(\d+)/day(\d{2})\.py",
        r"test/sol_(\d+)/test_day(\d{2})\.py",
        r"examples/(\d+)/day(\d{2})\.txt",
    )
    for path in diff.stdout.splitlines():
        for pattern in patterns:
            match = re.fullmatch(pattern, path)
            if match:
                year, day = match.groups()
                test = ROOT / f"test/sol_{year}/test_day{day}.py"
                if test.is_file():
                    selected.add(test.resolve())
                break
        else:
            return None
    return sorted(selected)


class PuzzleChecks:
    """Record missing part tests and skipped/expected-failure results."""

    def __init__(self, test_paths: set[Path]) -> None:
        self.test_paths = test_paths
        self.problems: list[str] = []

    def pytest_collection_finish(self, session: pytest.Session) -> None:
        for path in sorted(self.test_paths):
            names = {
                item.name.split("[", 1)[0]
                for item in session.items
                if item.path.resolve() == path
            }
            for name in ("test_part1", "test_part2"):
                if name not in names:
                    self.problems.append(
                        f"{path.relative_to(ROOT)} must collect {name}"
                    )

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.skipped or hasattr(report, "wasxfail"):
            self.problems.append(f"Incomplete test: {report.nodeid}")

    def pytest_collectreport(self, report: pytest.CollectReport) -> None:
        if report.skipped:
            self.problems.append(f"Skipped test module: {report.nodeid}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--ci", action="store_true")
    parser.add_argument("--base", help="base commit for affected-day selection in CI")
    options, pytest_args = parser.parse_known_args(argv)
    solutions = sorted((ROOT / "src").glob("sol_*/day[0-9][0-9].py"))
    tests = sorted((ROOT / "test").rglob("test_*.py"))
    if not solutions and not tests:
        print("Scaffold state: no solutions or tests yet.")
        return 0
    if not tests:
        print("Error: solutions exist but no tests were found.")
        return 1

    test_paths: set[Path] = set()
    if options.ci:
        for solution in solutions:
            test = ROOT / "test" / solution.parent.name / f"test_{solution.name}"
            example = ROOT / "examples" / solution.parent.name.removeprefix("sol_")
            example = example / solution.with_suffix(".txt").name
            for path in (test, example):
                if not path.is_file():
                    print(
                        f"Error: missing {path.relative_to(ROOT)} for {solution.name}."
                    )
                    return 1
            test_paths.add(test.resolve())

    selected = affected_tests(options.base) if options.ci else None
    if selected is not None:
        if not selected:
            print("No remaining tests for changed days.")
            return 0
        test_paths.intersection_update(selected)
        pytest_args.extend(str(path.relative_to(ROOT)) for path in selected)
        print("Testing affected days:", ", ".join(map(str, selected)))
    else:
        print("Testing the full suite.")
    checks = PuzzleChecks(test_paths)
    result = int(pytest.main(pytest_args, plugins=[checks] if options.ci else []))
    for problem in checks.problems:
        print(f"Error: {problem}")
    return result if result else int(bool(checks.problems))


if __name__ == "__main__":
    raise SystemExit(main())
