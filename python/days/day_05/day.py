import sys
import re
from typing import List, Set
from loguru import logger
from dataclasses import dataclass
from icecream import ic
from functools import reduce

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


@dataclass
class AgSection:
    destination_start: int
    source_start: int
    len: int


@dataclass
class AgMap:
    sections: List[AgSection]


@dataclass
class MappingFunction:
    from_: int
    to: int
    delta: int


class Day:
    def __init__(self):
        input_ = open("days/day_05/input.txt").read()
        # input_ = open("days/day_05/ex_input.txt").read()
        sections = input_.split("\n\n")
        seeds = sections[0]
        self.seeds = list(map(int, seeds.split(": ")[1].split(" ")))

        maps = sections[1:]
        layers = []

        for map_ in maps:
            lines = map_.splitlines()
            funs = []

            for line in lines[1:]:
                destination_start, source_start, len_ = [int(x) for x in line.split(" ")]
                funs.append(
                    MappingFunction(
                        source_start,
                        source_start + len_ -1,
                        destination_start - source_start,
                    )
                )
            funs.sort(key=lambda x: x.from_)
            layers.append(funs)

        self.layers = layers

    def _apply_layer(self, num, layer):
        return num + sum(fun.delta for fun in layer if fun.from_ <= num <= fun.to)

    def part_1(self):
        locations = []
        for num in self.seeds:
            for layer in self.layers:
                num = self._apply_layer(num, layer)
            locations.append(num)

        return min(locations)

    def part_2(self):
        starting_ranges = []
        for idx in range(len(self.seeds) // 2):
            starting_ranges.append([self.seeds[idx*2], self.seeds[idx*2] + self.seeds[idx*2+1]-1])

        ranges = starting_ranges.copy()
        for layer in self.layers:
            ranges = self._pass_ranges_through_layer(ranges, layer)

        return min(map(lambda x: x[0], ranges))

    def _pass_ranges_through_layer(self, ranges, layer):
        # initial ranges may need to be split:
        splitted_ranges = ranges 

        unchanged = False
        while not unchanged:
            unchanged = True
            
            ranges = splitted_ranges
            splitted_ranges = []

            for r in ranges:
                range_is_not_split = True

                for fun in layer:
                    if r[0] < fun.from_ <= r[1]:
                        range_is_not_split = False
                        splitted_ranges.append([r[0], fun.from_ - 1])
                        splitted_ranges.append([fun.from_, r[1]])
                        break

                    if r[0] <= fun.to < r[1]:
                        range_is_not_split = False
                        splitted_ranges.append([r[0], fun.to])
                        splitted_ranges.append([fun.to+1, r[1]])
                        break

                if range_is_not_split:
                    splitted_ranges.append(r)
                else:
                    unchanged = False

        # ranges are now split, we transform the limits
        new_ranges = []
        for r in splitted_ranges:
            new_range = []
            new_range.append(self._apply_layer(r[0], layer))
            new_range.append(self._apply_layer(r[1], layer))

            new_ranges.append(new_range)

        return new_ranges


def day():
    day = Day()
    print(f"day_05: {day.part_1()}, {day.part_2()}")
