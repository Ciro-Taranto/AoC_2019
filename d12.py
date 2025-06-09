from __future__ import annotations
import itertools
from dataclasses import dataclass, astuple
from tqdm import tqdm
import math


@dataclass
class Position:
    x: int
    y: int
    z: int

    # Yes: type annotation is wrong, 3.10 does not have Self.
    def __add__(self, other: Velocity) -> Position:
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)

    def energy(self) -> int:
        return sum(map(abs, astuple(self)))


class Velocity(Position):
    def invert(self) -> Velocity:
        return Velocity(-self.x, -self.y, -self.z)


@dataclass
class State:
    position: Position
    velocity: Velocity

    def energy(self) -> int:
        return self.position.energy() * self.velocity.energy()


def direction_vector(first: Position, second: Position) -> Velocity:
    return Velocity(
        *[unit_direction(p1, p2) for p1, p2 in zip(astuple(first), astuple(second))]
    )


def unit_direction(p1: int, p2: int) -> int:
    if p1 == p2:
        return 0
    return abs(p2 - p1) / (p2 - p1)


class System:
    def __init__(self, states: list[State]):
        self.states = states
        self.visited = {direction: {} for direction in "xyz"}
        self.steps = 0

    def update_gravity(self):
        for first, second in itertools.combinations(self.states, 2):
            vector = direction_vector(first.position, second.position)
            first.velocity += vector
            second.velocity += vector.invert()

    def update_positions(self):
        for state in self.states:
            state.position += state.velocity

    def update(self) -> None:
        self.update_gravity()
        self.update_positions()

    def part_two(self) -> int:
        cycles = {}
        for i in itertools.count():
            for direction, visited in self.visited.items():
                positions = tuple(
                    [getattr(state.position, direction) for state in self.states]
                )
                velocities = tuple(
                    [getattr(state.velocity, direction) for state in self.states]
                )
                if (positions, velocities) in visited and direction not in cycles:
                    t = visited[positions, velocities]
                    p = i - t
                    cycles[direction] = (t, p)
                    print(f"Cycle for {direction}: period={p}, start={t}")
                else:
                    visited[(positions, velocities)] = i
            self.update()
            if len(cycles) == 3:
                break
        return math.lcm(*[p for _, p in cycles.values()])

    def energy(self) -> int:
        return sum(state.energy() for state in self.states)


def part_one(system: System) -> int:
    for _ in range(1000):
        system.update()
    return system.energy()


if __name__ == "__main__":
    positions = [
        Position(x=5, y=13, z=-3),
        Position(x=18, y=-7, z=13),
        Position(x=16, y=3, z=4),
        Position(x=0, y=8, z=8),
    ]
    system = System([State(position, Velocity(0, 0, 0)) for position in positions])
    print(part_one(system))
    system = System([State(position, Velocity(0, 0, 0)) for position in positions])
    print(system.part_two())
