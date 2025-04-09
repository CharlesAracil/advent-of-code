# note: sample input was not the same between part 1 and part 2 on the AOC puzzle description,
# however sample from part 2 resulted in the same input in part 1, so we kept this one.

import re

from utils.solution import Solution


class DaySolution(Solution):
    def parse_input(self) -> str:
        return "".join(self.input_data)

    def solve_part1(self) -> int:
        data = self.parse_input()

        __import__("ipdb").set_trace()
        
        matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)
        
        return sum([int(a) * int(b) for a, b in matches])

    def solve_part2(self) -> int:
        data = self.parse_input()

        pattern_mul = r"mul\((\d{1,3}),(\d{1,3})\)"
        pattern_do = r"\(do\(\)\)"
        pattern_dont = r"\(don't\(\)\)"

        matches = re.findall("|".join([pattern_mul, pattern_do, pattern_dont]), data)

        __import__("ipdb").set_trace()
        return 0
