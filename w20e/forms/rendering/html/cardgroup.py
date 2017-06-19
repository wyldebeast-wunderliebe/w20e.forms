from .templates import get_template
from io import BytesIO
import codecs
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer


@implementer(IControlRenderer)
class CardGroupRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        def render_subs(sub):
            """ render the sub renderable """
            str_out = BytesIO()
            out = codecs.getwriter('utf-8')(str_out)
            sub.extra_classes = (sub.extra_classes or "") + " card"
            renderer.render(form, sub, out, **kwargs)
            return out.getvalue().decode('utf-8')

        print(get_template('cardgroup')(
            group=renderable,
            fmtmap=fmtmap,
            render_subs = render_subs
            ), file=out)
