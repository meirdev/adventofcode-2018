from .main import part1, part2


INPUT = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def test_part1():
    assert part1(INPUT) == 138


def test_part2():
    assert part2(INPUT) == 66


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 47112
    assert part2(input) == 28237
