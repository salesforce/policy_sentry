"""
Methods that are basically text/string operations for specific purposes
"""


def capitalize_first_character(some_string):
    """
    Description: Capitalizes the first character of a string
    :param some_string:
    :return:
    """
    return " ".join("".join([w[0].upper(), w[1:].lower()]) for w in some_string.split())
