from templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class RichTextRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Input to HTML """
        
        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        fmtmap['value'] = form.data[renderable.bind] or ""
        fmtmap['richconfig'] = renderer.opts.get('richconfig', '')
        fmtmap['richclass'] = 'wysiwyg'
        fmtmap['cols'] = renderable.cols or 80
        fmtmap['rows'] = renderable.rows or 3
    
        # added to guarantee backwards compatibilty (WGH)
        if not 'cols' in fmtmap:
            fmtmap['cols'] = '30'

        print >> out, get_template('richtext')(
            control=renderable,
            **fmtmap)
