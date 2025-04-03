import os
import re
from enum import IntEnum, StrEnum

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from markdownify import markdownify as md


class HTTPStatus(IntEnum):
    OK = 200


class SubmissionResult(StrEnum):
    CORRECT = "correct"
    TOO_HIGH = "too_high"
    TOO_LOW = "too_low"
    WRONG = "wrong"
    ALREADY_SOLVED = "already_solved"
    RATE_LIMIT = "rate_limit"


class UnexpectedResponseError(Exception):
    pass


class AOCClient:
    """Client for interacting with Advent of Code website."""

    BASE_URL = "https://adventofcode.com"

    def __init__(self):
        load_dotenv()
        self.session = os.getenv("AOC_SESSION")
        if not self.session:
            raise RuntimeError("AOC_SESSION environment variable not set")
        self.headers = {"Cookie": f"session={self.session}"}

    def fetch_problem(self, year: int, day: int) -> str:
        url = f"{self.BASE_URL}/{year}/day/{day}"
        response = requests.get(url, headers=self.headers)

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(f"Failed to fetch problem: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article", class_="day-desc")

        if not articles:
            raise RuntimeError("Could not find problem description")

        # Convert HTML to Markdown
        markdown = ""
        for article in articles:
            markdown += md(str(article)) + "\n\n"

        return markdown.strip()

    def fetch_input(self, year: int, day: int) -> str:
        url = f"{self.BASE_URL}/{year}/day/{day}/input"
        response = requests.get(url, headers=self.headers)

        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(f"Failed to fetch input: {response.status_code}")

        return response.text

    def submit_answer(
        self, year: int, day: int, part: int, answer: int
    ) -> SubmissionResult:
        url = f"{self.BASE_URL}/{year}/day/{day}/answer"
        data = {"level": part, "answer": str(answer)}

        response = requests.post(url, data=data, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Look for message in possible elements
        message = None
        for element in [soup.article, soup.main, soup.p]:
            if element and element.text.strip():
                message = element.text.strip()
                break

        if not message:
            raise UnexpectedResponseError("Could not find response message")

        message = message.replace("\n", " ").strip().lower()

        if "that's the right answer" in message:
            return SubmissionResult.CORRECT
        elif "that's not the right answer" in message:
            if "too high" in message:
                return SubmissionResult.TOO_HIGH
            elif "too low" in message:
                return SubmissionResult.TOO_LOW
            return SubmissionResult.WRONG
        elif "you gave an answer too recently" in message:
            return SubmissionResult.RATE_LIMIT
        elif "you don't seem to be solving the right level" in message:
            return SubmissionResult.ALREADY_SOLVED

        raise UnexpectedResponseError(f"Unexpected response: {message[:100]}")

    def read_problem(self, year: int, day: int) -> str:
        """Read the problem description from Advent of Code and return it as Markdown."""
        url = f"{self.BASE_URL}/{year}/day/{day}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article", class_="day-desc")

        if not articles:
            raise RuntimeError("No problem description found on the page")

        # Convert to Markdown
        markdown = []
        for article in articles:
            # Remove the "---" at the end of each part
            content = str(article)
            content = re.sub(r"<hr/>", "", content)
            markdown.append(md(content))

        return "\n\n---\n\n".join(markdown)
