import abc
import collections
import contextlib
import copy
import enum
import itertools
from typing import TypeAlias

import networkx as nx  # type: ignore


Position: TypeAlias = tuple[int, int]


class MapValue(enum.StrEnum):
    ELF = "E"
    GOBLIN = "G"
    WALL = "#"
    OPEN_CAVERN = "."


class Map(collections.UserDict[Position, MapValue]):
    def __init__(self, height: int, width: int) -> None:
        super().__init__(
            {(y, x): MapValue.OPEN_CAVERN for y in range(height) for x in range(width)}
        )

        self.height = height
        self.width = width

    def get_adjacent(
        self, position: Position, value: MapValue | None
    ) -> list[Position]:
        y, x = position

        return [
            (y, x)
            for y, x in [(y, x + 1), (y + 1, x), (y, x - 1), (y - 1, x)]
            if value is None or self.get((y, x)) == value
        ]


class Unit(abc.ABC):
    def __init__(self, position: Position, attack_power: int = 3) -> None:
        self.hits = 200
        self.position = position
        self.attack_power = attack_power

    @abc.abstractmethod
    def type(self) -> MapValue:
        ...

    @abc.abstractmethod
    def opponent(self) -> MapValue:
        ...

    def attack(self, unit: "Unit") -> None:
        unit.hits -= self.attack_power

    def move(self, position: Position) -> None:
        self.position = position

    def is_alive(self) -> bool:
        return self.hits > 0

    def __gt__(self, other: "Unit") -> bool:
        return self.position > other.position

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(hits={self.hits}, position={self.position})"


class Goblin(Unit):
    def type(self) -> MapValue:
        return MapValue.GOBLIN

    def opponent(self) -> MapValue:
        return MapValue.ELF


class Elf(Unit):
    def type(self) -> MapValue:
        return MapValue.ELF

    def opponent(self) -> MapValue:
        return MapValue.GOBLIN


class Game:
    def __init__(
        self, map: Map, elf_attack_power: int = 3, elf_no_losses: bool = False
    ) -> None:
        self.map = map
        self.elf_no_losses = elf_no_losses

        self.units: list[Unit] = []

        for position, value in map.items():
            match value:
                case MapValue.ELF:
                    self.units.append(Elf(position, elf_attack_power))
                case MapValue.GOBLIN:
                    self.units.append(Goblin(position))

    def _find_unit(self, position: Position) -> Unit:
        return next(unit for unit in self.units if unit.position == position)

    def attack(self, unit: Unit) -> Unit | None:
        opponents = sorted(
            (
                self._find_unit(adjacent)
                for adjacent in self.map.get_adjacent(unit.position, unit.opponent())
            ),
            key=lambda u: (u.hits, u.position),
        )

        if len(opponents) > 0:
            unit.attack(opponents[0])
            return opponents[0]

        return None

    def move(self, unit: "Unit") -> None:
        targets = [
            adjacent
            for position, value in self.map.items()
            if value == unit.opponent()
            for adjacent in self.map.get_adjacent(position, MapValue.OPEN_CAVERN)
        ]

        graph = create_graph(self.map, [unit.position] + targets)

        unit_target = []

        for target in targets:
            with contextlib.suppress(nx.exception.NetworkXNoPath):
                unit_target.append(
                    (nx.shortest_path_length(graph, unit.position, target), target)
                )

        if len(unit_target) == 0:
            return

        _, min_target = min(unit_target)

        adjacent_target = []

        for adjacent in self.map.get_adjacent(unit.position, MapValue.OPEN_CAVERN):
            with contextlib.suppress(nx.exception.NetworkXNoPath):
                adjacent_target.append(
                    (
                        nx.shortest_path_length(graph, adjacent, min_target),
                        adjacent,
                    )
                )

        if len(adjacent_target) == 0:
            return

        _, new_position = min(adjacent_target)

        self.map[unit.position] = MapValue.OPEN_CAVERN
        self.map[new_position] = unit.type()

        unit.move(new_position)

    def who_win(self) -> MapValue | None:
        result = list(set(unit.type() for unit in self.units if unit.is_alive()))

        return result[0] if len(result) == 1 else None

    def play(self) -> int:
        for round in itertools.count(1):
            units_round = sorted(self.units)

            while len(units_round):
                unit = units_round.pop(0)

                if not unit.is_alive():
                    continue

                attacked = self.attack(unit)

                if attacked is None:
                    self.move(unit)

                    attacked = self.attack(unit)

                if attacked:
                    if not attacked.is_alive():
                        if self.elf_no_losses and attacked.type() == MapValue.ELF:
                            return -1

                        self.units.remove(attacked)
                        self.map[attacked.position] = MapValue.OPEN_CAVERN

                winner = self.who_win()
                if winner:
                    if any(unit.is_alive() for unit in units_round):
                        round -= 1

                    return round * sum(
                        unit.hits for unit in self.units if unit.is_alive()
                    )

        return -1


def parse_input(input: str) -> Map:
    rows = input.strip().splitlines()

    map = Map(len(rows), len(rows[0]))

    for y, row in enumerate(rows):
        for x, column in enumerate(row):
            map[y, x] = MapValue(column)

    return map


def draw(map: Map) -> None:
    print(
        "\n".join(
            "".join(map[y, x].value for x in range(map.width))
            for y in range(map.height)
        )
    )


def create_graph(map: Map, include: list[Position]) -> nx.Graph:
    G = nx.Graph()

    G.add_nodes_from(map)

    valid = {
        position
        for position, value in map.items()
        if value == MapValue.OPEN_CAVERN or position in include
    }

    for y in range(map.height):
        for x in range(map.width):
            if (y, x) in valid and (y + 1, x) in valid:
                G.add_edge((y, x), (y + 1, x))
            if (y, x) in valid and (y, x + 1) in valid:
                G.add_edge((y, x), (y, x + 1))

    return G


def part1(input: str) -> int:
    map = parse_input(input)

    game = Game(map)
    return game.play()


def part2(input: str) -> int:
    map = parse_input(input)

    for i in itertools.count(4):
        game = Game(copy.deepcopy(map), elf_attack_power=i, elf_no_losses=True)

        result = game.play()
        if result != -1:
            return result

    return -1


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
