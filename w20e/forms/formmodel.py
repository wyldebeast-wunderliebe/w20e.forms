from model.fieldproperties import FieldProperties
from model import converters, validators
from registry import Registry
import types
import evaluator

converters.register()
validators.register()


class FormModel(object):
    """ Hold properties for form """

    def __init__(self, expressionlanguage='python'):

        self._props = {}
        self._bindings = {}
        self._expressionlanguage = expressionlanguage

    def __repr__(self):

        reprlist = ["FormModel:", ""]

        for prop in self._props.keys():
            reprlist.append(self._props[prop].__repr__())

        return "\n".join(reprlist)

    def __json__(self, request):
        return {
            "bindings": self._bindings
        }

    def _eval(self, expression, _globals, _locals):

        if self._expressionlanguage == 'javascript':
            return evaluator.eval_javascript(expression, _globals, _locals)

        return evaluator.eval_python(expression, _globals, _locals)

    def addFieldProperties(self, prop):

        self._props[prop.id] = prop
        binds = prop.bind
        if isinstance(binds, basestring):
            binds = [binds]
        for binding in binds:

            if binding not in self._bindings:
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
                if not self._eval(
                        props.getRelevant(),
                        {"data": data, "model": self}, Registry.funcs):
                    return False
            except:
                return True

        return True

    def isRequired(self, field_id, data):

        for props in self.getFieldProperties(field_id):

            try:
                if self._eval(
                            props.getRequired(), {"data": data, "model": self},
                            Registry.funcs):
                    return True
            except:
                return False

        return False

    def isReadonly(self, field_id, data):

        for props in self.getFieldProperties(field_id):

            try:
                if self._eval(
                        props.getReadonly(), {"data": data, "model": self},
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
                val = self._eval(
                           props.getCalculate(), {"data": data, "model": self},
                           Registry.funcs)
                return (val, True)

            except:
                pass

        return (None, False)

    def meetsConstraint(self, field_id, data):

        meets = True

        for props in self.getFieldProperties(field_id):

            try:
                if not self._eval(
                        props.getConstraint(), {"data": data, "model": self},
                        Registry.funcs):
                    meets = False
            except:
                pass

        return meets

    def checkDatatype(self, field_id, value):

        """ Check data type of value. Lists (multiple) is also ok. """

        valid = True

        for props in self.getFieldProperties(field_id):

            datatype = props.getDatatype()

            if datatype:

                try:
                    validator = Registry.get_validator(datatype)
                    valid = validator(value)
                    if not valid:
                        break
                except:
                    valid = False
                    break

        return valid

    def get_field_datatype(self, field_id):

        for props in self.getFieldProperties(field_id):

            datatype = props.getDatatype()

            if datatype:
                return datatype

        return "string"

    def convert(self, field_id, value):

        """ Convert field tp type given in constraint """

        for props in self.getFieldProperties(field_id):

            datatype = props.getDatatype()

            if datatype:

                try:
                    converter = Registry.get_converter(datatype)
                    value = converter(value)
                    break
                except:
                    pass

        return value

    def collectEfferentFields(self):

        """ Find all fields in the properties that actually have an effect
        on other fields. """

        fields = {}

        class Collector:

            def __init__(self, bind):
                if not isinstance(bind, types.ListType):
                    bind = [bind]
                self._bind = bind

            def __getitem__(self, name):

                if name not in fields:
                    fields[name] = []

                fields[name].extend(self._bind)

        for prop in self._props.values():

            for rule in ["_constraint", "_relevant", "_required", "_readonly",
                         "_calculate"]:

                try:
                    self._eval(
                        getattr(prop, rule, ""),
                        {"data": Collector(prop.bind)})
                except:
                    # this is possibly a calculated field which uses
                    # a registered function for it's calculation. There is no
                    # simple way to find which fields are used to calculated
                    # the value, so just add the current field to the efferent
                    # list, so the caller can at least process this fields
                    bind = prop.bind
                    if not isinstance(bind, types.ListType):
                        bind = [bind]
                    for name in bind:
                        if name not in fields:
                            fields[name] = []
                        fields[name].extend(bind)

        return fields
