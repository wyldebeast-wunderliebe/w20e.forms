
from .templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer


@implementer(IControlRenderer)
class CancelRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        print(get_template('cancel')(
            control=renderable,
            extra_classes=fmtmap['extra_classes'],
            fmtmap=fmtmap
            ), file=out)
