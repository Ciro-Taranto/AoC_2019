from computer import Computer
from typing import Optional, Literal
from tqdm import tqdm
from collections import deque
from colorama import Fore

Location = tuple[int, int]


movements = {1: (0, -1), 2: (0, 1), 3: (1, 0), 4: (-1, 0)}
Direction = Literal[1, 2, 3, 4]


def add(first: Location, second: Location) -> Location:
    return first[0] + second[0], first[1] + second[1]


class Droid:
    def __init__(self, program: list[int]):
        self.program = program
        self.start_position = (0, 0)
        self.visited = {self.start_position}
        self.walls = set()
        self.oxygen: Optional[Location] = None

    def explore(self) -> int:
        pbar = tqdm()
        visited = set()
        queue = deque([(self.start_position, Computer(self.program), 0)])
        while queue:
            position, old_computer, steps = queue.popleft()
            visited.add(position)
            for direction, increment in movements.items():
                new_position = add(position, increment)
                if new_position in visited or new_position in self.walls:
                    continue
                computer = old_computer.copy()
                computer.set_input([direction])
                output = computer.process()
                status = int(output.pop())
                if status == 0:
                    self.walls.add(new_position)
                elif status == 1:
                    queue.append((new_position, computer, steps + 1))
                elif status == 2:
                    self.visited = visited
                    self.oxygen = new_position
                    oxygen_steps = steps + 1
                pbar.set_postfix(
                    {
                        "Visited": len(visited),
                        "walls": len(self.walls),
                        "queue": len(queue),
                    }
                )
        return oxygen_steps

    def bfs(self, start: Location) -> int:
        visited = set()
        frontier = deque([(start, 0)])
        while frontier and self.visited.difference(visited):
            position, steps = frontier.popleft()
            visited.add(position)
            for increment in movements.values():
                new_position = add(position, increment)
                if new_position not in visited and new_position in self.visited:
                    frontier.append((new_position, steps + 1))
        return steps

    def draw(self) -> str:
        min_x = min(x for x, _ in self.visited.union(self.walls))
        min_y = min(y for _, y in self.visited.union(self.walls))
        max_x = max(x for x, _ in self.visited.union(self.walls))
        max_y = max(y for _, y in self.visited.union(self.walls))
        lines = []
        for y in range(min_y, max_y + 1):
            line = ""
            for x in range(min_x, max_x + 1):
                if (x, y) in self.walls:
                    line += f"{Fore.RED}#"
                elif (x, y) == (0, 0):
                    line += f"{Fore.GREEN}S"
                elif (x, y) in self.visited:
                    line += f"{Fore.YELLOW}."
                elif (x, y) == self.oxygen:
                    line += f"{Fore.GREEN}O"
                else:
                    line += " "
            lines.append(line)
        return "\n".join(lines)


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input15.txt", "r") as fin:
        program = list(map(int, fin.read().strip().split(",")))

    droid = Droid(program)
    print(droid.explore())
    print(droid.draw())
    print(droid.bfs(droid.oxygen))
