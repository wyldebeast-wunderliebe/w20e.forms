from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class ColorPickerRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):
        
        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)
        
        fmtmap['value'] = form.data[renderable.bind] or ""

        print >> out, TEMPLATES['CONTROL_HDR'] % fmtmap
        print >> out, TEMPLATES['COLORPICKER_TPL'] % fmtmap
        print >> out, TEMPLATES['CONTROL_FTR'] % fmtmap
