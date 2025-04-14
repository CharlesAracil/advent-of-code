from collections import Counter
from typing import Any

from utils.solution import InputParser, Solution


class DaySolution(Solution):
    INPUT_PARSER = InputParser.N_COLUMNS
    COLUMN_TYPES = [int, int]

    def solve_part1(self, data: Any) -> int:
        """
        Calculate total distance between the two lists.
        For each pair of numbers (sorted), calculate the absolute difference.
        """
        left_list, right_list = data

        # Sort both lists
        left_sorted = sorted(left_list)
        right_sorted = sorted(right_list)

        # Calculate sum of distances
        total_distance = sum(
            abs(left - right) for left, right in zip(left_sorted, right_sorted)
        )

        return total_distance

    def solve_part2(self, data: Any) -> int:
        """
        Calculate similarity score.
        For each number in the left list, multiply by its number
        of occurrences in the right list.
        """
        left_list, right_list = data

        # Count occurrences in right list
        right_counts = Counter(right_list)

        # Calculate similarity score
        similarity_score = sum(num * right_counts[num] for num in left_list)

        return similarity_score
