from typing import TypeAlias


Tree: TypeAlias = list[int]


def parse_input(input: str) -> list[int]:
    return list(map(int, input.strip().split(" ")))


def solution(tree: Tree, part: int, i: int) -> tuple[int, int]:
    childs = tree[i]
    i += 1

    metadata = tree[i]
    i += 1

    node_sum = 0

    childs_sum = {}
    for n in range(1, childs + 1):
        i, child_sum = solution(tree, part, i)
        childs_sum[n] = child_sum

    if part == 1:
        node_sum += sum(childs_sum.values())

    for _ in range(metadata):
        if part == 2 and len(childs_sum) > 0:
            node_sum += childs_sum.get(tree[i], 0)
        else:
            node_sum += tree[i]
        i += 1

    return i, node_sum


def part1(input: str) -> int:
    tree = parse_input(input)

    return solution(tree, 1, 0)[1]


def part2(input: str) -> int:
    tree = parse_input(input)

    return solution(tree, 2, 0)[1]


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
