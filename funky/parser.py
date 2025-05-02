import warnings
from typing import Callable, Any, Type

from pydoc import locate
from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from docstring_parser import parse as docstring_parse, Docstring, DocstringParam
import inspect


class ParserException(Exception):
    pass


@dataclass
class Parameter:
    name: str
    type: Type
    description: str = ""
    optional: bool = False
    default_value: Any = None


# TODO: Add ability to use class or method - if not callable(func):
#  May need to create an ABC for Parser and create ClassParser and MethodParser

class FunctionParser:
    def __init__(self, func: Callable):
        # Check to ensure the provided func variable is a function
        if not inspect.isfunction(func):
            raise ParserException(f"The object {func} is not a function")
        self.func = func
        self._docstring: Docstring = self._parse_docstring()

    def _parse_docstring(self) -> Docstring:
        docstring = inspect.getdoc(self.func)
        return docstring_parse(docstring)

    def _parse_func_parameters(self) -> dict[str, inspect.Parameter]:
        """Uses inspect library to read parameters from function"""
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
        return parameters

    def _parse_docstring_parameters(self) -> dict[str, DocstringParam]:
        """Uses docstring_parser library to read parameters from docstring"""
        parameters = self._docstring.params

        return {param.arg_name: param for param in parameters}


    @property
    def description(self) -> str:
        """
        If possible returns a description found in the function in the order below:
        - Description in docstring
        - Comment above function
        """

        # Description in docstring
        if self._docstring.description:
            return self._docstring.description

        # Comment above function
        elif inspect.getcomments(self.func):
            return inspect.getcomments(self.func).lstrip("#").strip()

        else:
            return ""

    @property
    def parameters(self) -> list[Parameter]:
        func_parameters = self._parse_func_parameters()
        ds_parameters = self._parse_docstring_parameters()

        params = []

        for name, func_param in func_parameters.items():
            ds_param = ds_parameters.get(name, DocstringParam)

            # Set Parameter type
            if func_param.annotation != func_param.empty:
                _type = func_param.annotation
            elif ds_param.type_name:
                _type = locate(ds_param.type_name)
            else:
                _type = None    # Will raise an exception!

            if func_param.default != func_param.empty or ds_param.is_optional:
                optional = True
            else:
                optional = False

            if func_param.default != func_param.empty:
                default_value = func_param.default
            elif ds_param.default:
                # Attempts to convert the default value if it was provided as a string
                default_value = TypeAdapter(_type).validate_python(ds_param.default)
            else:
                default_value = None

            params.append(Parameter(name=name,
                            description=ds_param.description,
                            type=_type,
                            optional=optional,
                            default_value=default_value
                            )
                          )

        return params


class MultiParser:
    def __init__(self, *funcs):
        for func in funcs:
            yield FunctionParser(func)


