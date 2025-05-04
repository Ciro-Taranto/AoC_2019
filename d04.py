from time import perf_counter
from aoc_utils import timing

puzzle_input = "130254-678275"
min_val, max_val = map(int, puzzle_input.split("-"))


def is_valid(password: int, part2: bool = False) -> bool:
    has_adjacent = False
    has_two_consecutive = False
    divisor = 10**5
    current = password // divisor
    rest = password % divisor
    consecutive = 1
    while divisor > 1:
        divisor //= 10
        next = rest // divisor
        is_consecutive = current == next
        has_adjacent = has_adjacent or is_consecutive
        if consecutive == 2 and is_consecutive is False:
            has_two_consecutive = True
        if is_consecutive:
            consecutive += 1
        else:
            consecutive = 1
        if next < current:
            return False
        current = next
        rest %= divisor
    if consecutive == 2:
        has_two_consecutive = True
    return has_adjacent if part2 is False else has_two_consecutive


for val in [112233, 123444, 111122]:
    print(val, is_valid(val, part2=True))

with timing():
    print(sum(is_valid(val, part2=False) for val in range(min_val, max_val + 1)))
with timing():
    print(sum(is_valid(val, part2=True) for val in range(min_val, max_val + 1)))
