from docstring_parser import parse as docstring_parse, Docstring
from typing import Callable, Any

class ParserException(Exception):
    pass


class FunctionParser:
    def __init__(self, func: Callable):
        self.func = func

        if not len(self.argument_names) == self.argument_count:
            raise ParserException("Function containing * or ** args are not supported.")

        self.variables = self.get_typehints()
        self.update_inputs()

    @property
    def argument_names(self) -> tuple[str, ...]:
        # Tuple of names of arguments and local variables
        return self.func.__code__.co_varnames

    @property
    def argument_count(self) -> int:
        # Number of arguments (not including keyword only arguments, * or ** args)
        return self.func.__code__.co_argcount

    def parse_docstring(self) -> Docstring:
        return docstring_parse(self.func.__doc__)

    def get_typehints(self) -> dict[str, Any]:
        annotations = self.func.__annotations__
        annotations.pop("return", None)

        return annotations

    def update_inputs(self):
        docstring = self.parse_docstring()

        for variable, _type in self.variables.items():
            pass





    def init_ui(self):
        pass
