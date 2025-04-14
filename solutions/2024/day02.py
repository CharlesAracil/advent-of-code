from typing import Any

from utils.solution import Solution


class DaySolution(Solution):
    def parse_data(self, data: str | list[str]) -> str | list[str]:
        return [[int(x) for x in line.split()] for line in data]

    def is_safe(self, report) -> bool:
        deltas = [a - b for a, b in zip(report, report[1:])]
        is_monotonic = all(delta > 0 for delta in deltas) or all(
            delta < 0 for delta in deltas
        )
        is_stable = all(0 < abs(delta) <= 3 for delta in deltas)

        return is_monotonic and is_stable

    def solve_part1(self, data: Any) -> int:
        safe_count = 0
        for report in data:
            if self.is_safe(report):
                safe_count += 1
        return safe_count

    def solve_part2(self, data: Any) -> int:
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
