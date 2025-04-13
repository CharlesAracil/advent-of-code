import importlib
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Union

from utils.aoc_client import AOCClient, SubmissionResult


def solution_factory(
    day: int, year: int, part: int, sample: bool, submit: bool
) -> "Solution":
    module_path = f"solutions.{year}.day{day:02d}"

    try:
        module = importlib.import_module(module_path)
        DaySolution = getattr(module, "DaySolution")
    except ModuleNotFoundError as e:
        raise ImportError(f"Module for {module_path} not found") from e
    except AttributeError as e:
        raise ImportError(f"No 'DaySolution' class in {module_path}") from e

    return DaySolution(day, year, part, sample, submit)


@dataclass
class SolutionPartReport:
    part: int
    result: Optional[Union[int]] = None
    time_taken: Optional[int] = None
    submission: Optional[SubmissionResult] = None
    implemented: bool = True
    error: Optional[Exception] = None


@dataclass
class SolutionReport:
    submit: Optional[bool] = False
    part1: Optional[SolutionPartReport] = None
    part2: Optional[SolutionPartReport] = None

    def __setitem__(self, key: str, value: SolutionPartReport):
        if key == 1:
            self.part1 = value
        elif key == 2:
            self.part2 = value
        else:
            raise KeyError(f"Invalid key: {key}")


class InputParser(Enum):
    ONE_LINE = "one line"
    MULTIPLE_LINES = "multiple lines"


def get_latest_year() -> int:
    now = datetime.now()
    year = now.year
    return year if now.month == 12 else year - 1


class Solution:
    INPUT_PARSER = InputParser.MULTIPLE_LINES

    def __init__(
        self,
        day: int,
        year: Optional[int] = None,
        part: Optional[int] = None,
        sample: Optional[bool] = False,
        submit: Optional[bool] = False,
    ):
        self.day = day
        self.year = year or get_latest_year()
        self.parts = [part] if part else [1, 2]
        self.input_data = self._load_input_data(sample)
        self.submit = submit

    # Methods that should be implemented by subclasses

    def parse_input(self) -> str | list[str]:
        """Parse the input data into a format suitable for solving the puzzle.

        This method must be implemented by each solution class.
        """
        raise NotImplementedError("parse_input must be implemented")

    def solve_part1(self) -> int:
        """Solve part 1 of the puzzle."""
        raise NotImplementedError("Part 1 not implemented")

    def solve_part2(self) -> int:
        """Solve part 2 of the puzzle."""
        raise NotImplementedError("Part 2 not implemented")

    # ---

    def _load_input_data(self, sample: bool = False) -> list[str] | str:
        file_suffix = "_sample" if sample else ""
        input_file = Path(f"inputs/{self.year}/day{self.day:02d}{file_suffix}.txt")

        if not input_file.exists():
            raise FileNotFoundError(
                f"Input file not found: {input_file}. Please run 'create' command first."
            )

        match self.INPUT_PARSER:
            case InputParser.ONE_LINE:
                return input_file.read_text().strip()
            case InputParser.MULTIPLE_LINES:
                return [
                    line for line in input_file.read_text().splitlines() if line.strip()
                ]

    def _run_part(self, part: int, submit: bool) -> SolutionPartReport:
        status = SolutionPartReport(part)

        try:
            start_time = time.time()
            status.result = getattr(self, f"solve_part{part}")()
            end_time = time.time()
            status.time_taken = end_time - start_time

            if submit:
                status.submission = self.submit_solution(part, status.result)
        except NotImplementedError:
            status.implemented = False

        return status

    def run(self) -> SolutionReport:
        solution_report = SolutionReport(submit=self.submit)
        for part in self.parts:
            solution_report[part] = self._run_part(part, self.submit)

        return solution_report

    def submit_solution(self, part: int, answer: int) -> SubmissionResult:
        client = AOCClient()
        result = client.submit_answer(self.year, self.day, part, answer)

        return result
