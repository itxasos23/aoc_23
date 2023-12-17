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
        ex_input_1 = "HASH"
        ex_input_2 = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
        input_ = open("days/day_15/input.txt").read().strip()

        self.strings = input_.split(",")


    def part_1(self):
        sum_ = 0
        for seq in self.strings:
            sum_ += self._get_hash_of_str(seq)
        return sum_

    def _get_hash_of_str(self, seq):
        cv = 0
        for char in seq:
            cv = self._get_hash(char, cv)
        return cv

    def _get_hash(self, char, cv):
        a = (ord(char) + cv) % 256
        return a * 17 % 256

    def _get_total_value(self, boxes):
        sum_ = 0
        for box_idx, box in boxes.items():
            for len_idx, len in enumerate(box):
                sum_ += (1 + box_idx) * (1 + len_idx) * len[1]

        return sum_

    def part_2(self):
        boxes = {}
        ic(len(self.strings))
        ic(self.strings)
        for instruction in self.strings:
            if "=" in instruction:
                label = instruction.split("=")[0]
                action = "="
                fl = int(instruction.split("=")[1])
            elif "-" in instruction:
                label = instruction.split("-")[0]
                action = "-"
                fl = None
            else:
                raise ValueError(f"Malformed instruction: {instruction}")

            box_id = self._get_hash_of_str(label)
            box = boxes.get(box_id, [])
            box_labels = [b[0] for b in box]

            if action == "=":

                if box and label in (b[0] for b in box):
                    idx = box_labels.index(label)
                    box[idx] = (label, fl)

                elif box:
                    box.append((label, fl))

                else:
                    boxes[box_id] = [(label, fl)]

            elif action == "-":
                if box and label in (b[0] for b in box):
                    idx = box_labels.index(label)
                    del box[idx]

                    if not box:
                        del boxes[box_id]

        return self._get_total_value(boxes)


def day():
    day = Day()
    # print(day.part_1())
    print(day.part_2())
