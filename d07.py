from pathlib import Path
from itertools import permutations
from tqdm import tqdm
from itertools import count

from computer import Computer, InvalidInput

with open(Path(__file__).parent / "input07.txt", "r") as f:
    program = list(map(int, f.read().strip().split(",")))


def find_highest_signal(program: list[int]) -> tuple[int, list[int]]:
    max_value = 0
    for inputs in tqdm(list(permutations(range(5)))):
        computers = [
            Computer(program.copy(), user_input=user_input) for user_input in inputs
        ]
        signal = 0
        for computer in computers:
            computer.set_input(signal)
            signal = computer.process()[-1]

        if signal > max_value:
            max_value = signal
            combo = inputs
    return max_value, list(combo)


def find_highest_signal_feedback_mode(program: list[int]) -> tuple[int, list[int]]:
    max_value = 0
    for inputs in tqdm(list(permutations(range(5, 10)))):
        computers = [
            Computer(program.copy(), user_input=user_input) for user_input in inputs
        ]
        signal = [0]
        for _ in count():
            for computer in computers:
                computer.set_input(signal)
                signal = computer.process()

            if computer.terminated:
                signal = signal.pop()
                if signal > max_value:
                    max_value = signal
                    combo = inputs
                break

    return max_value, list(combo)


print(find_highest_signal(program))
print(find_highest_signal_feedback_mode(program))
