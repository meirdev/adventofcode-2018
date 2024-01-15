import functools
from typing import Iterator


def run(input: str) -> Iterator[tuple[bool, int]]:
    magic_number = int(input.splitlines()[8].split()[1])

    seen = set()
    c = 0

    while True:
        a = c | 65536
        c = magic_number

        while True:
            c = (((c + (a & 255)) & 16777215) * 65899) & 16777215

            if 256 > a:
                k = c in seen

                yield k, c

                if not k:
                    seen.add(c)
                    break
            else:
                a //= 256


def part1(input: str) -> int:
    return next(c for _, c in run(input))


def part2(input: str) -> int:
    p = -1

    for seen, c in run(input):
        if not seen:
            p = c
        else:
            return p


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
