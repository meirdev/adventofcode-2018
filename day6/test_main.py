from .main import part1, part2


INPUT = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""


def test_part1():
    assert part1(INPUT) == 17


def test_part2():
    assert part2(INPUT, 32) == 16


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 3840
    assert part2(input) == 46542
