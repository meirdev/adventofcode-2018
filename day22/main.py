import enum
import re
from typing import TypeAlias

import networkx as nx  # type: ignore


class RegionType(enum.IntEnum):
    ROCKY = 0
    WET = 1
    NARROW = 2


class Tool(enum.IntEnum):
    TORCH = 0
    GEAR = 1
    NEITHER = 2


Position: TypeAlias = tuple[int, int]

CaveSystem: TypeAlias = dict[Position, RegionType]


def parse_input(input: str) -> tuple[int, Position]:
    match = re.search(r"depth: (\d+)", input)
    if match is None:
        raise ValueError("depth not found")

    depth = int(match.group(1))

    match = re.search(r"target: (\d+),(\d+)", input)
    if match is None:
        raise ValueError("target not found")

    target = int(match.group(1)), int(match.group(2))

    return depth, target


def get_cave_system(depth, size, target) -> CaveSystem:
    erosion_level: dict[Position, int] = {}

    for y in range(size[1] + 1):
        for x in range(size[0] + 1):
            if (x, y) in ((0, 0), target):
                geologic_index = 0
            elif y == 0:
                geologic_index = x * 16807
            elif x == 0:
                geologic_index = y * 48271
            else:
                geologic_index = erosion_level[x - 1, y] * erosion_level[x, y - 1]

            erosion_level[x, y] = (geologic_index + depth) % 20183

    return {k: RegionType(v % 3) for k, v in erosion_level.items()}


def part1(input: str) -> int:
    depth, target = parse_input(input)

    return sum(get_cave_system(depth, target, target).values())


def part2(input: str) -> int:
    depth, target = parse_input(input)

    corner = (target[0] + 100, target[1] + 100)

    cave_system = get_cave_system(depth, corner, target)

    valid_items = {
        RegionType.ROCKY: (Tool.TORCH, Tool.GEAR),
        RegionType.WET: (Tool.GEAR, Tool.NEITHER),
        Tool.NEITHER: (Tool.TORCH, Tool.NEITHER),
    }

    G = nx.Graph()

    for y in range(0, corner[1] + 1):
        for x in range(0, corner[0] + 1):
            items = valid_items[cave_system[x, y]]
            G.add_edge((x, y, items[0]), (x, y, items[1]), weight=7)
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x <= corner[0] and 0 <= new_y <= corner[1]:
                    new_items = valid_items[cave_system[new_x, new_y]]
                    for item in set(items) & set(new_items):
                        G.add_edge((x, y, item), (new_x, new_y, item), weight=1)

    return nx.dijkstra_path_length(
        G, (0, 0, Tool.TORCH), (target[0], target[1], Tool.TORCH)
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
