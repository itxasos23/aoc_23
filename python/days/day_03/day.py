import sys
import re
from typing import List
from loguru import logger
from dataclasses import dataclass
from icecream import ic
from functools import reduce

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


class Day:
    def __init__(self):
        self.input = list(
            filter(lambda x: x, open("days/day_03/input.txt").read().splitlines())
        )

    def part_1(self):
        return sum(self._get_list_of_valid_numbers())

    def part_2(self):
        return sum(self._get_gear_ratios(self._get_gear_positions()))

    def _is_symbol(self, char):
        return char not in (".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

    def _check_if_valid_number(self, row_idx, char_idx, digits):
        if self._is_valid_number(row_idx, char_idx, digits):
            return int("".join(digits))

    def _get_list_of_valid_numbers(self):
        valid_numbers = []
        digits = []

        for row_idx, row in enumerate(self.input):
            for char_idx, char in enumerate(row):
                digits.append(char) if char.isdigit() else None

                if not char.isdigit() and digits:
                    valid_numbers.append(
                        self._check_if_valid_number(row_idx, char_idx, digits) or 0
                    )
                    digits = []

            if digits:
                number = int("".join(digits))
                if self._is_valid_number(row_idx, len(self.input[row_idx]), digits):
                    valid_numbers.append(number)
                digits = []

        return valid_numbers

    def _is_valid_number(self, row_idx, char_idx, current_number_digits):
        first_digit_idx = char_idx - len(current_number_digits)
        last_digit_idx = char_idx - 1
        last_line_idx = len(self.input[row_idx]) - 1

        range_start = max([0, first_digit_idx - 1])
        range_end = min([last_line_idx, last_digit_idx + 1])

        for r_diff in (1, -1):
            if not 0 <= (r := row_idx + r_diff) < len(self.input):
                continue

            for c in range(range_start, range_end + 1):
                if self._is_symbol(self.input[r][c]):
                    return True

        for c in (first_digit_idx - 1, last_digit_idx + 1):
            if not 0 <= c < len(self.input[0]):
                continue

            if self._is_symbol(self.input[row_idx][c]):
                return True

        return False

    def _get_gear_positions(self):
        gear_positions = []

        for row_idx, row in enumerate(self.input):
            for char_idx, char in enumerate(row):
                if char == "*":
                    gear_positions.append((row_idx, char_idx))

        return gear_positions

    def _get_gear_ratios(self, gear_positions):
        ratios = []
        for row_idx, char_idx in gear_positions:
            numbers_around = self._get_numbers_around_scan(row_idx, char_idx)
            if len(numbers_around) == 2:
                ratios.append(numbers_around[0] * numbers_around[1])

        return ratios

    def _get_numbers_around_scan(self, row_idx, char_idx):
        found_numbers = []
        for r_diff in (1, -1):
            if not 0 <= (r := row_idx + r_diff) < len(self.input):
                continue

            if not self.input[r][char_idx].isdigit():
                for c_diff in (1, -1):
                    if not 0 <= (c := char_idx + c_diff) < len(self.input[0]):
                        continue

                    if self.input[r][c].isdigit():
                        found_numbers.append(self._get_number_in(r, c) or None)

            else:
                found_numbers.append(
                    self._get_number(
                        r,
                        max((0, char_idx - 1)),
                        min((len(self.input[0]) - 1, char_idx + 1)),
                    )
                )

        for c_diff in (1, -1):
            if not 0 <= (c := char_idx + c_diff) < len(self.input[0]):
                continue
            found_numbers.append(self._get_number_in(row_idx, c) or None)

        return [x for x in found_numbers if x is not None]

    def _get_number(self, r, r_from, r_to):
        return set(
            filter(
                lambda x: x is not None,
                set(self._get_number_in(r, c) for c in range(r_from, r_to + 1)),
            )
        ).pop()

    def _get_number_in(self, r, c):
        if not self.input[r][c].isdigit():
            return None

        start_c = c
        while start_c != 0 and self.input[r][start_c - 1].isdigit():
            start_c -= 1

        end_c = start_c
        while end_c != len(self.input[0]) - 1 and self.input[r][end_c + 1].isdigit():
            end_c += 1

        return int("".join([self.input[r][idx] for idx in range(start_c, end_c + 1)]))


def day():
    day = Day()
    print(f"day_03: {day.part_1()}, {day.part_2()}")
