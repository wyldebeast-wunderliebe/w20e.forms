"""
Any datatype validators should go here...
"""

from datetime import datetime
from w20e.forms.registry import Registry


class CheckInstance(object):

    def __init__(self, datatype):
        self._datatype = datatype

    def __call__(self, value):
        return isinstance(value, self._datatype)


def validate_file(value):
    """ is the value a file type """
    ftype = isinstance(value, file)

    if ftype:
        return True

    # hmm.. could be our own wrapped file thing.
    is_dict = isinstance(value, dict)
    has_name = 'name' in value
    has_data = 'data' in value

    # note: we could check here if the file is valid (has a length?)
    # or if it has a name?
    # for now, just having the attributes is good enough
    return is_dict and has_name and has_data


def register():

    validate_string = CheckInstance(str)
    validate_int = CheckInstance(int)
    validate_float = CheckInstance(float)
    validate_date = CheckInstance(datetime)

    Registry.register_validator("string", validate_string)
    Registry.register_validator("int", validate_int)
    Registry.register_validator("float", validate_float)
    Registry.register_validator("date", validate_date)
    Registry.register_validator("datetime", validate_date)
    Registry.register_validator("file", validate_file)
