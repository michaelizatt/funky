import pytest
from funky.parser import FunctionParser, ParserException
from funky.config import _capitalise_string


# This is the comment for a function that does nothing.
def example(number: int, flag: bool = True, *args, **kwargs) -> tuple[int, bool]:
    """
    A short description for a function that does nothing.

    This is the long description for a function that seems to not do anything at all...

    Args:
        number (int): A valid integer
        flag (bool, optional): A boolean flag
        *args:
        **kwargs:

    Returns:
        The input number and flag

    """
    return number, flag


# This is the comment for a function that does nothing.
def example_without_docstring(number: int, flag: bool, *args, **kwargs) -> tuple[int, bool]:
    return number, flag


def example_with_only_docstring(number, flag, *args, **kwargs):
    """
    A short description for a function that does nothing.

    This is the long description for a function that seems to not do anything at all...

    Args:
        number (int): A valid integer
        flag (bool, optional): A boolean flag
        *args:
        **kwargs:

    Returns:
        The input number and flag

    """
    return number, flag


def example_bare(number, flag, *args, **kwargs):
    return number, flag


class ExampleClass:
    def __init__(self, number: int, flag: bool = True, *args, **kwargs):
        self.number = number
        self.flag = flag

    def example_method(self, number: int, flag: bool = True, *args, **kwargs) -> tuple[int, bool]:
        return self.number, self.flag


# TODO Write tests for parsing arg_name, title (done), description, type, optional, default_value

def test_pretty_split():
    assert _capitalise_string("lower") == "Lower"
    assert _capitalise_string("Capitalised") == "Capitalised"
    assert _capitalise_string("snake_case") == "Snake Case"
    assert _capitalise_string("UPPER_SNAKE_CASE") == "Upper Snake Case"
    assert _capitalise_string("Capitilised_Snake_Case") == "Capitilised Snake Case"
    assert _capitalise_string("PascalCase") == "Pascal Case"
    assert _capitalise_string("camelCase") == "Camel Case"
    assert _capitalise_string("3DCamelCase") == "3D Camel Case"
    assert _capitalise_string("Camel5Case") == "Camel 5 Case"

def test_description():
    docstring_desc = "A short description for a function that does nothing.\n\n"\
                     "This is the long description for a function that seems to not do anything at all..."
    comment_desc = "This is the comment for a function that does nothing."

    assert FunctionParser(example).description == docstring_desc
    assert FunctionParser(example_with_only_docstring).description == docstring_desc
    assert FunctionParser(example_without_docstring).description == comment_desc
    assert FunctionParser(example_bare).description == ""

def test_parser_validation():
    FunctionParser(example)
    with pytest.raises(ParserException):
        FunctionParser(ExampleClass)
    with pytest.raises(ParserException):
        FunctionParser(ExampleClass(1).example_method)
    with pytest.raises(ParserException):
        FunctionParser("not_callable")

