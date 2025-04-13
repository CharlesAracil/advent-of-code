# note: sample input was not the same between part 1 and part 2 on the AOC puzzle description,
# however sample from part 2 resulted in the same input in part 1, so we kept this one.

import re

from utils.solution import InputParser, Solution


class DaySolution(Solution):
    INPUT_PARSER = InputParser.ONE_LINE

    def parse_input(self) -> str:
        return self.input_data

    def solve_part1(self) -> int:
        data = self.parse_input()

        matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)

        return sum([int(a) * int(b) for a, b in matches])

    def solve_part2(self) -> int:
        data = self.parse_input()

        patterns = [
            r"mul\((\d{1,3}),(\d{1,3})\)",
            r"do\(\)",
            r"don't\(\)",
        ]
        aggregated_pattern = r"|".join(patterns)
        matches = re.findall(rf"({aggregated_pattern})", data)

        result = 0
        active = True
        for match in matches:
            if match[0] == "do()":
                active = True
            elif match[0] == "don't()":
                active = False
            elif active:
                result += int(match[1]) * int(match[2])

        return result
