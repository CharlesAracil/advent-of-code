from typing import Any

from utils.solution import InputParser, Solution


class DaySolution(Solution):
    INPUT_PARSER = InputParser.MULTIPLE_LINES

    def parse_data(self, data: Any) -> Any:
        # you can delete this method if you don't need to parse the data
        return data

    def parse_line(self, line: str) -> str:
        # you can delete this method if you don't need to parse the line
        return line

    def solve_part1(self, data: Any) -> int:
        # Your part 1 logic here
        raise NotImplementedError("Part 1 not implemented")

    def solve_part2(self, data: Any) -> int:
        # Your part 2 logic here
        raise NotImplementedError("Part 2 not implemented")
