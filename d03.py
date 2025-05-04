from pathlib import Path
from typing import Literal

with open(Path(__file__).parent / "input03.txt", "r") as fin:
    instructions = fin.readlines()


class Wire(set):
    def __init__(self):
        self.current = (0, 0)
        self.ordered = {self.current: 0}
        self.steps = 0

    def move(self, direction: Literal["R", "L", "U", "D"], moves: int) -> None:
        y, x = self.current
        if direction == "R":
            to_add = [(y, val) for val in range(x + 1, x + moves + 1)]
        elif direction == "L":
            to_add = [(y, val) for val in range(x - 1, x - moves - 1, -1)]
        elif direction == "U":
            to_add = [(val, x) for val in range(y - 1, y - moves - 1, -1)]
        elif direction == "D":
            to_add = [(val, x) for val in range(y + 1, y + moves + 1)]
        for elem in to_add:
            self.add(elem)
        self.current = to_add[-1]

    def add(self, element) -> None:
        super().add(element)
        self.steps += 1
        if element not in self.ordered:
            self.ordered[element] = self.steps

    def visualize(self) -> str:
        min_x = min(val[1] for val in self)
        max_x = max(val[1] for val in self)
        min_y = min(val[0] for val in self)
        max_y = max(val[0] for val in self)
        lines = []
        for y in range(max_y, min_y - 1, -1):
            line = ""
            for x in range(min_x, max_x + 1):
                if (y, x) == 0:
                    line += "o"
                elif (y, x) in self:
                    line += "#"
                else:
                    line += "."
            lines.append(line)
        return "\n".join(lines)

    @classmethod
    def from_instruction(cls, instruction: str):
        wire = cls()
        for elem in instruction.strip().split(","):
            direction = elem[0]
            moves = int(elem[1:])
            wire.move(direction, moves)
        return wire


wire1 = Wire.from_instruction(instructions[0])
wire2 = Wire.from_instruction(instructions[1])
intersection = wire1.intersection(wire2)
vals = [(wire1.ordered[position], wire2.ordered[position]) for position in intersection]
print(vals)
print(min(a + b for a, b in vals))
