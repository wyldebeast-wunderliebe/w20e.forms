from w20e.forms.interfaces import IRenderable
from zope.interface import implements

DEFAULTS = {'input':
                {"rows": 1, "cols": 20},
            'password':
                {"rows": 1, "cols": 20},
            'select':
                {"multiple": "", "size": "1", "format": "compact",
                 "with_empty": False},
            'range':
                {"multiple": "", "size": "1", "format": "compact",
                 "with_empty": False},
            'table':
                {"rows": 3, "cols": 2},
            }


class Renderable(object):

    """ Base class for controls """

    implements(IRenderable)

    def __init__(self, id, **props):

        self.id = id
        self.type = self.__class__.__name__.lower()

        defaults = DEFAULTS.get(self.type, {}).copy()
        defaults.update(props)

        self._custom_props = props.keys()

        self.__dict__.update(defaults)

    def __getattr__(self, attr_name):

        try:
            return object.__getattr__(self, attr_name)
        except:
            return None


class Hidden(Renderable):

    """ Base hidden. Is somewhere between control and renderable... """

    def __init__(self, id, bind=None, **props):

        Renderable.__init__(self, id, **props)

        self.bind = bind


class Text(Renderable):

    def __init__(self, id, text, bind=None, **props):

        Renderable.__init__(self, id, **props)
        self.text = text
        # it can sometime be usefull to have relevance for a text field
        # so we need to set the bind here
        self.bind = bind


class Button(Renderable):
    """ Do we really need this? """
    def __init__(self, id, label, **props):

        Renderable.__init__(self, id, **props)
        self.label = label


class Submit(Renderable):

    def __init__(self, id, label, **props):

        Renderable.__init__(self, id, **props)
        self.label = label


class Cancel(Renderable):

    implements(IRenderable)

    def __init__(self, id, label, **props):

        Renderable.__init__(self, id, **props)
        self.label = label
