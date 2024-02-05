from compileError import CompileError
from node import Assign, BinOp, CodeBlock, FunctionCall, FunctionDefinition, Identifier, IfStatement, Node, Literal, Return, WhileLoop
from typing import Callable, List
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
        return CompileError(input[0].line, f"Expected {token}")
    return parser

def preceded[T1, T2](p1: Parser[T1], p2: Parser[T2]) -> Parser[T2]:
    def parser(input: list[Token]) -> Result[T2]:
        result = p1(input)
        if isinstance(result, CompileError):
            return result
        input = result[1]

        return p2(input)
    return parser

def terminated[T1, T2](p1: Parser[T1], p2: Parser[T2]) -> Parser[T1]:
    def parser(input: list[Token]) -> Result[T1]:
        result = p1(input)
        if isinstance(result, CompileError):
            return result
        x, input = result

        result = p2(input)
        if isinstance(result, CompileError):
            return result
        input = result[1]
        return x, input
    return parser

def pair[T1, T2](p1: Parser[T1], p2: Parser[T2]) -> Parser[tuple[T1, T2]]:
    def parser(input: list[Token]) -> Result[tuple[T1, T2]]:
        result = p1(input)
        if isinstance(result, CompileError):
            return result
        a, input = result

        result = p2(input)
        if isinstance(result, CompileError):
            return result
        b, input = result

        return ((a, b), input)
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

def delimited[T1, T2, T3](p1: Parser[T1], p2: Parser[T2], p3: Parser[T3]) -> Parser[T2]:
    def parser(input: list[Token]) -> Result[T2]:
        result = p1(input)
        if isinstance(result, CompileError):
            return result
        input = result[1]

        result = p2(input)
        if isinstance(result, CompileError):
            return result
        x, input = result

        result = p3(input)
        if isinstance(result, CompileError):
            return result
        input = result[1]
        return x, input
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

def separated_list_0[T, U](p: Parser[T], separator: Parser[U]) -> Parser[list[T]]:
    def parser(input: list[Token]) -> Result[list[T]]:
        items = []
        while True:
            result = p(input)
            if isinstance(result, CompileError):
                return items, input
            x, input = result
            items.append(x)

            result = separator(input)
            if isinstance(result, CompileError):
                return items, input
            input = result[1]
    return parser

def many_0[T](p: Parser[T]) -> Parser[list[T]]:
    def parser(input: list[Token]) -> Result[list[T]]:
        items = []
        while True:
            result = p(input)
            if isinstance(result, CompileError):
                return items, input
            x, input = result
            items.append(x)
    return parser

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

def parse_int(input: list[Token]) -> Result[Node]:
    if input == []:
        return CompileError(None, "Unexpected end of file")
    if input[0].value.isdigit():
        return Literal(int(input[0].value)), input[1:]
    return CompileError(input[0].line, "Expected integer")

def parse_string(input: list[Token]) -> Result[Node]:
    if input == []:
        return CompileError(None, "Unexpected end of file")
    if input[0].value[0] == "\"":
        return Literal(input[0].value[1:-1]), input[1:]
    return CompileError(input[0].line, "Expected string")

def parse_false(input: List[Token]) -> Result[Node]:
    return map_parser(parse_token("FaLsE"), lambda _ : Literal(False))(input)

def parse_true(input: List[Token]) -> Result[Node]:
    return map_parser(parse_token("tRuE"), lambda _ : Literal(True))(input)

def parse_identifier(input: list[Token]) -> Result[Identifier]:
    if input == []:
        return CompileError(None, "Unexpected end of file")
    if is_identifier(input[0].value):
        return Identifier(input[0].value), input[1:]
    return CompileError(input[0].line, "Expected identifier")

def parse_function_call(input: List[Token]) -> Result[Node]:
    return map_parser(
        pair(parse_identifier,
             delimited(parse_token("("), separated_list_0(parse_expr, parse_token(",")), parse_token(")"))
        ),
        lambda x : FunctionCall(x[0].name, x[1])
    )(input)

def parse_value(input: List[Token]) -> Result[Node]:
    return alt(parse_true, parse_false, parse_string, parse_function_call, parse_identifier, parse_int)(input)

def parse_product(input: list[Token]) -> Result[Node]:
    return left_ass_expr(["*", "/", "%"], parse_value)(input)

def parse_plus(input: list[Token]) -> Result[Node]:
    return left_ass_expr(["+", "-"], parse_product)(input)

def parse_comparison(input: list[Token]) -> Result[Node]:
    return left_ass_expr(["==", "!=", "<", ">", "<=", ">="], parse_plus)(input)

def parse_expr(input: list[Token]) -> Result[Node]:
    return parse_comparison(input)

def is_identifier(name: str) -> bool:
    return name[0].isalpha() or name[0] == "_"

def parse_assignment(input: list[Token]) -> Result[Node]:
    return map_parser(
        separated_pair(parse_identifier, parse_token("="), parse_expr),
        lambda x : Assign(x[0], x[1])
    )(input)

def parse_if(spaces: int) -> Parser[Node]:
    def parser(input: list[Token]):
        return map_parser(
            pair(
                delimited(parse_token("if"), parse_expr, parse_token(":")),
                preceded(parse_token("\n"), parse_code_block(spaces + 2))
            ),
            lambda x : IfStatement(x[0], x[1])
        )(input)
    return parser

def parse_while(spaces: int) -> Parser[Node]:
    def parser(input: list[Token]):
        return map_parser(
            pair(
                delimited(parse_token("while"), parse_expr, parse_token(":")),
                preceded(parse_token("\n"), parse_code_block(spaces + 2))
            ),
            lambda x : WhileLoop(x[0], x[1])
        )(input)
    return parser

def parse_definitely(spaces: int) -> Parser[Node]:
    def parser(input: list[Token]):
        return map_parser(
            parse_tuple(
                preceded(parse_token("definitely"), parse_identifier),
                terminated(delimited(parse_token("("), separated_list_0(parse_identifier, parse_token(",")), parse_token(")")), parse_token(":")),
                preceded(parse_token("\n"), parse_code_block(spaces + 2))
            ),
            lambda x : FunctionDefinition(x[0].name, list(map(lambda y : y.name, x[1])), x[2])
        )(input)
    return parser

def parse_return(input: list[Token]) -> Result[Node]:
    return map_parser(
        preceded(parse_token("return"), parse_expr),
        lambda x : Return(x)
    )(input)

def parse_line(spaces: int) -> Parser[Node]:
    def parser(input: list[Token]):
        p = alt(
            terminated(alt(parse_assignment, parse_return, parse_expr), parse_token("\n")),
            parse_if(spaces), parse_while(spaces), parse_definitely(spaces),
        )
        if spaces == 0:
            return p(input)
        return preceded(parse_token(" " * spaces), p)(input)
    return parser

def parse_code_block(spaces: int) -> Parser[CodeBlock]:
    def parser(input: list[Token]):
        return map_parser(
            many_0(parse_line(spaces)),
            lambda x : CodeBlock(x, spaces)
        )(input)
    return parser
