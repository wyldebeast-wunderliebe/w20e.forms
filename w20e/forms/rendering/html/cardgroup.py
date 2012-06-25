from templates import get_template
from StringIO import StringIO
import codecs
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class CardGroupRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        str_out = StringIO()
        sub_out = codecs.getwriter('utf-8')(str_out)

        print >> sub_out, """<div class="tabs">"""

        for sub_renderable in renderable.getRenderables():
            print >> sub_out, """<div class="tab" id="tab-%s">%s</div>""" % (sub_renderable.id, sub_renderable.label)

        print >> sub_out, "</div>"

        for sub_renderable in renderable.getRenderables():
            sub_renderable.extra_classes = (sub_renderable.extra_classes or "") + " card"
            renderer.render(form, sub_renderable, sub_out, **kwargs)

        print >> out, get_template('cardgroup')(
            group=renderable,
            content=str_out.getvalue().decode("utf-8"),
            extra_classes=fmtmap['extra_classes']
            )
