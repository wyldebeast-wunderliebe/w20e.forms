from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


PWD_TPL = """<input id="input-%(id)s" type="password" name="%(id)s" value="%(value)s" size="%(cols)s"/>"""

class PasswordRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Input to HTML """
    
        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        fmtmap['value'] = "*****"
            
        print >> out, TEMPLATES['CONTROL_HDR'] % fmtmap
        print >> out, PWD_TPL % fmtmap
        print >> out, TEMPLATES['CONTROL_FTR'] % fmtmap
