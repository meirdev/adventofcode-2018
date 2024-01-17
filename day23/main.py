import collections
import itertools
import re
from typing import Counter, NamedTuple


class Nanobot(NamedTuple):
    x: int
    y: int
    z: int
    r: int


def parse_input(input: str) -> list[Nanobot]:
    return [
        Nanobot(*map(int, i))
        for i in re.findall(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", input)
    ]


def get_distance(a: Nanobot, b: Nanobot) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def part1(input: str) -> int:
    nanobots = parse_input(input)

    nanobot = max(nanobots, key=lambda i: i.r)

    return sum(1 for i in nanobots if get_distance(i, nanobot) <= nanobot.r)


def part2(input: str) -> int:
    nanobots = parse_input(input)

    distances: Counter[int] = collections.Counter()

    for nanobot in nanobots:
        distances[sum(nanobot[:-1]) - nanobot.r] += 1
        distances[sum(nanobot) + 1] -= 1

    s = 0

    run = [(i, s := s + distances[i]) for i in sorted(distances)]

    max_ = max(i[1] for i in run)

    intervals = [(a, b - 1) for (a, n), (b, _) in itertools.pairwise(run) if n == max_]

    if any(a <= 0 <= b for a, b in intervals):
        return 0

    return min(-b if b < 0 else a for a, b in intervals)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
