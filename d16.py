import itertools
import typing
from functools import lru_cache
import numba
import tqdm
import numpy as np


@lru_cache(maxsize=1000)
def repeat(pattern: tuple[int], times: int, length: int) -> typing.Iterable[int]:
    repetitions = -(-(length + 1) // (len(pattern) * times))
    base = list(
        itertools.chain.from_iterable(itertools.repeat(x, times) for x in pattern)
    )
    repeated = sum([base for _ in range(repetitions)], [])
    return repeated[1 : length + 1]


@numba.njit
def triangular_multiplication(values: np.ndarray) -> np.ndarray:
    new_values = np.zeros_like(values)
    accumulator = 0
    for i in range(len(values) - 1, -1, -1):
        accumulator += values[i]
        new_values[i] = accumulator % 10
    return new_values


def just_numpy(values: np.ndarray) -> np.ndarray:
    return (np.cumsum(values[::-1]) % 10)[::-1]


class FFT:
    def __init__(self, pattern: list[int]):
        self.pattern = tuple(pattern)

    def apply(self, numbers: list[int]) -> list[int]:
        new_numbers = []
        for number_id in range(1, len(numbers) + 1):
            pattern = repeat(self.pattern, number_id, len(numbers))
            new_numbers.append(sum((a * b) for a, b in zip(numbers, pattern)))
        return [abs(n) % 10 for n in new_numbers]

    @staticmethod
    def part_two(numbers: list[int], repetitions: int = 10_000) -> int:
        digits_to_skip = int("".join(list(map(str, numbers[:7]))))
        values = (numbers * repetitions)[digits_to_skip:]
        for _ in tqdm.tqdm(range(100)):
            new_values = []
            value = 0
            for number in reversed(values):
                value = (value + number) % 10
                new_values.append(value)
            values = new_values
            values.reverse()
        return "".join(map(str, values[:8]))

    @staticmethod
    def part_two_armin(numbers: list[int], repetitions: int = 10_000) -> int:
        digits_to_skip = int("".join(list(map(str, numbers[:7]))))
        values = (numbers * repetitions)[digits_to_skip:]
        for _ in tqdm.tqdm(range(100)):
            tot = sum(values) % 10
            new_values = [tot]
            for number in values:
                tot = (tot - number) % 10
                new_values.append(tot)
            values = new_values
        return "".join(map(str, values[:8]))

    @staticmethod
    def part_two_fast(numbers: list[int], repetitions: int = 10_000) -> int:
        digits_to_skip = int("".join(list(map(str, numbers[:7]))))
        values = np.array((numbers * repetitions)[digits_to_skip:])
        for it in tqdm.tqdm(range(100)):
            values = triangular_multiplication(values)
        return "".join(map(str, values[:8]))

    @staticmethod
    def part_two_just_numpy(numbers: list[int], repetitions: int = 10_000) -> int:
        digits_to_skip = int("".join(list(map(str, numbers[:7]))))
        values = np.array((numbers * repetitions)[digits_to_skip:])
        for it in tqdm.tqdm(range(100)):
            values = just_numpy(values)
        return "".join(map(str, values[:8]))


if __name__ == "__main__":
    from pathlib import Path
    from time import perf_counter

    with (Path(__file__).parent / "input16.txt").open("r") as f:
        numbers = list(map(int, f.read().strip()))
    pattern = [0, 1, 0, -1]
    fft = FFT(pattern)
    start = perf_counter()
    print(fft.part_two(numbers))
    print(f"Elapsed: {perf_counter() - start:2.4f} seconds.")

    start = perf_counter()
    print(fft.armin(numbers))
    print(f"Elapsed: {perf_counter() - start:2.4f} seconds.")

    exit()
    start = perf_counter()
    print(fft.part_two_fast(numbers))
    print(f"Elapsed: {perf_counter() - start:2.4f} seconds.")

    start = perf_counter()
    print(fft.part_two_just_numpy(numbers))
    print(f"Elapsed: {perf_counter() - start:2.4f} seconds.")
