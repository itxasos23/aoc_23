import sys
import re
from typing import List, Set
from loguru import logger
from dataclasses import dataclass
from icecream import ic
from functools import reduce
from itertools import cycle
from math import lcm

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


class Day:
    def __init__(self):
        ex_input = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
        input_ = open("days/day_09/input.txt").read()
        sequences = []
        for line in input_.splitlines():
            if not line:
                continue

            sequences.append(list(map(lambda x: int(x), line.strip().split(" "))))

        self.sequences = sequences

    def part_1(self):
        sum_ = 0
        for sequence in self.sequences:
            next_value = self.get_next_value(sequence)
            sum_ += next_value

        return sum_

    def get_next_value(self, sequence: List[int]) -> int:
        working_sequence = sequence
        levels_deep = 0

        lists = [sequence]

        while not all(x == 0 for x in working_sequence):
            new_list = []

            for idx in range(len(working_sequence) - 1):
                new_list.append(working_sequence[idx+1] - working_sequence[idx])

            levels_deep += 1 
            working_sequence = new_list
            lists.append(new_list)

        lists.reverse()

        for l_idx, l in enumerate(lists):
            if l_idx == 0:
                l.append(0)
            else:
                l.append(l[-1] + lists[l_idx-1][-1])

        return lists[-1][-1] 

    def part_2(self):
        return sum(self._get_previous_value(seq) for seq in self.sequences)

    def _get_previous_value(self, seq):
        working_sequence = seq 
        levels_deep = 0

        lists = [seq]

        while not all(x == 0 for x in working_sequence):
            new_list = []

            for idx in range(len(working_sequence) - 1):
                new_list.append(working_sequence[idx+1] - working_sequence[idx])

            levels_deep += 1 
            working_sequence = new_list
            lists.append(new_list)

        lists.reverse()

        for l_idx, l in enumerate(lists):
            if l_idx == 0:
                l.insert(0, 0)
            else:
                l.insert(0, l[0] - lists[l_idx-1][0])
        return lists[-1][0] 


def day():
    day = Day()
    print(f"day_09: {day.part_1()}, {day.part_2()}")
