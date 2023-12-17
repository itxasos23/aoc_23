import sys
import re
from typing import List, Set
from loguru import logger
from dataclasses import dataclass
from icecream import ic
from functools import reduce
from itertools import cycle
from math import lcm
from itertools import combinations

from typing import Tuple, List, Dict, Any, Optional

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


class Day:
    def __init__(self):
        ex_input = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
        input_ = open("days/day_11/input.txt").read()
        self.lines = [x for x in input_.strip().splitlines() if x]

        self.empty_rows = [idx for idx, line in enumerate(self.lines) if all(x == '.' for x in line)]
        self.empty_cols = [idy for idy in range(len(self.lines[0])) if all(l[idy] == '.' for l in self.lines)]

    def part_1(self):
        return self._get_combination_distance_sum(combinations(self._get_galaxies(), 2), multiplier=2)

    def _get_combination_distance_sum(self, g_comb, multiplier=2):
        sum = 0

        for comb in g_comb:
            rows = [min(x[0] for x in comb), max(x[0] for x in comb)]
            cols = [min(x[1] for x in comb), max(x[1] for x in comb)]

            empty_rows = list(x for x in self.empty_rows if rows[0] < x < rows[1])
            empty_cols = list(x for x in self.empty_cols if cols[0] < x < cols[1])

            dist_x = abs(comb[0][0] - comb[1][0]) + (multiplier - 1) * len(empty_rows)
            dist_y = abs(comb[0][1] - comb[1][1]) + (multiplier - 1) * len(empty_cols)

            sum += dist_x + dist_y

        return sum
        
    def _get_galaxies(self):
        galaxies = []

        for idx, line in enumerate(self.lines):
            for idy, char in enumerate(line):
                if char == "#":
                    galaxies.append((idx, idy))

        return galaxies

    def part_2(self):
        return self._get_combination_distance_sum(combinations(self._get_galaxies(), 2), multiplier=1000000)


def day():
    day = Day()
    print(f"day_10: {day.part_1()}, {day.part_2()}")
