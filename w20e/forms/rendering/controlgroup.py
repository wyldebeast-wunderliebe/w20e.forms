from builtins import object
from zope.interface import implementer
from ...interfaces import IControlGroup


@implementer(IControlGroup)
class ControlGroup(object):
    pass

