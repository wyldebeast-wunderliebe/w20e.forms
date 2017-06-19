from .templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer


@implementer(IControlRenderer)
class FileRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render File to HTML """

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        fmtmap['value'] = renderable.lexVal(form.data[renderable.bind])

        print(get_template("file")(
            control=renderable,
            fmtmap=fmtmap,
            form_id=form.id
            ), file=out)
