from pathlib import Path
from itertools import product
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
    def __init__(self, asteroids: set[Location]):
        self.asteroids = asteroids
        self.visible: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
        self.covered: dict[Location, set[Location]] = defaultdict(set)

    @classmethod
    def from_string(cls, string: str) -> "OrbitalStation":
        asteroids = set()
        for y, line in enumerate(string.split("\n")):
            for x, char in enumerate(line):
                if char == "#":
                    asteroids.add((x, y))
        return cls(asteroids)

    def to_string(self) -> str:
        min_x = min(a[0] for a in self.asteroids)
        min_y = min(a[1] for a in self.asteroids)
        max_x = max(a[0] for a in self.asteroids)
        max_y = max(a[1] for a in self.asteroids)
        lines = []
        for y in range(min_y, max_y + 1):
            line = ""
            for x in range(min_x, max_x + 1):
                line += "#" if (x, y) in self.asteroids else "."
            lines.append(line)
        return "\n".join(lines)

    @classmethod
    def from_file(cls, path: Path) -> "OrbitalStation":
        with path.open("r") as f:
            return cls.from_string(f.read())

    def find_asteroids_in_sight(self) -> None:
        for first, second in tqdm(product(self.asteroids, self.asteroids)):
            if first == second:
                continue
            if second in self.covered[first] or second in self.visible[first]:
                continue
            locations = self.find_possible_locations_between_two_asteroids(
                first, second
            )
            if not locations:
                self.visible[first].add(second)
                self.visible[second].add(first)
            else:
                self.visible[first].add(locations[0])
                self.visible[locations[0]].add(first)
                for location in locations[1:]:
                    self.covered[location].add(first)
                    self.covered[first].add(location)
                self.visible[second].add(locations[-1])
                self.visible[locations[-1]].add(second)
                self.covered[first].add(second)
                self.covered[second].add(first)
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
            d, a, s, _ = self.find_line_and_distance(station, asteroid)
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
        _, a, sign, b = self.find_line_and_distance(first, second)
        if first[0] != second[0]:
            locations = [(x, b + a * x) for x in range(first[0], second[0], sign)][1:]
            locations = [
                (x, round(y)) for (x, y) in locations if math.isclose(y, round(y))
            ]
            return [location for location in locations if location in self.asteroids]

        else:
            return [
                (first[0], y)
                for y in range(first[1] + sign, second[1], sign)
                if (first[0], y) in self.asteroids
            ]

    @staticmethod
    def find_line_and_distance(
        first: Location, second: Location
    ) -> tuple[float, float, int, Optional[float]]:
        distance = (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2
        if first[0] != second[0]:
            a = round((second[1] - first[1]) / (second[0] - first[0]), 20)
            b = second[1] - a * second[0]
            sign = 1 if second[0] > first[0] else -1
        else:
            sign = 1 if second[1] > first[1] else -1
            a = 10**10 * sign
            b = None
        return distance, a, sign, b


if __name__ == "__main__":
    os = OrbitalStation.from_file(Path(__file__).parent / "input10.txt")
    start = perf_counter()
    print(os.part_one())
    print(f"Elapsed {perf_counter() - start:2.4f} seconds.")

    os = OrbitalStation.from_file(Path(__file__).parent / "input10.txt")

    start = perf_counter()
    destroyed = os.part_two()
    print(f"Elapsed {perf_counter() - start:2.4f} seconds.")

    print(len(destroyed), destroyed[-1], destroyed[-1][0] * 100 + destroyed[-1][1])
