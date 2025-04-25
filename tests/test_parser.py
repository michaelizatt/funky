import pytest
from funky.parser import FunctionParser, ParserException


def func_wo_hints(int_var, str_var):
    pass

def func_w_kw_only_arg(int_var, str_var, kw_arg: bool = False):
    pass

def func_w_docstring_hints(int_var, str_var):
    """
    Args:
        int_var (int): Integer
        str_var (str): String
    """
    pass


def func_wo_return_hint(int_var: int, str_var: str):
    pass


def func_w_hints(int_var: int, str_var: str) -> tuple[str, int]:
    return str_var, int_var


def test_arguments_wo_hints():
    assert FunctionParser(func_wo_hints).get_typehints() == {}

def test_arguments_wo_return_hint():
    assert FunctionParser(func_wo_return_hint).get_typehints() == {"str_var": str, "int_var": int}

def test_arguments_w_return_hint():
    assert FunctionParser(func_w_hints).get_typehints() == {"str_var": str, "int_var": int}

def test_invalid_funcs():
    def func_w_args(int_var, str_var, *args): pass
    def func_w_kwargs(int_var, str_var, *kwargs): pass

    with pytest.raises(ParserException):
        FunctionParser(func_w_args)
    with pytest.raises(ParserException):
        FunctionParser(func_w_kwargs)