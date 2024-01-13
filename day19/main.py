import re
from typing import Iterator, NamedTuple, Protocol, TypeAlias

Registers: TypeAlias = list[int]


class Instruction(NamedTuple):
    opcode: str
    a: int
    b: int
    c: int


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


def parse_input(input: str) -> tuple[int, list[Instruction]]:
    match = re.search(r"#ip (\d+)", input)
    if match is None:
        raise ValueError("ip not found")

    ip_register = int(match.group(1))

    instructions = []

    for instruction in re.findall(r"(\w+) (\d+) (\d+) (\d+)", input):
        opcode: str = instruction[0]
        a, b, c = list(map(int, instruction[1:]))

        instructions.append(Instruction(opcode, a, b, c))

    return ip_register, instructions


def run(input: str, registers: list[int]) -> Iterator[tuple[int, Registers]]:
    ip_register, instructions = parse_input(input)

    ip = 0

    while 0 <= ip < len(instructions):
        instruction = instructions[ip]

        yield ip, registers[:]

        globals()[instruction[0]](registers, instruction)

        registers[ip_register] += 1

        ip = registers[ip_register]


def part1(input: str) -> int:
    for _, registers in run(input, [0] * 6):
        pass

    return registers[0]


def part2(input: str) -> int:
    for ip, registers in run(input, [1] + [0] * 5):
        if ip == 33:
            break

    n = registers[2] + registers[5]

    return sum(filter(lambda x: n % x == 0, range(1, n + 1)))


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
