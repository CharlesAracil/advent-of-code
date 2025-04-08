import inspect
import os
import re
import time
from pathlib import Path
from typing import Any, Optional

from rich.console import Console
from rich.table import Table
from rich.text import Text

from utils.aoc_client import AOCClient
from utils.submit import submit_solution


class Solution:
    def __init__(self):
        # Get the file path of the calling module
        file_path = inspect.getmodule(self).__file__

        # Extract year and day from file path
        self.year = self._get_year_from_file(file_path)
        self.day = self._get_day_from_file(file_path)

        self._input_data: Optional[list[str]] = None
        self._part1_implemented = False
        self._part2_implemented = False

        # Check implementation status
        self._check_implementation()

    @property
    def input_data(self) -> list[str]:
        """Get the input data as a list of lines."""
        if self._input_data is None:
            input_file = Path(f"inputs/{self.year}/day{self.day:02d}.txt")
            if not input_file.exists():
                # Create inputs directory if it doesn't exist
                input_file.parent.mkdir(parents=True, exist_ok=True)
                # Fetch input from AOC website
                client = AOCClient()
                input_text = client.fetch_input(self.year, self.day)
                input_file.write_text(input_text)
            self._input_data = [
                line for line in input_file.read_text().splitlines() if line.strip()
            ]
        return self._input_data

    def parse_input(self, input_data: list[str]) -> Any:
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

    def _create_table(self, show_time: bool, submit: bool) -> Table:
        """Create and configure the results table."""
        table = Table(title=f"Solution for Day {self.day}, Year {self.year}")
        table.add_column("Part", style="cyan")
        table.add_column("Result", style="green")

        if show_time:
            table.add_column("Time", style="magenta")

        if submit and show_time:
            table.add_column("Submit Status", style="yellow")

        return table

    def _should_show_time(self, part: Optional[int]) -> bool:
        """Determine if we should show the Time column."""
        if part is not None:
            return (part == 1 and self._part1_implemented) or (
                part == 2 and self._part2_implemented
            )
        return self._part1_implemented or self._part2_implemented

    def _add_row_to_table(
        self,
        table: Table,
        part: str,
        result: str,
        show_time: bool,
        time_taken: str = "",
        status: Optional[Text] = None,
    ) -> None:
        """Add a row to the results table with appropriate columns."""
        if show_time and status is not None:
            table.add_row(part, result, time_taken, status)
        elif show_time:
            table.add_row(part, result, time_taken)
        elif status is not None:
            table.add_row(part, result, status)
        else:
            table.add_row(part, result)

    def _run_part(
        self, table: Table, part_num: int, show_time: bool, submit: bool
    ) -> None:
        """Run and display results for a specific part."""
        part_name = f"Part {part_num}"
        try:
            if getattr(self, f"_part{part_num}_implemented"):
                start_time = time.time()
                result = getattr(self, f"solve_part{part_num}")()
                end_time = time.time()
                time_taken = f"{end_time - start_time:.3f}s"

                if submit:
                    status = submit_solution(self.year, self.day, part_num, result)
                    self._add_row_to_table(
                        table, part_name, str(result), show_time, time_taken, status
                    )
                else:
                    self._add_row_to_table(
                        table, part_name, str(result), show_time, time_taken
                    )
            else:
                self._add_row_to_table(table, part_name, "Not implemented", show_time)
        except Exception as e:
            self._add_row_to_table(table, part_name, f"Error: {str(e)}", show_time)

    def run(
        self, part: Optional[int] = None, submit: bool = False, sample: bool = False
    ) -> None:
        """Run the solution for the specified part(s)."""
        console = Console()
        show_time = self._should_show_time(part)
        table = self._create_table(show_time, submit)

        # Reset input data if using a sample
        if sample:
            self._input_data = None
            input_file = Path(f"inputs/{self.year}/day{self.day:02d}_sample.txt")
            if not input_file.exists():
                raise FileNotFoundError(f"Sample input file not found: {input_file}")
            self._input_data = [
                line for line in input_file.read_text().splitlines() if line.strip()
            ]

        if part is None or part == 1:
            self._run_part(table, 1, show_time, submit)

        if part is None or part == 2:
            self._run_part(table, 2, show_time, submit)

        console.print(table)

    @property
    def status(self) -> dict:
        """Get the status of the solution implementation."""
        return {
            "file_exists": self._file_exists(),
            "part1_implemented": self._part1_implemented,
            "part2_implemented": self._part2_implemented,
        }

    def _file_exists(self) -> bool:
        """Check if the solution file exists."""
        return Path(f"solutions/{self.year}/day{self.day:02d}.py").exists()

    def _check_implementation(self) -> None:
        """Check if parts 1 and 2 are implemented by checking if they raise NotImplementedError."""
        try:
            self.solve_part1()
            self._part1_implemented = True
        except NotImplementedError:
            self._part1_implemented = False
        except Exception:
            self._part1_implemented = True  # If we get an error other than NotImplementedError, it's implemented

        try:
            self.solve_part2()
            self._part2_implemented = True
        except NotImplementedError:
            self._part2_implemented = False
        except Exception:
            self._part2_implemented = True  # If we get an error other than NotImplementedError, it's implemented

    def _get_year_from_file(self, file_path: str) -> int:
        """Extract the year from the file path."""
        match = re.search(r"solutions/(\d{4})/", file_path)
        if not match:
            raise ValueError("File must be in a solutions/YYYY/ directory")
        return int(match.group(1))

    def _get_day_from_file(self, file_path: str) -> int:
        """Extract the day number from the file path."""
        match = re.search(r"day(\d+)\.py$", file_path)
        if not match:
            raise ValueError("File must follow the format 'dayXX.py'")
        return int(match.group(1))
