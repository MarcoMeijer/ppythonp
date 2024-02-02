import argparse

class Token:
    def __init__(self, value: str, line: int):
        self.value = value
        self.line = line

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

class CompileError:
    def __init__(self, line: int | None, message: str) -> None:
        self.line = line
        self.message = message

    def display(self, lines: list[str]) -> None:
        if self.line != None:
            print(f"Compile error on line {self.line}:")
            print(" --> " + lines[self.line])
        print(self.message)

def tokenize(input: str) -> list[Token]:
    lines = input.split("\n")
    result = []
    for line in range(len(lines)):
        result.extend([Token(x, line) for x in lines[line].split(" ") if x != ""])
    return result

def parse_token(token):
    def parser(input: list[Token]) -> tuple[str, list[Token]] | CompileError:
        if input == []:
            return CompileError(None, "Unexpected end of file")
        if input[0].value == token:
            return input[0].value, input[1:]
        return CompileError(input[0].line, "Expected +")
    return parser

def parse_int(input: list[Token]) -> tuple[Node, list[Token]] | CompileError:
    if input == []:
        return CompileError(None, "Unexpected end of file")
    if input[0].value.isdigit():
        return Literal(int(input[0].value)), input[1:]
    return CompileError(input[0].line, "Expected integer")

def parse_plus(input: list[Token]) -> tuple[Node, list[Token]] | CompileError:
    result = parse_int(input)
    if isinstance(result, CompileError):
        return result
    lhs, input = result

    result = parse_token("+")(input)
    if isinstance(result, CompileError):
        return lhs, input
    input = result[1]

    result = parse_plus(input)
    if isinstance(result, CompileError):
        return result
    rhs, input = result

    return Add(lhs, rhs), input

parser = argparse.ArgumentParser("pythonpp")
parser.add_argument("filename")
args = parser.parse_args()

file = open(args.filename, 'r')
source = file.read()
result = parse_plus(tokenize(source))

if isinstance(result, CompileError):
    result.display(source.split("\n"))
if isinstance(result, tuple):
    print(result[0])
