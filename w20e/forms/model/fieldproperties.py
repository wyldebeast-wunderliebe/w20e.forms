from zope.interface import implementer
from w20e.forms.interfaces import IFieldProperties

REPR = u"""FieldProperties {id} for {bind}:
  required: {_required}
  relevant: {_relevant}
  readonly: {_readonly}
  constraint: {_constraint}
  calculate: {_calculate}
  datatype: {_datatype}
  default: {_default}
  """


@implementer(IFieldProperties)
class FieldProperties(object):

    """ Properties implementation class """

    def __repr__(self):

        result = REPR.format(**self.__dict__)
        return result.encode('utf-8')

    def __init__(self, id, bind,
                 required="0",  # False (in python + javascript)
                 relevant="1",  # True (in python + javascript)
                 datatype=None,
                 readonly="0",   # False
                 constraint="1",  # True
                 calculate=None,
                 default=None):

        object.__init__(self)
        self.id = id
        self.bind = bind
        self._required = required
        self._relevant = relevant
        self._readonly = readonly
        self._constraint = constraint
        self._calculate = calculate
        self._datatype = datatype
        self._default = default

    def __json__(self, request):
        return {
          "required": self._required,
          "relevant": self._relevant,
          "readonly": self._readonly,
          "constraint": self._constraint,
          "calculate": self._calculate,
          "datatype": self._datatype,
          "default": self._default
        }

    def getRequired(self):

        """ return expression for requiredness """

        return self._required

    def getRelevant(self):

        """ return expression for requiredness """

        return self._relevant

    def getReadonly(self):

        """ return expression for requiredness """

        return self._readonly

    def getConstraint(self):

        """ return expression for requiredness """

        return self._constraint

    def getCalculate(self):

        """ return expression for requiredness """

        return self._calculate

    def getDatatype(self):

        return self._datatype

    def getDefault(self):

        return self._default
