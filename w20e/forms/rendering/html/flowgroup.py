from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class FlowGroupRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):


        """ Render flow group that flows horizontally or vertically """

        print >> out, TEMPLATES['FLOWGROUP_TPL_HDR'] % renderer.createFormatMap(form, renderable, **kwargs)

        for item in renderable.getRenderables():

            renderer.render(form, item, out)

        print >> out, TEMPLATES['FLOWGROUP_TPL_FTR']
