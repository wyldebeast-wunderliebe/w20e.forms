from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class CancelRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)
        
        print >> out, TEMPLATES['CANCEL_TPL'](
            control=renderable,
            extra_classes=fmtmap['extra_classes']
            )
