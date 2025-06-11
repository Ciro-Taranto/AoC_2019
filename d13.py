from computer import Computer
import typing
from time import sleep
from colorama import Fore

Position = tuple[int, int]


# composition or inheritance?
class Arcade:
    def __init__(self, computer: Computer):
        self.tiles: dict[Position, typing.Literal[0, 1, 2, 3, 4]] = {}
        self.computer = computer
        self.points = 0

    def process(self, robot: bool = True, visualize: bool = False):
        dico = {8: -1, 9: 0, 0: 1}
        while not self.computer.terminated:
            out = self.computer.process()
            self.tiles = self.tiles | self.extract_tiles(out)
            if visualize:
                print(self.draw(), flush=True)
                sleep(0.1)
            if not robot:
                user_input = int(input("Give me input"))
                user_input = dico.get(user_input, 0)
            else:
                user_input = self.compute_input()
                print(f"you pressed: {user_input}")
            self.computer.set_input([user_input])
        print(self.draw())

    def compute_input(self) -> typing.Literal[-1, 0, 1]:
        """
        Simple heuristic: move in the direction where the block is.
        """
        for k, v in self.tiles.items():
            if v == 3:
                cursor, _ = k
            if v == 4:
                ball, _ = k
        print(f"ball={ball}, cursor={cursor}")
        if ball > cursor:
            return 1
        elif ball < cursor:
            return -1
        else:
            return 0

    def extract_tiles(
        self, out: list[int]
    ) -> dict[Position, typing.Literal[0, 1, 2, 3, 4]]:
        tiles = {}
        for i in range(0, len(out), 3):
            x, y, t = out[i : i + 3]
            if (x, y) == (-1, 0):
                self.points = t
            else:
                tiles[x, y] = t
        return tiles

    def draw(self) -> str:
        symbols = {
            0: f"{Fore.WHITE}.",
            1: f"{Fore.YELLOW}#",
            2: f"{Fore.WHITE}#",
            3: f"{Fore.GREEN}=",
            4: f"{Fore.GREEN}o",
        }
        min_x = min(x for x, _ in self.tiles)
        max_x = max(x for x, _ in self.tiles)
        min_y = min(y for _, y in self.tiles)
        max_y = max(y for _, y in self.tiles)
        lines = []
        for y in range(min_y, max_y + 1):
            line = ""
            for x in range(min_x, max_x + 1):
                line += symbols[self.tiles.get((x, y), 0)]
            lines.append(line)
        return "\n".join(lines) + f"\n{Fore.GREEN} Points: {self.points}"


def part_one(program: list[int]) -> int:
    computer = Computer(program)
    arcade = Arcade(computer)
    arcade.process()
    print(arcade.draw())
    return sum(v == 2 for v in arcade.tiles.values())


def part_two(program: list[int], robot: bool = False, visualize: bool = False) -> int:
    program = program.copy()
    program[0] = 2
    arcade = Arcade(Computer(program))
    arcade.process(robot=robot, visualize=visualize)


if __name__ == "__main__":
    from pathlib import Path

    with (Path(__file__).parent / "input13.txt").open("r") as fin:
        program = list(map(int, fin.read().strip().split(",")))

    print(part_one(program))
    part_two(program, robot=True, visualize=True)
