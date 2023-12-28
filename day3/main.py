import collections
import re
from typing import DefaultDict, NamedTuple, TypeAlias


class Claim(NamedTuple):
    id: int
    left: int
    top: int
    width: int
    height: int


Point: TypeAlias = tuple[int, int]


def parse_input(input: str) -> list[Claim]:
    return [
        Claim(*map(int, i))
        for i in re.findall(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", input)
    ]


def claim_points(claim: Claim) -> set[Point]:
    return {
        (y, x)
        for y in range(claim.top, claim.top + claim.height)
        for x in range(claim.left, claim.left + claim.width)
    }


def fabric_id_points(
    claims: list[Claim],
) -> tuple[dict[Point, int], DefaultDict[int, set[Point]]]:
    fabric: dict[Point, int] = collections.Counter()

    id_points: DefaultDict[int, set[Point]] = collections.defaultdict(set)

    for claim in claims:
        for point in claim_points(claim):
            fabric[point] += 1
            id_points[claim.id].add(point)

    return fabric, id_points


def part1(input: str) -> int:
    claims = parse_input(input)

    fabric, _ = fabric_id_points(claims)

    return sum(fabric[i] > 1 for i in fabric)


def part2(input: str) -> int:
    claims = parse_input(input)

    fabric, id_points = fabric_id_points(claims)

    not_overlap = set(i for i in fabric if fabric[i] == 1)

    return next(id for id, points in id_points.items() if points < not_overlap)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
