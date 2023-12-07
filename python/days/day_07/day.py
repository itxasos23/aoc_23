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


HIGH_CARD = 0
ONE_PAIR = 1
TWO_PAIR = 2
THREE_OF_A_KIND = 3
FULL_HOUSE = 4
FOUR_OF_A_KIND = 5
FIVE_OF_A_KIND = 6

TYPES = [
    HIGH_CARD,
    ONE_PAIR,
    TWO_PAIR,
    THREE_OF_A_KIND,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    FIVE_OF_A_KIND,
]

CARDS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

CARDS2 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


@dataclass
class Hand:
    cards: str
    bet: int

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        self_rank = self._get_rank()
        other_rank = other._get_rank()

        if self_rank < other_rank:
            return True

        if other_rank < self_rank:
            return False

        for self_card, other_card in zip(self.cards, other.cards):
            if CARDS[self_card] < CARDS[other_card]:
                return True

            if CARDS[self_card] > CARDS[other_card]:
                return False

        return False

    def _get_rank(self):
        cards_set = set(self.cards)

        occurrences = []
        for card_type in cards_set:
            occurrences.append(self.cards.count(card_type))

        if 5 in occurrences:
            return FIVE_OF_A_KIND
        elif 4 in occurrences:
            return FOUR_OF_A_KIND
        elif 3 in occurrences and 2 in occurrences:
            return FULL_HOUSE
        elif 3 in occurrences:
            return THREE_OF_A_KIND
        elif occurrences.count(2) == 2:
            return TWO_PAIR
        elif 2 in occurrences:
            return ONE_PAIR
        else:
            return HIGH_CARD


@dataclass
class Hand2:
    cards: str
    bet: int

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        self_rank = self._get_rank()
        other_rank = other._get_rank()

        if self_rank < other_rank:
            return True

        if other_rank < self_rank:
            return False

        for self_card, other_card in zip(self.cards, other.cards):
            if CARDS2[self_card] < CARDS2[other_card]:
                return True

            if CARDS2[self_card] > CARDS2[other_card]:
                return False

        return False

    def _get_rank(self):
        cards_dict = {c: self.cards.count(c) for c in set(self.cards)}

        if not cards_dict.get("J"):
            occurrences = list(cards_dict.values())
            if 5 in occurrences:
                return FIVE_OF_A_KIND
            elif 4 in occurrences:
                return FOUR_OF_A_KIND
            elif 3 in occurrences and 2 in occurrences:
                return FULL_HOUSE
            elif 3 in occurrences:
                return THREE_OF_A_KIND
            elif occurrences.count(2) == 2:
                return TWO_PAIR
            elif 2 in occurrences:
                return ONE_PAIR
            else:
                return HIGH_CARD

        js = cards_dict["J"]
        cards_dict_without_j = cards_dict.copy()
        cards_dict_without_j.pop("J")

        if len(list(cards_dict.keys())) == 2 or js == 5:
            return FIVE_OF_A_KIND
        
        
        if max(cards_dict_without_j.values()) + js == 4:
                return FOUR_OF_A_KIND

        if js == 1 and list(cards_dict_without_j.values()).count(2) == 2:
            return FULL_HOUSE

        if max(cards_dict_without_j.values()) + js == 3:
            return THREE_OF_A_KIND

        return ONE_PAIR 


class Day:
    def __init__(self):
        ex_input = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
        real_input = open("days/day_07/input.txt").read()
        lines = [x for x in ex_input.splitlines() if x]
        lines = [x for x in real_input.splitlines() if x]

        self.cards = []
        self.cards_2 = []
        for line in lines:
            cards, bet_str = line.strip().split(" ")
            self.cards.append(Hand(cards, int(bet_str)))
            self.cards_2.append(Hand2(cards, int(bet_str)))

    def part_1(self):
        sorted_cards = self._sort_cards()
        sum = 0
        for idx, hand in enumerate(sorted_cards):
            sum += (idx + 1) * hand.bet

        return sum

    def _sort_cards(self):
        sorted_cards = sorted(self.cards)
        return sorted_cards

    def _sort_cards_2(self):
        return sorted(self.cards_2)

    def part_2(self):
        sorted_cards = self._sort_cards_2()
        sum = 0
        for idx, hand in enumerate(sorted_cards):
            sum += (idx + 1) * hand.bet

        return sum


def day():
    day = Day()
    print(f"day_07: {day.part_1()}, {day.part_2()}")
