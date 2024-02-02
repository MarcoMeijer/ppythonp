from compileError import CompileError
from node import BinOp, Node, Literal
from typing import Callable, List
from tokenizer import Token

type Parser[T] = Callable[[List[Token]], tuple[T, List[Token]] | CompileError]

def parse_token(token):
    def parser(input: list[Token]) -> tuple[str, list[Token]] | CompileError:
        if input == []:
            return CompileError(None, "Unexpected end of file")
        if input[0].value == token:
            return input[0].value, input[1:]
        return CompileError(input[0].line, "Expected +")
    return parser

def preceded[T1, T2](p1: Parser[T1], p2: Parser[T2]) -> Parser[T2]:
    def parser(input: list[Token]) -> tuple[T2, list[Token]] | CompileError:
        result = p1(input)
        if isinstance(result, CompileError):
            return result
        input = result[1]

        return p2(input)
    return parser

def separated_pair[T1, T2, T3](p1: Parser[T1], p2: Parser[T2], p3: Parser[T3]) -> Parser[tuple[T1, T3]]:
    def parser(input: list[Token]) -> tuple[tuple[T1, T3], list[Token]] | CompileError:
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
    def parser(input: list[Token]) -> tuple[T, list[Token]] | CompileError:
        for p in args[:-1]:
            result = p(input)
            if isinstance(result, CompileError):
                continue
            return result
        return args[-1](input)
    return parser

def map_parser[T, U](p: Parser[T], f: Callable[[T], U]) -> Parser[U]:
    def parser(input: list[Token]) -> tuple[U, list[Token]] | CompileError:
        result = p(input)
        if isinstance(result, CompileError):
            return result
        x, input = result
        return f(x), input
    return parser

def parse_int(input: list[Token]) -> tuple[Node, list[Token]] | CompileError:
    if input == []:
        return CompileError(None, "Unexpected end of file")
    if input[0].value.isdigit():
        return Literal(int(input[0].value)), input[1:]
    return CompileError(input[0].line, "Expected integer")

def parse_product(input: list[Token]) -> tuple[Node, list[Token]] | CompileError:
    return alt(
        map_parser(
            separated_pair(parse_int, parse_token("*"), parse_product),
            lambda x : BinOp(x[0], "*", x[1])
        ),
        parse_int
    )(input)


def parse_plus(input: list[Token]) -> tuple[Node, list[Token]] | CompileError:
    return alt(
        map_parser(
            separated_pair(parse_product, parse_token("+"), parse_plus),
            lambda x : BinOp(x[0], "+", x[1])
        ),
        parse_product
    )(input)

