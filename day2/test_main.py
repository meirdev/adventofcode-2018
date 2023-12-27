from .main import part1, part2


def test_part1():
    input = """
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
"""

    assert part1(input) == 12


def test_part2():
    input = """
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
"""

    assert part2(input) == "fgij"


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 4693
    assert part2(input) == "pebjqsalrdnckzfihvtxysomg"
