from typing import Optional, Callable


class InvalidInput(Exception):
    pass


class Computer(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pointer = 0
        self.operations = {
            1: self.add,
            2: self.multiply,
            3: self.move,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less,
            8: self.equal,
        }

    def _two_inputs_op(self, mode: int, operation: Callable[[int, int], int]) -> None:
        input1 = self.get_input(mode)
        mode //= 10
        input2 = self.get_input(mode)
        mode //= 10
        self._store_value(mode, operation(input1, input2))

    def jump_if_true(self, mode: int, user_input: Optional[int] = None) -> None:
        self._jump_if(mode, True)

    def jump_if_false(self, mode: int, user_input: Optional[int] = None) -> None:
        self._jump_if(mode, False)

    def _jump_if(self, mode: int, if_true: bool) -> None:
        input = self.get_input(mode)
        mode //= 10
        position = self.get_input(mode)
        if (input != 0 and if_true) or (input == 0 and not if_true):
            # The -1 is to compensate for the increment with every operation
            self.pointer = position - 1

    def less(self, mode: int, user_input: Optional[int] = None) -> None:
        comparison = int.__lt__
        return self._two_inputs_op(mode, comparison)

    def equal(self, mode: int, user_input: Optional[int] = None) -> None:
        comparison = int.__eq__
        return self._two_inputs_op(mode, comparison)

    def _store_value(self, mode: int, value: int) -> None:
        self.pointer += 1
        if mode == 0:
            self[self[self.pointer]] = value
        else:
            raise ValueError("Verboten!")

    def get_input(self, mode: int) -> int:
        self.pointer += 1
        pointer = self.pointer
        input_mode = mode % 10
        if input_mode > 1:
            raise ValueError(
                "Input mode not supported {input_mode}".format(input_mode=input_mode)
            )
        return self[self[pointer]] if input_mode == 0 else self[pointer]

    def add(self, mode: int, user_input: Optional[int] = None) -> None:
        self._two_inputs_op(mode, int.__add__)

    def multiply(self, mode: int, user_input: Optional[int] = None) -> None:
        self._two_inputs_op(mode, int.__mul__)

    def output(self, mode: int, user_input: Optional[int] = None) -> int:
        return self.get_input(mode)

    def move(self, mode: int, user_input: int) -> None:
        if user_input is None:
            raise ValueError(f"External Input can not be None.")
        mode //= 10
        self._store_value(mode, user_input)

    def process(self, user_input: Optional[int] = None) -> list[int]:
        outputs = []
        while self.pointer <= len(self):
            instruction = self[self.pointer]
            opcode = instruction % 100
            mode = instruction // 100
            if opcode == 99:
                return outputs
            operation = self.operations[opcode]
            output = operation(mode, user_input)
            if output is not None:
                outputs.append(output)
            self.pointer += 1
        raise InvalidInput("Did not terminate with a 99")


if __name__ == "__main__":

    def test_case(values: list[int], user_input: int, expected_result: int):
        computer = Computer(values)
        output = computer.process(user_input)
        assert output[-1] == expected_result

    test_case([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, int(True))
    test_case([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 9, int(False))
    test_case([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 7, int(False))

    test_case([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, int(True))
    test_case([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8, int(False))
    test_case([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 9, int(False))

    test_case([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, int(True))
    test_case([3, 3, 1108, -1, 8, 3, 4, 3, 99], 7, int(False))
    test_case([3, 3, 1108, -1, 8, 3, 4, 3, 99], 9, int(False))

    test_case([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, int(True))
    test_case([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8, int(False))
    test_case([3, 3, 1107, -1, 8, 3, 4, 3, 99], 9, int(False))

    test_case([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, int(True))
    test_case([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, int(False))

    test_case([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, int(True))
    test_case([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, int(False))

    test_input = [
        3,
        21,
        1008,
        21,
        8,
        20,
        1005,
        20,
        22,
        107,
        8,
        21,
        20,
        1006,
        20,
        31,
        1106,
        0,
        36,
        98,
        0,
        0,
        1002,
        21,
        125,
        20,
        4,
        20,
        1105,
        1,
        46,
        104,
        999,
        1105,
        1,
        46,
        1101,
        1000,
        1,
        20,
        4,
        20,
        1105,
        1,
        46,
        98,
        99,
    ]

    test_case(
        test_input,
        7,
        999,
    )

    test_case(
        test_input,
        8,
        1000,
    )
    test_case(
        test_input,
        9,
        1001,
    )
