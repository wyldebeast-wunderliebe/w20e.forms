from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements
from templates import get_template


class InputRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Input to HTML """

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        try:
            value = form.getFieldValue(renderable.bind, lexical=True)
            # TODO: not sure about this string conversion..
            if not isinstance(value, unicode):
                value = value.decode('utf-8')
        except:
            value = u''

        if renderable.rows > 1:

            tpl = get_template("textarea")
        else:
            tpl = get_template("input")
            
        print >> out, tpl(
            control=renderable,
            value=value,
            extra_classes=fmtmap['extra_classes']
            )
