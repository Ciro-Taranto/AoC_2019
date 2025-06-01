from computer import Computer
from pathlib import Path
from time import perf_counter

with (Path(__file__).parent / "input09.txt").open("r") as fin:
    program = list(map(int, fin.read().strip().split(",")))
computer = Computer(program)
computer.set_input([1])
print(computer.process())

computer = Computer(program)
computer.set_input([2])

start = perf_counter()
print(computer.process())
print(f"Elapsed: {perf_counter() - start:2.4f} seconds.")
