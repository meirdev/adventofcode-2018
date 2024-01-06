import collections
import copy


def solution(serial_number: int, size: int | None = None) -> str:
    grid = [[0] * 301 for _ in range(301)]

    grid_calculated = copy.deepcopy(grid)

    for y in range(1, 301):
        for x in range(1, 301):
            rack_id = x + 10
            power_level = int((rack_id * y + serial_number) * rack_id / 100) % 10 - 5

            grid[y - 1][x - 1] = power_level

    max_square = float("-inf"), -1, -1, -1

    for i in range(size if size else 300):
        print(i)
        for y in range(len(grid_calculated)):
            for x in range(len(grid_calculated[x]) - i):
                grid_calculated[y][x] += grid[y][x + i]

        for x in range(len(grid_calculated[0]) - i):
            total_power = [0] + [grid_calculated[k][x] for k in range(i)]

            for y in range(i - 1, len(grid_calculated) - i):
                if y >= i:
                    total_power.pop(0)
                    total_power.append(grid_calculated[y + i][x])

                total_power_int = sum(total_power)

                if max_square[0] < total_power_int and not (size and size != i + 1):
                    max_square = total_power_int, x + 1, y + 1, i + 1

    return ",".join(map(str, max_square[1 : -1 if size else len(max_square) + 1]))


def part1(input: int) -> str:
    return solution(input, 3)


def part2(input: int) -> str:
    return solution(input)


def main() -> None:
    input = 7689

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
