from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class SubmitRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        print >> out, TEMPLATES['SUBMIT_TPL'] % renderer.createFormatMap(form, renderable)
