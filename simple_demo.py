'''
A simple Gooey example. One required field, one optional.
'''
from pprint import pprint

from funky import FunctionParser
import inspect




# This is the comment for a function that does nothing.
def test_function(number: int, flag: bool = True, *args, **kwargs) -> tuple[int, bool]:
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

#pprint(inspect.signature(integer_processor).parameters)
#for p in inspect.signature(integer_processor).parameters.values():
#    print(p.name)
#    print(p.kind)
#    print(p.default)
#    print(p.annotation)

#pprint(inspect.signature(integer_processor).parameters.values())
#for param in inspect.signature(integer_processor).parameters.values():
#    if param.kind not in [param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD]:
#        print('Parameter:', param.name)
#        print('Parameter:', param.empty)


def main():

    fp = FunctionParser(test_function)
    print(fp.description)


if __name__ == '__main__':
    main()
