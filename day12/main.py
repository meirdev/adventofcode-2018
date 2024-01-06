import re
from typing import NamedTuple


class Input(NamedTuple):
    initial_state: str
    notes: dict[str, str]


EMPTY = "....."


def parse_input(input: str) -> Input:
    initial_state = re.search(r"initial state: (.+)", input)
    if initial_state is None:
        raise ValueError("initial state not found")

    notes = re.findall(r"([\.#]+) => ([.#])", input)

    return Input(
        initial_state=initial_state.group(1),
        notes=dict(notes),
    )


def solution(input: str, max: int) -> int:
    state, notes = parse_input(input)

    state_idx: dict[str, int] = {}

    empty_padding, addition = 0, 0

    for i in range(max):
        if not state.startswith(EMPTY):
            empty_padding += 5
            state = EMPTY + state

        if not state.endswith(EMPTY):
            state += EMPTY

        short_state = state[state.find("#") : state.rfind("#") + 1]

        if short_state in state_idx:
            addition = (max - state_idx[short_state] - 1) * short_state.count("#")
            break

        state_idx[short_state] = i

        state_list = ["."] * len(state)
        for j in range(len(state) - 5):
            state_list[j + 2] = notes.get(state[j : j + 5], ".")

        state = "".join(state_list)

    return (
        sum(j for i, j in zip(state, range(-empty_padding, len(state))) if i == "#")
        + addition
    )


def part1(input: str) -> int:
    return solution(input, max=20)


def part2(input: str) -> int:
    return solution(input, max=50000000000)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
