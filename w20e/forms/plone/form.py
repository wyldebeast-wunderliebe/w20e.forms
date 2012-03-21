from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

from w20e.forms.xml.formfile import FormFile
from w20e.forms.xml.factory import XMLFormFactory
from w20e.forms.form import FormValidationError


class FormContext:

    """ An object that holds form data """

    def __init__(self, attr_name="_DATA", defaults=None):

        self.attr_name = attr_name
        self.formdefaults = defaults or {}

    def getFieldValue(self, name, default=None):

        """ Get the data field value or default """

        data = getattr(self, self.attr_name, None)

        if not data:
            return default

        return data.get(name, default)


class FormView(BrowserView):
    """ Base form for w20e.forms """

    template = ViewPageTemplateFile('form.pt')

    def __call__(self):

        """ The form posts to itself, so the call method handles the form,
        if need be. """

        errors = {}
        status = ''

        if self.request.form.get("formprocess", None):

            status, errors = self.handle_form()

        elif self.request.form.get("cancel", None):

            status = "cancelled"

        return self.template(errors=errors, status=status)

    @property
    def form(self):
        return self.get_form()

    @property
    def form_context(self):
        return self.get_form_context()

    def render_form(self, errors=None):

        """ Render the view, using the context's form """

        if not errors:
            errors = {}

        rendered = self.form.view.render(self.form, errors=errors,
                request=self.request, context=self.context)
        return unicode(rendered, "utf-8")

    def handle_form(self):

        """ Handle the form. Override this method if you wish... """

        form = self.form
        form_context = self.form_context

        self._process_data(form, form.view, self.request.form)
        status = 'processed'
        errors = {}

        try:
            form.validate()
            form.submission.submit(form, form_context, self.request.form)
            self.store_form_context(form_context)
            status = 'stored'

        except FormValidationError, fve:
            errors = fve.errors
            status = 'error'

        return (status, errors)

    def _process_data(self, form, view, data=None):

        """ Get data form request and see what we can post... """

        for renderable in view.getRenderables():

            try:
                fld = form.data.getField(renderable.bind)

                if not form.model.isRelevant(fld.id, form.data):
                    continue

                val = renderable.processInput(data)
                fld.value = form.model.convert(renderable.bind, val)

            except:
                pass

            if renderable.getRenderables:
                self._process_data(form, renderable, data)

    def get_form(self):

        """ Get the form and form content """

        # TODO: move the XML form creation out of this class
        form_file = FormFile(self.form_xml)
        xml_ff = XMLFormFactory(form_file.filename)
        form = xml_ff.create_form(action="")
        form_context = self.form_context

        # We may have data already...
        try:
            form.data = form.submission.retrieve(form, form_context)
        except:
            for key in form_context.formdefaults.keys():
                try:
                    form.data.getField(key).value = \
                            form_context.formdefaults[key]
                except:
                    pass

        return form

    def get_form_context(self):

        """ Override this function to get form context from an own source  """

        return FormContext()

    def store_form_context(self, form_context):

        """ Override this function to store form context from an own source """
