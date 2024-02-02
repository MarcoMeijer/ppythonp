import argparse

def tokenize(input: str) -> list[str]:
    return [x.strip() for x in input.split(" ")]

parser = argparse.ArgumentParser("pythonpp")
parser.add_argument("filename")
args = parser.parse_args()

file = open(args.filename, 'r')
source = file.read()
print(tokenize(source))
