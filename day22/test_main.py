from .main import part1, part2


INPUT = """
depth: 510
target: 10,10
"""


def test_part1():
    assert part1(INPUT) == 114


def test_part2():
    assert part2(INPUT) == 45


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 8575
    assert part2(input) == 0
