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

class Day:
    def __init__(self):
        input_ = open("days/day_05/input.txt").read()
        sections = input_.split('\n\n')
        seeds = sections[0]
        self.seeds = list(map(int, seeds.split(": ")[1].split(" ")))
    
        maps = sections[1:]
        parsed_maps = []
        for map_ in maps:
            lines = map_.splitlines()
            chained_maps = []
            for line in lines[1:]:
                chained_maps.append(AgSection(*[int(z) for z in line.split(" ")]))

            parsed_maps.append(AgMap(sections=chained_maps))

        self.ag_maps = parsed_maps

        ic(self.seeds)

    def _map_value(self, value: int, section: AgSection):
        if section.source_start <= value < section.source_start + section.len:
            return True, section.destination_start + (value - section.source_start)
        return False, value

    def part_1(self):
        locations = []
        for num in self.seeds:
            for map_ in self.ag_maps:
                for section in map_.sections:
                    mapped, num = self._map_value(num, section)

                    if mapped:
                        break

            locations.append(num)
        return min(locations)

    def part_2(self):
        pass

def day():
    day = Day()
    print(f"day_05: {day.part_1()}, {day.part_2()}")
