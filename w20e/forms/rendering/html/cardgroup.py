from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class CardGroupRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        print >> out, TEMPLATES['CARDGROUP_TPL_HDR'] % renderer.createFormatMap(form, renderable, **kwargs)

        print >> out, """<div class="tabs">"""

        for item in renderable.getRenderables():
            print >> out, """<div class="tab" id="tab-%s">%s</div>""" % (item.id, item.label)

        print >> out, "</div>"
        
        for item in renderable.getRenderables():        

            renderer.render(form, item, out, extra_classes="card", **kwargs)

        print >> out, TEMPLATES['CARDGROUP_TPL_FTR']
