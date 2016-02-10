from w20e.forms.interfaces import IRenderable
from zope.interface import implements

DEFAULTS = {'input': {"rows": 1, "cols": 20},
            'password': {"rows": 1, "cols": 20},
            'select': {
                "multiple": "", "size": "1", "format": "compact",
                "with_empty": False},
            'range': {
                "multiple": "", "size": "1", "format": "compact",
                "with_empty": False},
            'table': {
                "rows": 3, "cols": 2},
            }

renderable_attrs = [
    'extra_classes', 'format', 'dateFormat', 'timeFormat',
    'data_options', 'vocab', 'addOption', 'cols', 'getRenderables', 'rows',
    'size', 'with_empty', 'orientation', 'multiple', 'options',
    'processInput', 'vocab_args', 'alert',
]


class Renderable(object):
    """ Base class for controls """

    implements(IRenderable)

    def __init__(self, id, **props):

        self.id = id
        self.type = self.__class__.__name__.lower()

        defaults = DEFAULTS.get(self.type, {}).copy()
        defaults.update(props)

        self.property_keys = defaults.keys()
        self.property_keys += ['id', 'type', ]

        self.__dict__.update(defaults)

    def __json__(self, request):
        return {k: self.__dict__[k] for k in self.property_keys}

    def __getattr__(self, attr_name):
        """ override the __getattr__ and return None instead of the
            AttributeError exception was a bad idea. It breaks things
            in e.g. the deepcopy. For backward compatibility it now still
            works for a number of attributes that are declared in the
            'renderable_attrs'. This might need some more work
        """

        if attr_name in renderable_attrs:
            try:
                return object.__getattribute__(self, attr_name)
            except AttributeError:
                return None
        else:
            return object.__getattribute__(self, attr_name)


class Hidden(Renderable):
    """ Base hidden. Is somewhere between control and renderable... """

    def __init__(self, id, bind=None, **props):
        Renderable.__init__(self, id, **props)

        self.bind = bind
        self.property_keys += ['bind', ]


class Text(Renderable):
    def __init__(self, id, text, bind=None, **props):
        Renderable.__init__(self, id, **props)
        self.text = text
        # it can sometime be usefull to have relevance for a text field
        # so we need to set the bind here
        self.bind = bind
        self.property_keys += ['bind', 'text', ]


class Button(Renderable):
    """ Do we really need this? """

    def __init__(self, id, label, bind=None, **props):
        Renderable.__init__(self, id, **props)
        self.label = label
        # it can sometime be usefull to have relevance for a text field
        # so we need to set the bind here
        self.bind = bind
        self.property_keys += ['bind', 'label', ]


class Submit(Renderable):
    def __init__(self, id, label, bind=None, **props):
        Renderable.__init__(self, id, **props)
        self.label = label
        self.bind = bind
        self.property_keys += ['bind', 'label', ]


class Cancel(Renderable):
    implements(IRenderable)

    def __init__(self, id, label, bind=None, **props):
        Renderable.__init__(self, id, **props)
        self.label = label
        self.bind = bind
        self.property_keys += ['bind', 'label', ]


class Reset(Renderable):
    implements(IRenderable)

    def __init__(self, id, label, bind=None, **props):
        Renderable.__init__(self, id, **props)
        self.label = label
        self.bind = bind
        self.property_keys += ['bind', 'label', ]
