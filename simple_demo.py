'''
A simple Gooey example. One required field, one optional.
'''
from pprint import pprint

from funky import FunctionParser
import inspect




# This does a thing!
def integer_processor(number, banana: str, flag: bool = True, test: str = "yo", *args, **kwargs) -> tuple[str, int]:
    """
    Yoyoyo. This is a function

    Args:
        banana:
        number: A valid integer
        flag: A boolean flag

    Returns:
        A string or integer

    """
    return banana, number

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

    fp = FunctionParser(integer_processor)
    print(fp.description)


if __name__ == '__main__':
    main()
