from submission import SubmissionBase


class MethodCall(SubmissionBase):

    """ Submission handler that submits data to content type.
    """

    type = "methodcall"

    def __init__(self, **props):

        """ Method call submission enables calling a method of the
        form context, or attributes thereof. To call methods on
        subparts, do something like 'subattribute.method'.
        """

        SubmissionBase.__init__(self, **props)

        self.submit_method = props.get("submit_method", None)
        self.retrieve_method = props.get("retrieve_method", None)


    def submit(self, form, context, *args):

        if self.submit_method:
            func = None
            ctx = context

            for part in self.submit_method.split("."):
                func = getattr(ctx, part)
                ctx = func
                
            if callable(func):
                func(form, *args)


    def retrieve(self, form, context, *args):

        if self.submit_method:

            func = None
            ctx = context

            for part in self.submit_method.split("."):
                func = getattr(ctx, part)
                ctx = func

            if callable(func):
                return func(form, *args)

        return None
