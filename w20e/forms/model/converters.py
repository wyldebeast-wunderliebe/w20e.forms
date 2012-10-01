"""
Any datatype converters that are not yet standard python should go here...
"""

from datetime import datetime
from w20e.forms.registry import Registry


def to_date(value, format):

    return datetime.strptime(value, format)


Registry.register_converter("string", str)
Registry.register_converter("str", str)
Registry.register_converter("int", int)
Registry.register_converter("float", float)
Registry.register_converter("date", to_date)
Registry.register_converter("datetime", to_date)
