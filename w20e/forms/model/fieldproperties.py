
from zope.interface import implementer
from w20e.forms.interfaces import IFieldProperties

REPR = """FieldProperties {id} for {bind}:
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

        return REPR.format(**self.__dict__)

    def __init__(self, id, bind,
                 required=None,
                 relevant=None,
                 datatype=None,
                 readonly=None,
                 constraint=None,
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

        result = {}
        keys = [
            "required", "relevant", "readonly", "constraint", "calculate",
            "datatype", "default", ]

        for key in keys:
            v = getattr(self, '_{}'.format(key))
            if v is not None:
                result[key] = v

        return result

    def getRequired(self):

        """ return expression for requiredness """

        if self._required is None:
            return "0"  # try not to break old code which might check for 0

        return self._required

    def getRelevant(self):

        """ return expression for relevancy """

        if self._relevant is None:
            return "1"  # try not to break old code which might check for 1

        return self._relevant

    def getReadonly(self):

        """ return expression for readonlyness """

        if self._readonly is None:
            return "0"  # try not to break old code which might check for 0

        return self._readonly

    def getConstraint(self):

        """ return expression for constraint """

        if self._constraint is None:
            return "1"  # try not to break old code which might check for 1

        return self._constraint

    def getCalculate(self):

        """ return expression for calculation """

        return self._calculate

    def getDatatype(self):

        """ return expression for datatype """

        return self._datatype

    def getDefault(self):

        """ return expression for default value """

        return self._default
