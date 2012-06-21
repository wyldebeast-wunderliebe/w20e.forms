from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class CardGroupRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        str_out = StringIO()
        sub_out = codecs.getwriter('utf-8')(str_out)

        for sub_renderable in renderable.getRenderables():
            print >> sub_out, """<div class="tab" id="tab-%s">%s</div>""" % (sub_renderable.id, sub_renderable.label)
            renderer.render(form, sub_renderable, sub_out, **kwargs)
            print >> sub_out, "</div>"

        print >> out, get_template('cardgroup')(
            group=renderable,
            content=sub_out.getvalue(),
            extra_classes=fmtmap['extra_classes']
            )
