class ATCTBaseObject:

    """ Base class for using w20e.forms as editing front-end for your
    ATCT content. For your specific implementation, make sure to
    register an adapter for your type that provides an IForm instance.
    TODO: maybe we should cache the form?
    """

    def __init__(self, attr_name="_DATA", defaults=None):

        self.attr_name = attr_name
        self.formdefaults = defaults or {}

    def Title(self):
        """ Return title or id """

        return self.getFieldValue('title', self.getId())

    def getFieldValue(self, name, default=None):
        """ Get the data field value or default """

        data = getattr(self, self.attr_name, None)

        if not data:
            return default

        #return value or default
        return data.get(name, default)
