import warnings
from docstring_parser import parse as docstring_parse, Docstring
from typing import Callable
import inspect

class ParserException(Exception):
    pass


class FunctionParser:
    def __init__(self, func: Callable):
        self.func = func
        self.docstring = self.parse_docstring()
        self.parameters = self.parse_parameters()

        print(self.parameters)

    # TODO Add check to ensure func parameter is a actually a function

    def parse_docstring(self) -> Docstring:
        docstring = inspect.getdoc(self.func)
        return docstring_parse(docstring)

    def parse_parameters(self) -> list[inspect.Parameter]:
        # Get dictionary of parameters by name
        parameters = dict(inspect.signature(self.func).parameters)

        # Remove unsupported parameter types
        for param in list(parameters.values()):
            if param.kind is param.VAR_POSITIONAL:
                warnings.warn(f"*args parameters ({param.name}) are ignored")
                parameters.pop(param.name)

            elif param.kind is param.VAR_KEYWORD:
                warnings.warn(f"**kwargs parameters ({param.name}) are ignored")
                parameters.pop(param.name)

        # Return the list of supported parameters
        return list(parameters.values())

    @property
    def description(self) -> str:
        """Returns the description found in the function"""
        # Long description in docstring
        if self.docstring.long_description:
            return self.docstring.long_description

        # Short description at top of docstring
        elif self.docstring.short_description:
            return self.docstring.short_description

        # Comment above function
        elif inspect.getcomments(self.func):
            return inspect.getcomments(self.func).lstrip("# ")

        else:
            return ""


class MultiFunctionParser:
    def __init__(self, *funcs):
        for func in funcs:
            yield FunctionParser(func)