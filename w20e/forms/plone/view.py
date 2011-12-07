from Products.Five.browser import BrowserView
from w20e.forms.xml.factory import XMLFormFactory
from xml.dom.minidom import Document
from w20e.forms.form import FormValidationError
import sys


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
                    self.form.data.getField(key).value = \
                            context.formdefaults[key]
                except:
                    pass

    def render_form(self, errors=None):

        """ Render the view, using the context's form """

        return unicode(self.form.view.render(self.form, errors=errors),
                "utf-8")

    def handle_form(self):

        """ Handle the form. Override this method if you wish... """

        form = self.form
        self._process_data(form, form.view, self.request.form)
        status = 'processed'
        errors = {}

        try:
            form.validate()
            form.submission.submit(form, self.context, self.request.form)
            status = 'stored'

        except FormValidationError, fve:
            errors = fve.errors
            status = 'error'

        return (status, errors)

    def __call__(self):

        """ The form posts to itself, so the call method handles the form,
        if need be. """

        errors = {}
        status = ''

        if self.request.form.get("submit", None):

            status, errors = self.handle_form()

        elif self.request.form.get("cancel", None):

            status = "cancelled"

        return {'errors': errors, 'status': status}

    def _process_data(self, form, view, data=None):

        """ Get data form request and see what we can post...
        """

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

    def ajax_validate(self):

        """
        Validate data given the context, request and formview. The
        latter is needed to be able to use the correct widgets for
        processing the incoming data.
        """

        model = self.form.model
        form = self.form

        self._process_data(form, form.view, self.request.form)

        effected = []
        efferent = model.collectEfferentFields()

        ctls = [form.view.getRenderable(key) for key in \
                self.request.form.keys()]
        ctls = [c for c in ctls if c]

        for ctl in ctls:
            for effected_field in efferent.get(ctl.bind, []):
                if not effected_field in effected:
                    effected.append(effected_field)

        data = form.data
        state = {}

        for field in effected:

            ctrl = form.view.getRenderableByBind(field)

            if ctrl:
                state[ctrl.id] = {}
                state[ctrl.id]['readonly'] = model.isReadonly(field, data)
                state[ctrl.id]['relevant'] = model.isRelevant(field, data)
                state[ctrl.id]['required'] = model.isRequired(field, data)

        errors = []
        error = None

        # Do actual validation
        try:
            fields = [control.bind for control in ctls]

            form.validate(fields=fields)
        except FormValidationError:

            error = sys.exc_info()[1]

        for control in ctls:

            if error and control.bind in error.errors:
                errors.append((control.id, control.alert or "Invalid value"))
            else:
                errors.append((control.id, ""))

        # Create the minidom document
        doc = Document()
        root = doc.createElement("validation")
        doc.appendChild(root)

        # Let's send back changes
        for f in state.keys():

            for cmd in ['required', 'relevant', 'readonly']:

                command = doc.createElement("command")
                command.setAttribute("selector", "#%s" % f)
                command.setAttribute("name", cmd)
                command.setAttribute("value", "%s" % state[f][cmd])
                root.appendChild(command)

        for field, message in errors:

            command = doc.createElement("command")
            command.setAttribute("selector", "#%s" % field)
            command.setAttribute("name", "alert")
            command.setAttribute("value", "%s" % message)
            root.appendChild(command)

        # Print our newly created XML
        self.request.RESPONSE.setHeader('Content-Type', 'text/xml')
        return doc.toprettyxml(indent="  ")


class XMLFormView(FormView):

    def __init__(self, context, request, formfile):

        xmlff = XMLFormFactory(formfile.filename)

        form = xmlff.create_form(action="")

        FormView.__init__(self, context, request, form)
