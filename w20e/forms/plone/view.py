from Products.Five.browser import BrowserView
from w20e.forms.xml.factory import XMLFormFactory


class FormView(BrowserView):


    def __init__(self, context, request, form):

        BrowserView.__init__(self, context, request)
        self.form = form

        # We may have data already...
        try:
            self.form.data = self.form.submission.retrieve(form, self.context)
        except:
            for key in context.formdefaults.keys():
                try:
                    self.form.data.getField(key).value = context.formdefaults[key]
                except:
                    pass


    def render_form(self):

        """ Render the view, using the context's form """

        action = "%s/%s" % (self.context.absolute_url(), self.form.submission.action)

        self.form.submission.action = action

        return self.form.view.render(self.form)


class XMLFormView(FormView):


    def __init__(self, context, request, formfile):

        xmlff = XMLFormFactory(formfile.filename)

        form = xmlff.create_form(action="")

        FormView.__init__(self, context, request, form)
