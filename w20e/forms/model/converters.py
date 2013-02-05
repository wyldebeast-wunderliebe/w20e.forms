"""
Any datatype converters that are not yet standard python should go here...
"""

from datetime import datetime
import dateutil.parser
from w20e.forms.registry import Registry


def to_date(value, format=None):

    # return empty string is empty string was passed in..
    if not (value and value.strip()):
        return ''

    if format:
        return datetime.strptime(value, format)

    else:
        # converting datetime sucks.. fingers crossed for dateutil
        return dateutil.parser.parse(value)


def to_str(value):
    if value is None:
        return ''
    else:
        return str(value)


def register():

    Registry.register_converter("string", to_str)
    Registry.register_converter("str", to_str)
    Registry.register_converter("int", int)
    Registry.register_converter("float", float)
    Registry.register_converter("date", to_date)
    Registry.register_converter("datetime", to_date)
