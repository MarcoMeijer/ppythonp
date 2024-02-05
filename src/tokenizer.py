
class Token:
    def __init__(self, value: str, line: int):
        self.value = value
        self.line = line

special_tokens = ["==", "!=", "<=", ">=", "**"]

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
        i = -1
        n = len(lines[line])
        while i + 1 < n:
            i = i + 1
            c = lines[line][i]
            if chars != []:
                if chars[0].isdigit():
                    if c.isdigit():
                        chars.append(c)
                        continue
                elif chars[0] == "\"":
                    chars.append(c)
                    if c == "\"":
                        result.append(Token("".join(chars), line))
                        chars = []
                    continue
                else:
                    if c.isdigit() or c.isalpha() or c == "_":
                        chars.append(c)
                        continue

            if chars != []:
                result.append(Token("".join(chars), line))
                chars = []

            if c.isspace():
                continue

            if c.isalpha() or c.isdigit() or c == "_" or c == "\"":
                chars.append(c)
                continue

            found = False
            for t in special_tokens:
                if lines[line][i:i+len(t)] == t:
                    result.append(Token(t, line))
                    found = True
                    i += len(t) - 1
            if not found:
                result.append(Token(c, line))

        if chars != []:
            result.append(Token("".join(chars), line))
            chars = []

        result.append(Token("\n", line))
    return result

