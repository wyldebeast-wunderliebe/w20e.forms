from zope.interface import implements
from w20e.forms.interfaces import IFieldProperties

REPR="""FieldProperties %(id)s for %(bind)s:
  required: %(_required)s
  relevant: %(_relevant)s
  readonly: %(_readonly)s
  constraint: %(_constraint)s
  calculate: %(_calculate)s
  datatype: %(_datatype)s
  """

class FieldProperties(object):

    """ Properties implementation class """

    implements(IFieldProperties)


    def __repr__(self):

        return REPR % self.__dict__


    def __init__(self, id, bind,
                 required="False",
                 relevant="True",
                 datatype=None,
                 readonly="False",
                 constraint="True",
                 calculate=None):

        object.__init__(self)
        self.id = id
        self.bind = bind
        self._required = required
        self._relevant = relevant        
        self._readonly = readonly
        self._constraint = constraint
        self._calculate = calculate
        self._datatype = datatype


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
