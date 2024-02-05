from typing import Any


class Context:
    def __init__(self) -> None:
        self.variables = {}
        self.functions = {}

    def get_variable(self, name: str) -> Any:
        return self.variables[name]

    def set_variable(self, name: str, value: Any):
        self.variables[name] = value

    def set_function(self, name: str, f: Any):
        self.functions[name] = f

    def call_function(self, name: str, arguments: list[Any]) -> Any:
        return self.functions[name](*arguments)

