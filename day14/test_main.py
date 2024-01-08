from .main import part1, part2


def test_part1():
    for input, expected in (
        ("9", "5158916779"),
        ("5", "0124515891"),
        ("18", "9251071085"),
        ("2018", "5941429882"),
    ):
        assert part1(input) == expected


def test_part2():
    for input, expected in (
        ("51589", 9),
        ("01245", 5),
        ("92510", 18),
        ("59414", 2018),
    ):
        assert part2(input) == expected


def test_input():
    input = "825401"

    assert part1(input) == "6289129761"
    assert part2(input) == 20207075
