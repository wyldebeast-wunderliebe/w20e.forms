from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements
from templates import TEMPLATES


class InputRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Input to HTML """

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        try:
            value = form.getFieldValue(renderable.bind, lexical=True)
            # TODO: not sure about this string conversion..
            if not isinstance(value, str):
                value = str(value)
        except:
            value = ''

        if renderable.rows > 1:

            print >> out, TEMPLATES['TEXTAREA'](
                control=renderable,
                value=value.decode('utf-8'),
                extra_classes=fmtmap['extra_classes']
                )
        else:
            print >> out, TEMPLATES['INPUT'](
                control=renderable,
                value=value.decode('utf-8'),
                extra_classes=fmtmap['extra_classes']
                )
