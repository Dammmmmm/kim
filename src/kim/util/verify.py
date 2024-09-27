import re
import keyword

def is_valid_filename(filename):
    if len(filename) > 255:
        return False
    invalid_chars = r'[<>:"/\\|?*]'
    if re.search(invalid_chars, filename):
        return False
    if filename.startswith('.') or filename.endswith('.') or filename.startswith(' ') or filename.endswith(' '):
        return False
    return True


def is_valid_variable_name(variable_name):
    if variable_name in keyword.kwlist:
        return False
    if not variable_name[0].isalpha() and variable_name[0] != '_':
        return False
    for char in variable_name:
        if not (char.isalnum() or char == '_'):
            return False
    return True
