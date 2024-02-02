
class CompileError:
    def __init__(self, line: int | None, message: str) -> None:
        self.line = line
        self.message = message

    def display(self, lines: list[str]) -> None:
        if self.line != None:
            print(f"Compile error on line {self.line}:")
            print(" --> " + lines[self.line])
        print(self.message)
