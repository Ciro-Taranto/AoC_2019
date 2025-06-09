from __future__ import annotations
import itertools
from dataclasses import dataclass
import math

Position = Velocity = tuple[int, int, int]


def add(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def energy(position: Position) -> int:
    return sum(abs(v) for v in position)


@dataclass
class State:
    position: Position
    velocity: Velocity

    def energy(self) -> int:
        return energy(self.position) * energy(self.velocity)


def direction_vector(
    first: tuple[int, int, int], second: tuple[int, int, int]
) -> tuple[int, int, int]:
    # ugly implement to help numba understand
    return (
        unit_direction(first[0], second[0]),
        unit_direction(first[1], second[1]),
        unit_direction(first[2], second[2]),
    )


def unit_direction(p1: int, p2: int) -> int:
    if p2 > p1:
        return 1
    if p1 == p2:
        return 0
    return -1


class System:
    def __init__(self, states: list[State]):
        self.states = states
        self.steps = 0

    def update_gravity(self):
        for first, second in itertools.combinations(self.states, 2):
            vector = direction_vector(first.position, second.position)
            first.velocity = add(first.velocity, vector)
            second.velocity = add(second.velocity, (-vector[0], -vector[1], -vector[2]))

    def update_positions(self):
        for state in self.states:
            state.position = add(state.position, state.velocity)

    def update(self) -> None:
        self.update_gravity()
        self.update_positions()

    def part_two(self) -> int:
        cycles = {}
        visited = {i: {} for i in range(3)}

        for i in itertools.count():
            for direction, visited_in_direction in visited.items():
                positions = tuple([state.position[direction] for state in self.states])
                velocities = tuple([state.velocity[direction] for state in self.states])
                if (
                    positions,
                    velocities,
                ) in visited_in_direction and direction not in cycles:
                    t = visited_in_direction[positions, velocities]
                    p = i - t
                    cycles[direction] = (t, p)
                    print(f"Cycle for {direction}: period={p}, start={t}")
                else:
                    visited_in_direction[(positions, velocities)] = i
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
        (5, 13, -3),
        (18, -7, 13),
        (16, 3, 4),
        (0, 8, 8),
    ]
    system = System([State(position, (0, 0, 0)) for position in positions])
    print(part_one(system))
    system = System([State(position, (0, 0, 0)) for position in positions])
    print(system.part_two())
