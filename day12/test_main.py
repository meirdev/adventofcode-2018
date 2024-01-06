from .main import part1, part2


INPUT = """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
"""


def test_part1():
    assert part1(INPUT) == 325


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 3793
    assert part2(input) == 4300000002414
