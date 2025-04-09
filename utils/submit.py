from rich.text import Text

from utils.aoc_client import AOCClient, SubmissionResult


def submit_solution(year: int, day: int, part: int, answer: int) -> Text:
    """Submit a solution to Advent of Code website and parse the response."""

    client = AOCClient()
    result = client.submit_answer(year, day, part, answer)

    text = Text()

    match result:
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
