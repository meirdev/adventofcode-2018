from .main import part1, part2


INPUT = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
"""


def test_part1():
    assert part1(INPUT) == 57


def test_part2():
    assert part2(INPUT) == 29


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 31883
    assert part2(input) == 24927
