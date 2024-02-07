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
        if self.op == "%":
            return self.lhs.execute(context) % self.rhs.execute(context)
        if self.op == "/":
            return self.lhs.execute(context) / self.rhs.execute(context)
        if self.op == "==":
            return self.lhs.execute(context) == self.rhs.execute(context)
        if self.op == "!=":
            return self.lhs.execute(context) != self.rhs.execute(context)
        if self.op == "<":
            return self.lhs.execute(context) < self.rhs.execute(context)
        if self.op == ">":
            return self.lhs.execute(context) > self.rhs.execute(context)
        if self.op == "<=":
            return self.lhs.execute(context) <= self.rhs.execute(context)
        if self.op == ">=":
            return self.lhs.execute(context) >= self.rhs.execute(context)

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
    def __init__(self, function: str, arguments: list[Node]) -> None:
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
        if self.function == "print":
            print(self.arguments[0].execute(context))
        else:
            return context.call_function(self.function, list(map(lambda x : x.execute(context), self.arguments)))

class CodeBlock(Node):
    def __init__(self, lines: list[Node], indent: int) -> None:
        self.lines = lines
        self.indent = indent

    def __str__(self) -> str:
        return "\n".join(map(lambda x : " " * self.indent + str(x), self.lines))

    def execute(self, context: Context) -> Any:
        i = 0
        while i >= 0 and i < len(self.lines):
            line = self.lines[i]
            line.execute(context)
            if context.get_variable("reverse"):
                i -= 1
            else:
                i += 1
            if context.returning:
                return

class IfStatement(Node):
    def __init__(self, condition: Node, if_true: CodeBlock) -> None:
        self.condition = condition
        self.if_true = if_true

    def __str__(self) -> str:
        return "if " + str(self.condition) + ":\n" + str(self.if_true)

    def execute(self, context: Context) -> Any:
        if self.condition.execute(context):
            self.if_true.execute(context)

class WhileLoop(Node):
    def __init__(self, condition: Node, while_true: CodeBlock) -> None:
        self.condition = condition
        self.while_true = while_true

    def __str__(self) -> str:
        return "while " + str(self.condition) + ":\n" + str(self.while_true)

    def execute(self, context: Context) -> Any:
        while self.condition.execute(context):
            self.while_true.execute(context)

class FunctionDefinition(Node):
    def __init__(self, name: str, arguments: list[str], code: CodeBlock) -> None:
        self.name = name
        self.arguments = arguments
        self.code = code

    def __str__(self) -> str:
        return "definitely " + str(self.name) + "(" + ", ".join(list(map(str, self.arguments))) + "):\n" + str(self.code)

    def execute(self, context: Context) -> Any:
        def f(*args):
            if len(args) != len(self.arguments):
                print(f"Incorrect number of arguments passed to function {self.name}")
            context.add_scope()
            for i in range(len(self.arguments)):
                context.set_variable(self.arguments[i], args[i])
            self.code.execute(context)
            ret = context.return_value
            context.return_value = None
            context.returning = False
            context.pop_scope()
            return ret
        context.set_function(self.name, f)

class Return(Node):
    def __init__(self, expr: Node) -> None:
        self.expr = expr

    def __str__(self) -> str:
        return "return " + str(self.expr)

    def execute(self, context: Context) -> Any:
        context.return_value = self.expr.execute(context)
        context.returning = True

class NewList(Node):
    def __init__(self, values: list[Node]) -> None:
        self.values = values

    def __str__(self) -> str:
        return "[" + ", ".join(list(map(str, self.values))) + "]"

    def execute(self, context: Context) -> Any:
        result = []
        for value in self.values:
            result.append(value.execute(context))
        return result
