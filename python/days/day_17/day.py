import sys
import re
from typing import List, Set
from loguru import logger
from dataclasses import dataclass, field
from dataclasses import replace as copy_dataclass
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

@dataclass
class NodeDir:
    acc_weight: int
    steps_left: int
    path: List[Tuple[int]]


@dataclass
class Node:
    idx: int
    idy: int
    weight: int
    north: List[NodeDir] = field(default_factory=lambda: []) 
    south: List[NodeDir] = field(default_factory=lambda: []) 
    east: List[NodeDir] = field(default_factory=lambda: []) 
    west: List[NodeDir] = field(default_factory=lambda: []) 


class Day:
    directions = {
        "north": {"delta": (-1, 0), "sides": ("east", "west")},
        "south": {"delta": (1, 0), "sides": ("east", "west")},
        "east": {"delta": (0, 1), "sides": ("north", "south")},
        "west": {"delta": (0, -1), "sides": ("north", "south")},
    }

    def __init__(self):
        ex_000 = """
12
34
"""

        ex_001 = """
123
456
789
"""

        ex_input_1 = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

        lines = ex_input_1.strip().splitlines()
        lines = open("days/day_17/input.txt").read().strip().splitlines()
        self.map = []

        for row_idx, row in enumerate(lines):
            nodes_row = []
            for col_idx, char in enumerate(row):
                nodes_row.append(Node(row_idx, col_idx, int(char)))

            self.map.append(nodes_row)

        self.map[0][0].east = [NodeDir(acc_weight=0, steps_left=3, path=[(0, 0)])]
        self.map[0][0].south = [NodeDir(acc_weight=0, steps_left=3, path=[(0, 0)])]

    def part_1(self):
        changed = True


        laps = 0
        while changed:
            changed = False
            sum_changed = 0
            for row_idx, node_row in enumerate(self.map):
                for col_idx, node in enumerate(node_row):
                    for side in ("north", "south", "east", "west"):
                        changed_node = self._visit_side(node, side)
                        if changed_node:
                            sum_changed += 1

                        changed = changed_node or changed

            laps += 1
            ic(laps, sum_changed)

        min_weight = float('inf')
        for side in ("north", "south", "east", "west"):
            for path in getattr(self.map[-1][-1], side):
                min_weight = min(min_weight, path.acc_weight)

        return min_weight


    def _visit_side(self, node, side):
        host_node_idx, host_node_idy = (
            node.idx + self.directions[side]["delta"][0],
            node.idy + self.directions[side]["delta"][1],
        )

        if not all(
            (0 <= host_node_idx < len(self.map), 0 <= host_node_idy < len(self.map[0]))
        ):
            return

        if not (node_side := getattr(node, side)):
            return

        host_node = self.map[host_node_idx][host_node_idy]
        host_node_side = getattr(host_node, side)

        changed = False
        for path_to_here in node_side:
            if path_to_here.steps_left == 1:
                # if we can take only one step, we don't write the 0 steps left path to the new node to go on 
                continue

            new_node_dir = NodeDir(
                acc_weight=path_to_here.acc_weight + host_node.weight,
                steps_left=path_to_here.steps_left - 1,
                path=path_to_here.path + [(host_node.idx, host_node.idy)],
            )
            changed = self._update_nodedir(new_node_dir, host_node_side) or changed

        lowest_weight_path_to_here = min(node_side, key=lambda x: x.acc_weight)

        new_node_dir_side = NodeDir(
            acc_weight=lowest_weight_path_to_here.acc_weight + host_node.weight,
            steps_left=3,
            path=lowest_weight_path_to_here.path + [(host_node.idx, host_node.idy)],
        )
        side_1, side_2 = self.directions[side]["sides"]
        changed = (
            self._update_nodedir(
                copy_dataclass(new_node_dir_side), getattr(host_node, side_1)
            )
            or changed
        )
        changed = (
            self._update_nodedir(
                copy_dataclass(new_node_dir_side), getattr(host_node, side_2)
            )
            or changed
        )

        return changed

    def _update_nodedir(self, new_node_dir, node_dirs):
        if any(
            paths_with_same_steps_left := [x for x in node_dirs if x.steps_left == new_node_dir.steps_left]
        ):
            if len(paths_with_same_steps_left) > 1:
                raise ValueError("Malformed paths_with_same_steps_left")

            other_node_dir = paths_with_same_steps_left[0]
            if other_node_dir.acc_weight <= new_node_dir.acc_weight:
                return False

            node_dirs[node_dirs.index(other_node_dir)] = new_node_dir
            return True

        else:
            node_dirs.append(new_node_dir)
            return True

    def part_2(self):
        pass


def day():
    day = Day()
    print(day.part_1())
