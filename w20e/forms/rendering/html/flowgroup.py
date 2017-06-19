from io import BytesIO
import codecs
from .templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer


@implementer(IControlRenderer)
class FlowGroupRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        """ Render flow group that flows horizontally or vertically """

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        str_out = BytesIO()
        sub_out = codecs.getwriter('utf-8')(str_out)

        for sub_renderable in renderable.getRenderables():
            renderer.render(form, sub_renderable, sub_out, **kwargs)

        print(get_template('flowgroup')(
            group=renderable,
            content=str_out.getvalue().decode("utf-8"),
            fmtmap=fmtmap
            ), file=out)
