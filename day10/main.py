import dataclasses
import itertools
import re
import time
from typing import NamedTuple

from PIL import Image


class Velocity(NamedTuple):
    x: int
    y: int


@dataclasses.dataclass
class Position:
    x: int
    y: int


@dataclasses.dataclass
class Point:
    position: Position
    velocity: Velocity

    def next_position(self, factor: int = 1) -> None:
        self.position.x += self.velocity.x * factor
        self.position.y += self.velocity.y * factor


def parse_input(input: str) -> list[Point]:
    return [
        Point(Position(*map(int, point[:2])), Velocity(*map(int, point[2:])))
        for point in re.findall(
            r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>",
            input.strip(),
        )
    ]


def draw_image(points: list[Point]) -> Image:
    positions = [point.position for point in points]

    min_x = min(positions, key=lambda p: p.x).x
    max_x = max(positions, key=lambda p: p.x).x
    min_y = min(positions, key=lambda p: p.y).y
    max_y = max(positions, key=lambda p: p.y).y

    width = max_x
    if min_x < 0:
        width += -min_x

    height = max_y
    if min_y < 0:
        height += -min_y

    image = Image.new("1", (width + 1, height + 1))

    for position in positions:
        image.putpixel((abs(position.x), abs(position.y)), 1)

    return image


def solution(input: str) -> tuple[str, int]:
    points = parse_input(input)

    min_velocity = min(
        abs(
            min(
                p.position.x // p.velocity.x if p.velocity.x != 0 else 1,
                p.position.y // p.velocity.y if p.velocity.y != 0 else 1,
            )
        )
        for p in points
    )

    for p in points:
        p.next_position(min_velocity)

    for i in itertools.count(min_velocity):
        image = draw_image(points)
        image.save("image.jpg")

        print(i)

        # TODO: how to check the image?
        # if (text := get_text(image)):
        #     return text, i

        time.sleep(0.5)

        for point in points:
            point.next_position()

    return "", -1


def part1(input: str) -> str:
    return solution(input)[0]


def part2(input: str) -> int:
    return solution(input)[1]


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
