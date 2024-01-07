import collections
import enum
import itertools
from typing import Callable, Counter, TypeAlias


Position: TypeAlias = tuple[int, int]

Track: TypeAlias = list[list[str]]


class Turn(enum.IntEnum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2


class Direction(enum.StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


class Cart:
    def __init__(self, position: Position, direction: Direction) -> None:
        self.position = position
        self.direction = direction

        self.turn = itertools.cycle(Turn)

    def __repr__(self) -> str:
        return f"({self.position})"

    def next(self, track: Track) -> None:
        y, x = self.position

        match self.direction:
            case Direction.UP:
                self.position = (y - 1, x)
            case Direction.DOWN:
                self.position = (y + 1, x)
            case Direction.LEFT:
                self.position = (y, x - 1)
            case Direction.RIGHT:
                self.position = (y, x + 1)

        y, x = self.position

        match track[y][x], self.direction:
            # /
            case "/", Direction.UP:
                self.direction = Direction.RIGHT
            case "/", Direction.DOWN:
                self.direction = Direction.LEFT
            case "/", Direction.LEFT:
                self.direction = Direction.DOWN
            case "/", Direction.RIGHT:
                self.direction = Direction.UP
            # \
            case "\\", Direction.UP:
                self.direction = Direction.LEFT
            case "\\", Direction.DOWN:
                self.direction = Direction.RIGHT
            case "\\", Direction.LEFT:
                self.direction = Direction.UP
            case "\\", Direction.RIGHT:
                self.direction = Direction.DOWN
            # +
            case "+", _:
                match self.direction, next(self.turn):
                    case Direction.UP, Turn.LEFT:
                        self.direction = Direction.LEFT
                    case Direction.UP, Turn.RIGHT:
                        self.direction = Direction.RIGHT
                    case Direction.DOWN, Turn.LEFT:
                        self.direction = Direction.RIGHT
                    case Direction.DOWN, Turn.RIGHT:
                        self.direction = Direction.LEFT
                    case Direction.RIGHT, Turn.LEFT:
                        self.direction = Direction.UP
                    case Direction.RIGHT, Turn.RIGHT:
                        self.direction = Direction.DOWN
                    case Direction.LEFT, Turn.LEFT:
                        self.direction = Direction.DOWN
                    case Direction.LEFT, Turn.RIGHT:
                        self.direction = Direction.UP


def draw(track: Track, carts: list[Cart]) -> None:
    carts_dict: dict[Position, Cart] = {cart.position: cart for cart in carts}

    for y, row in enumerate(track):
        for x, column in enumerate(row):
            if (y, x) in carts_dict:
                print(str(carts_dict[y, x].direction), end="")
            else:
                print(column, end="")
        print()


def parse_input(input: str) -> tuple[Track, list[Cart]]:
    track: Track = []

    carts: list[Cart] = []

    rows = input.strip("\n\r").splitlines()

    for y, row in enumerate(rows):
        track_row = []

        for x, column in enumerate(row):
            if column in [">", "<", "^", "v"]:
                carts.append(Cart((y, x), Direction(column)))

                if column in [">", "<"]:
                    column = "-"
                else:
                    column = "|"

            track_row.append(column)

        track.append(track_row)

    return track, carts


def solution(
    input: str, update_carts: Callable[[Position, list[Cart]], list[Cart]]
) -> str:
    track, carts = parse_input(input)

    while len(carts) != 1:
        carts.sort(key=lambda i: i.position)

        for cart in carts:
            cart.next(track)

            positions: Counter[Position] = collections.Counter(
                cart.position for cart in carts
            )

            crash = max(positions, key=lambda i: positions[i])

            if positions[crash] > 1:
                carts = update_carts(crash, carts)

    y, x = carts.pop().position

    return f"{x},{y}"


def part1(input: str) -> str:
    return solution(
        input,
        lambda crash, carts: [next(cart for cart in carts if cart.position == crash)],
    )


def part2(input: str):
    return solution(
        input,
        lambda crash, carts: [cart for cart in carts if cart.position != crash],
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
