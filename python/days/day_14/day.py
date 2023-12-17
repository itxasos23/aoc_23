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
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".strip()

        input_ = open("days/day_14/input.txt").read()
        self.starting_setup = input_.splitlines()

    def part_1(self):
        moved = True

        setup = [l for l in self.starting_setup]

        while moved:
            moved = False
            for row_idx in range(len(setup) - 1):
                for col_idx in range(len(setup[0])):
                    if (
                        setup[row_idx][col_idx] == "."
                        and setup[row_idx + 1][col_idx] == "O"
                    ):
                        setup[row_idx] = (
                            setup[row_idx][:col_idx]
                            + "O"
                            + setup[row_idx][col_idx + 1 :]
                        )
                        setup[row_idx + 1] = (
                            setup[row_idx + 1][:col_idx]
                            + "."
                            + setup[row_idx + 1][col_idx + 1 :]
                        )
                        moved = True

        return self._calculate_load(setup)

    def _calculate_load(self, setup):
        sum_ = 0
        for row_idx, row in enumerate(setup):
            for char in row:
                if char == "O":
                    sum_ += len(setup) - row_idx

        return sum_

    def _move_north(self, setup):
        moved = True
        while moved:
            moved = False
            for row_idx in range(len(setup) - 1):
                for col_idx in range(len(setup[0])):
                    if (
                        setup[row_idx][col_idx] == "."
                        and setup[row_idx + 1][col_idx] == "O"
                    ):
                        moved = True
                        setup[row_idx] = (
                            setup[row_idx][:col_idx]
                            + "O"
                            + setup[row_idx][col_idx + 1 :]
                        )
                        setup[row_idx + 1] = (
                            setup[row_idx + 1][:col_idx]
                            + "."
                            + setup[row_idx + 1][col_idx + 1 :]
                        )

        return setup

    def _move_south(self, setup):
        moved = True
        while moved:
            moved = False
            for row_idx in range(len(setup) - 1, 0, -1):
                for col_idx in range(len(setup[0])):
                    if (
                        setup[row_idx][col_idx] == "."
                        and setup[row_idx - 1][col_idx] == "O"
                    ):
                        moved = True
                        setup[row_idx] = (
                            setup[row_idx][:col_idx]
                            + "O"
                            + setup[row_idx][col_idx + 1 :]
                        )
                        setup[row_idx - 1] = (
                            setup[row_idx - 1][:col_idx]
                            + "."
                            + setup[row_idx - 1][col_idx + 1 :]
                        )

        return setup

    def _move_west(self, setup):
        moved = True
        while moved:
            moved = False
            for row_idx in range(len(setup)):
                for col_idx in range(len(setup[0]) - 1):
                    if (
                        setup[row_idx][col_idx] == "."
                        and setup[row_idx][col_idx + 1] == "O"
                    ):
                        moved = True
                        setup[row_idx] = (
                            setup[row_idx][:col_idx]
                            + "O"
                            + "."
                            + setup[row_idx][col_idx + 2 :]
                        )
        return setup

    def _move_east(self, setup):
        moved = True
        while moved:
            moved = False
            for row_idx in range(len(setup)):
                for col_idx in range(len(setup[0]) - 1, 0, -1):
                    if (
                        setup[row_idx][col_idx] == "."
                        and setup[row_idx][col_idx - 1] == "O"
                    ):
                        moved = True
                        setup[row_idx] = (
                            setup[row_idx][: col_idx - 1]
                            + "."
                            + "O"
                            + setup[row_idx][col_idx + 1 :]
                        )

        return setup

    def _cycle(self, setup):
        setup = self._move_north(setup)
        setup = self._move_west(setup)
        setup = self._move_south(setup)
        setup = self._move_east(setup)
        return setup

    def part_2(self):
        setup = [l for l in self.starting_setup]
        configs = [[l for l in self.starting_setup]]

        found = False
        cycles = 0
        while not found:
            ic(cycles)
            setup = self._cycle(setup)
            cycles += 1

            if setup in configs:
                break

            configs.append([l for l in setup])

        cycles_to_start_of_loop = configs.index(setup)
        cycle_length = len(configs) - cycles_to_start_of_loop
        configs_loop = configs[cycles_to_start_of_loop:]

        offset = (10 ** 9 - cycles_to_start_of_loop) % cycle_length
        ic(offset)

        return self._calculate_load(configs_loop[offset])


def day():
    day = Day()
    print(day.part_2())
