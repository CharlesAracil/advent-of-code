# Advent of Code Solutions

This project contains my solutions for Advent of Code puzzles. It includes utilities for managing inputs, solutions, and problem descriptions, as well as a command-line interface (CLI) for solving and managing puzzles.

## Project Structure

```
advent_of_code/
├── solutions/           # Solutions for each year
│   ├── 2024/          # Solutions for 2024
│   │   ├── day01.py   # Solution for day 1
│   │   └── ...
│   └── 2015/          # Solutions for 2015
│       ├── day01.py
│       └── ...
├── problems/          # Problem descriptions and sample inputs
├── inputs/            # Input files for each puzzle
│   ├── 2024/
│   └── 2015/
├── utils/            # Shared utilities
│   ├── solution.py   # Base solution class
│   ├── solution_template.py # Template for new solutions
│   └── aoc_client.py # Advent of Code API client
├── tests/           # Unit tests
├── app.py          # Main entry point with CLI
├── pyproject.toml   # Poetry configuration
└── .env            # Environment variables (to be created)
```

## Installation

1. Make sure you have Poetry installed:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone this repository and install dependencies:

```bash
poetry install
```

## Configuration

1. Create a `.env` file in the project root
2. Add your Advent of Code session cookie:

```
AOC_SESSION=your_session_cookie_here
```

## Usage

The project provides a command-line interface with several useful commands:

### Solve a puzzle

```bash
# Solve both parts of a puzzle
poetry run aoc solve 1

# Solve a specific part
poetry run aoc solve 1 --part 1

# Solve and submit the solution
poetry run aoc solve 1 --submit

# Solve specific part and submit
poetry run aoc solve 1 --part 1 --submit

# Specify the year
poetry run aoc solve --year 2024 1 --submit

# Use sample input
poetry run aoc solve 1 --sample
```

The `--submit` flag will automatically submit your solution to Advent of Code.
Responses will be color-coded:

- ✨ Green: Correct answer
- ❌ Red: Wrong answer (with indication if too high/low)
- ⏳ Yellow: Need to wait before submitting again

### Create a new solution file

```bash
# Create a file for current year
poetry run aoc create 1

# Create a file for a specific year
poetry run aoc create 1 --year 2024

# Overwrite existing file
poetry run aoc create 1 --overwrite
```

This command uses a template file located at `utils/solution_template.py` to create new solution files. Ensure this template exists and is up-to-date.

### Read a problem description

```bash
# Fetch and save the problem description for a specific day
poetry run aoc read 1

# Specify the year
poetry run aoc read 1 --year 2024

# Overwrite existing file
poetry run aoc read 1 --overwrite
```

### Delete files for a specific day

```bash
# Delete all files related to a specific day
poetry run aoc delete 1

# Specify the year
poetry run aoc delete 1 --year 2024
```

This command deletes the solution file, input files, and problem description for the specified day and year.

## Solution Format

Each solution file should follow this format:

```python
from utils.solution import Solution

class DaySolution(Solution):
    def parse_input(self) -> str | list[str]:
        return self.input_data

    def solve_part1(self) -> int:
        data = self.parse_input()
        # Solution for part 1
        raise NotImplementedError("Part 1 not implemented")

    def solve_part2(self) -> int:
        data = self.parse_input()
        # Solution for part 2
        raise NotImplementedError("Part 2 not implemented")
```

## Dynamic Input Parsing

The `parse_input` method in each solution class has been enhanced to support dynamic input parsing. It can now handle both single-line and multi-line inputs, returning either a `str` or a `list[str]` depending on the input format. This flexibility allows for easier handling of diverse input formats across different puzzles.

## Key Features

- **Dynamic Input Parsing**: The `parse_input` method now supports both single-line and multi-line inputs, returning `str | list[str]`.
- **Template-Based Solution Creation**: New solution files are created using a customizable template located at `utils/solution_template.py`.
- **Comprehensive CLI**: Manage solutions, inputs, and problem descriptions directly from the command line.
- **Error Handling**: Clear error messages and warnings for missing files or invalid operations.
