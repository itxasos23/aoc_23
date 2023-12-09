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
        input_ = open("days/day_08/input.txt").read()
        instructions, mapping = input_.split("\n\n")
        mapping_dict = {}
        for line in (x for x in mapping.splitlines() if x):
            key, value_str = line.split(" = ")
            left, right = value_str[1:-1].split(", ")
            mapping_dict[key] = {"L": left, "R": right}

        self.instructions_cycle = cycle(instructions.strip())
        self.instructions = instructions.strip()
        self.mapping = mapping_dict

    def part_1(self):
        current_node = "AAA"

        steps = 0
        while current_node != "ZZZ":
            current_node = self.mapping[current_node][next(self.instructions_cycle)]
            steps += 1

        return steps

    def _get_cycle_number_from_node(self, node):
        steps = 0
        instruction_pointer = 0

        while True:
            node = self.mapping[node][self.instructions[instruction_pointer]]
            instruction_pointer = (steps := steps + 1) % len(self.instructions)

            if node[-1] == "Z":
                return steps

    def part_2(self):
        starting_nodes = list(filter(lambda x: x[-1] == "A", self.mapping.keys()))
        return lcm(*[self._get_cycle_number_from_node(x) for x in starting_nodes])

def day():
    day = Day()
    print(f"day_08: {day.part_1()}, {day.part_2()}")
