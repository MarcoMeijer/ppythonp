import argparse
from compileError import CompileError
from context import Context
from parser import parse_line
from tokenizer import tokenize

parser = argparse.ArgumentParser("pythonpp")
parser.add_argument("filename")
args = parser.parse_args()

file = open(args.filename, 'r')
source = file.read()
result = parse_line(tokenize(source))

if isinstance(result, CompileError):
    result.display(source.split("\n"))
if isinstance(result, tuple):
    context = Context()
    print(result[0].execute(context))
