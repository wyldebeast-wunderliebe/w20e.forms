from submission import SubmissionBase

DATA_ATTR_NAME = "survey"


class PyramidSessionStorage(SubmissionBase):

    """ Submission handler that submits data to content type.
    """

    type = "pyramidsession"

    def __init__(self, **props):

        """ PyramidSessionStorage stores the data container in the session
        """

        SubmissionBase.__init__(self, **props)

        self.attr_name = props.get("attr_name", DATA_ATTR_NAME)

    def submit(self, form, context, request, *args):

        """ Submit data. This involves storing it in the session
        The submit call should provide the context as first
        param.
        """

        request.session[self.attr_name] = form.data

    def retrieve(self, form, context, request, *args):

        """ Restore data. """

        return request.session[self.attr_name]
