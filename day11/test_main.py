from .main import part1, part2


def test_part1():
    for serial_number, expected in (
        (18, "33,45"),
        (42, "21,61"),
    ):
        assert part1(serial_number) == expected


def test_part2():
    for serial_number, expected in (
        (18, "90,269,16"),
        (42, "232,251,12"),
    ):
        assert part2(serial_number) == expected


def test_input():
    input = 7689

    assert part1(input) == "20,37"
    assert part2(input) == "90,169,15"
