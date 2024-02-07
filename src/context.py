from typing import Any


class Context:
    def __init__(self) -> None:
        self.variables = [{"reverse":False}]
        self.functions = {}
        self.return_value = None
        self.returning = False

    def get_variable(self, name: str) -> Any:
        for scope in self.variables[::-1]:
            if name in scope:
                return scope[name]
        return None

    def add_scope(self):
        self.variables.append({})

    def pop_scope(self):
        self.variables.pop()

    def set_variable(self, name: str, value: Any):
        self.variables[-1][name] = value

    def set_function(self, name: str, f: Any):
        self.functions[name] = f

    def call_function(self, name: str, arguments: list[Any]) -> Any:
        return self.functions[name](*arguments)

