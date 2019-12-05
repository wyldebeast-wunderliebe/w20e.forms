from builtins import object
from zope.interface import implements
from ...interfaces import IControlGroup


class ControlGroup(object):

    implements(IControlGroup)
