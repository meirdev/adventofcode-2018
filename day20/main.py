import functools
from typing import Iterator, TypeAlias

import networkx as nx  # type: ignore


Position: TypeAlias = tuple[int, int]


ROUTE: dict[str, Position] = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}


def parse_input(input: str) -> str:
    return input.strip()[1:-1]


@functools.cache
def get_shortest_path_length(input: str) -> Iterator[int]:
    routes = parse_input(input)

    G = nx.Graph()

    stack = []
    position: set[Position] = {(0, 0)}
    starts: set[Position] = {(0, 0)}
    ends: set[Position] = set()

    for route in routes:
        match route:
            case "(":
                stack.append((starts, ends))
                starts, ends = position, set()
            case ")":
                position.update(ends)
                starts, ends = stack.pop()
            case "|":
                ends.update(position)
                position = starts
            case "N" | "S" | "E" | "W":
                y, x = ROUTE[route]
                edges = [(p, (p[0] + y, p[1] + x)) for p in position]
                G.add_edges_from(edges)
                position = set(e[1] for e in edges)

    return nx.algorithms.shortest_path_length(G, (0, 0)).values()


def part1(input: str) -> int:
    return max(get_shortest_path_length(input))


def part2(input: str) -> int:
    return sum(1 for length in get_shortest_path_length(input) if length >= 1000)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
