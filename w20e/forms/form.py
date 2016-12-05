from zope.interface import implements
from interfaces import IForm


class FormValidationError(Exception):

    def __init__(self, errors=None):
        super(FormValidationError, self).__init__()

        if not errors:
            errors = {}
        self._errors = errors

    def __repr__(self):

        return "FormValidationError: %s" % self._errors

    @property
    def errors(self):

        return self._errors

    def addError(self, fieldId, error):

        if fieldId in self._errors:
            self._errors[fieldId] = []

        self._errors[fieldId].append(error)


class Form(object):

    """ Basic form implementation class. This class basically holds a
    data object, a model and a view.
    """

    implements(IForm)

    def __init__(self, id, data, model, view, submission, set_defaults=True):

        """ Initialize the form, using the given data, model and view.
        """

        self.id = id
        self.data = data
        self.model = model
        self.view = view
        self.submission = submission

        # set the default values
        if set_defaults:
            self.setDefaults()

    def __json__(self, request):
        return {
            "id": self.id,
            "data": self.data,
            "model": self.model,
            "view": self.view,
            "submission": self.submission
        }

    def setDefaults(self):
        """ set the default values from the model field properties """

        for prop in self.model.getAllFieldProperties():
            expression = prop.getDefault()
            if expression:
                binds = prop.bind
                for bind in binds:
                    (value, found) = self.model.getDefault(bind, self.data)
                    if found:
                        self.data[bind] = value

    def render(self):
        return self.view.render(self)

    def validate(self, fields=None):

        """ Validate the form. If this fails, an FormValidationError is raised,
        that holds the errors encountered in an associative array, using the
        node id as key, and an array of error messages as value.

        Validation works as follows:
         * check for requiredness for each field. If a field is required, and
           not set, this is an error
         * check for constraints on the field. If any are failed to meet,
           this is an error

        """

        errors = {}
        value = None

        if not fields:

            fields = self.data.getFields()

        for field in fields:

            field_errors = []

            try:
                value = self.data[field]
            except:
                pass

            # Requiredness
            if self.isEmpty(value) and self.model.isRequired(field, self.data):

                field_errors.append("required")

            # check datatype
            # TODO: should we get the non lexical value using getFieldValue?
            if value:
                # NOTE: we check the converted value, since e.g. int types
                # will always be passed in as string by HTML submit
                converted = self.model.convert(field, value)
                if not self.model.checkDatatype(field, converted, self.data):
                    field_errors.append("datatype")

            # Constraint checking...
            if not self.model.meetsConstraint(field, self.data):
                field_errors.append("constraint")

            if field_errors:
                errors[field] = field_errors

        if errors:
            raise FormValidationError(errors)
        else:
            return True

    def isEmpty(self, value):

        """ Check whether value is empty """

        if value is None or value == "":

            return True

        # empty list or tuple is considered empty as well
        if value == [] or value == ():

            return True

        return False

    def getFieldValue(self, name, default=None, val=None, lexical=False,
                      only_relevant=False, **kwargs):

        """ Get the data field value or default or calculated
        value. If lexical is something true-ish, return lexical space
        value.
        NOTE: if the only_relevant parameter was specified and if this field
        is not relevant with regards to the relevance properties in the form's
        model, then None will be returned.
        In this case the field might have a value, but since it's not
        relevant we return None
        """

        if only_relevant and not self.model.isRelevant(name, self.data):
            return None

        calculate_found = False

        try:
            (val, calculate_found) = self.model.getCalculate(name, self.data)
            if not calculate_found:
                val = self.data.getField(name).value
        except:
            pass

        if not lexical:
            try:
                return self.model.convert(name, val)
            except:
                return None
        else:

            default = default or ''

            try:
                if not calculate_found and val is None:
                    val = default

                val = self.model.convert(name, val)

                return self.view.getRenderableByBind(name).lexVal(
                    val, **kwargs)
            except:
                return val
