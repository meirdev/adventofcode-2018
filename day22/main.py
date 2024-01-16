import enum
import re
from typing import TypeAlias


class RegionType(enum.IntEnum):
    ROCKY = 0
    WET = 1
    NARROW = 2


Position: TypeAlias = tuple[int, int]

CaveSystem: TypeAlias = dict[Position, RegionType]


def parse_input(input: str) -> tuple[int, tuple[int, int]]:
    match = re.search(r"depth: (\d+)", input)
    if match is None:
        raise ValueError("depth not found")

    depth = int(match.group(1))

    match = re.search(r"target: (\d+),(\d+)", input)
    if match is None:
        raise ValueError("target not found")

    target = int(match.group(1)), int(match.group(2))

    return depth, target


def get_cave_system(depth, target) -> CaveSystem:
    erosion_level: dict[Position, int] = {}

    for y in range(target[1] + 1):
        for x in range(target[0] + 1):
            if (x, y) in ((0, 0), target):
                geologic_index = 0
            elif y == 0:
                geologic_index = x * 16807
            elif x == 0:
                geologic_index = y * 48271
            else:
                geologic_index = erosion_level[y, x - 1] * erosion_level[y - 1, x]

            erosion_level[y, x] = (geologic_index + depth) % 20183

    return {k: RegionType(v % 3) for k, v in erosion_level.items()}


def part1(input: str) -> int:
    depth, target = parse_input(input)

    return sum(get_cave_system(depth, target).values())


def part2(input: str) -> int:
    return 0


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
