'''
A simple Gooey example. One required field, one optional.
'''
from funky import FunctionParser


def integer_processor(number: int, banana: str, flag: bool = False) -> tuple[str, int]:
    """

    Args:
        banana:
        number: A valid integer
        flag: A boolean flag

    Returns:
        A string or integer

    """
    return banana, number

def main():
    FunctionParser(integer_processor)



if __name__ == '__main__':
    main()
