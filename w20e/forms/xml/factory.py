""" Factory class to generate forms from XML """

from builtins import object
from lxml import etree
from w20e.forms.formdata import FormData
from w20e.forms.formview import FormView
from w20e.forms.formmodel import FormModel
from w20e.forms.form import Form
from w20e.forms.data.field import Field
from w20e.forms.model.fieldproperties import FieldProperties
from w20e.forms.rendering.control import Option
from w20e.forms.rendering.group import *
from w20e.forms.rendering.renderables import *
from w20e.forms.interfaces import IFormFactory
from w20e.forms.registry import Registry
from zope.interface import implementer


@implementer(IFormFactory)
class XMLFormFactory(object):
    """ The XMLFormFactory uses lxml to generate a form from an XML
    definition.
    """

    # Define specific element/class mappings here
    controlClasses = {}

    def __init__(self, xml, **kwargs):

        self.xml = xml
        self.opts = kwargs

    def create_form(self, **opts):

        """ Create form based on XML
        TODO: make view type configurable
        """

        tree = None
        root = None

        # Try parsing as string first, then go for other options...
        # TODO: parsing the first line and look for <?xml sucks
        try:
            xml_found = self.xml.splitlines()[0].strip().find(b"<?xml") > -1
        except TypeError:
            xml_found = None

        if xml_found:
            root = etree.fromstring(self.xml)
        else:
            tree = etree.parse(self.xml)
            root = tree.getroot()

        model = self.create_model(root.find("model"), **opts)

        data = self.create_data(root.find("data"), model, **opts)

        view = self.create_view(root.find("view"), **opts)

        submission = self.create_submission(root.find("submission"))

        version = root.get("version")

        return Form(
            root.get("id"), data, model, view, submission, version=version)

    def create_data(self, root, model, **opts):

        """ Create FormData instance """

        data = FormData()

        for child in root.getchildren():

            if child.tag != etree.Comment:

                val = None

                if child.get("value"):

                    try:
                        val = model.convert(child.tag, child.get("value"))
                    except:
                        pass

                field = Field(child.tag, val)

                data.addField(field)

        return data

    def create_model(self, root, **opts):

        """ Create the form model. """

        kwargs = {}

        for k, v in list(root.items()):
            kwargs[k] = v

        model = FormModel(**kwargs)

        for child in root.getchildren():

            bind = []

            for elt in child.xpath("./bind"):
                bind.append(elt.text)

            kwargs = {}

            for elt in ["required", "relevant", "readonly", "calculate",
                        "datatype", "constraint", "default", ]:
                if child.xpath("./%s" % elt):

                    expr = child.xpath("./%s" % elt)[0].text.strip()
                    expr = expr.replace("\n", " ")

                    if expr:
                        kwargs[elt] = expr

            prop = FieldProperties(child.get("id"), bind, **kwargs)
            model.addFieldProperties(prop)

        return model

    def create_view(self, root, **opts):

        """ Create renderable part """

        kwargs = {}

        for prop in root.xpath("./property"):
            kwargs[prop.get("name")] = prop.text

        view = FormView(**kwargs)

        for child in root.getchildren():

            if child.__class__.__name__ == "_Element":

                if not child.tag == "property":
                    self._create_renderables(child, view)

        return view

    def _create_renderables(self, child, view):

        cls = ""

        if child.tag in XMLFormFactory.controlClasses:
            cls = XMLFormFactory.controlClasses[child.tag]
        elif Registry.get_renderable(child.tag):
            cls = Registry.get_renderable(child.tag)
        else:
            cls = eval(child.tag.capitalize())

        kwargs = {}

        for attrib in list(child.keys()):
            if attrib in kwargs_attrs:
                kwargs[attrib] = child.get(attrib)

        for elt in child.xpath("./property"):
            kwargs[elt.get("name")] = elt.text

        for elt in ["hint", "help", "alert", "placeholder"]:
            if child.xpath("./%s" % elt):
                kwargs[elt] = child.xpath("./%s" % elt)[0].text or ''

        if cls == Text:

            ctrl = cls(child.get("id"),
                       ''.join(child.xpath("./text()")),
                       **kwargs)

        elif cls == Hidden:
            ctrl = cls(child.get("id"),
                       **kwargs)

        elif cls == Submit:

            ctrl = cls(child.get("id"),
                       child.find("label").text,
                       **kwargs)
        elif cls == Group:

            layout_class = "%sGroup" % child.get("layout", "flow").capitalize()

            if Registry.get_renderable(layout_class.lower()):
                cls = Registry.get_renderable(layout_class.lower())
            else:
                cls = eval(layout_class)

            label = ''

            try:
                label = child.find("label").text
            except:
                pass

            ctrl = cls(child.get("id"),
                       label,
                       **kwargs)
        else:
            label = ''

            try:
                label = child.find("label").text
            except:
                pass

            ctrl = cls(child.get("id"),
                       label,
                       **kwargs)

        if hasattr(ctrl, "addOption") and getattr(ctrl, "addOption"):

            for subchild in child.xpath("option"):
                if subchild.xpath("label"):
                    # assume only one
                    text = subchild.xpath("label")[0].text
                else:
                    text = subchild.text or ''

                ctrl.addOption(Option(subchild.get("value"), text))

        for subchild in child.xpath("|".join(
                Registry.get_registered_renderables())):
            self._create_renderables(subchild, ctrl)

        view.addRenderable(ctrl)

    def create_submission(self, root):

        cls = Registry.get_submission(root.get("type"))

        if not cls:
            return None

        kwargs = {}

        for prop in root.xpath("./property"):
            kwargs[prop.get("name")] = prop.text

        submission = cls(**kwargs)

        return submission
