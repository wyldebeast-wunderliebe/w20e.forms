from templates import TEMPLATES
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


FILE_TPL = """
<input id="input-%(id)s" type="file" name="%(id)s"/>
"""

EDIT_FILE_TPL = """
%(value)s<br/>
<input name="%(id)s" type="hidden" value="1"/>
<input id="file-%(id)s" type="file" name="%(id)s-new"/>
"""



class FileRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render File to HTML """
    
        tpl = FILE_TPL

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        fmtmap['value'] = renderable.lexVal(form.data[renderable.bind])

        if form.data[renderable.bind]:

            tpl = EDIT_FILE_TPL

        print >> out, TEMPLATES['CONTROL_HDR'] % fmtmap
        print >> out, tpl % fmtmap
        print >> out, TEMPLATES['CONTROL_FTR'] % fmtmap
