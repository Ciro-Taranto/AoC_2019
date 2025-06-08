from computer import Computer
import typing

Location = tuple[int, int]

rotations = {
    ((0, -1), 1): (1, 0),
    ((0, 1), 1): (-1, 0),
    ((1, 0), 1): (0, 1),
    ((-1, 0), 1): (0, -1),
    ((0, -1), 0): (-1, 0),
    ((0, 1), 0): (1, 0),
    ((1, 0), 0): (0, -1),
    ((-1, 0), 0): (0, 1),
}


class HullPaintingRobot:
    def __init__(self, computer: Computer):
        self.computer = computer
        self.current_location = (0, 0)
        self.current_direction = (0, -1)
        self.painted_white: set[Location] = set()
        self.visited: set[Location] = set()

    def paint(self, camera_input: typing.Literal[0, 1] = 0) -> None:
        while not self.computer.terminated:
            self.computer.set_input([camera_input])
            color, signal = self.computer.process()
            if color == 1:
                self.painted_white.add(self.current_location)
            if color == 0 and self.current_location in self.painted_white:
                self.painted_white.remove(self.current_location)
            self.rotate(signal)
            self.update_location()
            self.visited.add(self.current_location)
            camera_input = self.get_input()

    @staticmethod
    def move(location: Location, direction: tuple[int, int]) -> Location:
        return location[0] + direction[0], location[1] + direction[1]

    def get_input(self) -> bool:
        return self.current_location in self.painted_white

    def update_location(self) -> None:
        self.current_location = self.move(self.current_location, self.current_direction)

    def rotate(self, signal: typing.Literal[0, 1]):
        self.current_direction = rotations[self.current_direction, signal]

    def draw(self) -> str:
        max_x = max(x for x, _ in self.painted_white)
        min_x = min(x for x, _ in self.painted_white)
        max_y = max(y for _, y in self.painted_white)
        min_y = min(y for _, y in self.painted_white)
        lines = []
        for y in range(min_y, max_y + 1):
            line = ""
            for x in range(min_x, max_x + 1):
                line += "#" if (x, y) in self.painted_white else "."
            lines.append(line)
        return "\n".join(lines)


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input11.txt", "r") as fin:
        program = list(map(int, fin.read().strip().split(",")))
    hpr = HullPaintingRobot(Computer(program))
    hpr.paint(1)
    print(len(hpr.visited))
    print(hpr.draw())
