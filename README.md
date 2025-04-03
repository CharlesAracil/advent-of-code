# Advent of Code Solutions

This project contains my solutions for Advent of Code puzzles.

## Project Structure

```
advent_of_code/
├── solutions/           # Solutions for each year
│   ├── 2024/          # Solutions for 2024
│   │   ├── day01.py   # Solution for day 1
│   │   └── ...
│   └── 2022/          # Solutions for 2022
│       ├── day01.py
│       └── ...
├── problems/          # Problem descriptions and sample inputs
├── inputs/            # Input files for each puzzle
│   ├── 2024/
│   └── 2022/
├── utils/            # Shared utilities
│   ├── __init__.py
│   ├── solution.py   # Base solution class
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

### List available solutions
```bash
# List solutions for current year
poetry run aoc list

# List solutions for a specific year
poetry run aoc list --year 2024
```

### Create a new solution file
```bash
# Create a file for current year
poetry run aoc create 1

# Create a file for a specific year
poetry run aoc create 1 --year 2024

# Overwrite existing file
poetry run aoc create 1 --overwrite
```

## Solution Format

Each solution file should follow this format:
```python
from utils.solution import Solution

class DaySolution(Solution):
    def parse_input(self) -> list:
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
