from .main import part1, part2


INPUT = "dabAcCaCBAcCcaDA"


def test_part1():
    assert part1(INPUT) == 10


def test_part2():
    assert part2(INPUT) == 4


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 9390
    assert part2(input) == 5898
