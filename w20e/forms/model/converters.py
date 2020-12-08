"""
Any datatype converters that are not yet standard python should go here...
"""

from builtins import str
from past.builtins import basestring
from datetime import datetime, date
import dateutil.parser
from w20e.forms.registry import Registry


def to_date(value, format=None):

    if isinstance(value, basestring):
        # return empty string is empty string was passed in..
        if not (value and value.strip()):
            return ''

        if format:
            return datetime.strptime(value, format).date()

        else:
            # converting datetime sucks.. fingers crossed for dateutil
            return dateutil.parser.parse(value).date()

    return value


def to_datetime(value, format=None):

    if isinstance(value, basestring):
        # return empty string is empty string was passed in..
        if not (value and value.strip()):
            return ''

        if format:
            return datetime.strptime(value, format)

        else:
            # converting datetime sucks.. fingers crossed for dateutil
            return dateutil.parser.parse(value)

    return value


def to_str(value):
    if isinstance(value, str) or isinstance(value, str):
        return value

    if value is None:
        return ''
    else:
        return str(value)


def to_int(value):
    """"convert any value to int.
     e.g. '123.567' -> 124
    """
    return int(round(float(value)))


def to_bool(value):

    # try to convert "False" and "0" strings
    str_val = to_str(value).lower()
    if str_val in ("false", "0"):
        return False

    # use the default converter
    return bool(value)


def to_list(value):

    # convert to list
    if type(value) != list:
        return [value]

    return value


def register():

    Registry.register_converter("string", to_str)
    Registry.register_converter("str", to_str)
    Registry.register_converter("int", to_int)
    Registry.register_converter("bool", to_bool)
    Registry.register_converter("float", float)
    Registry.register_converter("date", to_date)
    Registry.register_converter("datetime", to_datetime)
    Registry.register_converter("list", to_list)
