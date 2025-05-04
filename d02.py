from pathlib import Path
from itertools import product
from tqdm import tqdm

with open(Path(__file__).parent / "input02.txt", "r") as f:
    numbers = list(map(int, f.read().strip().split(",")))


class InvalidInput(Exception):
    pass


class Computer(list):
    def process(self) -> None:
        pointer = 0
        while pointer <= len(self):
            optcode = self[pointer]
            if optcode == 99:
                return
            source1, source2, target = self[pointer + 1 : pointer + 4]
            v1 = self[source1]
            v2 = self[source2]
            if optcode == 1:
                self[target] = v1 + v2
            elif optcode == 2:
                self[target] = v1 * v2
            else:
                raise InvalidInput(optcode)
            pointer += 4
        raise InvalidInput("Did not terminate")


computer = Computer(numbers.copy())
computer[1] = 12
computer[2] = 2
computer.process()
print(computer[0])
for val1, val2 in tqdm(product(range(100), range(100))):
    computer = Computer(numbers.copy())
    computer[1] = val1
    computer[2] = val2
    try:
        computer.process()
    except InvalidInput:
        continue
    if computer[0] == 19690720:
        break
print(val1 * 100 + val2)
