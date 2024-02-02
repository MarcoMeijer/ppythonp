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

class BinOp(Node):
    def __init__(self, lhs: Node, op: str, rhs: Node) -> None:
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __str__(self) -> str:
        return str(self.lhs) + self.op + str(self.rhs)

    def execute(self) -> Any:
        if self.op == "+":
            return self.lhs.execute() + self.rhs.execute()
        if self.op == "-":
            return self.lhs.execute() - self.rhs.execute()
        if self.op == "*":
            return self.lhs.execute() * self.rhs.execute()
        if self.op == "/":
            return self.lhs.execute() / self.rhs.execute()

