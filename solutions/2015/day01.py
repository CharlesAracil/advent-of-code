# note: we needed to parse data because input is a oneliner and our framework always use splitlines
# we could parametrize the class with the kind of input we have

from utils.solution import InputParser, Solution


class DaySolution(Solution):
    INPUT_PARSER = InputParser.ONE_LINE

    def parse_input(self) -> list:
        return self.input_data

    def solve_part1(self) -> int:
        data = self.parse_input()  # noqa: F841
        floor = 0
        for parenthesis in data:
            if parenthesis == "(":
                floor += 1
            elif parenthesis == ")":
                floor -= 1

        return floor

    def solve_part2(self) -> int:
        data = self.parse_input()  # noqa: F841
        floor = 0
        for position, parenthesis in enumerate(data):
            if parenthesis == "(":
                floor += 1
            elif parenthesis == ")":
                floor -= 1

            if floor == -1:
                return position + 1

        raise ValueError("Santa never entered the basement!")
