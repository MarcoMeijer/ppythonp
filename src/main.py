import argparse
from compileError import CompileError
from context import Context
from parser import parse_code_block
from tokenizer import tokenize

parser = argparse.ArgumentParser("ppythonp")
parser.add_argument("filename")
args = parser.parse_args()

file = open(args.filename, 'r')
source = file.read()
tokens = tokenize(source)
print(list(map(lambda x : x.value, tokens)))
result = parse_code_block(0)(tokens)

if isinstance(result, CompileError):
    result.display(source.split("\n"))
if isinstance(result, tuple):
    print(result[0])
    context = Context()
    result[0].execute(context)
