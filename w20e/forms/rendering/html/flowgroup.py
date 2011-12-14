from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class FlowGroupRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):


        """ Render flow group that flows horizontally or vertically """

        params = renderer.createFormatMap(form, renderable, **kwargs)
        if 'stepgroup_classes' not in params:
            params['stepgroup_classes'] = ''

        print >> out, TEMPLATES['FLOWGROUP_TPL_HDR'] % params

        for item in renderable.getRenderables():

            params = kwargs
            params['extra_classes'] = ""

            renderer.render(form, item, out, **kwargs)

        print >> out, TEMPLATES['FLOWGROUP_TPL_FTR']
