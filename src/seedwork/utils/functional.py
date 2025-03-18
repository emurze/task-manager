import re


def string_to_kwarg_name(string):
    # Remove invalid characters and replace them with underscores
    valid_string = re.sub(r"[^a-zA-Z0-9_]", "_", string)

    # Ensure the name starts with a letter or underscore
    if not valid_string[0].isalpha() and valid_string[0] != "_":
        valid_string = "_" + valid_string

    return valid_string
