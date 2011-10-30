from submission import SubmissionBase


class MethodCall(SubmissionBase):

    """ Submission handler that submits data to content type.
    """

    type = "methodcall"

    def __init__(self, **props):

        """ Method call submission enables calling a method of the
        form context.
        """

        SubmissionBase.__init__(self, **props)

        self.submit_method = props.get("submit_method", None)
        self.retrieve_method = props.get("retrieve_method", None)


    def submit(self, form, context, *args):

        if self.submit_method:
            func = getattr(context, self.submit_method)
            if callable(func):
                func(form, context, args)


    def retrieve(self, form, context, *args):

        if self.submit_method:
            func = getattr(context, self.retrieve_method)
            if callable(func):
                return func(form, context, args)

        return None
