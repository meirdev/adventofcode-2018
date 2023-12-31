import collections
import itertools
from typing import DefaultDict, NamedTuple


class Coordinate(NamedTuple):
    x: int
    y: int


def parse_input(input: str) -> list[Coordinate]:
    return [
        Coordinate(*map(int, line.split(", "))) for line in input.strip().splitlines()
    ]


def get_border(coordinates: list[Coordinate]) -> tuple[int, int, int, int]:
    top, bottom = (
        min(coordinates, key=lambda i: i.y).y,
        max(coordinates, key=lambda i: i.y).y,
    )
    left, right = (
        min(coordinates, key=lambda i: i.x).x,
        max(coordinates, key=lambda i: i.x).x,
    )

    return top, right, bottom, left


def get_distance(a: Coordinate, b: Coordinate) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def part1(input: str) -> int:
    coordinates = parse_input(input)

    top, right, bottom, left = get_border(coordinates)

    closest: DefaultDict[Coordinate, set[Coordinate]] = collections.defaultdict(set)

    for y, x in itertools.product(range(top, bottom + 1), range(left, right + 1)):
        min_distance, coordinates_ = float("inf"), []
        for coordinate in coordinates:
            distance = get_distance(Coordinate(x, y), coordinate)
            if distance < min_distance:
                coordinates_ = [coordinate]
                min_distance = distance
            elif distance == min_distance:
                coordinates_.append(coordinate)

        if len(coordinates_) == 1:
            closest[coordinates_[0]].add(Coordinate(x, y))

    return max(
        len(closest[i])
        for i in closest
        if not any(j.x in [left, right] or j.y in [top, bottom] for j in closest[i])
    )


def part2(input: str, less_than: int = 10_000) -> int:
    coordinates = parse_input(input)

    top, right, bottom, left = get_border(coordinates)

    return sum(
        sum(get_distance(Coordinate(x, y), coordinate) for coordinate in coordinates)
        < less_than
        for (y, x) in itertools.product(range(top, bottom + 1), range(left, right + 1))
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
