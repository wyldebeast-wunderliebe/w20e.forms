from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object
from zope.interface import implements, implementer
from w20e.forms.interfaces import IControl
from .renderables import Renderable
from w20e.forms.registry import Registry
import json
from numbers import Number

REPR = """%(type)s %(id)s, bound to '%(bind)s':
  label: %(label)s
  hint:  %(hint)s
  help:  %(help)s
  alert: %(alert)s
  """


@implementer(IControl)
class Control(Renderable):
    """ Base class for controls """

    def __init__(self, _id, label, bind=None, hint="", help="", alert="",
                 **props):

        if _id is None:
            _id = bind

        Renderable.__init__(self, _id, **props)

        self.bind = bind
        self.label = label
        self.hint = hint
        self.help = help
        self.alert = alert

        self.property_keys += ['bind', 'label', 'hint', 'help', 'alert', ]

    def __repr__(self):
        return REPR % self.__dict__

    def processInput(self, data=None, datatype="string"):

        """ Base implementation """

        val = None

        if data:
            # for multiselects we need to read all values from the request.
            # TODO: note that this is done in different ways per framework
            # I think for plone the HTML markup should use ":list" as a
            # control name. But for now I need this in pyramid, and the
            # getall method works fine..
            if self.multiple:
                val = data.getall(self.id)
            else:
                val = data.get(self.id, None)

        try:
            converter = Registry.get_converter(datatype)
            val = converter(val)
            # TODO: what to do when multiple values are present? convert each
            # item in the list?
            # if self.multiple:
            #     newval = []
            #     for item in val:
            #         newval.append(converter(item))
            #     val = newval
            # else:
            #     val = converter(val)
        except:  # noqa
            pass

        return val

    def lexVal(self, value, **kwargs):

        return value


class Input(Control):
    """ Base input """

    @property
    def rows(self):
        return int(self.__dict__['rows'])

class Date(Control):
    """ Date widget """

    def __init__(self, *args, **kwargs):

        super(Date, self).__init__(*args, **kwargs)
        extra_classes = self.extra_classes or ""
        self.extra_classes = extra_classes + " date"
        if not self.format:
            self.format = "%Y-%m-%d"

        data_options = {}
        if self.dateFormat:
            data_options['dateFormat'] = self.dateFormat
        data_options['showTimepicker'] = 0  # not sure if this is used..
        self.data_options = json.dumps(data_options)

    def processInput(self, data=None, datatype="datetime"):

        """ Base implementation """

        val = None

        if data:
            val = data.get(self.id, None)

        try:
            converter = Registry.get_converter(datatype)

            val = converter(val.strip(), self.format)
        except:  # noqa
            pass

        return val

    def lexVal(self, value, **kwargs):

        return value.strftime(self.format)


class Month(Date):
    """ Month input type """

    def __init__(self, *args, **kwargs):
        super(Month, self).__init__(*args, **kwargs)
        self.format = "%Y-%m"


class DateTime(Control):
    """ Datetime widget """

    def __init__(self, *args, **kwargs):

        super(DateTime, self).__init__(*args, **kwargs)
        extra_classes = self.extra_classes or ""
        self.extra_classes = extra_classes + " datetime"
        if not self.format:
            self.format = "%Y-%m-%d %H:%M"

        data_options = {}
        if self.dateFormat:
            data_options['dateFormat'] = self.dateFormat
        if self.timeFormat:
            data_options['timeFormat'] = self.timeFormat
        if self.showTimepicker:
            data_options['showTimepicker'] = self.showTimepicker
        self.data_options = json.dumps(data_options)

    def processInput(self, data=None, datatype="datetime"):

        """ Base implementation """

        val = None

        if data:
            val = data.get(self.id, None)

        try:
            converter = Registry.get_converter(datatype)

            val = converter(val.strip(), self.format)
        except:  # noqa
            pass

        return val

    def lexVal(self, value, **kwargs):

        return value.strftime(self.format)


class Password(Control):
    """ Base input with '*'... """


class File(Control):
    """ File upload control """


class Checkbox(Control):
    """ Checkbox """


class RichText(Control):
    """ Base input """


class Option(object):
    def __init__(self, value, label):
        self.value = value
        self.label = label
        self.default = False

    def __json__(self, request):
        return {
            "value": self.value,
            "label": self.label,
            "default": self.default
        }


class Select(Control):
    def __init__(self, control_id, label, options=[], bind=None, **properties):

        Control.__init__(self, control_id, label, bind=bind, **properties)
        self._options = options[:]

    def __json__(self, request):
        json = super(Select, self).__json__(request)
        json['options'] = self._options
        return json

    @property
    def options(self):

        return self._options

    def addOption(self, option):

        """ Add single option """

        self._options.append(option)

    def addOptions(self, options):

        """ Add list of options """

        self._options = self._options + options[:]

    def lexVal(self, value, **kwargs):

        """ Lexical value of select should return the label of the
        matching option. """

        if type([]) == type(value):

            res = []

            for val in value:
                res.append(self.lexVal(val))

            return res

        options = []

        if self.vocab:
            vocab = Registry.get_vocab(self.vocab)

            args = []
            if self.vocab_args:
                args = self.vocab_args.split(",")

            if callable(vocab):
                options = vocab(*args, **kwargs)

        options.extend(self.options)

        for opt in options:

            if self._is_same(opt.value, value):
                return opt.label

        return value

    def _is_same(self, opt_value, value):

        """ Yeah, well, this is a tad nasty. The type of the optin may
        or may not be the same as the type of the actual value. So
        let's see where we get from here..."""

        if type(opt_value) == type(value):
            if opt_value == value:
                return True
            else:
                return False
        else:
            return str(opt_value) == str(value)


class Range(Select):
    """ Show range of options """

    def __init__(self, control_id, label, bind=None, start=0,
                 end=0, step=1, reverse=False, **properties):

        # options that are outside the auto generated start + end range
        self._added_options = []

        self.start = start
        self.end = end
        self.step = step

        try:
            self.start = int(start)
            self.end = int(end)
            self.step = int(step)
        except:  # noqa
            # probably no integers: just fail silently and return empty
            # option list.
            pass

        opts = []

        if (isinstance(self.start, Number) and
                isinstance(self.end, Number) and
                isinstance(self.step, Number)):

            opts = [
                Option(i, str(i)) for i in
                range(int(start), int(end), int(step))]

            if reverse:
                opts.reverse()

        Select.__init__(self, control_id, label, options=opts,
                        bind=bind, **properties)

        self.property_keys += ['start', 'end', 'step', 'reverse', ]

    def addOption(self, option):

        """ Add single option """

        super(Range, self).addOption(option)
        self._added_options.append(option)

    def addOptions(self, options):

        """ Add list of options """

        super(Range, self).addOptions(options)
        self._added_options = self._added_options + options[:]

    def __json__(self, request):
        json = super(Range, self).__json__(request)
        # only add the _extra_ specified options, not the ones that are in the
        # start + end range
        json['options'] = self._added_options
        return json
