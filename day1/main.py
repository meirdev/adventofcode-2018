import itertools


def parse_input(input: str) -> list[int]:
    return list(map(int, input.strip().splitlines()))


def part1(input: str) -> int:
    frequencies = parse_input(input)

    return sum(frequencies)


def part2(input: str) -> int:
    frequencies = parse_input(input)

    current = 0

    seen = set([current])

    for i in itertools.cycle(frequencies):
        current += i

        if current in seen:
            break

        seen.add(current)

    return current


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
