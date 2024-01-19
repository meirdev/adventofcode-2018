from typing import TypeAlias

import networkx as nx


Points: TypeAlias = tuple[int, int, int, int]


def get_distance(a: Points, b: Points) -> int:
    return sum(abs(i - j) for i, j in zip(a, b))


def parse_input(input: str) -> list[Points]:
    return [tuple(map(int, row.split(","))) for row in input.strip().splitlines()]


def part1(input: str) -> int:
    list_points = parse_input(input)

    G = nx.Graph()

    G.add_edges_from(
        (i, j)
        for i in range(len(list_points))
        for j in range(len(list_points))
        if get_distance(list_points[i], list_points[j]) <= 3
    )

    return sum(1 for _ in nx.connected_components(G))


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))


if __name__ == "__main__":
    main()
