from zope.interface import implements
from w20e.forms.interfaces import IControl
from renderables import Renderable


REPR = """%(type)s %(id)s, bound to '%(bind)s':
  label: %(label)s
  hint: %(hint)s
  help: %(help)s
  alert: %(alert)s
  """


class Control(Renderable):

    """ Base class for controls """

    implements(IControl)

    def __init__(self, id, label, bind=None, hint="", help="", alert="",
                 **props):

        Renderable.__init__(self, id, **props)

        self.bind = bind
        self.label = label
        self.hint = hint
        self.help = help
        self.alert = alert

    def __repr__(self):

        return REPR % self.__dict__

    def processInput(self, data=None):
        """ Base implementation """

        if data:
            return data.get(self.id, None)

    def lexVal(self, value):

        return value


class Input(Control):

    """ Base input """


class Password(Control):

    """ Base input with '*'... """


class File(Control):

    """ File upload control """


class Checkbox(Control):

    """ Checkbox """


class RichText(Control):

    """ Base input """


class Option:

    def __init__(self, value, label):

        self.value = value
        self.label = label
        self.selected = "false"


class Select(Control):

    def __init__(self, control_id, label, options=[], bind=None, **properties):

        Control.__init__(self, control_id, label, bind=bind, **properties)
        self._options = options[:]

    @property
    def options(self):

        return self._options

    def addOption(self, option):

        """ Add single option """

        self._options.append(option)

    def addOptions(self, options):

        """ Add list of options """

        self._options = self._options + options[:]

    def lexVal(self, value):

        """ Lexical value of select should return the label of the
        matching option. """

        if type([]) == type(value):

            res = []

            for val in value:

                res.append(self.lexVal(val))

            return res

        else:
            for opt in self.options:

                if opt.value == str(value):

                    return opt.label

        return value


class Range(Select):

    """ Show range of options """

    def __init__(self, control_id, label, bind=None, start=0,
                 end=0, step=1, reverse=False, **properties):

        opts = [Option(i, str(i)) for i in range(int(start),
            int(end), int(step))]
        if reverse:
            opts.reverse()

        Select.__init__(self, control_id, label, options=opts,
                        bind=bind, **properties)

