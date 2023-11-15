
from zope.interface import implementer
from w20e.forms.interfaces import IField


@implementer(IField)
class Field(object):

    def __init__(self, id, value=None):

        self._id = id
        self.value = value

    def __call__(self):

        return self.value

    @property
    def id(self):

        return self._id
