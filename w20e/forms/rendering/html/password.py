from templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class PasswordRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Input to HTML """
    
        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        fmtmap['value'] = "*****"

        print >> out, get_template('password')(
            control=renderable,
            **fmtmap
            )
            
