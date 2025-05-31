from pathlib import Path
from collections import Counter
from colorama import Fore

WIDTH = 25
HEIGHT = 6
PIXELS = WIDTH * HEIGHT


with open(Path(__file__).parent / "input08.txt", "r") as f:
    digits = list(map(int, f.read().strip()))
layers = [digits[i : i + PIXELS] for i in range(0, len(digits), PIXELS)]


def part_one(layers: list[list[int]]) -> int:
    counts = [Counter(layer) for layer in layers]
    zeros = [count[0] for count in counts]
    idx = zeros.index(min(zeros))
    return counts[idx][1] * counts[idx][2]


def part_two(digits: list[int], width: int = WIDTH, height: int = HEIGHT) -> str:
    pixels = width * height
    layers = [digits[i : i + pixels] for i in range(0, len(digits), pixels)]
    mapping = {0: f"{Fore.BLACK}.", 1: f"{Fore.YELLOW}#"}
    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            idx = y * width + x
            for layer in layers:
                c = layer[idx]
                if c != 2:
                    break
            line += mapping[c]
        lines.append(line)
    return "\n".join(lines)


print(part_one(layers))
print(part_two(digits))
