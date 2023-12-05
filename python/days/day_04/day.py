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
class Card:
    id: int
    winning_numbers: Set[int]
    numbers: Set[int]

class Day:
    def __init__(self):
        lines = open("days/day_04/input.txt").read().splitlines()

        lines = [line for line in lines if line]
        cards = []
        for line in lines:
            card_str, numbers_str = line.split(": ")
            card_int = int(card_str.split(" ")[-1])
            winning_numbers_str, numbers_str = numbers_str.split(" | ")
            cards.append(Card(card_int, set([int(x) for x in winning_numbers_str.strip().split(" ") if x != ""]), set([int(x) for x in numbers_str.strip().split(" ") if x != ""])))

        self.cards = cards
            
    def part_1(self):
        return self._add_points()

    def _add_points(self):
        total_points = 0
        for card in self.cards:
            intersection_length = len(card.winning_numbers.intersection(card.numbers))
            total_points += 2 ** (intersection_length - 1) if intersection_length else 0 

        return total_points

    def part_2(self):
        return self._add_scratchcards()

    def _add_scratchcards(self):
        scratchards_list = [1] * len(self.cards)

        for idx, card in enumerate(self.cards):
            matching_numbers = len(card.winning_numbers.intersection(card.numbers))
            for idy in range(idx+1, idx+matching_numbers+1):
                scratchards_list[idy] += scratchards_list[idx]

        return sum(scratchards_list)

def day():
    day = Day()
    print(f"day_04: {day.part_1()}, {day.part_2()}")
