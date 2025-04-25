import pytest
from funky.parser import FunctionParser, ParserException

# This is the comment for a function that does nothing.
def example_function(number: int, flag: bool = True, *args, **kwargs) -> tuple[int, bool]:
    """
    This is the short description for a function that does nothing.

    This is the long description for a function that does nothing.

    Args:
        *args:
        **kwargs:
        number (int): A valid integer
        flag (bool, optional): A boolean flag

    Returns:
        The input number and flag

    """
    return number, flag

# TODO Write tests for parsing arg_name, title (done), description, type, optional, default_value

def test_pretty_split():
    assert FunctionParser._title("lower") == "Lower"
    assert FunctionParser._title("Capitalised") == "Capitalised"
    assert FunctionParser._title("snake_case") == "Snake Case"
    assert FunctionParser._title("UPPER_SNAKE_CASE") == "Upper Snake Case"
    assert FunctionParser._title("Capitilised_Snake_Case") == "Capitilised Snake Case"
    assert FunctionParser._title("PascalCase") == "Pascal Case"
    assert FunctionParser._title("camelCase") == "Camel Case"
    assert FunctionParser._title("3DCamelCase") == "3D Camel Case"
    assert FunctionParser._title("Camel5Case") == "Camel 5 Case"


