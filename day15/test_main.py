from .main import part1, part2

EXAMPLES = (
    (
"""
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""", 27730, 4988
    ),
    (
"""
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
""", 36334, -1
    ),
    (
"""
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""", 39514, 31284
    ),
    (
"""
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""", 27755, 3478
    ),
    (
"""
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""", 28944, 6474
    ),
    (
"""
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
""", 18740, 1140
    )
)

def test_part1():
    for input, expected, _ in EXAMPLES:
        assert part1(input) == expected


def test_part2():
    for input, _, expected in EXAMPLES:
        if expected != -1:
            assert part2(input) == expected


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 190012
    assert part2(input) == 34364
