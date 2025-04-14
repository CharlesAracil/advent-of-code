from typing import Any

from utils.solution import InputParser, Solution


class DaySolution(Solution):
    INPUT_PARSER = InputParser.ONE_LINE

    def solve_part1(self, data: Any) -> int:
        floor = 0
        for parenthesis in data:
            if parenthesis == "(":
                floor += 1
            elif parenthesis == ")":
                floor -= 1

        return floor

    def solve_part2(self, data: Any) -> int:
        floor = 0
        for position, parenthesis in enumerate(data):
            if parenthesis == "(":
                floor += 1
            elif parenthesis == ")":
                floor -= 1

            if floor == -1:
                return position + 1

        raise ValueError("Santa never entered the basement!")
