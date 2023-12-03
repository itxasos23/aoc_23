import sys
from loguru import logger

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)

class Day:
    str_to_int = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    digit_strs = list(str_to_int.keys())

    def part_1(self):
        lines = open("days/day_01/input.txt").read().splitlines()
        return sum(self._get_first_and_last_from_string(line) for line in lines)

    def part_2(self):
        lines = open("days/day_01/input.txt").read().splitlines()
        return sum(
            self._get_first_and_last_from_string(line, include_words=True)
            for line in lines
        )

    def _digit_to_key(self, digit_str):
        return int(digit_str) if digit_str.isdigit() else self.str_to_int[digit_str]

    def _get_first_and_last_from_string(self, input_string, include_words=False):
        digits = {}

        for idx, char in enumerate(input_string):
            if char.isdigit():
                digits.setdefault(self._digit_to_key(char), []).append(idx)

            if include_words:
                for digit_str in self.digit_strs:
                    if input_string[idx:].startswith(digit_str):
                        digits.setdefault(self._digit_to_key(digit_str), []).append(idx)

        return (
            min(digits.items(), key=lambda entry: min(entry[1]))[0] * 10
            + max(digits.items(), key=lambda entry: max(entry[1]))[0]
        )


def day():
    day = Day()
    print(f"day_01: {day.part_1()}, {day.part_2()}")

