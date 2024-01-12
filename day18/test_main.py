from .main import part1, part2


INPUT = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""


def test_part1():
    assert part1(INPUT) == 1147


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 495236
    assert part2(input) == 201348
