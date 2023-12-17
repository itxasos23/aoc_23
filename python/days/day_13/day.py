import sys
import re
from typing import List, Set
from loguru import logger
from dataclasses import dataclass
from icecream import ic
from functools import reduce
from itertools import cycle
from math import lcm
from itertools import combinations, product, combinations_with_replacement
from more_itertools import distinct_permutations
from tqdm import tqdm

from typing import Tuple, List, Dict, Any, Optional

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


class Day:
    def __init__(self):
        ex_input = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
        input_ = open("days/day_13/input.txt").read()
        maps = input_.split("\n\n")
        self.maps = [[y for y in x.splitlines() if y] for x in maps]

    def part_1(self):
        count = 0

        for map_ in self.maps:
            h_axis, v_axis = None, None
            h_axis = self.get_horizontal_reflection_axis(map_)
            v_axis = self.get_vertical_reflection_axis(map_)
            count += h_axis + 1 if h_axis is not None else (v_axis + 1) * 100 if v_axis is not None else 0

        return count

    def get_vertical_reflection_axis(self, map_):
        p_axes = []

        for idx, _ in enumerate(map_):
            if idx == 0:
                continue

            idx_0 = idx - 1
            idx_1 = idx

            if map_[idx_0] == map_[idx_1]:
                p_axes.append(idx_0)

        reflection_axes = []
        for axis in p_axes:
            broken_reflection = False
            for offset in range(axis + 1):
                if axis + 1 + offset >= len(map_):
                    break
            
                first_row = map_[axis - offset]
                second_row = map_[axis + 1 + offset]

                if first_row != second_row:
                    broken_reflection = True
                    break

            if not broken_reflection:
                reflection_axes.append(axis)
                
        if len(reflection_axes) > 1:
            ic(reflection_axes)
        return reflection_axes[0] if reflection_axes else None


    def get_horizontal_reflection_axis(self, map_):
        potential_reflection_axes = []
        for idx, _ in enumerate(map_[0]):
            if idx == 0:
                continue

            idx_0 = idx - 1
            idx_1 = idx

            if map_[0][idx_0] == map_[0][idx_1]:
                if all(
                    map_[idy][idx_0] == map_[idy][idx_1] for idy in range(len(map_))
                ):
                    potential_reflection_axes.append(idx_0)

        reflection_axes = []
        for axis in potential_reflection_axes:
            broken_reflection = False

            for offset in range(axis + 1):
                if axis + 1 + offset >= len(map_[0]):
                    break

                first_row = [x[axis - offset] for x in map_]
                second_row = [x[axis + 1 + offset] for x in map_]

                if first_row != second_row:
                    broken_reflection = True
                    break

            if not broken_reflection:
                reflection_axes.append(axis)

        if len(reflection_axes) > 1:
            ic(reflection_axes)
        return reflection_axes[0] if reflection_axes else None

    def part_2(self):
        count = 0

        for map_ in self.maps:
            h_axis, v_axis = None, None
            h_axis = self.get_horizontal_reflection_axis_with_1_smidge(map_)
            v_axis = self.get_vertical_reflection_axis_with_1_smidge(map_)
            ic(h_axis, v_axis)
            count += h_axis + 1 if h_axis is not None else (v_axis + 1) * 100 if v_axis is not None else 0

        return count

    def get_horizontal_reflection_axis_with_1_smidge(self, map_):
        smidge_axes = []

        for idx in range(len(map_[0]) - 1):
            mistakes = 0

            for offset in range(idx + 1):
                if idx + 1 + offset >= len(map_[0]):
                    break

                first_row = ''.join(x[idx - offset] for x in map_)
                second_row = ''.join(x[idx + 1 + offset] for x in map_) 
                mistakes += self.count_row_differences(first_row, second_row)

                if mistakes > 1:
                    break
            
            if mistakes == 1:
                smidge_axes.append(idx)

        return smidge_axes[0] if smidge_axes else None

    def get_vertical_reflection_axis_with_1_smidge(self, map_):
        smidge_axes = []

        for idx in range(len(map_) - 1):
            mistakes = 0

            for offset in range(idx + 1):
                if idx + 1 + offset >= len(map_):
                    break

                first_row = map_[idx - offset] 
                second_row = map_[idx + 1 + offset] 
                mistakes += self.count_row_differences(first_row, second_row)
                if mistakes > 1:
                    break
            
            if mistakes == 1:
                smidge_axes.append(idx)

        return smidge_axes[0] if smidge_axes else None


    def count_row_differences(self, r0, r1) -> int:
        if len(r0) != len(r1):
            raise ValueError("Rows are different sizes")

        return sum(1 for r0, r1 in zip(r0, r1) if r0 != r1)


def day():
    day = Day()
    # print(f"day_13: {day.part_1()}, {day.part_2()}")
    print(day.part_2())
