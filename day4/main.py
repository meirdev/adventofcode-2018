import collections
import re
from datetime import datetime, timedelta
from typing import Callable, DefaultDict, NamedTuple


class GuardDuty(NamedTuple):
    time: datetime
    log: str


def parse_input(input: str) -> list[GuardDuty]:
    return [
        GuardDuty(datetime.strptime(i[0], "%Y-%m-%d %H:%M"), i[1])
        for i in re.findall(r"\[(.*?)\] (.*)", input)
    ]


def solution(input: str, key: Callable[[collections.Counter[int]], int]) -> int:
    guard_duties = parse_input(input)

    sleep_time: DefaultDict[int, collections.Counter[int]] = collections.defaultdict(
        collections.Counter
    )

    guard_id: int
    start_sleep: datetime

    for time, log in sorted(guard_duties):
        if match := re.match(r"Guard #(\d+)", log):
            guard_id = int(match.group(1))
        elif log == "falls asleep":
            start_sleep = time
        elif log == "wakes up":
            while start_sleep < time:
                sleep_time[guard_id][start_sleep.minute] += 1
                start_sleep += timedelta(minutes=1)

    id, sleep_times = max(sleep_time.items(), key=lambda i: key(i[1]))

    return id * sleep_times.most_common(1)[0][0]


def part1(input: str) -> int:
    return solution(input, lambda i: i.total())


def part2(input: str) -> int:
    return solution(input, lambda i: i.most_common(1)[0][1])


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
