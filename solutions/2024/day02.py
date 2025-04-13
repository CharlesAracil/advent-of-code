from utils.solution import Solution


class DaySolution(Solution):
    def parse_input(self) -> str | list[str]:
        return [[int(x) for x in line.split()] for line in self.input_data]

    def is_safe(self, report) -> bool:
        deltas = [a - b for a, b in zip(report, report[1:])]
        is_monotonic = all(delta > 0 for delta in deltas) or all(
            delta < 0 for delta in deltas
        )
        is_stable = all(0 < abs(delta) <= 3 for delta in deltas)

        return is_monotonic and is_stable

    def solve_part1(self) -> int:
        data = self.parse_input()
        safe_count = 0
        for report in data:
            if self.is_safe(report):
                safe_count += 1
        return safe_count

    def solve_part2(self) -> int:
        data = self.parse_input()
        safe_count = 0
        for report in data:
            # Check if report is already safe without removing any level
            if self.is_safe(report):
                safe_count += 1
                continue

            # Try removing each level and check if resulting report is safe
            for i in range(len(report)):
                modified_report = report[:i] + report[i + 1 :]
                if self.is_safe(modified_report):
                    safe_count += 1
                    break

        return safe_count


class TestDaySolutionPart:
    TEST_CASES = {
        "2x3x4": 58,
        "1x1x10": 43,
    }
