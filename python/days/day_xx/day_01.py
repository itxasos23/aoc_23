import sys
from loguru import logger

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


def part_1():
    print("part_1")


def part_2():
    print("part_2")


def day():
    part_1()
    part_2()
