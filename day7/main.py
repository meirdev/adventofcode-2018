import re
from typing import TypeAlias

Instruction: TypeAlias = tuple[str, str]

Graph: TypeAlias = dict[str, list[str]]


def parse_input(input: str) -> list[Instruction]:
    return re.findall(
        r"Step (\w+) must be finished before step (\w+) can begin.", input
    )


def build_graph(instructions: list[Instruction]) -> Graph:
    graph: Graph = {}

    for a, b in instructions:
        for n in [a, b]:
            if n not in graph:
                graph[n] = []
        graph[b].append(a)

    return graph


def part1(input: str) -> str:
    instructions = parse_input(input)

    graph = build_graph(instructions)
    nodes = sorted(graph)

    steps = []

    while len(nodes):
        node = next(n for n in nodes if len(graph[n]) == 0)

        nodes.remove(node)
        steps.append(node)

        for n in graph:
            if node in graph[n]:
                graph[n].remove(node)

    return "".join(steps)


def part2(input: str, num_workers: int = 5, base_seconds: int = 60) -> int:
    instructions = parse_input(input)

    graph = build_graph(instructions)
    nodes = sorted(graph)

    add_to_queue = lambda nodes: (n for n in nodes if len(graph[n]) == 0)

    cal_seconds = lambda char: base_seconds + 1 + ord(char) - ord("A")

    workers = [
        (cal_seconds(n), n) for _, n in zip(range(num_workers), add_to_queue(nodes))
    ]

    second = 0

    queue: list[str] = []

    while len(workers):
        workers = sorted(workers)

        second, node = workers.pop(0)

        reversed_nodes = [n for n in graph if node in graph[n]]

        for n in graph:
            if node in graph[n]:
                graph[n].remove(node)

        queue += add_to_queue(reversed_nodes)

        while len(workers) < num_workers and queue:
            n = queue.pop()
            workers.append((second + cal_seconds(n), n))

    return second


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
