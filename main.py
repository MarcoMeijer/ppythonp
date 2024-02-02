import argparse
from typing import Union

class Token:
    def __init__(self, value: str, line: int):
        self.value = value
        self.line = line

class Literal:
    def __init__(self, value: int) -> None:
        self.value = value

class CompileError:
    def __init__(self, line, message) -> None:
        self.line = line
        self.message = message

    def display(self, lines: list[str]) -> None:
        print(f"Compile error on line {self.line}:")
        print(" --> " + lines[self.line])
        print(self.message)

def tokenize(input: str) -> list[Token]:
    lines = input.split("\n")
    result = []
    for line in range(len(lines)):
        result.extend([Token(x, line) for x in lines[line].split(" ")])
    return result

def parse_int(input: list[Token]) -> Union[tuple[Literal, list[Token]], CompileError]:
    if input[0].value.isdigit():
        return (Literal(int(input[0].value)), input[1:])
    return CompileError(input[0].line, "Expected integer")

parser = argparse.ArgumentParser("pythonpp")
parser.add_argument("filename")
args = parser.parse_args()

file = open(args.filename, 'r')
source = file.read()
result = parse_int(tokenize(source))

if isinstance(result, CompileError):
    result.display(source.split("\n"))
if isinstance(result, tuple):
    print(result[0].value)
