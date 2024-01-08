import itertools
import collections
from typing import Deque, Iterator


def get_recipes() -> Iterator[int]:
    recipes = [3, 7]

    yield from recipes

    elf1, elf2 = 0, 1

    while True:
        new_recipe = recipes[elf1] + recipes[elf2]

        i = (new_recipe,) if new_recipe < 10 else divmod(new_recipe, 10)

        recipes += i

        yield from i

        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)


def part1(input: str) -> str:
    num = int(input)

    return "".join(
        str(recipe) for n, recipe in zip(range(num + 10), get_recipes()) if num <= n
    )


def part2(input: str) -> int:
    latest_recipes: Deque[str] = collections.deque([], maxlen=len(input))

    for i, recipe in zip(itertools.count(1), get_recipes()):
        latest_recipes.append(str(recipe))

        if "".join(latest_recipes) == input:
            return i - len(latest_recipes)

    return -1


def main() -> None:
    input = "825401"

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
