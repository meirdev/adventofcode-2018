import collections
import itertools


def parse_input(input: str) -> list[str]:
    return input.strip().splitlines()


def part1(input: str) -> int:
    strings = parse_input(input)

    letters = {2: 0, 3: 0}

    for string in strings:
        counter = list(collections.Counter(string).values())

        for letter in letters:
            letters[letter] += letter in counter

    return letters[2] * letters[3]


def part2(input: str) -> str:
    strings = parse_input(input)

    return next(
        (
            "".join(i for _, i in sorted(a & b))
            for a, b in itertools.combinations(
                map(lambda i: set(enumerate(i)), strings), 2
            )
            if len(a - b) == 1
        ),
        "",
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
