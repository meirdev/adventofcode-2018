from .main import part1, part2


INPUT = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""


def test_part1():
    assert part1(INPUT) == "CABDFE"


def test_part2():
    assert part2(INPUT, 2, 0) == 15


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == "BCADPVTJFZNRWXHEKSQLUYGMIO"
    assert part2(input) == 973
