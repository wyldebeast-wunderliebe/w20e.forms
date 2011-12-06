from zope.interface import implements
from w20e.forms.interfaces import IField


class Field(object):

    implements(IField)

    def __init__(self, id, value=None):

        self._id = id
        self.value = value

    def __call__(self):

        return self.value

    @property
    def id(self):

        return self._id
