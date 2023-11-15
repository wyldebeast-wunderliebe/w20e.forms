
from .templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer


@implementer(IControlRenderer)
class ResetRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        print(get_template('reset')(
            control=renderable,
            fmtmap=fmtmap
            ), file=out)
