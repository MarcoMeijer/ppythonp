import argparse
from compileError import CompileError
from context import Context
from parser import parse_code_block
from tokenizer import tokenize
import sys

sys.setrecursionlimit(1_000_000)

parser = argparse.ArgumentParser("ppythonp")
parser.add_argument("filename")
args = parser.parse_args()

file = open(args.filename, 'r')
source = file.read()
tokens = tokenize(source)
result = parse_code_block(0)(tokens)

if isinstance(result, CompileError):
    result.display(source.split("\n"))
if isinstance(result, tuple):
    context = Context()
    result[0].execute(context)
