import importlib
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from utils.aoc_client import AOCClient

console = Console()


def get_available_days(year: int) -> list[int]:
    """Get the list of available days for a given year."""
    solutions_dir = Path(f"solutions/{year}")
    if not solutions_dir.exists():
        return []

    days = []
    for file in solutions_dir.glob("day*.py"):
        try:
            day = int(file.stem[3:])
            days.append(day)
        except ValueError:
            continue
    return sorted(days)


def get_current_year() -> int:
    """Get the current year for Advent of Code."""
    now = datetime.now()
    year = now.year
    # If we're in December, use the current year
    # Otherwise, use the previous year
    return year if now.month == 12 else year - 1


def run_solution(
    year: int, day: int, part: int = None, submit: bool = False, sample: int = None
) -> None:
    """Run the solution for a given day."""
    solution_file = Path(f"solutions/{year}/day{day:02d}.py")
    if not solution_file.exists():
        console.print(
            f"[red]Error:[/red] Solution file not found for day {day} of {year}"
        )
        return

    try:
        # Dynamically import the solution module
        module = importlib.import_module(f"solutions.{year}.day{day:02d}")

        # Get the DaySolution class from the module
        solution_class = getattr(module, "DaySolution")

        # Create solution instance
        solution = solution_class()

        # Run the solution
        solution.run(part, submit, sample)

    except ImportError:
        console.print(f"[red]Error:[/red] Solution not found for day {day} of {year}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")


@click.group()
def cli():
    """Advent of Code - Puzzle Solving Tool"""
    pass


@click.command()
@click.argument("day", type=int)
@click.option(
    "--year",
    "-y",
    type=int,
    default=get_current_year(),
    help="Year of the puzzle (default: current year)",
)
@click.option(
    "--part",
    "-p",
    type=click.Choice(["1", "2"]),
    help="Specific part to solve (1 or 2)",
)
@click.option("--submit", is_flag=True, help="Submit the solution to Advent of Code")
@click.option(
    "--sample", is_flag=True, help="Use the sample input file (dayXX_sample.txt)"
)
def solve(year: int, day: int, part: str, submit: bool, sample: bool):
    """Solve a specific puzzle and optionally submit the solution"""
    if submit and sample:
        raise click.ClickException(
            "Cannot use both --submit and --sample options together"
        )
    part_num = int(part) if part else None
    run_solution(year, day, part_num, submit, sample)


@click.command()
@click.option(
    "--year",
    "-y",
    type=int,
    default=get_current_year(),
    help="Year to list (default: current year)",
)
def list(year: int):
    """List available days for a given year"""
    days = get_available_days(year)

    if not days:
        console.print(f"[yellow]No solutions available for year {year}[/yellow]")
        return

    table = Table(title=f"Available solutions for {year}")
    table.add_column("Day", style="cyan")
    table.add_column("Status", style="green")

    for day in days:
        solution_file = Path(f"solutions/{year}/day{day:02d}.py")
        if not solution_file.exists():
            table.add_row(f"Day {day:02d}", "❌ File missing")
            continue

        try:
            module = importlib.import_module(f"solutions.{year}.day{day:02d}")
            solution_class = getattr(module, "DaySolution")
            solution = solution_class()
            status = solution.status
        except Exception:
            table.add_row(f"Day {day:02d}", "⚠️ Error loading solution")
            continue

        if not status["part1_implemented"] and not status["part2_implemented"]:
            status_text = "⚠️  Not implemented"
        elif status["part1_implemented"] and status["part2_implemented"]:
            status_text = "✅ Complete"
        else:
            parts = []
            if status["part1_implemented"]:
                parts.append("1")
            if status["part2_implemented"]:
                parts.append("2")
            status_text = f"🟨 Part{'s' if len(parts) > 1 else ''} {', '.join(parts)}"

        table.add_row(f"Day {day:02d}", status_text)

    console.print(table)


