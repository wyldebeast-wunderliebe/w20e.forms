from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class CheckboxRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Input to HTML """

        value = form.data[renderable.bind]
        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        fmtmap['checked'] = ""
        fmtmap['value'] = "1"

        if value:
            fmtmap['checked'] = 'checked="yes"'

        print >> out, TEMPLATES['CONTROL_HDR'] % fmtmap
        print >> out, TEMPLATES['CHECK_TPL'] % fmtmap
        print >> out, TEMPLATES['CONTROL_FTR'] % fmtmap
