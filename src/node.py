from typing import Any

from context import Context

def my_range(*args):
    if len(args) <= 2:
        for x in range(*args):
            yield x
        return
    i = args[0]
    end = args[1]
    di = list(args[2:])
    while True:
        if di[0] > 0 and i >= end:
            break
        if di[0] < 0 and i <= end:
            break
        yield i
        i += di[0]
        for j in range(1,len(di)):
            di[j - 1] += di[j]

class Node:
    def execute(self, _: Context, _lvalue: bool = False) -> Any:
        pass

class Literal(Node):
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        if type(self.value) == str:
            return "\"" + self.value + "\""
        return str(self.value)

    def execute(self, _: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print("ERROR: literal can't be an lvalue")
            exit(1)
        return self.value

class Identifier(Node):
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
       return str(self.name)

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            node = self
            class Prox:
                def __getitem__(self, _):
                    return context.get_variable(node.name)
                def __setitem__(self, _, v):
                    return context.set_variable(node.name, v)
            return Prox()
        return context.get_variable(self.name)

class BinOp(Node):
    def __init__(self, lhs: Node, op: str, rhs: Node) -> None:
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __str__(self) -> str:
        return str(self.lhs) + self.op + str(self.rhs)

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print(f"ERROR: operator {self.op} can't be an lvalue")
            exit(1)
        if self.op == "+":
            lhs = self.lhs.execute(context)
            rhs = self.rhs.execute(context)
            if type(lhs) == str or type(rhs) == str:
                return str(lhs) + str(rhs)
            return lhs + rhs
        if self.op == "++":
            return self.lhs.execute(context) + self.rhs.execute(context)
        if self.op == "-":
            return self.lhs.execute(context) - self.rhs.execute(context)
        if self.op == "*":
            return self.lhs.execute(context) * self.rhs.execute(context)
        if self.op == "%":
            return self.lhs.execute(context) % self.rhs.execute(context)
        if self.op == "/":
            return self.lhs.execute(context) / self.rhs.execute(context)
        if self.op == "<<":
            return self.lhs.execute(context) << self.rhs.execute(context)
        if self.op == ">>":
            return self.lhs.execute(context) >> self.rhs.execute(context)
        if self.op == "&":
            return self.lhs.execute(context) & self.rhs.execute(context)
        if self.op == "^":
            return self.lhs.execute(context) ^ self.rhs.execute(context)
        if self.op == "|":
            return self.lhs.execute(context) | self.rhs.execute(context)
        if self.op == "==":
            lhs = self.lhs.execute(context)
            rhs = self.rhs.execute(context)
            if type(lhs) == str or type(rhs) == str:
                return str(lhs) == str(rhs)
            return lhs == rhs
        if self.op == "===":
            return self.lhs.execute(context) == self.rhs.execute(context)
        if self.op == "====":
            return self.lhs.execute(context) is self.rhs.execute(context)
        if self.op == "!=":
            lhs = self.lhs.execute(context)
            rhs = self.rhs.execute(context)
            if type(lhs) == str or type(rhs) == str:
                return str(lhs) != str(rhs)
            return lhs != rhs
        if self.op == "!==":
            return self.lhs.execute(context) != self.rhs.execute(context)
        if self.op == "!===":
            return self.lhs.execute(context) is not self.rhs.execute(context)
        if self.op == "<":
            return self.lhs.execute(context) < self.rhs.execute(context)
        if self.op == ">":
            return self.lhs.execute(context) > self.rhs.execute(context)
        if self.op == "<=":
            return self.lhs.execute(context) <= self.rhs.execute(context)
        if self.op == ">=":
            return self.lhs.execute(context) >= self.rhs.execute(context)
        if self.op == "and":
            return self.lhs.execute(context) and self.rhs.execute(context)
        if self.op == "or":
            return self.lhs.execute(context) or self.rhs.execute(context)

class Assign(Node):
    def __init__(self, lhs: Node, rhs: Node) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return str(self.lhs) + "=" + str(self.rhs)

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print(f"ERROR: assigment can't be an lvalue")
            exit(1)
        variable = self.lhs.execute(context, True)
        variable[:] = self.rhs.execute(context)

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

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print(f"ERROR: cannot assign the the result of a function call")
            exit(1)
        arguments = list(map(lambda x : x.execute(context), self.arguments))
        if not isinstance(self.function, Identifier):
            print("Trying to call a non function")
            exit(1)
        else:
            name = self.function.name
            if name == "print":
                print(*arguments)
            elif name == "range":
                return my_range(*arguments)
            else:
                return context.call_function(name, arguments)

class CodeBlock(Node):
    def __init__(self, lines: list[Node], indent: int) -> None:
        self.lines = lines
        self.indent = indent

    def __str__(self) -> str:
        return "\n".join(map(lambda x : " " * self.indent + str(x), self.lines))

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print(f"ERROR: cannot assign to a code block")
            exit(1)
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

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print(f"ERROR: cannot assign to an if statement")
            exit(1)
        if self.condition.execute(context):
            self.if_true.execute(context)

class WhileLoop(Node):
    def __init__(self, condition: Node, while_true: CodeBlock) -> None:
        self.condition = condition
        self.while_true = while_true

    def __str__(self) -> str:
        return "while " + str(self.condition) + ":\n" + str(self.while_true)

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print(f"ERROR: cannot assign to a while loop")
            exit(1)
        while self.condition.execute(context):
            self.while_true.execute(context)

class ForLoop(Node):
    def __init__(self, variable_name: Identifier, values: Node, for_each: CodeBlock) -> None:
        self.variable_name = variable_name
        self.values = values
        self.for_each = for_each

    def __str__(self) -> str:
        return "for " + str(self.variable_name) + " in " + str(self.values) + ":\n" + str(self.for_each)

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print(f"ERROR: cannot assign to a while loop")
            exit(1)
        for x in self.values.execute(context):
            context.set_variable(self.variable_name.name, x)
            self.for_each.execute(context)

class FunctionDefinition(Node):
    def __init__(self, name: str, arguments: list[str], code: CodeBlock) -> None:
        self.name = name
        self.arguments = arguments
        self.code = code

    def __str__(self) -> str:
        return "definitely " + str(self.name) + "(" + ", ".join(list(map(str, self.arguments))) + "):\n" + str(self.code)

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print(f"ERROR: cannot assign to a function")
            exit(1)
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

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print(f"ERROR: cannot assign to an return statement")
            exit(1)
        context.return_value = self.expr.execute(context)
        context.returning = True

class NewList(Node):
    def __init__(self, values: list[Node]) -> None:
        self.values = values

    def __str__(self) -> str:
        return "[" + ", ".join(list(map(str, self.values))) + "]"

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print(f"ERROR: cannot assign to a list literal")
            exit(1)
        result = []
        for value in self.values:
            result.append(value.execute(context))
        return result

class NotOp(Node):
    def __init__(self, expr: Node) -> None:
        self.expr = expr

    def __str__(self) -> str:
        return "not " + str(self.expr)

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        if lvalue:
            print(f"ERROR: cannot assign to a not operation")
            exit(1)
        return not self.expr.execute(context)

class Index(Node):
    def __init__(self, value: Node, index: Node) -> None:
        self.value = value
        self.index = index

    def __str__(self) -> str:
        return str(self.value) + "[" + str(self.index) + "]"

    def execute(self, context: Context, lvalue: bool = False) -> Any:
        value = self.value.execute(context)
        index = self.index.execute(context)
        if lvalue:
            class Prox:
                def __getitem__(self, _):
                    return value[index]
                def __setitem__(self, _, v):
                    value[index] = v
            return Prox()
        return value[index]
