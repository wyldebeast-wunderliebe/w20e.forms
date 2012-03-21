from model.fieldproperties import FieldProperties
from model.converters import *
from registry import Registry


class FormModel(object):

    """ Hold properties for form """

    def __init__(self):

        self._props = {}
        self._bindings = {}

    def __repr__(self):

        reprlist = ["FormModel:", ""]

        for prop in self._props.keys():
            reprlist.append(self._props[prop].__repr__())

        return "\n".join(reprlist)

    def addFieldProperties(self, prop):

        self._props[prop.id] = prop
        for binding in prop.bind:

            if not binding in self._bindings:
                self._bindings[binding] = []

            self._bindings[binding].append(prop)

    def getAllFieldProperties(self):

        return self._props.values()

    def getFieldProperties(self, binding):

        """ Get the properties for the given id, or return default
        properties
        """

        return self._bindings.get(binding, [FieldProperties("default", [])])

    def getFieldValue(self, name, data):

        """ Get the data field value calculated value."""

        try:
            (val, found) = self.getCalculate(name, data)
            if not found:
                val = data.getField(name).value
        except:
            pass

        try:
            return self.convert(name, val)
        except:
            return None

    def isGroupRelevant(self, group, data):

        """ Determine relevance of group. This is relevant if any nested
        controlled bind is relevant """

        for sub in group.getRenderables():

            if hasattr(sub, 'getRenderables') and callable(sub.getRenderables):
                if self.isGroupRelevant(sub, data):
                    return True
            else:
                if sub.bind and self.isRelevant(sub.bind, data):
                    return True

        return False

    def isRelevant(self, field_id, data):

        """ Check whether the field id is relevant. This checks all
        relevance rules of all bound properties. If one says 'not relevant',
        this is leading. Defaults to True.
        """

        for props in self.getFieldProperties(field_id):

            try:
                if not eval(props.getRelevant(), {"data": data, "model": self},
                        Registry.funcs):
                    return False
            except:
                return True

        return True

    def isRequired(self, field_id, data):

        for props in self.getFieldProperties(field_id):

            try:
                if eval(props.getRequired(), {"data": data, "model": self},
                        Registry.funcs):

                    return True
            except:
                return False

        return False

    def isReadonly(self, field_id, data):

        for props in self.getFieldProperties(field_id):

            try:
                if eval(props.getReadonly(), {"data": data, "model": self},
                        Registry.funcs):

                    return True
            except:
                return False

        return False

    def getCalculate(self, field_id, data):
        """ return a tuple with first param the calculated value
        and the second param indicates whether a calculation has been found
        """

        for props in self.getFieldProperties(field_id):

            try:
                val = eval(props.getCalculate(), {"data": data, "model": self},
                           Registry.funcs)
                return (val, True)

            except:
                pass

        return (None, False)

    def meetsConstraint(self, field_id, data):

        meets = True

        for props in self.getFieldProperties(field_id):

            try:
                if not eval(props.getConstraint(), {"data": data,
                    "model": self}, Registry.funcs):

                    meets = False
            except:
                pass

        return meets

    def checkDatatype(self, field_id, value):

        """ Check data type of value. Lists (multiple) is also ok. """

        for props in self.getFieldProperties(field_id):

            datatype = props.getDatatype()

            #TODO do a proper validation for file
            if datatype and datatype != 'file':

                """ if hasattr(value, "__iter__"):

                newvalue = []

                for val in value:

                newvalue.append(eval("%s(val)" % datatype),
                {'val': val}, Registry.funcs)

                return newvalue

                else: """

                return eval("%s(val)" % datatype,
                            {'val': value}, Registry.funcs)

        return value

    def convert(self, field_id, value):

        """ Convert field tp type given in constraint """

        for props in self.getFieldProperties(field_id):

            datatype = props.getDatatype()

            if datatype and datatype != 'file':

                try:
                    return eval("%s(arg)" % datatype, {'arg': value})
                except:
                    return value

        return value

    def collectEfferentFields(self):

        """ Find all fields in the properties that actually have an effect
        on other fields. """

        fields = {}

        class Collector:

            def __init__(self, bind):
                self._bind = bind

            def __getitem__(self, name):

                if not name in fields:
                    fields[name] = []

                fields[name] += self._bind

        for prop in self._props.values():

            for rule in ["_constraint", "_relevant", "_required", "_readonly",
                         "_calculate"]:

                try:
                    eval(getattr(prop, rule, ""),
                         {"data": Collector(prop.bind)})
                except:
                    pass

        return fields
