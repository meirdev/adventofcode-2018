from .main import part1, part2


INPUT = """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"""


def test_part1():
    assert part1(INPUT) == 4


def test_part2():
    assert part2(INPUT) == 3


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 97218
    assert part2(input) == 717
