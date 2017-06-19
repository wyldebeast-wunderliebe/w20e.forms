from .templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer


@implementer(IControlRenderer)
class PasswordRenderer:

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Input to HTML """

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        fmtmap['value'] = "*****"

        print(get_template('password')(
            control=renderable,
            fmtmap=fmtmap
            ), file=out)

