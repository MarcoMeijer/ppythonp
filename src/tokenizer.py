
class Token:
    def __init__(self, value: str, line: int):
        self.value = value
        self.line = line

def tokenize(input: str) -> list[Token]:
    lines = input.split("\n")
    result = []
    for line in range(len(lines)):
        result.extend([Token(x, line) for x in lines[line].split(" ") if x != ""])
    return result

