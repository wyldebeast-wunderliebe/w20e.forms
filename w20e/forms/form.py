from zope.interface import implements
from interfaces import IForm


class FormValidationError(Exception):

    def __init__(self, errors=None):
        super(FormValidationError, self).__init__()

        if not errors:
            errors = {}
        self._errors = errors

    def __repr__(self):

        print "FormValidationError: %s" % self._errors

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

    def __init__(self, id, data, model, view, submission):

        """ Initialize the form, using the given data, model and view.
        """

        self.id = id
        self.data = data
        self.model = model
        self.view = view
        self.submission = submission

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
            if value:
                try:
                    self.model.checkDatatype(field, value)
                except:
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

        return False

    def getFieldValue(self, name, default=None, val=None, lexical=False):

        """ Get the data field value or default or calculated
        value. If lexical is something true-ish, return lexical space
        value."""

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

                return self.view.getRenderableByBind(name).lexVal(val)
            except:
                return val

            return default
