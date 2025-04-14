from typing import Any

from utils.solution import Solution


class DaySolution(Solution):
    def parse_line(self, line):
        # note: sorted is only used for part 2
        return sorted([int(x) for x in line.split("x")])

    def solve_part1(self, data: Any) -> int:
        area = sum(
            [
                2 * (length * width + width * height + height * length)
                + min(length * width, width * height, height * length)
                for length, width, height in data
            ]
        )

        return area

    def solve_part2(self, data: Any) -> int:
        ribbon_length = sum(
            [
                2 * (length + width) + length * width * height
                for length, width, height in data
            ]
        )

        return ribbon_length
