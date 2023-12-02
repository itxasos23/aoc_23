import sys
import re
from typing import List
from loguru import logger
from dataclasses import dataclass
from icecream import ic
from functools import reduce 

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)

@dataclass
class GameHand:
    count: int
    color: str

@dataclass
class GameSet:
    hands: List[GameHand]

@dataclass
class Game:
    id: int
    sets: List[GameSet]


class Day:

    limits = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    game_regex = re.compile(r"Game (\d*): (.*)")
    sets_regex = re.compile(r"([^;]*)")
    hands_regex = re.compile(r"([^,]*)")
    color_count_regex = re.compile(r"(\d+) (\w+)")

    def part_1(self):
        return self._sum_ids_of_possible_games(self._parse_game_input(open("days/day_02/input.txt").read().splitlines()))

    def part_2(self):
        return self._sum_power_of_minimum_set_of_cubes(self._parse_game_input(open("days/day_02/input.txt").read().splitlines()))

    def _parse_game_input(self, lines: List[str]) -> List[Game]:
        games = []
        for line in lines:
            game_id, game_str = self.game_regex.match(line).groups()
            sets = []
            for set_ in [x.strip() for x in self.sets_regex.findall(game_str) if x]:
                hands = []
                for hand in [x.strip() for x in self.hands_regex.findall(set_) if x]:
                    count, color = self.color_count_regex.match(hand).groups()
                    hands.append(GameHand(int(count), color))
                sets.append(GameSet(hands))
            games.append(Game(int(game_id), sets))
        return games
    
    def _sum_ids_of_possible_games(self, games):
        is_possible = lambda game: all(hand.count <= self.limits.get(hand.color, float("inf")) for set_ in game.sets for hand in set_.hands)
        return sum(game.id for game in games if is_possible(game))

    def _sum_power_of_minimum_set_of_cubes(self, games):
        sum_ = 0
        for game in games:
            minimum_set_of_cubes = {}
            for set_ in game.sets:
                for hand in set_.hands:
                    minimum_set_of_cubes[hand.color] = max(minimum_set_of_cubes.get(hand.color, 0), hand.count) 
                    
            power = reduce(lambda x, acc: acc * x, minimum_set_of_cubes.values()) 
            sum_ += power

        return sum_


def day():
    day = Day()
    print("day_02:")
    print(day.part_1())
    print(day.part_2())
