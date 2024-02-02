from typing import Any


class Node:
    def execute(self) -> Any:
        pass

class Literal(Node):
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
       return str(self.value)

    def execute(self) -> Any:
        return self.value

class Add(Node):
    def __init__(self, lhs: Node, rhs: Node) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return str(self.lhs) + "+" + str(self.rhs)

    def execute(self) -> Any:
        return self.lhs.execute() + self.rhs.execute()

