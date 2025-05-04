from pathlib import Path
import math

with open(Path(__file__).parent / "input01.txt", "r") as f:
    nums = list(map(int, f.readlines()))


def fun(val: int) -> int:
    return math.floor(val / 3) - 2


print(sum(map(fun, nums)))


def part2(val: int) -> int:
    val = max(fun(val), 0)
    return val + part2(val) if val else val


print(sum(map(part2, nums)))
