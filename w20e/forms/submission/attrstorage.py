from submission import SubmissionBase

DATA_ATTR_NAME = "_w20e_forms_data"


class AttrStorage(SubmissionBase):

    """ Submission handler that submits data to content type.
    """

    type = "attr"

    def __init__(self, **props):

        """ AttrStorage uses simple attribute storage to store the
        whole data container on the context.
        """

        SubmissionBase.__init__(self, **props)

        self.attr_name = props.get("attr_name", DATA_ATTR_NAME)


    def submit(self, form, context, *args):

        """ Submit data. This involves storing it onto the content
        type. The submit call should provide the context as first
        param.
        """

        try:
            setattr(context, self.attr_name, form.data)            
        except:
            pass


    def retrieve(self, form, context, *args):

        """ Restore data. """

        if not hasattr(context, self.attr_name):
            raise AttributeError(self.attr_name)
        return getattr(context, self.attr_name)
