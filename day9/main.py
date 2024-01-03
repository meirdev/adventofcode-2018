import collections
import re
from typing import DefaultDict, NamedTuple


class Game(NamedTuple):
    players: int
    points: int


def parse_input(input: str):
    match = re.match(r"(\d+) players; last marble is worth (\d+) points", input)
    if match is None:
        raise ValueError

    return Game(int(match.group(1)), int(match.group(2)))


def solution(players: int, points: int) -> int:
    scores: DefaultDict[int, int] = collections.defaultdict(int)

    marbles = collections.deque([0])

    for marble in range(1, points + 1):
        if marble % 23 == 0:
            marbles.rotate(7)
            scores[marble % players] += marble + marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(marble)

    return max(scores.values())


def part1(input: str) -> int:
    game = parse_input(input)

    return solution(game.players, game.points)


def part2(input: str) -> int:
    game = parse_input(input)

    return solution(game.players, game.points * 100)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
