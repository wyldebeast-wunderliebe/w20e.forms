""" Factory class to generate forms from XML """

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
from zope.interface import implements


class XMLFormFactory:

    """ The XMLFormFactory uses lxml to generate a form from an XML
    definition.
    """

    implements(IFormFactory)

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
        if self.xml.splitlines()[0].strip().find("<?xml") > -1:
            root = etree.fromstring(self.xml)
        else:
            tree = etree.parse(self.xml)
            root = tree.getroot()

        model = self.create_model(root.find("model"), **opts)

        data = self.create_data(root.find("data"), model, **opts)

        view = self.create_view(root.find("view"), **opts)

        submission = self.create_submission(root.find("submission"))

        return Form(root.get("id"), data, model, view, submission)

    def create_data(self, root, model, **opts):

        """ Create FormData instance """

        data = FormData()

        for child in root.getchildren():

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

        model = FormModel()

        for child in root.getchildren():

            bind = []

            for elt in child.xpath("./bind"):
                bind.append(elt.text)

            kwargs = {}

            for elt in ["required", "relevant", "readonly",
                        "calculate", "datatype", "constraint"]:
                if child.xpath("./%s" % elt):
                    kwargs[elt] = child.xpath("./%s" % elt)[0].text

            prop = FieldProperties(child.get("id"), bind, **kwargs)
            model.addFieldProperties(prop)

        return model

    def create_view(self, root, **opts):

        """ Create renderable part """

        view = FormView()

        for child in root.getchildren():

            if child.__class__.__name__ == "_Element":
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

        for elt in child.xpath("./property"):
            kwargs[elt.get("name")] = elt.text

        for elt in ["hint", "help", "alert"]:
            if child.xpath("./%s" % elt):
                kwargs[elt] = child.xpath("./%s" % elt)[0].text or ''

        if cls == Text:
            ctrl = cls(child.get("id"),
                       child.text,
                       bind=child.get("bind"),
                       **kwargs)

        elif cls.__name__ == "Hidden":
            ctrl = cls(child.get("id"),
                       bind=child.get("bind"),
                       **kwargs)

        elif cls == Submit:

            ctrl = cls(child.get("id"),
                       child.find("label").text,
                       **kwargs)
        elif cls == Group:
            cls = eval("%sGroup" % child.get("layout", "flow").capitalize())

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
                       bind=child.get("bind"),
                       **kwargs)

        if hasattr(ctrl, "addOption"):

            for subchild in child.xpath("option"):
                ctrl.addOption(Option(subchild.get("value"),
                                      subchild.text or ''))

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
