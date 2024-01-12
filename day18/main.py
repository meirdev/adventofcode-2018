import collections
import copy
import enum
from typing import NamedTuple, TypeAlias


Position: TypeAlias = tuple[int, int]


class AcreType(enum.StrEnum):
    OPEN_GROUND = "."
    TREE = "|"
    LUMBERYARD = "#"


class Scan(NamedTuple):
    grid: dict[Position, AcreType]
    height: int
    width: int


def parse_input(input: str) -> Scan:
    grid: dict[tuple[int, int], AcreType] = {}

    rows = input.strip().splitlines()

    for y, row in enumerate(rows):
        for x, acre in enumerate(row):
            grid[y, x] = AcreType(acre)

    return Scan(grid=grid, height=len(rows), width=len(rows[0]))


def draw(scan: Scan) -> None:
    for y in range(scan.height):
        for x in range(scan.width):
            print(scan.grid[y, x].value, end="")
        print()


def solution(input: str, minutes: int) -> int:
    scan = parse_input(input)

    seen: dict[tuple[tuple[Position, AcreType], ...], int] = {}

    for minute in range(1, minutes + 1):
        grid = scan.grid
        grid_ = copy.deepcopy(scan.grid)

        for (y, x), acre in grid_.items():
            adjacents = collections.Counter(
                grid_.get(i)
                for i in (
                    (y, x + 1),
                    (y, x - 1),
                    (y + 1, x),
                    (y - 1, x),
                    (y - 1, x - 1),
                    (y + 1, x + 1),
                    (y + 1, x - 1),
                    (y - 1, x + 1),
                )
            )

            if acre == AcreType.OPEN_GROUND and adjacents[AcreType.TREE] >= 3:
                grid[(y, x)] = AcreType.TREE
            elif acre == AcreType.TREE and adjacents[AcreType.LUMBERYARD] >= 3:
                grid[(y, x)] = AcreType.LUMBERYARD
            elif acre == AcreType.LUMBERYARD and not (
                adjacents[AcreType.LUMBERYARD] >= 1 and adjacents[AcreType.TREE] >= 1
            ):
                grid[(y, x)] = AcreType.OPEN_GROUND

        grid_as_tuple = tuple(grid.items())

        if grid_as_tuple in seen:
            final = seen[grid_as_tuple] + (
                (minutes - minute) % (minute - seen[grid_as_tuple])
            )
            grid = dict(next(k for k, v in seen.items() if v == final))
            break

        seen[grid_as_tuple] = minute

    values = list(grid.values())

    return values.count(AcreType.LUMBERYARD) * values.count(AcreType.TREE)


def part1(input: str) -> int:
    return solution(input, minutes=10)


def part2(input: str) -> int:
    return solution(input, minutes=1_000_000_000)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
