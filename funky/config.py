import re

def _capitalise_string(arg_name: str) -> str:
    """Formats a function name or variable to be Capitalised and split words"""
    # Split Snake Case and return
    if "_" in arg_name:
        return arg_name.replace("_", " ").title()

    # Convert Camel Case to Pascal Case
    if arg_name[0].islower():
        arg_name = arg_name[:1].upper() + arg_name[1:]

    # Split Pascal Case - Thanks mnesarco for this solution (regex oof...)
    split_pascal = re.findall('[A-Z][a-z]+|[0-9A-Z]+(?=[A-Z][a-z])|[0-9A-Z]{2,}|[a-z0-9]{2,}|[a-zA-Z0-9]',
                              arg_name)

    return " ".join(split_pascal)