@click.command()
@click.option(
    "--year", "-y", type=int, default=get_current_year(), help="Year of the puzzle"
)
@click.option(
    "--overwrite", "-o", is_flag=True, help="Overwrite the file if it already exists"
)
@click.argument("day", type=int)
def create(year: int, day: int, overwrite: bool) -> None:
    """Create a new solution file for the specified day."""
    if not 1 <= day <= 25:
        raise click.BadParameter("Day must be between 1 and 25")

    # Create the solutions directory for the year if it doesn't exist
    solutions_dir = Path(f"solutions/{year}")
    solutions_dir.mkdir(parents=True, exist_ok=True)

    # Create the solution file
    solution_file = solutions_dir / f"day{day:02d}.py"
    if solution_file.exists() and not overwrite:
        raise click.ClickException(
            f"Solution file for day {day} already exists. Use --overwrite to overwrite it."
        )

    template = """from utils.solution import Solution


class DaySolution(Solution):
    def parse_input(self) -> list:
        return self.input_data

    def solve_part1(self) -> int:
        data = self.parse_input()  # noqa: F841
        raise NotImplementedError("Part 1 not implemented")

    def solve_part2(self) -> int:
        data = self.parse_input()  # noqa: F841
        raise NotImplementedError("Part 2 not implemented")
"""
    solution_file.write_text(template)
    click.echo(f"Created solution file for day {day}")

    # Create the inputs directory for the year if it doesn't exist
    inputs_dir = Path(f"inputs/{year}")
    inputs_dir.mkdir(parents=True, exist_ok=True)

    # Create an empty sample input file
    sample_file = inputs_dir / f"day{day:02d}_sample.txt"
    if not sample_file.exists() or overwrite:
        sample_file.write_text("")
        click.echo(f"Created empty sample input file for day {day}")

    # Download the input file
    input_file = inputs_dir / f"day{day:02d}.txt"
    if not input_file.exists() or overwrite:
        try:
            client = AOCClient()
            input_text = client.fetch_input(year, day)
            input_file.write_text(input_text)
            click.echo(f"Downloaded input file for day {day}")
        except Exception as e:
            click.echo(f"Failed to download input file: {str(e)}")

    # Download the problem description
    problems_dir = Path(f"problems/{year}")
    problems_dir.mkdir(parents=True, exist_ok=True)
    problem_file = problems_dir / f"day{day:02d}.md"
    if not problem_file.exists() or overwrite:
        try:
            client = AOCClient()
            markdown = client.read_problem(year, day)
            problem_file.write_text(markdown)
            click.echo(f"Downloaded problem description for day {day}")
        except Exception as e:
            click.echo(f"Failed to download problem description: {str(e)}")


@click.command()
@click.option(
    "--year", "-y", type=int, default=get_current_year(), help="Year of the puzzle"
)
@click.option(
    "--overwrite", "-o", is_flag=True, help="Overwrite the file if it already exists"
)
@click.argument("day", type=int)
def read(year: int, day: int, overwrite: bool) -> None:
    """Read the problem description from Advent of Code and save it as Markdown."""
    if not 1 <= day <= 25:
        raise click.BadParameter("Day must be between 1 and 25")

    # Create the problems directory for the year if it doesn't exist
    problems_dir = Path(f"problems/{year}")
    problems_dir.mkdir(parents=True, exist_ok=True)

    # Check if the problem file already exists
    problem_file = problems_dir / f"day{day:02d}.md"
    if problem_file.exists() and not overwrite:
        raise click.ClickException(
            f"Problem file for day {day} already exists. Use --overwrite to overwrite it."
        )

    # Fetch and convert problem description using AOCClient
    client = AOCClient()
    markdown = client.read_problem(year, day)

    # Write to file
    problem_file.write_text(markdown)
    click.echo(f"Saved problem description for day {day} to {problem_file}")


cli.add_command(solve)
cli.add_command(list)
cli.add_command(create)
cli.add_command(read)

if __name__ == "__main__":
    cli()
