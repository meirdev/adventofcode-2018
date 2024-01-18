from .main import part1, part2


INPUT = """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
"""


def test_part1():
    assert part1(INPUT) == 5216


def test_part2():
    assert part2(INPUT) == 51


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 22996
    assert part2(input) == 4327
