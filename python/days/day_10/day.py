import sys
import re
from typing import List, Set
from loguru import logger
from dataclasses import dataclass
from icecream import ic
from functools import reduce
from itertools import cycle
from math import lcm

from typing import Tuple, List, Dict, Any, Optional

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


class Day:
    pipes = {
        "|": [(1, 0), (-1, 0)],
        "-": [(0, 1), (0, -1)],
        "L": [(-1, 0), (0, 1)],
        "J": [(-1, 0), (0, -1)],
        "7": [(1, 0), (0, -1)],
        "F": [(1, 0), (0, 1)],
        ".": [],
        "S": [],
    }

    regions = {
        "|": (((0, -1)), ((0, 1))),
        "-": (((-1, 0)), ((1, 0))),
        "L": (((0, -1), (1, 0)), ()),
        "J": (((0, 1), (1, 0)), ()),
        "7": (((0, 1), (-1, 0)), ()),
        "F": (((0, -1), (-1, 0)), ()),
        ".": [],
        "S": [],
    }

    def __init__(self):
        ex_input_1 = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

        ex_input_2 = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

        ex_input_3 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

        ex_input_4 = """
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
"""
        
        ex_input_5 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

        ex_input_6 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

        input_ = open("days/day_10/input.txt").read()
        lines = input_ 
        self.lines = lines.strip().splitlines()
        self.start = None
        for idx, line in enumerate(self.lines):
            for idy, char in enumerate(line):
                if char == "S":
                    self.start = (idx, idy)
                    break

            if self.start:
                break

    def part_1(self):
        path = self._get_path()
        return len(path) // 2

    def _get_path(self):
        path = [self.start]
        first_pipe = self._get_first_pipe()
        path.append(first_pipe)

        while True:
            last_pipe = path[-1]
            _2last_pipe = path[-2]

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pipe = (last_pipe[0] + dx, last_pipe[1] + dy)

                if _2last_pipe == next_pipe:
                    continue

                if next_pipe[0] >= len(self.lines) or next_pipe[1] >= len(
                    self.lines[0]
                ):
                    continue

                if self._do_pipes_connect(last_pipe, next_pipe):
                    path.append(next_pipe)
                    break

            if next_pipe == self.start:
                break

        return path

    def _get_first_pipe(self):
        for dx, dy in [(0, 1), (0, -1), (1, 0), (1, -1)]:
            if self._do_pipes_connect(
                self.start, (self.start[0] + dx, self.start[1] + dy)
            ):
                next_pipe = (self.start[0] + dx, self.start[1] + dy)
        return next_pipe

    def _do_pipes_connect(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
        p1_pipe = self.lines[p1[0]][p1[1]]
        p1_connections = self.pipes[p1_pipe]

        p2_pipe = self.lines[p2[0]][p2[1]]
        p2_connections = self.pipes[p2_pipe]

        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        p1_connects_to_p2 = (dx, dy) in p1_connections
        p2_connects_to_p1 = (-dx, -dy) in p2_connections

        return any(
            (
                p1_connects_to_p2 and p2_connects_to_p1,
                p1_connects_to_p2 and p2_pipe == "S",
                p2_connects_to_p1 and p1_pipe == "S",
            )
        )

    def part_2(self):
        path = self._get_path()
        self.new_lines = self._get_lines_with_loop_only(path)
        is_right_turn_loop = self._is_right_turn_loop(path)

        outside_tiles = set()
        inside_tiles = set()

        for idx, line in enumerate(self.new_lines):
            for idy, char in enumerate(line):
                if char != ".":
                    continue
                
                if self._tile_connects_to_outside_straight(idx, idy):
                    outside_tiles.add((idx, idy))
                    continue

                elif self._tile_hits_path_on_the_inside(
                    idx, idy, path, is_right_turn_loop
                ):
                    inside_tiles.add((idx, idy))

                else:
                    outside_tiles.add((idx, idy))


        new_new_lines = []
        for idx, line in enumerate(self.new_lines):
            new_new_line = ""

            for idy, char in enumerate(line):
                if (idx, idy) in path:
                    new_new_line += char 

                elif (idx, idy) in outside_tiles:
                    new_new_line += " "

                else:
                    new_new_line += "#"

            new_new_lines.append(new_new_line)

        for line in self.new_lines:
            print(line)

        for line in new_new_lines:
            print(line)

        return len(inside_tiles)

    def _tile_connects_to_outside_straight(self, idx, idy):
        return any(
            (
                all(x == "." for x in self.new_lines[idx][:idy]),
                all(x == "." for x in self.new_lines[idx][idy + 1 :]),
                all(l[idy] == "." for l in self.new_lines[:idx]),
                all(l[idy] == "." for l in self.new_lines[idx + 1 :]),
            )
        )

    def _tile_hits_path_on_the_inside(self, idx, idy, path, is_right_turn_loop):
        # we go up
        tiles_to_check = [(x, idy) for x in list(range(idx))[::-1]]

        if (idx, idy) == (4, 10):
            ic.enable()
            ic(idx, idy)
        else:
            ic.disable()

        for idx, idy in tiles_to_check:
            if (pipe := self.new_lines[idx][idy]) in ("|", "-", "7", "F", "J", "L"):
                path_index = path.index((idx, idy))
                pipe_node = path[path_index]
                previous_pipe_node = path[path_index - 1]

                dx, dy = (
                    pipe_node[0] - previous_pipe_node[0],
                    pipe_node[1] - previous_pipe_node[1],
                )

                if pipe == "F":
                    # ...
                    # .F1
                    # .2.

                    if (dx, dy) == (0, -1):  # 1 -> F -> 2 above
                        return is_right_turn_loop
                    else:  # 2 -> F -> 1 above:
                        return not is_right_turn_loop

                if pipe == "7":
                    # ...
                    # 17.
                    # .2.
                    if (dx, dy) == (0, 1):  # 1 -> 7 -> 2 above
                        return not is_right_turn_loop
                    else:
                        return is_right_turn_loop

                if pipe == "J":
                    # .2.
                    # 1J.
                    # ...

                    if (dx, dy) == (0, 1):  # 1 -> J -> 2 above
                        return is_right_turn_loop
                    else:
                        return not is_right_turn_loop

                if pipe == "L":
                    # .2.
                    # .L1
                    # ...

                    ic(dx, dy, is_right_turn_loop, pipe_node, previous_pipe_node)

                    if (dx, dy) == (0, -1):  # 1 -> L -> 2 above
                        return not is_right_turn_loop
                    else:
                        return is_right_turn_loop

                if pipe == "-":
                    # ...
                    # 2-1
                    # .^.
                    # .|.

                    # we're below the line
                    if (dx, dy) == (0, -1):  # 1 -> - -> 2 above
                        return not is_right_turn_loop
                    else:
                        return is_right_turn_loop

                ic("We should not be here")

    def _get_lines_with_loop_only(self, path):
        new_lines = []
        for idx, line in enumerate(self.lines):
            new_line = ""
            for idy, char in enumerate(line):
                if (idx, idy) in path:
                    new_line += char
                else:
                    new_line += "."
            new_lines.append(new_line)
        return new_lines

    def _is_right_turn_loop(self, path):
        for idx, current_node in enumerate(path):
            if idx == 0:
                continue

            previous_node = path[idx - 1]

            dx = current_node[0] - previous_node[0]
            dy = current_node[1] - previous_node[1]

            if dx:
                # we check left and right
                if all(
                    x == "." for x in self.new_lines[current_node[0]][: current_node[1]]
                ):
                    ic()
                    ic(previous_node, current_node)
                    return dx < 0

                if all(
                    x == "." for x in self.new_lines[current_node[0]][current_node[1]+1:]
                ):
                    ic()
                    ic(previous_node, current_node)
                    return dx > 0


def day():
    day = Day()
    print(f"day_10: {day.part_1()}, {day.part_2()}")
