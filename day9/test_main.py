from .main import part1, part2


def test_part1():
    for input, expected in (
        ("9 players; last marble is worth 25 points", 32),
        ("10 players; last marble is worth 1618 points", 8317),
        ("13 players; last marble is worth 7999 points", 146373),
        ("17 players; last marble is worth 1104 points", 2764),
        ("21 players; last marble is worth 6111 points", 54718),
        ("30 players; last marble is worth 5807 points", 37305),
    ):
        assert part1(input) == expected


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 371284
    assert part2(input) == 3038972494
