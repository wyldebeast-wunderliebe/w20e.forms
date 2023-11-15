
from .templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer


@implementer(IControlRenderer)
class CheckboxRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Input to HTML """

        value = form.data[renderable.bind]
        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        checked = None

        if value:
            checked = "checked"

        value = "1"

        print(get_template("checkbox")(
            control=renderable,
            value=value,
            checked=checked,
            fmtmap=fmtmap,
            ), file=out)
