import collections
import enum
import re
from typing import NamedTuple, TypeAlias

Position: TypeAlias = tuple[int, int]


class TileType(enum.IntEnum):
    SAND = 0
    CLAY = 1
    WATER = 2
    WATER_AT_REST = 3


class Scan(NamedTuple):
    grid: list[list[TileType]]
    min_y: int
    max_y: int


def parse_input(input: str) -> Scan:
    clay: list[Position] = []

    for i in re.findall(r"(\w)=(\d+), (\w)=(\d+)\.\.(\d+)", input):
        k = int(i[1])

        for j in range(int(i[3]), int(i[4]) + 1):
            if i[0] == "y":
                clay.append((k, j))
            else:
                clay.append((j, k))

    _, max_x = max(clay, key=lambda i: i[1])

    min_y, _ = min(clay)
    max_y, _ = max(clay)

    grid = [[TileType.SAND] * (max_x + 2) for _ in range(max_y + 2)]

    for y, x in clay:
        grid[y][x] = TileType.CLAY

    return Scan(
        grid=grid,
        min_y=min_y,
        max_y=max_y,
    )


def draw(grid: list[list[TileType]]) -> None:
    for row in grid:
        for tile in row:
            match tile:
                case TileType.SAND:
                    symbol = "."
                case TileType.CLAY:
                    symbol = "#"
                case TileType.WATER:
                    symbol = "|"
                case TileType.WATER_AT_REST:
                    symbol = "~"
            print(symbol, end="")

        print()


def solution(input: str, count: list[TileType]) -> int:
    scan = parse_input(input)

    spring = (0, 500)

    grid, min_y, max_y = scan

    belows = collections.deque([spring])
    while belows:
        y, x = belows.popleft()

        while y <= max_y and grid[y][x] == TileType.SAND:
            grid[y][x] = TileType.WATER
            y += 1

        if y > max_y or grid[y][x] == TileType.WATER:
            continue

        y -= 1
        x_ = x

        fall = False
        while True:
            for k in (-1, 1):
                x = x_
                while (
                    grid[y + 1][x + k] != TileType.SAND
                    and grid[y][x + k] != TileType.CLAY
                ):
                    x += k
                    grid[y][x] = TileType.WATER

                if (
                    grid[y][x + k] != TileType.CLAY
                    and grid[y + 1][x + k] != TileType.CLAY
                ):
                    belows.append((y, x + k))
                    fall = True

            if fall:
                break

            for k in (-1, 1):
                x = x_
                while grid[y][x] in [TileType.WATER, TileType.WATER_AT_REST]:
                    grid[y][x] = TileType.WATER_AT_REST
                    x += k

            x, y = x_, y - 1
            if grid[y][x] != TileType.WATER:
                grid[y][x] = TileType.WATER

    return sum(
        1
        for y, row in enumerate(grid)
        for tile in row
        if min_y <= y <= max_y and tile in count
    )


def part1(input: str) -> int:
    return solution(input, [TileType.WATER, TileType.WATER_AT_REST])


def part2(input: str) -> int:
    return solution(input, [TileType.WATER_AT_REST])


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
