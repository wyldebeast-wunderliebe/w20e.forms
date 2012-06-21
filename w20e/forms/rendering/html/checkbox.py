from templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class CheckboxRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Input to HTML """

        value = form.data[renderable.bind]
        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        checked = ""

        if value:
            checked = 'checked="yes"'

        print >> out, get_template("checkbox")(
            control=renderable,
            value=value,
            checked=checked,
            extra_classes=fmtmap['extra_classes']
            )
