

from xml.dom.minidom import Document

from w20e.forms.form import FormValidationError
from w20e.forms.xml.factory import XMLFormFactory
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

        if retrieve_data:
            try:
                data = self.form.submission.retrieve(form, context, request)
                self.form.data.update(data)
            except:
                pass

        if defaults:
            for key in list(defaults.keys()):
                self.form.data.getField(key).value = defaults[key]

    def renderform(self, errors=None, status=None, **opts):

        """ Render the form.
        """

        params = {}
        try:
            params = self.request.json
        except:
            params = self.request.params

        rendered = self.form.view.render(
            self.form, errors=errors, status=status,
            data=params, context=self.context, request=self.request, **opts)
        rendered = str(rendered, "utf-8")
        # remove empty lines
        filtered = '\n'.join([l for l in rendered.splitlines() if l.strip()])
        return filtered

    def handle_form(self):

        """ Handle the form. Override this method if you wish... """

        form = self.form
        params = {}
        try:
            params = self.request.json
        except:
            params = self.request.params

        self._process_data(form, form.view, params)
        status = 'processed'
        errors = {}

        try:
            form.validate()
            form.submission.submit(form, self.context, self.request)
            status = 'stored'

        except FormValidationError as fve:
            errors = fve.errors
            status = 'error'

        return (status, errors)

    def __call__(self):

        """ The form posts to itself, so the call method handles the form,
        if need be. """

        errors = {}
        status = ''

        params = {}
        try:
            params = self.request.json
        except:
            params = self.request.params

        submissions = set(["submit", "save", "w20e.forms.next",
            "w20e.forms.process"])

        if params.get("cancel", None):
            status = "cancelled"

        elif submissions.intersection(list(params.keys())):
            status, errors = self.form.view.handle_form(self.form,
                    params)


        if status in ["completed"]:
            self.form.submission.submit(self.form, self.context, self.request)

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

                datatype = form.model.get_field_datatype(fld.id)
                fld.value = renderable.processInput(data, datatype=datatype)

            except:
                pass

            if renderable.getRenderables:
                self._process_data(form, renderable, data)

    def retrieve_efferent_fields(self, format="json"):

        return self.form.model.collectEfferentFields()

    def ajax_validate(self, format="xml", requested_params_only=True):

        """
        Validate data given the context, request and formview. The
        latter is needed to be able to use the correct widgets for
        processing the incoming data.
        """

        model = self.form.model
        form = self.form

        params = {}
        try:
            params = self.request.json
        except:
            params = self.request.params

        self._process_data(form, form.view, params)

        effected = []
        efferent = model.collectEfferentFields()

        # HB: take inputs from self.request.params is not safe, since not
        # all fields are serialized by jquery (e.g. empty multiselect)
        if requested_params_only:
            ctls = [form.view.getRenderable(key) for key in
                    list(params.keys())]
        else:
            ctls = form.view.getRenderables(recursive=True)
            ctls = [_c for _c in ctls if hasattr(_c, 'bind')]

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
                state[ctrl.id]['calculate'] = model.getCalculate(field, data)

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
        for f in list(state.keys()):

            for cmd in ['required', 'relevant', 'readonly', 'calculate']:

                value = state[f][cmd]

                # for calculates it's a bit different: this is a tuple with
                # first param the calculated value, second whether a
                # calculation was found
                if cmd == 'calculate':
                    if value[1]:
                        value = value[0]
                    else:
                        continue  # skip this entry

                command = doc.createElement("command")
                command.setAttribute("selector", "#%s" % f)
                command.setAttribute("name", cmd)
                command.setAttribute("value", "%s" % value)
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
