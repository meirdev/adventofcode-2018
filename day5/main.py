import collections
import string


def parse_input(input: str) -> str:
    return input.strip()


def polymers_len(polymers: str) -> int:
    polymers_ = collections.deque(map(ord, polymers))

    i = 0

    while i < len(polymers_) - 1:
        if abs(polymers_[i] - polymers_[i + 1]) == 32:
            del polymers_[i + 1]
            del polymers_[i]
            i = max(0, i - 1)
        else:
            i += 1

    return len(polymers_)


def part1(input: str) -> int:
    polymers = parse_input(input)

    return polymers_len(polymers)


def part2(input: str) -> int:
    polymers = parse_input(input)

    return min(
        polymers_len(polymers.replace(i, "").replace(j, ""))
        for i, j in zip(string.ascii_lowercase, string.ascii_uppercase)
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
