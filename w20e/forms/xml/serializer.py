


from lxml import etree
import base64

from w20e.forms.rendering.renderables import DEFAULTS

BASE_PROPS = ["label", "hint", "help", "alert", "placeholder"]


class XMLSerializer(object):

    def serialize(self, form):

        root = etree.Element("form", id=form.id)

        data = etree.SubElement(root, "data")

        model = etree.SubElement(root, "model")

        view = etree.SubElement(root, "view")

        submission = etree.SubElement(root, "submission")

        self.create_data(form.data, data)

        self.create_model(form.model, model)

        self.create_view(form.view, view)

        self.create_submission(form.submission, submission)

        return etree.tostring(root, pretty_print=True)

    def create_data(self, data, root):

        """ Serialize data part """

        for field in [data.getField(id) for id in data.getFields()]:

            sub = etree.SubElement(root, field.id)

            if field.value is not None:
                self._set_value(sub, field.value)

    def create_model(self, model, root):

        """ Serialize model part """

        for prop in model.getAllFieldProperties():

            sub = etree.SubElement(root, "properties", id=prop.id)

            for bind in prop.bind:
                bindElt = etree.SubElement(sub, "bind")
                bindElt.text = bind

            if prop.getRequired() != "0":
                subsub = etree.SubElement(sub, "required")
                subsub.text = prop.getRequired()

            if prop.getRelevant() != "1":
                subsub = etree.SubElement(sub, "relevant")
                subsub.text = prop.getRelevant()

            if prop.getReadonly() != "0":
                subsub = etree.SubElement(sub, "readonly")
                subsub.text = prop.getReadonly()

            if prop.getConstraint() != "1":
                subsub = etree.SubElement(sub, "constraint")
                subsub.text = prop.getConstraint()

            if prop.getCalculate():
                subsub = etree.SubElement(sub, "calculate")
                subsub.text = prop.getRelevant()

            if prop.getDatatype():
                subsub = etree.SubElement(sub, "datatype")
                subsub.text = prop.getDatatype()

            if prop.getDefault():
                subsub = etree.SubElement(sub, "default")
                subsub.text = prop.getDefault()

    def create_view(self, view, root):

        """ Serialize  view """

        for renderable in view.getRenderables():

            kwargs = {'id': renderable.id}

            if hasattr(renderable, 'bind') and renderable.bind:
                kwargs['bind'] = renderable.bind

            elt = etree.SubElement(root, self._determine_tag(renderable),
                                   **kwargs)

            for p in BASE_PROPS:
                if getattr(renderable, p, None):
                    prop_elt = etree.SubElement(elt, p)
                    prop_elt.text = getattr(renderable, p)

            for p in getattr(renderable, '_custom_props', []):
                if getattr(renderable, p, None) != \
                        DEFAULTS.get(renderable.type, {}).get(p, None):
                    prop_elt = etree.SubElement(elt, "property", name=p)
                    prop_elt.text = str(getattr(renderable, p))

            for opt in renderable.options or []:
                opt_elt = etree.SubElement(elt, "option", value=opt.value)
                opt_elt.text = opt.label

            if hasattr(renderable, "getRenderables") and \
                    renderable.getRenderables:

                self.create_view(renderable, elt)

    def create_submission(self, submission, root):

        """ Serialize submission info. """

        root.set("type", submission.type)

        for p in submission._custom_props:
            if getattr(submission, p, None):
                prop_elt = etree.SubElement(root, "property", name=p)
                prop_elt.text = str(getattr(submission, p))

    def _set_value(self, field, value):

        try:
            if not isinstance(value, str):
                value = str(value)
            field.set("value", value)
        except:
            field.set("value", base64.b64encode(str(value)))

    def _determine_tag(self, renderable):

        """ Return the renderable's tag """

        if hasattr(renderable, 'type'):

            return renderable.type

        return renderable.__class__.__name__.lower()
