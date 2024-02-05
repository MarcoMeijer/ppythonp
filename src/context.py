from typing import Any


class Context:
    def __init__(self) -> None:
        self.variables = {}

    def get_variable(self, name: str) -> Any:
        return self.variables[name]

    def set_variable(self, name: str, value: Any):
        self.variables[name] = value
