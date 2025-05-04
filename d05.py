from pathlib import Path
from computer import Computer

with open(Path(__file__).parent / "input05.txt", "r") as fin:
    numbers = list(map(int, fin.read().split(",")))

computer = Computer(numbers)
output = computer.process(1)
print(output)

computer = Computer(numbers)
output = computer.process(5)
print(output)
