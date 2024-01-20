import copy
import dataclasses
import enum
import itertools
import re
from typing import TypeAlias


class Army(enum.IntEnum):
    IMMUNE_SYSTEM = 0
    INFECTION = 1


@dataclasses.dataclass
class Group:
    id: str
    army: Army
    units: int
    hit_points: int
    weaknesses: set[str]
    immunities: set[str]
    attack_damage: int
    attack_type: str
    initiative: int

    def __hash__(self) -> int:
        return hash(f"{self.army}-{self.id}")

    @property
    def effective_power(self) -> int:
        return self.units * self.attack_damage

    def damage(self, other: "Group") -> int:
        if self.attack_type in other.weaknesses:
            factor = 2
        elif self.attack_type in other.immunities:
            factor = 0
        else:
            factor = 1

        return self.effective_power * factor

    def attack(self, other: "Group") -> int:
        killed = min(other.units, self.damage(other) // other.hit_points)

        other.units -= killed

        return killed


Groups: TypeAlias = list[Group]


def sort_choose_order(groups: Groups) -> Groups:
    return sorted(groups, key=lambda i: (-i.effective_power, -i.initiative))


def sort_select_target(attacker: Group, groups: Groups, targets: set[Group]) -> Groups:
    def key(i: Group):
        return (-attacker.damage(i), -i.effective_power, -i.initiative)

    return sorted(
        (
            i
            for i in groups
            if i.army != attacker.army and i not in targets and attacker.damage(i) > 0
        ),
        key=key,
    )


def is_battle_finished(groups: Groups) -> Army | None:
    armies = set(i.army for i in groups if i.units > 0)

    return armies.pop() if len(armies) == 1 else None


def add_boost(groups: Groups, boost: int) -> Groups:
    groups = copy.deepcopy(groups)

    for group in groups:
        if group.army == Army.IMMUNE_SYSTEM:
            group.attack_damage += boost

    return groups


def parse_input(input: str) -> Groups:
    split = input.find("Infection:")

    armies = {Army.IMMUNE_SYSTEM: input[:split], Army.INFECTION: input[split:]}

    groups: Groups = []

    for army in Army:
        rows = re.findall(
            r"(?P<units>\d+) units each with (?P<hit_points>\d+) hit points (?P<weaknesses_immunities>.*?)"
            r"with an attack that does (?P<attack_damage>\d+) (?P<attack_type>\w+) "
            r"damage at initiative (?P<initiative>\d+)",
            armies[army],
        )

        for id_, (
            units,
            hit_points,
            weaknesses_immunities,
            attack_damage,
            attack_type,
            initiative,
        ) in enumerate(rows, start=1):
            weaknesses: set[str] = set()
            immunities: set[str] = set()

            weaknesses_immunities = weaknesses_immunities.strip(" ()")

            for type, items in re.findall(
                r"(immune|weak) to ([^;]+)", weaknesses_immunities
            ):
                if type == "immune":
                    set_ref = immunities
                else:
                    set_ref = weaknesses

                set_ref.update(filter(None, items.split(", ")))

            groups.append(
                Group(
                    id=str(id_),
                    army=army,
                    units=int(units),
                    hit_points=int(hit_points),
                    attack_damage=int(attack_damage),
                    attack_type=attack_type,
                    initiative=int(initiative),
                    weaknesses=weaknesses,
                    immunities=immunities,
                )
            )

    return groups


def fight(groups: Groups, boost: int = 0) -> tuple[Army, int] | None:
    groups = add_boost(groups, boost)

    while True:
        groups = sort_choose_order(groups)

        battles: dict[Group, Group] = {}
        targets: set[Group] = set()

        for group in groups:
            enemies = sort_select_target(group, groups, targets)
            if len(enemies) > 0:
                enemy = enemies[0]
                battles[group] = enemy
                targets.add(enemy)

        any_killed = False
        for i in sorted(battles, key=lambda i: -i.initiative):
            attacker, defender = i, battles[i]
            if attacker.attack(defender) > 0:
                any_killed = True

        if not any_killed:
            return None

        groups = [i for i in groups if i.units > 0]

        winner = is_battle_finished(groups)

        if winner is not None:
            return winner, sum(i.units for i in groups)


def part1(input: str) -> int:
    groups = parse_input(input)

    if result := fight(groups):
        return result[1]

    return -1


def part2(input: str) -> int:
    groups = parse_input(input)

    for boost in itertools.count(1):
        if result := fight(groups, boost):
            winner, left = result
            if winner == Army.IMMUNE_SYSTEM:
                return left

    return -1


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
