'''
A simple Gooey example. One required field, one optional.
'''
from funky import FunctionParser




# This is the comment for a function that does nothing.
def some_function(number: int, flag: bool = True, *args, **kwargs) -> tuple[int, bool]:
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

def main():
    fp = FunctionParser(some_function)

if __name__ == '__main__':
    main()
