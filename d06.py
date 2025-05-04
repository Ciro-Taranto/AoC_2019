from pathlib import Path
from collections import defaultdict

with open(Path(__file__).parent / "input06.txt", "r") as fin:
    orbits = [line.strip().split(")") for line in fin.readlines()]


class Graph:
    def __init__(self, orbits: list[tuple[str, str]]):
        graph = {}
        com_seen = False
        for parent, child in orbits:
            graph[child] = parent
            com_seen = com_seen or parent == "COM"
        if not com_seen:
            raise ValueError(f"I am looking for a permanent center of mass!")
        self.graph = graph
        self.distances = {"COM": 0}
        connections = defaultdict(set)
        for child, parent in self.graph.items():
            connections[child].add(parent)
            connections[parent].add(child)
        self.connections = connections

    def distance(self, planet: str) -> int:
        if planet in self.distances:
            return self.distances[planet]
        distance = 1 + self.distance(self.graph[planet])
        self.distances[planet] = distance
        return distance

    def total_orbits(self) -> int:
        return sum(self.distance(key) for key in self.graph)

    def explore(self, start: str, end: str) -> int:
        visited = set()
        frontier = [(start, 0)]
        while frontier:
            planet, distance = frontier.pop()
            if planet == end:
                return distance
            visited.add(planet)
            for next_planet in self.connections[planet].difference(visited):
                frontier.append((next_planet, distance + 1))
        print(visited)
        raise ValueError


graph = Graph(orbits)
print(graph.total_orbits())
print(graph.explore(graph.graph["YOU"], graph.graph["SAN"]))
