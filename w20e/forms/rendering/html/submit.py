from .templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer


@implementer(IControlRenderer)
class SubmitRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        if 'name' not in fmtmap:
            fmtmap['name'] = 'submit'  # default name

        print(get_template("submit")(
            control=renderable,
            fmtmap=fmtmap
            ), file=out)
