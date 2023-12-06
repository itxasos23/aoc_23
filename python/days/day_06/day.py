import sys
import re
from typing import List, Set
from loguru import logger
from dataclasses import dataclass
from icecream import ic
from functools import reduce
from math import ceil

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)

class Day:
    def __init__(self):
        ex_input = """
Time:      7  15   30
Distance:  9  40  200
"""

        input_ = open("days/day_06/input.txt").read()

        lines = input_.splitlines() 
        time_line = lines[0].split(":")[1]
        distance_line = lines[1].split(": ")[1]

        while "  " in time_line:
            time_line = time_line.replace("  ", " ")

        while "  " in distance_line:
            distance_line = distance_line.replace("  ", " ")

        time_line = time_line.strip()
        distance_line = distance_line.strip()

        self.times = [int(x) for x in time_line.split(" ")]
        self.distances = [int(x) for x in distance_line.split(" ")]

    def part_1(self):
        ways_to_win = 1
        for time, distance in zip(self.times, self.distances):
            range_min, range_max = self._get_min_max_range(time, distance)
            ways_to_win *= (range_max - range_min) + 1
        return ways_to_win

    def _get_min_max_range(self, time, distance):
        distance = distance + 1
        pre_ratio = ceil(distance / (time - 1))
        post_ratio = 0 
        while pre_ratio != post_ratio:
            pre_ratio = post_ratio
            post_ratio = ceil(distance / (time - pre_ratio))

        ratio = post_ratio
        first_possible_min = ceil(ratio)
        last_possible_max = (time - ceil(ratio))

        return first_possible_min, last_possible_max

    def part_2(self):
        time = int("".join(str(x) for x in self.times))
        distance = int("".join(str(x) for x in self.distances))
        range_min, range_max = self._get_min_max_range(time, distance)
        return range_max - range_min + 1


def day():
    day = Day()
    print(f"day_05: {day.part_1()}, {day.part_2()}")
