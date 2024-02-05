from typing import Any

from context import Context


class Node:
    def execute(self, _: Context) -> Any:
        pass

class Literal(Node):
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
       return str(self.value)

    def execute(self, _: Context) -> Any:
        return self.value

class Identifier(Node):
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
       return str(self.name)

    def execute(self, context: Context) -> Any:
        return context.get_variable(self.name)

class BinOp(Node):
    def __init__(self, lhs: Node, op: str, rhs: Node) -> None:
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __str__(self) -> str:
        return str(self.lhs) + self.op + str(self.rhs)

    def execute(self, context: Context) -> Any:
        if self.op == "+":
            return self.lhs.execute(context) + self.rhs.execute(context)
        if self.op == "-":
            return self.lhs.execute(context) - self.rhs.execute(context)
        if self.op == "*":
            return self.lhs.execute(context) * self.rhs.execute(context)
        if self.op == "/":
            return self.lhs.execute(context) / self.rhs.execute(context)

class Assign(Node):
    def __init__(self, lhs: Node, rhs: Node) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return str(self.lhs) + "=" + str(self.rhs)

    def execute(self, context: Context) -> Any:
        if isinstance(self.lhs, Identifier):
            context.set_variable(self.lhs.name, self.rhs.execute(context))
        else:
            print("RUNTIME ERROR: Trying to assign to a non variable")
            exit(-1)

class FunctionCall(Node):
    def __init__(self, function: Node, arguments: list[Node]) -> None:
        self.function = function
        self.arguments = arguments

    def __str__(self) -> str:
        result = str(self.function) + "("
        first = True
        for arg in self.arguments:
            if not first:
                result += ", "
            result += str(arg)
            first = False
        return result + ")"

    def execute(self, context: Context) -> Any:
        print(self.arguments[0].execute(context))

class CodeBlock(Node):
    def __init__(self, lines: list[Node]) -> None:
        self.lines = lines

    def __str__(self) -> str:
        return "\n".join(map(str, self.lines))

    def execute(self, context: Context) -> Any:
        for line in self.lines:
            line.execute(context)

class IfStatement(Node):
    def __init__(self, condition: Node, if_true: CodeBlock) -> None:
        self.condition = condition
        self.if_true = if_true

    def __str__(self) -> str:
        return "if " + str(self.condition) + ":\n" + str(self.if_true)

    def execute(self, context: Context) -> Any:
        if self.condition.execute(context):
            self.if_true.execute(context)

