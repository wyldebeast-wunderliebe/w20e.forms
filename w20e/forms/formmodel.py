from model.fieldproperties import FieldProperties
from model.converters import *
from registry import Registry


class FormModel:

    """ Hold properties for form """

    def __init__(self):

        self._props = {}
        self._bindings= {}


    def __repr__(self):

        reprlist = ["FormModel:", ""]
        
        for prop in self._props.keys():
            reprlist.append(self._props[prop].__repr__())

        return "\n".join(reprlist)


    def addFieldProperties(self, prop):

        self._props[prop.id] = prop
        for binding in prop.bind:

            if not self._bindings.has_key(binding):
                self._bindings[binding] = []
                
            self._bindings[binding].append(prop)
        

    def getAllFieldProperties(self):

        return self._props.values()


    def getFieldProperties(self, binding):

        """ Get the properties for the given id, or return default
        properties
        """
      
        return self._bindings.get(binding, [FieldProperties("default", [])])
        

    def isGroupRelevant(self, group, data):

        """ Determine relevance of group. This is relevant if any nested
        control is relevant """

        for sub in group.getRenderables():

            if hasattr(sub, 'getRenderables'):
                if self.isGroupRelevant(sub, data):
                    return True
            else:
                if self.isRelevant(sub.id, data):
                    return True

        return False


    def isRelevant(self, field_id, data):

        """ Check whether the field id is relevant. This checks all
        relevance rules of all bound properties. If one says 'not relevant',
        this is leading. Defaults to True.
        """

        for props in self.getFieldProperties(field_id):

            try:
                if not eval(props.getRelevant(), {"data": data}, Registry.funcs):
                    return False
            except:
                return True

        return True


    def isRequired(self, field_id, data):

        for props in self.getFieldProperties(field_id):

            try:
                if eval(props.getRequired(), {"data": data}, Registry.funcs):

                    return True
            except:
                return False

        return False


    def isReadonly(self, field_id, data):

        for props in self.getFieldProperties(field_id):

            try:
                if eval(props.getReadonly(), {"data": data}, Registry.funcs):

                    return True
            except:
                return False

        return False


    def getCalculate(self, field_id, data):

        val = None

        for props in self.getFieldProperties(field_id):

            try:
                val = eval(props.getCalculate(), {"data": data}, Registry.funcs)
            except:
                pass

            if val:
                break

        return val


    def meetsConstraint(self, field_id, data):

        meets = True

        for props in self.getFieldProperties(field_id):

            try:
                if not eval(props.getConstraint(), {"data": data}, 
                            Registry.funcs):

                    meets = False
            except:
                pass

        return meets


    def checkDatatype(self, field_id, value):

        """ Check data type of value. Lists (multiple) is also ok. """

        for props in self.getFieldProperties(field_id):

            datatype = props.getDatatype()

            if datatype:

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

            if datatype:

                try:
                    return eval("%s('%s')" % (datatype, value))
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

                if not fields.has_key(name):
                    fields[name] = []

                fields[name] += self._bind


        for prop in self._props.values():

            for rule in ["_constraint", "_relevant", "_required", "_readonly", 
                         "_calculate"]:
                
                try:
                    eval(getattr(prop, rule, ""), {"data": Collector(prop.bind)})
                except:
                    pass
                    
        return fields
