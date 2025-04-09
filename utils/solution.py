import inspect
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

    def _load_input_data(self, sample: bool = False) -> list[str]:
        """Load input data from file."""
        file_suffix = "_sample" if sample else ""
        input_file = Path(f"inputs/{self.year}/day{self.day:02d}{file_suffix}.txt")
        
        if not input_file.exists():
            if sample:
                raise FileNotFoundError(f"Sample input file not found: {input_file}")
            # If the input file doesn't exist, we can't proceed
            raise FileNotFoundError(f"Input file not found: {input_file}. Please run 'create' command first.")
        
        return [line for line in input_file.read_text().splitlines() if line.strip()]

    @property
    def input_data(self) -> list[str]:
        """Get the input data as a list of lines."""
        if self._input_data is None:
            self._input_data = self._load_input_data()
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
        if part is None:
            # If no specific part is requested, check if either part is implemented
            return self._is_part_implemented(1) or self._is_part_implemented(2)
        else:
            # If a specific part is requested, check if that part is implemented
            return self._is_part_implemented(part)

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
        except NotImplementedError:
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

        # Load appropriate input data
        self._input_data = self._load_input_data(sample)

        # Determine which parts to run
        parts_to_run = []
        if part is None:
            parts_to_run = [1, 2]
        else:
            parts_to_run = [part]

        # Run the specified parts
        for part_num in parts_to_run:
            self._run_part(table, part_num, show_time, submit)

        console.print(table)

    def _is_part_implemented(self, part_num: int) -> bool:
        """Check if a specific part is implemented."""
        try:
            getattr(self, f"solve_part{part_num}")()
            return True
        except NotImplementedError:
            return False
        except Exception:
            return True  # If we get an error other than NotImplementedError, it's implemented

    @property
    def status(self) -> dict:
        """Get the status of the solution implementation."""
        return {
            "file_exists": self._file_exists(),
            "part1_implemented": self._is_part_implemented(1),
            "part2_implemented": self._is_part_implemented(2),
        }

    def _file_exists(self) -> bool:
        """Check if the solution file exists."""
        return Path(f"solutions/{self.year}/day{self.day:02d}.py").exists()

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
