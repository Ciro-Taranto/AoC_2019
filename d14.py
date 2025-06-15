from collections import defaultdict
from typing import Optional


class Material:
    def __init__(self, identifier: str, amount: int, parents: list[tuple[str, int]]):
        self.identifier = identifier
        self.amount = amount
        self.parents = parents


class Reactions:
    def __init__(
        self,
        reaction_table: list[tuple[list[tuple[int, str]]], tuple[str, int]],
        use_tqdm: bool = True,
    ):
        self.materials: dict[str, Material] = {"ORE": Material("ORE", 1, [])}
        for parents, (identifier, amount) in reaction_table:
            self.materials[identifier] = Material(identifier, amount, parents)
        self.use_tqdm = use_tqdm

    def part_one(self) -> int:
        return self.find_needed_material("FUEL", 1)

    def part_two_binsearch(self, available_ore: int = 1000000000000) -> int:
        current = 1
        required_ore = 0
        while required_ore < available_ore:
            current *= 2
            required_ore = self.find_needed_material("FUEL", current)
            print(
                f"For fuel={current}, required: {required_ore}, average: {required_ore/current:2.4f}"
            )
        if required_ore == available_ore:
            return current
        low = current // 2
        high = current
        while low < high:
            mid = (low + high) // 2
            required = self.find_needed_material("FUEL", mid)
            print(
                f"For fuel={current}, required: {required_ore}, average: {required_ore/current:2.4f}",
                f"high={high}, low={low}",
            )
            if required <= available_ore:
                low = mid + 1
            else:
                high = mid
        return low - 1

    def find_needed_material(
        self,
        material_id: str,
        required_amount: int,
        available_materials: Optional[dict] = None,
    ) -> int:
        if available_materials is None:
            available_materials = defaultdict(int)
        if material_id == "ORE":
            return required_amount
        material = self.materials[material_id]
        available_amount = available_materials[material_id]
        if available_amount >= required_amount:
            available_materials[material_id] -= required_amount
            return 0
        required_amount -= available_materials[material_id]
        available_materials[material_id] = 0
        reaction_amount = material.amount
        number_of_reactions = -(-required_amount // reaction_amount)
        required_ore = sum(
            self.find_needed_material(
                parent,
                number_of_reactions * amount,
                available_materials=available_materials,
            )
            for parent, amount in material.parents
        )
        available_materials[material_id] = (
            number_of_reactions * reaction_amount - required_amount
        )
        return required_ore


if __name__ == "__main__":
    from pathlib import Path
    from time import perf_counter

    def split_entry(entry: str):
        amount, identifier = entry.strip().split(" ")
        return identifier, int(amount)

    materials = []
    with Path(__file__).parent.joinpath("input" + "14.txt").open("r") as f:
        for line in f.readlines():
            sources, target = line.strip().split("=>")
            sources = [split_entry(entry) for entry in sources.split(", ")]
            materials.append((sources, split_entry(target)))

    reactions = Reactions(materials)
    print(reactions.part_one())

    reactions = Reactions(materials)
    start = perf_counter()
    print(reactions.part_two_binsearch())
    print(f"Elapsed: {perf_counter() - start:2.4f} seconds.")
