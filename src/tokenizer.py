
class Token:
    def __init__(self, value: str, line: int):
        self.value = value
        self.line = line

def tokenize(input: str) -> list[Token]:
    lines = input.split("\n")
    result = []
    for line in range(len(lines)):
        # whitespace
        spaces = 0
        for c in lines[line]:
            if c == " ":
                spaces += 1
            else:
                break
        if spaces != 0:
            result.append(Token(" " * spaces, line))

        chars = []
        for c in lines[line]:
            if chars != [] and chars[0].isdigit():
                if c.isdigit():
                    chars.append(c)
                    continue
            else:
                if c.isdigit() or c.isalpha() or c == "_":
                    chars.append(c)
                    continue

            if chars != []:
                result.append(Token("".join(chars), line))
                chars = []

            if c.isalpha() or c.isdigit() or c == "_" :
                chars.append(c)
            elif not c.isspace():
                result.append(Token(c, line))

        if chars != []:
            result.append(Token("".join(chars), line))
            chars = []

        result.append(Token("\n", line))
    return result

