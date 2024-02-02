
class Node:
    pass

class Literal(Node):
    def __init__(self, value: int) -> None:
        self.value = value

    def __str__(self) -> str:
       return str(self.value)

class Add(Node):
    def __init__(self, lhs: Node, rhs: Node) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return str(self.lhs) + "+" + str(self.rhs)

