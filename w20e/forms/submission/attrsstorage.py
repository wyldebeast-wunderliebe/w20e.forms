from submission import SubmissionBase
from w20e.forms.formdata import FormData
from w20e.forms.data.field import Field


class AttrsStorage(SubmissionBase):

    """ Submission handler that submits data as separate attributes on
    a given context.
    """

    type = "attrs"

    def __init__(self, **props):

        """ AttrsStorage uses simple attribute storage to store the
        separate fields onto the context.
        """

        SubmissionBase.__init__(self, **props)


    def submit(self, form, context, *args):

        """ Submit data. This involves storing it onto the content
        type. The submit call should provide the context as first
        param.
        """

        for field_name in form.data.getFields():
            try:
                field = form.data.getField(field_name)
                setattr(context, field.id, field.value)
            except:
                pass


    def retrieve(self, form, context, *args):

        """ Restore data. """

        data = FormData()

        for field_name in form.data.getFields():
            
            data.addField(Field(field_name, getattr(context, field_name, None)))

        return data
