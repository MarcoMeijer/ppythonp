
from token import Token

from compileError import CompileError
from node import Add, Node, Literal


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

