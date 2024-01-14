from .main import part1, part2


def test_part1():
    for input, expected in (
        ("^WNE$", 3),
        ("^ENWWW(NEEE|SSE(EE|N))$", 10),
        ("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 18),
        ("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23),
        ("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31),
    ):
        assert part1(input) == expected


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 3218
    assert part2(input) == 8725
