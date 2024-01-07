from .main import part1, part2


def test_part1():
    input = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
"""

    assert part1(input) == "7,3"


def test_part2():
    input = r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
"""

    assert part2(input) == "6,4"


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == "124,130"
    assert part2(input) == "143,123"
