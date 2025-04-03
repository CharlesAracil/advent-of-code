from collections import Counter

from utils.solution import Solution


class DaySolution(Solution):
    def parse_input(self) -> tuple[list[int], list[int]]:
        """Parse input into two lists of numbers."""
        left_list = []
        right_list = []

        for line in self.input_data:
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))

        return left_list, right_list

    def solve_part1(self) -> int:
        """
        Calculate total distance between the two lists.
        For each pair of numbers (sorted), calculate the absolute difference.
        """
        left_list, right_list = self.parse_input()

        # Sort both lists
        left_sorted = sorted(left_list)
        right_sorted = sorted(right_list)

        # Calculate sum of distances
        total_distance = sum(
            abs(left - right) for left, right in zip(left_sorted, right_sorted)
        )

        return total_distance

    def solve_part2(self) -> int:
        """
        Calculate similarity score.
        For each number in the left list, multiply by its number
        of occurrences in the right list.
        """
        left_list, right_list = self.parse_input()

        # Count occurrences in right list
        right_counts = Counter(right_list)

        # Calculate similarity score
        similarity_score = sum(num * right_counts[num] for num in left_list)

        return similarity_score
