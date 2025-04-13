from utils.solution import Solution


class DaySolution(Solution):
    def callback(self, line):
        # note: sorted is only used for part 2
        return sorted([int(x) for x in line.split("x")])

    def parse_input(self) -> str | list[str]:
        return self.input_data

    def solve_part1(self) -> int:
        data = self.parse_input()
        area = sum(
            [
                2 * (length * width + width * height + height * length)
                + min(length * width, width * height, height * length)
                for length, width, height in data
            ]
        )

        return area

    def solve_part2(self) -> int:
        data = self.parse_input()

        ribbon_length = sum(
            [
                2 * (length + width) + length * width * height
                for length, width, height in data
            ]
        )

        return ribbon_length


class TestDaySolutionPart:
    TEST_CASES = {
        "2x3x4": 58,
        "1x1x10": 43,
    }
