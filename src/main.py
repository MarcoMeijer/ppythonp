import argparse
from compileError import CompileError
from parser import parse_plus
from tokenizer import tokenize

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
