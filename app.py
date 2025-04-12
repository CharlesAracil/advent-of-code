from pathlib import Path
from typing import Annotated

import typer

from utils.aoc_client import AOCClient
from utils.display_manager import create_report, print, print_error, print_warning
from utils.solution import get_latest_year, solution_factory

app = typer.Typer(help="Advent of Code - Puzzle Solving Tool", add_completion=False)

DayArg = Annotated[int, typer.Argument(min=1, max=25, help="Day of the puzzle (1-25)")]


@app.command()
def solve(
    day: DayArg,
    year: Annotated[
        int, typer.Option("--year", "-y", help="Year of the puzzle")
    ] = get_latest_year(),
    part: Annotated[
        int,
        typer.Option(
            "--part",
            "-p",
            min=1,
            max=2,
            help="Specific part to solve (1 or 2)",
        ),
    ] = None,
    submit: Annotated[
        bool, typer.Option("--submit", help="Submit the solution to Advent of Code")
    ] = False,
    sample: Annotated[
        bool,
        typer.Option("--sample", help="Use the sample input file (dayXX_sample.txt)"),
    ] = False,
):
    # submit and sample are mutually exclusive
    if submit and sample:
        print_error("Cannot use both --submit and --sample options together.")
        raise typer.Exit(code=1)  # Use typer.Exit for errors

    # run solution
    try:
        solution = solution_factory(day, year, part, sample, submit)
        solution_report = solution.run()
    except ImportError:
        print_error(
            f"Solution for {year}/{day} is not implemeted. Please run 'create' command first."
        )
        raise typer.Exit(code=1)

    # display results
    create_report(solution_report)


@app.command()
def create(
    day: DayArg,
    year: Annotated[
        int, typer.Option("--year", "-y", help="Year of the puzzle")
    ] = get_latest_year(),
    overwrite: Annotated[
        bool, typer.Option("--overwrite", "-o", help="Overwrite existing files")
    ] = False,
) -> None:
    # Create the solutions directory for the year if it doesn't exist
    solutions_dir = Path(f"solutions/{year}")
    solutions_dir.mkdir(parents=True, exist_ok=True)

    # Create the solution file
    solution_file = solutions_dir / f"day{day:02d}.py"
    if solution_file.exists() and not overwrite:
        print_error(
            f"Solution file {solution_file} already exists. Use --overwrite to replace it."
        )
        raise typer.Exit(code=1)

    # Read the content of the solution template file
    template_path = Path("utils/solution_template.py")
    if not template_path.exists():
        print_error(f"Template file {template_path} not found.")
        raise typer.Exit(code=1)

    template = template_path.read_text()
    solution_file.write_text(template)
    print(f"Created solution file: {solution_file}")

    # Create the inputs directory for the year if it doesn't exist
    inputs_dir = Path(f"inputs/{year}")
    inputs_dir.mkdir(parents=True, exist_ok=True)

    # Create an empty sample input file
    sample_file = inputs_dir / f"day{day:02d}_sample.txt"
    if not sample_file.exists() or overwrite:
        sample_file.write_text("")
        print(f"Created empty sample input file: {sample_file}")

    # Download the input file
    input_file = inputs_dir / f"day{day:02d}.txt"
    if not input_file.exists() or overwrite:
        try:
            print(f"Attempting to download input for {year} Day {day}...")
            client = AOCClient()
            input_text = client.fetch_input(year, day)
            input_file.write_text(input_text)
            print(f"Downloaded input file: {input_file}")
        except Exception as e:
            print_warning(f"Failed to download input file: {e}")

    # Download the problem description
    problems_dir = Path(f"problems/{year}")
    problems_dir.mkdir(parents=True, exist_ok=True)
    problem_file = problems_dir / f"day{day:02d}.md"
    if not problem_file.exists() or overwrite:
        try:
            print(f"Attempting to download problem description for {year} Day {day}...")
            client = AOCClient()
            markdown = client.read_problem(year, day)
            problem_file.write_text(markdown)
            print(f"Downloaded problem description: {problem_file}")
        except Exception as e:
            print_warning(f"Failed to download problem description: {e}")


@app.command()
def read(
    day: DayArg,
    year: Annotated[
        int, typer.Option("--year", "-y", help="Year of the puzzle")
    ] = get_latest_year(),
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite", "-o", help="Overwrite the file if it already exists"
        ),
    ] = False,
) -> None:
    """Read the problem description from Advent of Code and save it as Markdown."""

    # Create the problems directory for the year if it doesn't exist
    problems_dir = Path(f"problems/{year}")
    problems_dir.mkdir(parents=True, exist_ok=True)

    # Check if the problem file already exists
    problem_file = problems_dir / f"day{day:02d}.md"
    if problem_file.exists() and not overwrite:
        print_error(
            f"Problem file {problem_file} already exists. Use --overwrite to replace it."
        )
        raise typer.Exit(code=1)

    # Fetch and convert problem description using AOCClient
    try:
        print(f"Attempting to download problem description for {year} Day {day}...")
        client = AOCClient()
        markdown = client.read_problem(year, day)

        # Write to file
        problem_file.write_text(markdown)
        print(f"Saved problem description for day {day} to {problem_file}")
    except Exception as e:
        print_error(f"Failed to download and save problem description: {e}")
        raise typer.Exit(code=1)


@app.command()
def delete(
    day: DayArg,
    year: Annotated[
        int, typer.Option("--year", "-y", help="Year of the puzzle")
    ] = get_latest_year(),
) -> None:
    """Delete all files related to a specific day (solution, inputs, problem)."""

    # List of files to delete
    files_to_delete = [
        Path(f"solutions/{year}/day{day:02d}.py"),
        Path(f"inputs/{year}/day{day:02d}.txt"),
        Path(f"inputs/{year}/day{day:02d}_sample.txt"),
        Path(f"problems/{year}/day{day:02d}.md"),
    ]

    deleted_count = 0
    # Delete each file if it exists
    for file in files_to_delete:
        if file.exists():
            try:
                file.unlink()
                print(f"Deleted {file}")
                deleted_count += 1
            except OSError as e:
                print_error(f"Error deleting {file}: {e}")
        else:
            print(f"File not found, skipping: {file}")

    if deleted_count > 0:
        print(f"Finished deleting files for day {day} of {year}.")
    else:
        print(f"No files found to delete for day {day} of {year}.")


if __name__ == "__main__":
    app()
