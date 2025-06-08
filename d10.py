from pathlib import Path
from itertools import combinations
from collections import defaultdict
from tqdm import tqdm
import math
from heapq import heappop, heappush
from time import perf_counter
from typing import Optional
from functools import cmp_to_key
from itertools import cycle

Location = tuple[int, int]


def compare_lines(first: tuple[float, float], second: tuple[float, float]) -> bool:
    if first[1] == 1 and second[1] == -1:
        return 1
    elif first[1] == -1 and second[1] == 1:
        return -1
    elif first[1] == second[1] == 1:
        return first[0] - second[0]
    else:
        return -first[0] + second[0]


class OrbitalStation:
    def __init__(self, asteroids: set[Location], use_tqdm: bool = False):
        self.asteroids = asteroids
        self.visible: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
        self.covered: dict[Location, set[Location]] = defaultdict(set)
        self.tqdm = tqdm if use_tqdm else lambda x: x

    @classmethod
    def from_string(cls, string: str, *args, **kwargs) -> "OrbitalStation":
        asteroids = set()
        for y, line in enumerate(string.split("\n")):
            for x, char in enumerate(line):
                if char == "#":
                    asteroids.add((x, y))
        return cls(asteroids, *args, **kwargs)

    @classmethod
    def from_file(cls, path: Path, *args, **kwargs) -> "OrbitalStation":
        with path.open("r") as f:
            return cls.from_string(f.read(), *args, **kwargs)

    def find_asteroids_in_sight(self) -> None:
        for first, second in self.tqdm(combinations(self.asteroids, 2)):
            if first == second:
                continue
            if second in self.covered[first] or second in self.visible[first]:
                continue
            locations = self.find_possible_locations_between_two_asteroids(
                first, second
            )
            self.visible[first].add(locations[0])
            self.visible[locations[0]].add(first)
            for location in locations[1:]:
                self.covered[first].add(location)
                self.covered[location].add(first)
        return

    def part_one(self) -> int:
        self.find_asteroids_in_sight()
        return max(len(visible) for visible in self.visible.values())

    def part_two(self, total: int = 200) -> int:
        self.find_asteroids_in_sight()
        station = max(self.visible, key=lambda x: len(self.visible[x]))
        print(f"Station @ {station}")
        asteroids_by_line = dict()
        for asteroid in self.asteroids:
            if asteroid == station:
                continue
            d, a, s = self.find_line_and_distance(station, asteroid)
            if (a, s) not in asteroids_by_line:
                asteroids_by_line[a, s] = []
            heappush(asteroids_by_line[a, s], (d, asteroid))
        sorted_keys = sorted(
            asteroids_by_line, key=cmp_to_key(compare_lines), reverse=True
        )
        asteroid_groups = [asteroids_by_line[key] for key in sorted_keys]
        destroyed = []
        for group in cycle(asteroid_groups):
            if group:
                _, asteroid = heappop(group)
                destroyed.append(asteroid)
            if len(destroyed) == total:
                return destroyed

    def find_possible_locations_between_two_asteroids(
        self, first: Location, second: Location
    ) -> list[Location]:
        dx = second[0] - first[0]
        dy = second[1] - first[1]
        if dx != 0:
            greatest_common_divisor = math.gcd(dx, dy)
            increment_x = dx // greatest_common_divisor
            increment_y = dy // greatest_common_divisor
            max_steps = (dx // increment_x) + 1
        else:
            increment_x = 0
            increment_y = dy // abs(dy)
            max_steps = (dy // increment_y) + 1
        locations = []
        for step in range(1, max_steps):
            location = (
                first[0] + increment_x * step,
                first[1] + increment_y * step,
            )
            if location in self.asteroids:
                locations.append(location)
        return locations

    @staticmethod
    def find_line_and_distance(
        first: Location, second: Location
    ) -> tuple[float, float, int]:
        distance = abs(first[0] - second[0]) + abs(first[1] - second[1])
        if first[0] != second[0]:
            a = round((second[1] - first[1]) / (second[0] - first[0]), 20)
            sign = 1 if second[0] > first[0] else -1
        else:
            sign = 1 if second[1] > first[1] else -1
            a = 10**10 * sign
        return distance, a, sign


if __name__ == "__main__":
    os = OrbitalStation.from_file(Path(__file__).parent / "input10.txt", use_tqdm=False)
    start = perf_counter()
    print(os.part_one())
    print(f"Elapsed {perf_counter() - start:2.4f} seconds.")

    os = OrbitalStation.from_file(Path(__file__).parent / "input10.txt")

    start = perf_counter()
    destroyed = os.part_two()
    print(f"Elapsed {perf_counter() - start:2.4f} seconds.")

    print(len(destroyed), destroyed[-1], destroyed[-1][0] * 100 + destroyed[-1][1])
