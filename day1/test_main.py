from .main import part1, part2


def test_part1():
    for input, expected in [
        ("+1\n-2\n+3\n+1", 3),
        ("+1\n+1\n+1", 3),
        ("+1\n+1\n-2", 0),
        ("-1\n-2\n-3", -6),
    ]:
        assert part1(input) == expected


def test_part2():
    for input, expected in [
        ("+1\n-2\n+3\n+1", 2),
        ("+1\n-1", 0),
        ("+3\n+3\n+4\n-2\n-4", 10),
        ("-6\n+3\n+8\n+5\n-6", 5),
        ("+7\n+7\n-2\n-7\n-4", 14),
    ]:
        assert part2(input) == expected


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 477
    assert part2(input) == 390
