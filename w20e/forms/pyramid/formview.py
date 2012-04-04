from inspect import getmembers, ismethod

from xml.dom.minidom import Document

from w20e.forms.form import FormValidationError
from w20e.forms.xml.factory import XMLFormFactory
from w20e.forms.registry import Registry
import sys


class formview(object):

    """ Pyramid form view """

    def __init__(self, context, request, form, retrieve_data=True,
            defaults=None):

        """ Initiate the form view. If retrieve_data is True(ish), the
        submission handler will be asked for the data. If defaults is
        given, any fields available in the defaults will be preloaded.
        """

        if not defaults:
            defaults = {}

        self.context = context
        self.request = request
        self.form = form

        # vocabs
        # TODO: Now really...
        #for method in getmembers(context, ismethod):

        #    try:
        #        if getattr(method[1], "__vocab__", False):

        #            Registry.register_vocab(method[0], method[1])
        #    except:
        #        pass

        if retrieve_data:
            try:
                data = self.form.submission.retrieve(form, context)
                self.form.data.update(data)
            except:
                pass

        if defaults:
            for key in defaults.keys():
                self.form.data.getField(key).value = defaults[key]

    def renderform(self, errors=None, status=None):

        """ Render the form.
        """

        rendered = self.form.view.render(
            self.form, errors=errors, status=status,
            request=self.request.params)
        return unicode(rendered, "utf-8")

    def handle_form(self):

        """ Handle the form. Override this method if you wish... """

        form = self.form
        self._process_data(form, form.view, self.request.params)
        status = 'processed'
        errors = {}

        try:
            form.validate()
            form.submission.submit(form, self.context, self.request)
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

        if self.request.params.get("submit", None):

            status, errors = self.handle_form()

        elif self.request.params.get("cancel", None):

            status = "cancelled"

        return {'errors': errors, 'status': status}

    def _process_data(self, form, view, data=None):

        """ Get data form request and see what we can post...
        """

        if not data:
            data = {}

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

    def retrieve_efferent_fields(self, format="json"):

        return self.form.model.collectEfferentFields()

    def ajax_validate(self, format="xml"):

        """
        Validate data given the context, request and formview. The
        latter is needed to be able to use the correct widgets for
        processing the incoming data.
        """

        model = self.form.model
        form = self.form

        self._process_data(form, form.view, self.request.params)

        effected = []
        efferent = model.collectEfferentFields()

        ctls = [form.view.getRenderable(key) for key in \
                self.request.params.keys()]
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
        results = doc.toprettyxml(indent="  ")
        # can't return unicode to the XML renderer apparently..
        return results.encode('utf-8')


class xmlformview(formview):

    """ View class taking an XML path as argument to create the form """

    def __init__(self, context, request, formfile, retrieve_data=True,
                 defaults=None):

        if hasattr(formfile, 'filename'):
            xmlff = XMLFormFactory(formfile.filename)
        else:
            xmlff = XMLFormFactory(formfile)

        form = xmlff.create_form(action="")

        formview.__init__(self, context, request, form,
                          retrieve_data=retrieve_data, defaults=defaults)
