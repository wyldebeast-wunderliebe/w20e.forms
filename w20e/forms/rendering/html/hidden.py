from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer
from .templates import get_template


@implementer(IControlRenderer)
class HiddenRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Hidden to HTML """

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        try:
            value = form.getFieldValue(renderable.bind)
        except:
            value = ""

        print(get_template('hidden')(
            control=renderable,
            value=value,
            fmtmap=fmtmap), file=out)
