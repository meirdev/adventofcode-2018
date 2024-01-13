from .main import part1, part2


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 1350
    assert part2(input) == 15844608
