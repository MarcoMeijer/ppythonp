from compileError import CompileError
from node import Assign, BinOp, Identifier, Node, Literal
from typing import Any, Callable, List, Type
from tokenizer import Token

type Result[T] = tuple[T, List[Token]] | CompileError
type Parser[T] = Callable[[List[Token]], Result[T]]

def satisfy(f: Callable[[Token], bool]) -> Parser[Token]:
    def parser(input: list[Token]) -> Result[Token]:
        if input == []:
            return CompileError(None, "Unexpected end of file")
        if not f(input[0]):
            return CompileError(input[0].line, "Didn't satisfy condition.")
        return input[0], input[1:]
    return parser

def parse_token(token):
    def parser(input: list[Token]) -> Result[str]:
        if input == []:
            return CompileError(None, "Unexpected end of file")
        if input[0].value == token:
            return input[0].value, input[1:]
        return CompileError(input[0].line, "Expected +")
    return parser

def preceded[T1, T2](p1: Parser[T1], p2: Parser[T2]) -> Parser[T2]:
    def parser(input: list[Token]) -> Result[T2]:
        result = p1(input)
        if isinstance(result, CompileError):
            return result
        input = result[1]

        return p2(input)
    return parser

def separated_pair[T1, T2, T3](p1: Parser[T1], p2: Parser[T2], p3: Parser[T3]) -> Parser[tuple[T1, T3]]:
    def parser(input: list[Token]) -> Result[tuple[T1, T3]]:
        result = p1(input)
        if isinstance(result, CompileError):
            return result
        a, input = result

        result = p2(input)
        if isinstance(result, CompileError):
            return result
        input = result[1]

        result = p3(input)
        if isinstance(result, CompileError):
            return result
        b, input = result
        return ((a, b), input)
    return parser

def alt[T](*args: Parser[T]) -> Parser[T]:
    def parser(input: list[Token]) -> Result[T]:
        for p in args[:-1]:
            result = p(input)
            if isinstance(result, CompileError):
                continue
            return result
        return args[-1](input)
    return parser


def parse_tuple(*args):
    def parser(input):
        res = []
        for p in args:
            result = p(input)
            if isinstance(result, CompileError):
                return result
            x, input = result
            res.append(x)
        return (tuple(res), input)
    return parser

def map_parser[T, U](p: Parser[T], f: Callable[[T], U]) -> Parser[U]:
    def parser(input: list[Token]) -> Result[U]:
        result = p(input)
        if isinstance(result, CompileError):
            return result
        x, input = result
        return f(x), input
    return parser

def parse_int(input: list[Token]) -> Result[Node]:
    if input == []:
        return CompileError(None, "Unexpected end of file")
    if input[0].value.isdigit():
        return Literal(int(input[0].value)), input[1:]
    return CompileError(input[0].line, "Expected integer")

def left_ass_expr(tokens: list[str], p: Parser[Node]) -> Parser[Node]:
    def parser(input: list[Token]) -> Result[Node]:
        result = p(input)
        if isinstance(result, CompileError):
            return result
        node, input = result

        while True:
            result = satisfy(lambda x : x.value in tokens)(input)
            if isinstance(result, CompileError):
                return node, input
            op, input = result

            result = p(input)
            if isinstance(result, CompileError):
                return result
            rhs, input = result
            node = BinOp(node, op.value, rhs)

    return parser

def parse_product(input: list[Token]) -> Result[Node]:
    return left_ass_expr(["*", "/"], parse_int)(input)


def parse_plus(input: list[Token]) -> Result[Node]:
    return left_ass_expr(["+", "-"], parse_product)(input)

def parse_expr(input: list[Token]) -> Result[Node]:
    return parse_plus(input)

def is_identifier(name: str) -> bool:
    return name[0].isalpha() or name[0] == "_"

def parse_identifier(input: list[Token]) -> Result[Node]:
    if input == []:
        return CompileError(None, "Unexpected end of file")
    if is_identifier(input[0].value):
        return Identifier(input[0].value), input[1:]
    return CompileError(input[0].line, "Expected identifier")

def parse_assignment(input: list[Token]) -> Result[Node]:
    return map_parser(
        separated_pair(parse_identifier, parse_token("="), parse_expr),
        lambda x : Assign(x[0], x[1])
    )(input)

def parse_line(input: list[Token]) -> Result[Node]:
    return alt(parse_assignment, parse_expr)(input)

