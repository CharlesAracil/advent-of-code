from rich.console import Console
from rich.table import Table
from rich.text import Text

from utils.solution import SolutionReport, SubmissionResult

console = Console()


def print(message: str) -> None:
    console.print(message)


def print_dim(message: str) -> None:
    console.print(f"[dim]{message}[/dim]")


def print_success(message: str) -> None:
    console.print(f"[green]Success:[/green] {message}")


def print_warning(message: str) -> None:
    console.print(f"[yellow]Warning:[/yellow] {message}")


def print_error(message: str) -> None:
    console.print(f"[red]Error:[/red] {message}")


def create_table(submit: bool) -> Table:
    table = Table(title="Solution")
    table.add_column("Part", style="cyan")
    table.add_column("Result", style="green")
    table.add_column("Time", style="magenta")

    if submit:
        table.add_column("Submit Status", style="yellow")

    return table


def create_report(solution_report: SolutionReport) -> None:
    table = create_table(solution_report.submit)

    for solution_part_report in [solution_report.part1, solution_report.part2]:
        if not solution_part_report:
            continue

        columns = [
            f"Part {solution_part_report.part}",
            str(solution_part_report.result),
            f"{solution_part_report.time_taken * 1000:.3f} ms",
        ]
        if solution_report.submit:
            submission_result = format_submission_result(
                solution_part_report.submission
            )
            columns.append(submission_result)

        table.add_row(*columns)

    print(table)


def format_submission_result(submission_result: SubmissionResult) -> Text:
    text = Text()

    match submission_result:
        case SubmissionResult.CORRECT:
            text.append("✨ ", style="bright_yellow")
            text.append("Correct!", style="bright_green")
        case SubmissionResult.TOO_HIGH:
            text.append("❌ ", style="bright_red")
            text.append("Wrong - Too high!", style="red")
        case SubmissionResult.TOO_LOW:
            text.append("❌ ", style="bright_red")
            text.append("Wrong - Too low!", style="red")
        case SubmissionResult.WRONG:
            text.append("❌ ", style="bright_red")
            text.append("Wrong answer!", style="red")
        case SubmissionResult.RATE_LIMIT:
            text.append("⏳ ", style="bright_yellow")
            text.append("Please wait before trying again", style="yellow")
        case SubmissionResult.ALREADY_SOLVED:
            text.append("🎯 ", style="bright_yellow")
            text.append("Already solved!", style="yellow")
        case _:
            text.append("⚠️ ", style="bright_yellow")
            text.append("Unexpected response", style="yellow")

    return text
