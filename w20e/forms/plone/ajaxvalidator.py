from xml.dom.minidom import Document
from Products.Five.browser import BrowserView
import sys
from w20e.forms.form import FormValidationError
from Acquisition import aq_inner, aq_parent


class AjaxValidator(BrowserView):

    """ Validator class that assumes a few things that a BrowserView,
    should be able to provide... The validator will return XML, that
    can be used for Ajax style validation.
    """

    def __call__(self):

        viewname = "edit"

        try:
            viewname = self.request.get_header("referer").split('/')[-1]
        except:
            pass

        ti = self.context.getTypeInfo()

        viewname = ti.queryMethodID(viewname) or viewname

        formview = self.context.unrestrictedTraverse(viewname, default=None)

        return self.validate(self.request, formview.form, self.context)


    def validate(self, request, form, ctx):

        """
        Validate data given the context, request and formview. The
        latter is needed to be able to use the correct widgets for
        processing the incoming data.
        """

        state = {}

        model = form.model
        data = form.data

        # two phase detection of changes
        for field in form.data.getFields():

            state[field] = {'before':{}, 'after':{}}
            state[field]['before']['readonly']= form.model.isReadonly(field, data)
            state[field]['before']['relevant']= form.model.isRelevant(field, data)
            state[field]['before']['required']= form.model.isRequired(field, data)

        # process request
        self.setData(request, form, ctx, request.form)

        for field in form.data.getFields():

            state[field]['after']['readonly']= form.model.isReadonly(field, data)
            state[field]['after']['relevant']= form.model.isRelevant(field, data)
            state[field]['after']['required']= form.model.isRequired(field, data)

        errors = []
        ctls = [form.view.getRenderable(key) for key in request.form.keys()]
        ctls = [c for c in ctls if c]
        error = None

        # Do actual validation
        try:
            fields = [control.bind for control in ctls]

            form.validate(fields=fields)
        except FormValidationError:

            error = sys.exc_info()[1]

        for control in ctls:

            if error and error.errors.has_key(control.bind):
                errors.append((control.id, control.alert or "Invalid value"))
            else:
                errors.append((control.id, ""))


        # Create the minidom document
        doc = Document()
        root = doc.createElement("validation")
        doc.appendChild(root)

        # Let's send back changes
        for f in form.data.getFields():

            for cmd in ['required', 'relevant', 'readonly']:

                if state[f]['before'][cmd] != state[f]['after'][cmd]:
                    command = doc.createElement("command")
                    command.setAttribute("selector", "#%s" % f)
                    command.setAttribute("name", cmd)
                    command.setAttribute("value", "%s" % state[f]['after'][cmd])
                    root.appendChild(command)

        for field, message in errors:

            command = doc.createElement("command")
            command.setAttribute("selector", "#%s" % field)
            command.setAttribute("name", "alert")
            command.setAttribute("value", "%s" % message)
            root.appendChild(command)


        request.RESPONSE.setHeader('Pragma', 'no-cache')
        request.RESPONSE.setHeader('Cache-Control', 'no-cache')
        request.RESPONSE.setHeader('Content-Type', "text/xml")

        # Print our newly created XML
        return doc.toprettyxml(indent="  ")

    def setData(self, request, form, ctx, data=None):

        """ Get data form request and see what we can post...
        We always process the incoming raw data through the renderable, so
        as to make sure the proper datatype is set. The real data variable
        is begot from the renderable's binding.
        """

        if not data:
            data = {}

        for key in data:

            renderable = form.view.getRenderable(key)

            if renderable and hasattr(renderable, 'bind'):

                fld = form.data.getField(renderable.bind)

                if fld:
                    value = renderable.processInput(request.form)

                    # Do typing
                    fld.value = form.model.convert(fld.id, value)

        form.submission.submit(form, ctx)
