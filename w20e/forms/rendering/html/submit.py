from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class SubmitRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)
        if 'name' not in fmtmap:
            fmtmap['name'] = 'submit'  # default name

        print >> out, TEMPLATES['SUBMIT_TPL'] % fmtmap
