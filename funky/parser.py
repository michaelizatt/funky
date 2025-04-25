import re
import warnings
from docstring_parser import parse as docstring_parse, Docstring
from typing import Callable
import inspect

class ParserException(Exception):
    pass


class FunctionParser:
    def __init__(self, func: Callable):
        self.func = func
        self._docstring = self.parse_docstring()

        print(self.parameters)

    # TODO Add check to ensure func parameter is a actually a function

    def parse_docstring(self) -> Docstring:
        docstring = inspect.getdoc(self.func)
        return docstring_parse(docstring)

    def _parse_func_parameters(self) -> list[inspect.Parameter]:
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
        if self._docstring.long_description:
            return self._docstring.long_description

        # Short description at top of docstring
        elif self._docstring.short_description:
            return self._docstring.short_description

        # Comment above function
        elif inspect.getcomments(self.func):
            return inspect.getcomments(self.func).lstrip("# ")

        else:
            return ""

    def parameters(self):
        func_parameters = self._parse_func_parameters()
        ds_parameters = self._docstring.params

        for param in func_parameters:
            name = param.name
            ds_param = ds_parameters[name]

            d = {'arg_name': name,
                 'title': self._title(name),
                 'description': '',
                 'type': None,
                 'optional': None,
                 'default_value': None
                 }

    @staticmethod
    def _title(arg_name: str) -> str:
        """Formats the title to be Capitalised and split words"""
        # Split Snake Case and return
        if "_" in arg_name:
            return arg_name.replace("_", " ").title()

        # Convert Camel Case to Pascal Case
        if arg_name[0].islower():
            arg_name = arg_name[:1].upper() + arg_name[1:]

        # Thanks mnesarco for this solution
        def split_pascal(value):
            return re.findall('[A-Z][a-z]+|[0-9A-Z]+(?=[A-Z][a-z])|[0-9A-Z]{2,}|[a-z0-9]{2,}|[a-zA-Z0-9]', value)

        # Split Pascal Case
        return " ".join(split_pascal(arg_name))

class MultiFunctionParser:
    def __init__(self, *funcs):
        for func in funcs:
            yield FunctionParser(func)