import re
from typing import NamedTuple, Protocol, TypeAlias

Instruction: TypeAlias = tuple[int, ...]

Registers: TypeAlias = list[int]


class Sample(NamedTuple):
    before: Registers
    instruction: Instruction
    after: Registers


class OpCode(Protocol):
    def __call__(self, registers: Registers, instruction: Instruction) -> None:
        ...


def addr(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = registers[instruction[2]]
    registers[instruction[3]] = a + b


def addi(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = instruction[2]
    registers[instruction[3]] = a + b


def mulr(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = registers[instruction[2]]
    registers[instruction[3]] = a * b


def muli(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = instruction[2]
    registers[instruction[3]] = a * b


def banr(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = registers[instruction[2]]
    registers[instruction[3]] = a & b


def bani(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = instruction[2]
    registers[instruction[3]] = a & b


def borr(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = registers[instruction[2]]
    registers[instruction[3]] = a | b


def bori(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = instruction[2]
    registers[instruction[3]] = a | b


def setr(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    registers[instruction[3]] = a


def seti(registers: Registers, instruction: Instruction) -> None:
    a = instruction[1]
    registers[instruction[3]] = a


def gtir(registers: Registers, instruction: Instruction) -> None:
    a = instruction[1]
    b = registers[instruction[2]]
    registers[instruction[3]] = int(a > b)


def gtri(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = instruction[2]
    registers[instruction[3]] = int(a > b)


def gtrr(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = registers[instruction[2]]
    registers[instruction[3]] = int(a > b)


def eqir(registers: Registers, instruction: Instruction) -> None:
    a = instruction[1]
    b = registers[instruction[2]]
    registers[instruction[3]] = int(a == b)


def eqri(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = instruction[2]
    registers[instruction[3]] = int(a == b)


def eqrr(registers: Registers, instruction: Instruction) -> None:
    a = registers[instruction[1]]
    b = registers[instruction[2]]
    registers[instruction[3]] = int(a == b)


OPCODES: list[OpCode] = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr,
]


def to_ints(numbers: list[str]) -> list[int]:
    return list(map(int, numbers))


def parse_input(input: str) -> tuple[list[Sample], list[Instruction]]:
    part_1, part_2 = input.split("\n\n\n")

    samples = []

    for numbers in re.findall(
        r"Before:\s*\[(\d+), (\d+), (\d+), (\d+)]\n"
        r"(\d+) (\d+) (\d+) (\d+)\n"
        r"After:\s*\[(\d+), (\d+), (\d+), (\d+)\]",
        part_1,
    ):
        ints = to_ints(numbers)

        samples.append(Sample(ints[:4], tuple(ints[4:8]), ints[8:]))

    program = [
        tuple(to_ints(numbers))
        for numbers in re.findall(r"(\d+) (\d+) (\d+) (\d+)", part_2)
    ]

    return samples, program


def samples_to_instruction(samples: list[Sample]) -> list[tuple[int, list[OpCode]]]:
    instruction_opcodes = []

    for before, instruction, after in samples:
        opcodes = []
        for opcode in OPCODES:
            registers = before[:]
            opcode(registers, instruction)
            if registers == after:
                opcodes.append(opcode)

        instruction_opcodes.append((instruction[0], opcodes))

    return instruction_opcodes


def part1(input: str) -> int:
    samples, _ = parse_input(input)

    return sum(1 for _, opcodes in samples_to_instruction(samples) if len(opcodes) >= 3)


def part2(input: str) -> int:
    samples, program = parse_input(input)

    id_to_opcodes: dict[int, set[OpCode]] = {i: set(OPCODES) for i in range(16)}

    for opcode_id, opcodes in samples_to_instruction(samples):
        id_to_opcodes[opcode_id] &= set(opcodes)

    while True:
        once = {next(iter(i)) for i in id_to_opcodes.values() if len(i) == 1}
        if len(once) == 16:
            break

        for i in id_to_opcodes:
            if len(id_to_opcodes[i]) > 1:
                id_to_opcodes[i] -= once

    id_to_opcode = {i: next(iter(id_to_opcodes[i])) for i in id_to_opcodes}

    registers = [0, 0, 0, 0]
    for instruction in program:
        id_to_opcode[instruction[0]](registers, instruction)

    return registers[0]


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
